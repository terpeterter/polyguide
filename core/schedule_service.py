"""Сервис расписания учебных занятий Московского Политеха.

Ответственный разработчик: Тимлид / Разработчик расписания
Задачи модуля:
1. Интеграция с официальным боевым API расписания Политеха: https://rasp.dmami.ru/
2. Автоматическое получение списка всех 700+ академических групп университета.
3. Парсинг сетки пар (аудитории, преподаватели, вебинары, корпуса, периоды дисциплин).
4. Локальный кэш и оффлайн-fallback (MOCK_SCHEDULE) для надежной работы без сети.
"""

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Lesson:
    """Учебное занятие (пара)."""
    number: int                  # Номер пары (1-7)
    time_start: str              # Время начала (например, "09:00")
    time_end: str                # Время окончания (например, "10:30")
    subject: str                 # Название дисциплины
    lesson_type: str             # Вид занятия: "Лекция", "Практика", "Лабораторная"
    teacher: str                 # Преподаватель
    room: str                    # Аудитория (например, "А-312" или ссылка на Вебинар)
    campus: str                  # Корпус (например, "Б. Семёновская, 38")
    dates: Optional[str] = None  # Период проведения (например, "01 Сен - 01 Ноя")
    e_link: Optional[str] = None # Ссылка на вебинар или материалы


# Типовое расписание звонков Мосполитеха
BELL_SCHEDULE = [
    (1, "09:00", "10:30"),
    (2, "10:40", "12:10"),
    (3, "12:20", "13:50"),
    (4, "14:30", "16:00"),
    (5, "16:10", "17:40"),
    (6, "17:50", "19:20"),
    (7, "19:30", "21:00"),
]

BELL_TIMES = {item[0]: (item[1], item[2]) for item in BELL_SCHEDULE}

DAY_MAPPING = {
    "1": "Понедельник",
    "2": "Вторник",
    "3": "Среда",
    "4": "Четверг",
    "5": "Пятница",
    "6": "Суббота",
    "7": "Воскресенье",
}

DAYS_ORDER = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

DEFAULT_POPULAR_GROUPS = [
    "241-321",
    "241-211",
    "231-161",
    "221-811",
]

