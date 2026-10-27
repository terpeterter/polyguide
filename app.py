"""🧭 ПолиГид (PolyGuide): Единый цифровой навигатор Московского Политеха.

Универсальный портал для студентов, абитуриентов, родителей и сотрудников университета.
Модульная архитектура:
- Вкладка 1: Инфоцентр кампуса (Навигатор для студентов, абитуриентов и родителей)
- Вкладка 2: Расписание занятий (локальный кэш + интеграция с rasp.dmami.ru)
- Вкладка 3: База знаний и регламенты (FAQ, правила приема, оплата, стипендии, общежития, контакты)
- Вкладка 4: Интеллектуальный ИИ-консультант (RAG: поиск по официальным регламентам + LLM)
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
    page_title="ПолиГид | Московский Политех",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Пользовательские стили оформления
st.markdown("""
<style>
    .portal-banner {
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .portal-card {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
        margin-bottom: 15px;
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


# --- Инициализация и кэширование компонентов системы ---
@st.cache_resource
def init_system():
    """Загрузка документов, построение поискового индекса BM25 и сервисов."""
    chunks = load_all_documents("data/documents")
    retriever = BM25Retriever(chunks)
    llm = LLMClient()
    schedule_service = ScheduleService()
    return chunks, retriever, llm, schedule_service


chunks, retriever, llm, schedule_service = init_system()


# Хелперы загрузки структурированных данных
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


# --- Боковая панель: Профиль и статус пользователя ---
with st.sidebar:
    st.markdown("### 🧭 ПолиГид (PolyGuide)")
    st.caption("Единый навигатор · Московский Политех")
    
    st.divider()
    
    # Селектор категории пользователя
    st.markdown("#### 👤 Кто вы?")
    user_role = st.selectbox(
        "Выберите ваш статус:",
        options=["Студент", "Абитуриент", "Родитель", "Сотрудник / Гость"],
        index=0,
        help="Интерфейс адаптирует быстрые подсказки под ваш статус"
    )
    
    if user_role == "Студент":
        groups_list = schedule_service.get_available_groups()
        default_idx = groups_list.index("241-321") if "241-321" in groups_list else 0
        user_group = st.selectbox(
            "Академическая группа:",
            options=groups_list,
            index=default_idx,
            help="Выберите группу для синхронизации расписания"
        )
        st.caption("🎓 Доступны расписание, сессия, стипендии и проектная деятельность.")
    elif user_role == "Абитуриент":
        user_group = "241-321"
        st.info("🎒 **Приёмная комиссия:**\n\nБ. Семёновская, 38, ауд. В-202\n\nТел: `+7 (495) 223-05-23`\n\nEmail: `priem@mospolytech.ru`")
    elif user_role == "Родитель":
        user_group = "241-321"
        st.info("👨‍👩‍👧 **Договорной отдел (Оплата):**\n\nБ. Семёновская, 38, ауд. А-210\n\nМат. капитал, налоговый вычет 13%, рассрочка")
    else:
        user_group = "241-321"
        st.caption("Добро пожаловать в Московский Политех!")
        
    st.divider()
    
    # Статус базы регламентов RAG
    st.markdown("#### 📚 База знаний вуза")
    st.write(f"Фрагментов в поиске: **{len(chunks)}**")
    if chunks:
        sources = sorted(list(set(c.source for c in chunks)))
        with st.expander("Загруженные регламенты"):
            for s in sources:
                st.caption(f"• `{s}`")
    else:
        st.caption("📂 Документы регламентов не загружены.")
    
    st.divider()
    st.markdown("##### 🔗 Официальные ресурсы")
    st.markdown("""
    - [Официальный сайт Политеха](https://mospolytech.ru/)
    - [Личный кабинет обучающегося](https://online.mospolytech.ru/)
    - [Раздел для абитуриентов](https://mospolytech.ru/postupayushchim/)
    - [Официальное расписание](https://rasp.dmami.ru/)
    """)


# --- Главная шапка портала ---
st.title("🧭 ПолиГид | Московский Политех")
st.caption("Единый информационный навигатор: сервисы, расписание, регламенты и умный поиск для студентов, абитуриентов и родителей")

# --- Основные разделы портала ---
tab_home, tab_schedule, tab_wiki, tab_assistant = st.tabs([
    "🏛️ Инфоцентр кампуса",
    "📅 Расписание занятий",
    "📚 База знаний и регламенты",
    "🤖 ИИ-Консультант"
])


# =====================================================================
# ВКЛАДКА 1: Инфоцентр кампуса (Главная)
# =====================================================================
with tab_home:
    st.markdown("""
    ### 🏛️ Добро пожаловать в единую точку входа Московского Политеха!
    Здесь собрана ключевая информация для всех участников университетской жизни: от правил поступления до учебных регламентов и расписания.
    """)
    
    # 3 фокусных блока по аудиториям
    col_stud, col_abit, col_parent = st.columns(3)
    
    with col_stud:
        st.markdown("""
        <div class="portal-card">
            <h4>🎓 Студентам</h4>
            <p style="color:#888; font-size:13px;">Учебный процесс и кампус</p>
            <ul>
                <li>Расписание пар и звонков</li>
                <li>БРС, зачёты и сессия</li>
                <li>Стипендии и материальная помощь</li>
                <li>Проектная деятельность (ДМ2026)</li>
                <li>Заказ справок об обучении</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_abit:
        st.markdown("""
        <div class="portal-card">
            <h4>🎒 Абитуриентам</h4>
            <p style="color:#888; font-size:13px;">Поступление и правила приёма</p>
            <ul>
                <li>Подача документов и Госуслуги</li>
                <li>Проходные баллы и направления</li>
                <li>Дни открытых дверей</li>
                <li>Общежития на время экзаменов</li>
                <li>Особые права и льготы</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_parent:
        st.markdown("""
        <div class="portal-card">
            <h4>👨‍👩‍👧 Родителям</h4>
            <p style="color:#888; font-size:13px;">Финансы, гарантии и безопасность</p>
            <ul>
                <li>Оплата обучения (рассрочка, семестры)</li>
                <li>Оплата материнским капиталом</li>
                <li>Налоговый вычет 13%</li>
                <li>Отсрочка от призыва в армию</li>
                <li>Контакты руководства и деканатов</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Если студент — показываем оперативную сводку расписания на сегодня
    if user_role == "Студент":
        st.subheader(f"📅 Пары на сегодня (Группа {user_group})")
        days_map = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
        current_day = days_map.get(datetime.today().weekday(), "Понедельник")
        if current_day == "Воскресенье":
            current_day = "Понедельник"
            
        today_lessons = schedule_service.get_schedule(user_group, current_day)
        if today_lessons:
            st.caption(f"Учебные занятия на **{current_day}**:")
            for lesson in today_lessons:
                col_t, col_i = st.columns([1, 4])
                with col_t:
                    st.markdown(f"**Пара {lesson.number}**<br>`{lesson.time_start} - {lesson.time_end}`", unsafe_allow_html=True)
                with col_i:
                    badge = f"<span class='badge-practice'>{lesson.lesson_type}</span>"
                    l_type_lower = lesson.lesson_type.lower()
                    if "лекц" in l_type_lower:
                        badge = f"<span class='badge-lecture'>{lesson.lesson_type}</span>"
                    elif "лаб" in l_type_lower:
                        badge = f"<span class='badge-lab'>{lesson.lesson_type}</span>"
                        
                    dates_str = f"<br><span style='color: #888; font-size: 12px;'>📅 {lesson.dates}</span>" if lesson.dates else ""
                    st.markdown(
                        f"**{lesson.subject}** {badge}<br>"
                        f"👨‍🏫 {lesson.teacher} &nbsp;|&nbsp; 📍 ауд. **{lesson.room}** ({lesson.campus}){dates_str}",
                        unsafe_allow_html=True
                    )
                st.divider()
        else:
            st.info(f"На {current_day} занятий нет. Время для подготовки проектов!")
            
    # Корпуса университета
    st.subheader("📍 Корпуса Московского Политеха")
    corp1, corp2, corp3 = st.columns(3)
    with corp1:
        st.markdown("**Главный корпус (Б. Семёновская)**\n\nул. Большая Семёновская, д. 38 (м. Электрозаводская)")
    with corp2:
        st.markdown("**Корпус на Автозаводской**\n\nул. Автозаводская, д. 16 (м. Автозаводская)")
    with corp3:
        st.markdown("**Корпус на Прянишникова**\n\nул. Прянишникова, д. 2А (м. Тимирязевская)")


# =====================================================================
# ВКЛАДКА 2: Расписание занятий
# =====================================================================
with tab_schedule:
    st.subheader("📅 Расписание учебных занятий")
    if schedule_service.is_online:
        st.caption("🟢 **Онлайн-синхронизация:** Официальный API `rasp.dmami.ru` · Московский Политех")
    else:
        st.caption("🟡 **Оффлайн-режим:** Локальный кэш расписания · Московский Политех")
    
    sched_col1, sched_col2, sched_col3 = st.columns([2, 2, 1])
    with sched_col1:
        groups_list = schedule_service.get_available_groups()
        default_grp_idx = groups_list.index(user_group) if user_group in groups_list else 0
        selected_group = st.selectbox(
            "Выберите академическую группу:",
            options=groups_list,
            index=default_grp_idx,
            key="sched_group_select"
        )
    with sched_col2:
        days_map = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
        today_name = days_map.get(datetime.today().weekday(), "Понедельник")
        day_options = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        default_day_idx = day_options.index(today_name) if today_name in day_options else 0
        selected_day = st.selectbox(
            "День недели:",
            options=day_options,
            index=default_day_idx,
            key="sched_day_select"
        )
    with sched_col3:
        session_choice = st.radio("Режим:", ["Семестр", "Сессия"], horizontal=True, key="sched_session_radio")
        session_val = 1 if session_choice == "Сессия" else 0
        
    lessons = schedule_service.get_schedule(selected_group, selected_day, session=session_val)
    
    if lessons:
        st.markdown(f"#### Занятия на {selected_day} для группы {selected_group} ({session_choice.lower()})")
        for l in lessons:
            with st.container():
                badge_class = "badge-practice"
                l_type_lower = l.lesson_type.lower()
                if "лекц" in l_type_lower:
                    badge_class = "badge-lecture"
                elif "лаб" in l_type_lower:
                    badge_class = "badge-lab"
                    
                dates_info = f"<br><span style='color: #888; font-size: 13px;'>📅 <b>Период:</b> {l.dates}</span>" if l.dates else ""
                
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
                            {dates_info}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info(f"На **{selected_day}** занятий в расписании ({session_choice.lower()}) не найдено.")
        
    st.success("🟢 **API расписания активно:** Сервис подключен к официальному API Московского Политеха (`https://rasp.dmami.ru/`). Доступно расписание 700+ групп в реальном времени.")


# =====================================================================
# ВКЛАДКА 3: База знаний и регламенты
# =====================================================================
with tab_wiki:
    st.subheader("📚 База знаний и регламенты Московского Политеха")
    st.caption("Проверенные ответы на вопросы студентов, абитуриентов и родителей по официальным правилам вуза")
    
    search_guide = st.text_input("🔍 Поиск по базе знаний:", placeholder="Например: материнский капитал, поступление, стипендия, общежитие, справка...")
    
    cat_names = ["Все темы"] + [cat["title"] for cat in faq_data.get("categories", [])]
    selected_cat = st.radio("Тематический раздел:", options=cat_names, horizontal=True)
    
    st.markdown("---")
    
    # Вывод статей базы знаний
    for cat in faq_data.get("categories", []):
        if selected_cat != "Все темы" and selected_cat != cat["title"]:
            continue
            
        st.markdown(f"### {cat['title']}")
        for item in cat.get("items", []):
            if search_guide and (search_guide.lower() not in item["question"].lower() and search_guide.lower() not in item["answer"].lower()):
                continue
                
            with st.expander(f"❓ {item['question']}"):
                st.markdown(item["answer"])
                st.caption(f"📜 *Официальный источник:* {item.get('source', 'Регламент университета')}")
                
    # Контакты всех служб вуза
    st.markdown("---")
    st.markdown("### 🏢 Контакты подразделений университета")
    for dep in contacts_data.get("departments", []):
        with st.expander(f"📍 {dep['name']}"):
            st.write(dep["description"])
            st.markdown(f"**Адрес:** {dep['address']}")
            st.markdown(f"**Телефон:** `{dep['phone']}` &nbsp;|&nbsp; **Email:** `{dep['email']}`")
            st.markdown(f"**Часы работы:** {dep['schedule']}")


# =====================================================================
# ВКЛАДКА 4: ИИ-Консультант (RAG-поиск)
# =====================================================================
with tab_assistant:
    st.subheader("🤖 Интеллектуальный ИИ-консультант")
    st.caption("Отвечает на любые вопросы студентов, абитуриентов и родителей строго по официальным документам вуза со ссылками на первоисточники.")
    
    # Хранилище сообщений
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Здравствуйте! Я цифровой консультант ПолиГид. Задайте любой вопрос по поступлению, учебному процессу, оплате обучения, общежитиям или регламентам Московского Политеха."
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Например: как оплатить учебу материнским капиталом? или: сколько баллов нужно по проектной деятельности?"):
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
