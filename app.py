"""Цифровой кампус Московского Политеха: Личный кабинет и Справочник первокурсника.

Модульная архитектура:
- Вкладка 1: Личный кабинет студента (Дашборд и дедлайны)
- Вкладка 2: Расписание занятий (локальный кэш + интеграция с rasp.dmami.ru)
- Вкладка 3: Интерактивный справочник первокурсника (база знаний по регламентам)
- Вкладка 4: Интеллектуальный ИИ-ассистент (RAG: BM25 поиск + LLM)
"""

import json
import os
import streamlit as st
from datetime import datetime

from core.document_loader import load_all_documents
from core.retriever import BM25Retriever
from core.llm_client import LLMClient
from core.schedule_service import ScheduleService

# --- Конфигурация страницы ---
st.set_page_config(
    page_title="Цифровой кампус | Московский Политех",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Пользовательские стили для оформления в стиле современного студенческого портала
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, rgba(20, 30, 48, 0.05), rgba(36, 59, 85, 0.08));
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .lesson-card {
        border-left: 4px solid #0066cc;
        background: rgba(0, 102, 204, 0.04);
        padding: 12px 16px;
        border-radius: 4px 8px 8px 4px;
        margin-bottom: 10px;
    }
    .badge-lecture {
        background-color: #2e7d32;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-practice {
        background-color: #0288d1;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-lab {
        background-color: #ed6c02;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# --- Инициализация и кэширование компонентов ---
@st.cache_resource
def init_system():
    """Загрузка документов, построение поискового индекса BM25 и сервисов."""
    chunks = load_all_documents("data/documents")
    retriever = BM25Retriever(chunks)
    llm = LLMClient()
    schedule_service = ScheduleService()
    return chunks, retriever, llm, schedule_service


chunks, retriever, llm, schedule_service = init_system()


# Хелперы для загрузки справочных данных
@st.cache_data
def load_faq():
    faq_path = "config/faq.json"
    if os.path.exists(faq_path):
        with open(faq_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": []}


@st.cache_data
def load_contacts():
    contacts_path = "config/contacts.json"
    if os.path.exists(contacts_path):
        with open(contacts_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"departments": []}


faq_data = load_faq()
contacts_data = load_contacts()


# --- Боковая панель: Профиль и навигация ---
with st.sidebar:
    st.markdown("### 🎓 Цифровой кампус")
    st.caption("Московский Политех · 2026")
    
    st.divider()
    
    # Виджет студента
    st.markdown("#### 👤 Профиль студента")
    user_group = st.selectbox(
        "Академическая группа:",
        options=schedule_service.get_available_groups(),
        index=0,
        help="Выберите группу для синхронизации расписания"
    )
    st.markdown(
        f"""
        - **Курс:** 1 курс (бакалавриат)
        - **Форма:** Очная (бюджет)
        - **Факультет:** Информационных технологий
        """
    )
    
    st.divider()
    
    # Статус базы знаний RAG
    st.markdown("#### 📚 База регламентов")
    st.write(f"Фрагментов в индексе: **{len(chunks)}**")
    if chunks:
        sources = sorted(list(set(c.source for c in chunks)))
        with st.expander("Загруженные регламенты"):
            for s in sources:
                st.caption(f"• `{s}`")
    
    st.divider()
    st.markdown("##### 🔗 Полезные ссылки")
    st.markdown("""
    - [Личный кабинет Мосполитеха](https://online.mospolytech.ru/)
    - [СДО (Moodle)](https://online.mospolytech.ru/)
    - [Расписание занятий (Официальное)](https://rasp.dmami.ru/)
    """)


# --- Верхний заголовок ---
st.title("🎓 Личный кабинет & Справочник первокурсника")
st.caption("Единый портал навигации, расписания и консультаций по регламентам Московского Политеха")

# --- Основные вкладки портала ---
tab_cabinet, tab_schedule, tab_guide, tab_assistant = st.tabs([
    "🏠 Личный кабинет",
    "📅 Расписание",
    "📖 Справочник регламентов",
    "🤖 ИИ-Консультант"
])


# =====================================================================
# ВКЛАДКА 1: Личный кабинет (Дашборд)
# =====================================================================
with tab_cabinet:
    st.subheader("👋 Добро пожаловать в Цифровой кампус!")
    st.write(
        "Здесь собраны ключевые сервисы для первокурсника: расписание пар на сегодня, "
        "контрольные точки проектной деятельности и быстрый доступ к регламентам университета."
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📌 **Текущая неделя:** Числитель\n\nСеместр: Осенний 2026/2027")
    with col2:
        st.warning("⏳ **Ближайший дедлайн:**\n\nКТ-1: Паспорт проекта (до 15 ноября)")
    with col3:
        st.success("💳 **Стипендия:**\n\nНачислена за текущий месяц (25-е число)")

    st.markdown("---")
    
    # Ближайшие пары сегодня
    st.subheader(f"📅 Пары на сегодня (Группа {user_group})")
    
    # Определяем день недели (по умолчанию Понедельник для демонстрации)
    days_map = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    current_day = days_map.get(datetime.today().weekday(), "Понедельник")
    if current_day == "Воскресенье":
        current_day = "Понедельник"
        
    today_lessons = schedule_service.get_schedule(user_group, current_day)
    
    if today_lessons:
        st.caption(f"Расписание на **{current_day}**:")
        for lesson in today_lessons:
            col_time, col_info = st.columns([1, 4])
            with col_time:
                st.markdown(f"**Пара {lesson.number}**<br>`{lesson.time_start} - {lesson.time_end}`", unsafe_allow_html=True)
            with col_info:
                badge = f"<span class='badge-practice'>{lesson.lesson_type}</span>"
                if lesson.lesson_type == "Лекция":
                    badge = f"<span class='badge-lecture'>{lesson.lesson_type}</span>"
                elif lesson.lesson_type == "Лабораторная":
                    badge = f"<span class='badge-lab'>{lesson.lesson_type}</span>"
                    
                st.markdown(
                    f"**{lesson.subject}** {badge}<br>"
                    f"👨‍🏫 {lesson.teacher} &nbsp;|&nbsp; 📍 ауд. **{lesson.room}** ({lesson.campus})",
                    unsafe_allow_html=True
                )
            st.divider()
    else:
        st.write("🎉 Сегодня занятий нет или день самостоятельной подготовки!")
        
    # Блок быстрых действий
    st.subheader("⚡ Быстрые действия")
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        st.markdown("**📄 Справка об обучении**")
        st.caption("Для военкомата, налогового вычета или пенсионного фонда.")
        st.button("Как получить справку →", key="btn_ref_cert", use_container_width=True)
    with qa_col2:
        st.markdown("**💰 Стипендиальные выплаты**")
        st.caption("Условия получения академической и повышенной стипендии.")
        st.button("Узнать регламент выплат →", key="btn_ref_scholarship", use_container_width=True)
    with qa_col3:
        st.markdown("**🎯 Проектная деятельность**")
        st.caption("Критерии оценивания и правила сдачи отчетов по ДМ2026.")
        st.button("Открыть регламент проектов →", key="btn_ref_project", use_container_width=True)


# =====================================================================
# ВКЛАДКА 2: Расписание
# =====================================================================
with tab_schedule:
    st.subheader("📅 Расписание учебных занятий")
    st.caption("Синхронизировано с базой учебного процесса Московского Политеха")
    
    sched_col1, sched_col2 = st.columns([2, 2])
    with sched_col1:
        selected_group = st.selectbox(
            "Выберите академическую группу:",
            options=schedule_service.get_available_groups(),
            index=0,
            key="sched_group_select"
        )
    with sched_col2:
        selected_day = st.selectbox(
            "День недели:",
            options=["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
            index=0,
            key="sched_day_select"
        )
        
    lessons = schedule_service.get_schedule(selected_group, selected_day)
    
    if lessons:
        st.markdown(f"#### Занятия на {selected_day} для группы {selected_group}")
        for l in lessons:
            with st.container():
                badge_class = "badge-practice"
                if l.lesson_type == "Лекция":
                    badge_class = "badge-lecture"
                elif l.lesson_type == "Лабораторная":
                    badge_class = "badge-lab"
                    
                st.markdown(
                    f"""
                    <div class="lesson-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>Пара {l.number} ({l.time_start} — {l.time_end})</strong>
                            <span class="{badge_class}">{l.lesson_type}</span>
                        </div>
                        <h4 style="margin: 6px 0;">{l.subject}</h4>
                        <div style="color: #666; font-size: 14px;">
                            👤 <b>Преподаватель:</b> {l.teacher} &nbsp;•&nbsp; 
                            📍 <b>Аудитория:</b> {l.room} ({l.campus})
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info(f"На **{selected_day}** занятий в расписании не найдено.")
        
    st.info("💡 **Для разработчиков (Модуль расписания):** Модуль подключен к `core.schedule_service`. В дальнейшем здесь подключается прямой запрос к API `https://rasp.dmami.ru/`.")


# =====================================================================
# ВКЛАДКА 3: Справочник первокурсника
# =====================================================================
with tab_guide:
    st.subheader("📖 Официальный справочник первокурсника")
    st.caption("Проверенная база знаний по правилам, регламентам и службам кампуса")
    
    search_guide = st.text_input("🔍 Быстрый поиск по справочнику:", placeholder="Например: социальная стипендия, справка, общежитие...")
    
    # Категории справочника
    cat_names = ["Все темы"] + [cat["title"] for cat in faq_data.get("categories", [])]
    selected_cat = st.radio("Категория:", options=cat_names, horizontal=True)
    
    st.markdown("---")
    
    # Вывод статей FAQ
    matched_items = 0
    for cat in faq_data.get("categories", []):
        if selected_cat != "Все темы" and selected_cat != cat["title"]:
            continue
            
        st.markdown(f"### {cat['title']}")
        for item in cat.get("items", []):
            # Простая фильтрация по строке поиска
            if search_guide and (search_guide.lower() not in item["question"].lower() and search_guide.lower() not in item["answer"].lower()):
                continue
                
            matched_items += 1
            with st.expander(f"❓ {item['question']}"):
                st.markdown(item["answer"])
                st.caption(f"📜 *Официальный источник:* {item.get('source', 'Регламент университета')}")
                
    # Контакты подразделений
    st.markdown("---")
    st.markdown("### 🏢 Контакты и часы приёма подразделений")
    for dep in contacts_data.get("departments", []):
        with st.expander(f"📍 {dep['name']}"):
            st.write(dep["description"])
            st.markdown(f"**Адрес:** {dep['address']}")
            st.markdown(f"**Телефон:** `{dep['phone']}` &nbsp;|&nbsp; **Email:** `{dep['email']}`")
            st.markdown(f"**Часы работы:** {dep['schedule']}")


# =====================================================================
# ВКЛАДКА 4: ИИ-Консультант (RAG-чат)
# =====================================================================
with tab_assistant:
    st.subheader("🤖 Интеллектуальный ИИ-ассистент")
    st.caption("Задайте любой вопрос в свободной форме. Ответ формируется строго по официальным документам с ссылками на страницы.")
    
    # Хранилище истории диалога
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Привет! Я твой цифровой ассистент. Я могу ответить на любой сложный вопрос по стипендиям, регламентам проектной деятельности, сессии или общежитиям."
            }
        ]

    # Отрисовка сообщений
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ввод вопроса
    if prompt := st.chat_input("Спросите что угодно по регламентам (например: сколько баллов нужно по проектной деятельности?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Ищу регламенты в базе знаний университета..."):
                # 1. Поиск релевантных фрагментов через BM25
                search_results = retriever.search(prompt, top_k=3)
                context_chunks = [res.chunk for res in search_results]

                # 2. Формирование ответа языковой моделью
                answer = llm.generate_answer(prompt, context_chunks)
                st.markdown(answer)

                # 3. Вывод первоисточников
                if context_chunks:
                    with st.expander("🔍 Посмотреть найденные фрагменты регламентов"):
                        for i, res in enumerate(search_results, 1):
                            meta = f"**{res.chunk.source}**"
                            if res.chunk.page:
                                meta += f" (стр. {res.chunk.page})"
                            st.markdown(f"{i}. {meta} — *соответствие: {res.score:.2f}*")
                            st.caption(f"> {res.chunk.text[:220]}...")

        st.session_state.messages.append({"role": "assistant", "content": answer})