# Локальный демонстрационный кэш на случай оффлайна
MOCK_SCHEDULE: Dict[str, Dict[str, List[Lesson]]] = {
    "241-321": {
        "Понедельник": [
            Lesson(1, "09:00", "10:30", "Математический анализ", "Лекция", "Иванов А. В.", "А-201", "ул. Б. Семёновская, 38"),
            Lesson(2, "10:40", "12:10", "Информатика и программирование", "Практика", "Смирнова Е. П.", "В-405", "ул. Б. Семёновская, 38"),
            Lesson(3, "12:20", "13:50", "Иностранный язык", "Практика", "Джонсон М. К.", "Б-310", "ул. Б. Семёновская, 38"),
        ],
        "Вторник": [
            Lesson(2, "10:40", "12:10", "Физика", "Лекция", "Петров С. Н.", "А-100", "ул. Б. Семёновская, 38"),
            Lesson(3, "12:20", "13:50", "Физика", "Лабораторная", "Петров С. Н.", "Ф-102", "ул. Б. Семёновская, 38"),
            Lesson(4, "14:30", "16:00", "Введение в проектную деятельность", "Практика", "Кудрявцева Ю. С.", "1405", "ул. Автозаводская, 16"),
        ],
        "Среда": [
            Lesson(1, "09:00", "10:30", "Линейная алгебра и геометрия", "Лекция", "Сидоров К. В.", "А-202", "ул. Б. Семёновская, 38"),
            Lesson(2, "10:40", "12:10", "Линейная алгебра и геометрия", "Практика", "Сидоров К. В.", "В-208", "ул. Б. Семёновская, 38"),
            Lesson(3, "12:20", "13:50", "История России", "Лекция", "Васильев О. Г.", "А-200", "ул. Б. Семёновская, 38"),
        ],
        "Четверг": [
            Lesson(2, "10:40", "12:10", "Алгоритмы и структуры данных", "Лекция", "Морозов Д. И.", "А-301", "ул. Б. Семёновская, 38"),
            Lesson(3, "12:20", "13:50", "Алгоритмы и структуры данных", "Лабораторная", "Морозов Д. И.", "В-502", "ул. Б. Семёновская, 38"),
            Lesson(4, "14:30", "16:00", "Элективная физическая культура", "Практика", "Кафедра ФВиС", "Спорткомплекс", "ул. Б. Семёновская, 38"),
        ],
        "Пятница": [
            Lesson(1, "09:00", "10:30", "Проектная мастерская (ЦПД)", "Практика", "Куратор проекта", "1410", "ул. Автозаводская, 16"),
            Lesson(2, "10:40", "12:10", "Проектная мастерская (ЦПД)", "Практика", "Куратор проекта", "1410", "ул. Автозаводская, 16"),
        ],
        "Суббота": [
            Lesson(1, "09:00", "10:30", "Самостоятельная работа в библиотеке", "Консультация", "Дежурный тьютор", "Читальный зал", "ул. Б. Семёновская, 38"),
        ]
    },
    "241-211": {
        "Понедельник": [
            Lesson(1, "09:00", "10:30", "Начертательная геометрия", "Лекция", "Козлов А. М.", "А-105", "ул. Б. Семёновская, 38"),
            Lesson(2, "10:40", "12:10", "Инженерная графика", "Практика", "Козлов А. М.", "Г-302", "ул. Б. Семёновская, 38"),
        ],
        "Вторник": [
            Lesson(2, "10:40", "12:10", "Математический анализ", "Практика", "Иванов А. В.", "А-203", "ул. Б. Семёновская, 38"),
            Lesson(3, "12:20", "13:50", "Введение в проектную деятельность", "Практика", "Кудрявцева Ю. С.", "1405", "ул. Автозаводская, 16"),
        ],
        "Среда": [
            Lesson(2, "10:40", "12:10", "Теоретическая механика", "Лекция", "Николаев В. Д.", "А-101", "ул. Б. Семёновская, 38"),
        ],
        "Четверг": [
            Lesson(1, "09:00", "10:30", "Иностранный язык", "Практика", "Смирнова Л. А.", "Б-205", "ул. Б. Семёновская, 38"),
            Lesson(2, "10:40", "12:10", "Информатика", "Лабораторная", "Семенов В. В.", "В-401", "ул. Б. Семёновская, 38"),
        ],
        "Пятница": [
            Lesson(3, "12:20", "13:50", "Элективная физическая культура", "Практика", "Кафедра ФВиС", "Спортзал", "ул. Прянишникова, 2А"),
        ],
        "Суббота": []
    }
}


def resolve_campus(location: str, room_title: str) -> str:
    """Интеллектуальное определение корпуса Московского Политеха."""
    text = (location + " " + room_title).lower()
    if "webinar" in text or "вебинар" in text or "онлайн" in text:
        return "Дистанционно (Вебинар)"
    if "спорт" in text:
        return "Спортивный комплекс"
    if "ав" in text or "автозавод" in text:
        return "ул. Автозаводская, 16"
    if "пр" in text or "пряниш" in text:
        return "ул. Прянишникова, 2А"
    if "пк" in text or "корчагин" in text:
        return "ул. Павла Корчагина, 22"
    if "мих" in text or "михалков" in text:
        return "ул. Михалковская, 7"
    if any(letter in text for letter in ["а-", "б-", "в-", "г-", "н-", "семен", "семён"]):
        return "ул. Б. Семёновская, 38"
    return location if location else "Московский Политех"


class ScheduleService:
    """Сервис для получения, кэширования и фильтрации расписания занятий."""

    def __init__(self, use_api: bool = True, timeout: int = 5):
        self.use_api = use_api
        self.timeout = timeout
        self.api_url = "https://rasp.dmami.ru/site/group"
        self._cache: Dict[str, Dict[str, List[Lesson]]] = {}
        self._groups_cache: Optional[List[str]] = None
        self._is_online: bool = True

    @property
    def is_online(self) -> bool:
        """Статус доступности официального API rasp.dmami.ru."""
        return self._is_online

    def get_available_groups(self) -> List[str]:
        """Возвращает список всех академических групп (через API с кэшированием)."""
        if self._groups_cache is not None:
            return self._groups_cache

        if self.use_api:
            try:
                req = urllib.request.Request(
                    "https://rasp.dmami.ru/",
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')
                    m = re.search(r'var globalListGroups\s*=\s*(\{.*?\})\.groups;', html, re.DOTALL)
                    if m:
                        data = json.loads(m.group(1))
                        api_groups = list(data.get('groups', {}).keys())
                        api_groups_set = set(api_groups)
                        # Популярные группы первокурсников в начало, остальные отсортированы
                        ordered = [g for g in DEFAULT_POPULAR_GROUPS if g in api_groups_set]
                        rest = sorted(list(api_groups_set - set(ordered)))
                        self._groups_cache = ordered + rest
                        self._is_online = True
                        return self._groups_cache
            except Exception as e:
                self._is_online = False
                print(f"[ScheduleService] Ошибка загрузки списка групп из API: {e}")

        # Fallback при недоступности сети
        self._groups_cache = list(MOCK_SCHEDULE.keys()) + [g for g in DEFAULT_POPULAR_GROUPS if g not in MOCK_SCHEDULE]
        return self._groups_cache

    def _fetch_from_api(self, group: str, session: int = 0) -> Dict[str, List[Lesson]]:
        """Запрос недельного расписания группы из API rasp.dmami.ru."""
        url = f"{self.api_url}?group={group}&session={session}"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://rasp.dmami.ru/',
                'X-Requested-With': 'XMLHttpRequest'
            }
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') != 'ok':
                return {}

            grid = data.get('grid', {})
            result: Dict[str, List[Lesson]] = {d: [] for d in DAYS_ORDER}

            for day_idx, pairs in grid.items():
                day_name = DAY_MAPPING.get(str(day_idx))
                if not day_name:
                    continue

                if day_name not in result:
                    result[day_name] = []

                for pair_str, lesson_list in sorted(pairs.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 99):
                    pair_num = int(pair_str) if pair_str.isdigit() else 1
                    t_start, t_end = BELL_TIMES.get(pair_num, ("09:00", "10:30"))

                    for item in lesson_list:
                        subject = item.get('sbj', 'Без названия')
                        l_type = item.get('type', 'Занятие')
                        teacher = item.get('teacher', 'Преподаватель не указан')
                        location = item.get('location', '')
                        dates = item.get('dts', '')
                        e_link = item.get('e_link')

                        auditories = item.get('auditories', [])
                        rooms = [a.get('title', '') for a in auditories if a.get('title')]
                        room_str = ", ".join(rooms) if rooms else (location or "Аудитория не указана")

                        campus = resolve_campus(location, room_str)

                        result[day_name].append(
                            Lesson(
                                number=pair_num,
                                time_start=t_start,
                                time_end=t_end,
                                subject=subject,
                                lesson_type=l_type,
                                teacher=teacher,
                                room=room_str,
                                campus=campus,
                                dates=dates,
                                e_link=e_link
                            )
                        )
            self._is_online = True
            return result

    def get_schedule(self, group: str, day_of_week: str, session: int = 0) -> List[Lesson]:
        """Получить список занятий для группы на выбранный день.
        
        Args:
            group: номер академической группы (например, '241-321')
            day_of_week: день недели ('Понедельник', 'Вторник', и т.д.)
            session: 0 — учебный семестр, 1 — экзаменационная сессия
        """
        cache_key = f"{group}_{session}"

        # 1. Запрос из API (если включено и еще нет в кэше)
        if self.use_api and cache_key not in self._cache:
            try:
                week_sched = self._fetch_from_api(group, session)
                if week_sched:
                    self._cache[cache_key] = week_sched
            except Exception as e:
                self._is_online = False
                print(f"[ScheduleService] Ошибка запроса расписания для группы {group}: {e}")

        # 2. Если расписание получено и закэшировано
        if cache_key in self._cache:
            return self._cache[cache_key].get(day_of_week, [])

        # 3. Fallback на локальный mock-кэш
        if group in MOCK_SCHEDULE:
            return MOCK_SCHEDULE[group].get(day_of_week, [])

        return []
