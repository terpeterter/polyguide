"""🧭 Личный кабинет студента и База знаний Московского Политеха.

Стилистика: Y2K Ретро (Windows 98 / Web 1.0) + МосПолитех Модерн.
Включает:
- Живой глобальный поиск с выпадающими подсказками
- Левый сайдбар со всеми 8 разделами Базы знаний и вкладками
- Расписание занятий: колонка «Сводка дня» (Сегодня/Завтра/Дальше) + табличная сетка звонков с корпусами
- База знаний: карточки «КОРОТКО», источники и похожие вопросы
- Заметки и трекер дедлайнов
- Плавающий ИИ-виджет (Floating Action Button) справа внизу
"""

import streamlit as st
import streamlit.components.v1 as components

# Конфигурация Streamlit страницы
st.set_page_config(
    page_title="Московский Политех | Личный кабинет и База знаний",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Скрываем стандартные отступы и шапку Streamlit для бесшовного SPA фронтенда
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden !important; }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
        min-height: 980px !important;
    }
</style>
""", unsafe_allow_html=True)

# Полноценный автономный фронтенд (HTML5 + CSS3 + Vanilla JS)
HTML_FRONTEND = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Личный кабинет студента · Московский Политех</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
  /* ================== ТЕМА 1: СОЧНЫЙ Y2K РЕТРО-ВЕБ ================== */
  --bg-desktop: #006666 radial-gradient(#008f8f 15%, transparent 16%), radial-gradient(#004d4d 15%, transparent 16%);
  --bg-desktop-size: 24px 24px;
  --win-bg: #ece9d8; /* Теплый ностальгический оттенок Windows XP / 2000 */
  --win-face: #f4f1e6;
  --win-header-from: #002b80;
  --win-header-to: #0077ff;
  --win-text: #1a1a1a;
  --win-title-text: #ffffff;
  --border-light: #ffffff;
  --border-dark: #9e9a8e;
  --border-darkest: #4a473f;
  --primary-accent: #0052cc;
  --primary-accent-hover: #003d99;
  
  /* Сочные и аппетитные цвета карточек расписания */
  --card-lecture: linear-gradient(135deg, #fff9db 0%, #ffe066 100%);
  --card-lecture-border: #f59f00;
  --card-lecture-shadow: #e67700;
  
  --card-practice: linear-gradient(135deg, #ffe8cc 0%, #ffd8a8 100%);
  --card-practice-border: #f76707;
  --card-practice-shadow: #d9480f;
  
  --card-lab: linear-gradient(135deg, #d3f9d8 0%, #b2f2bb 100%);
  --card-lab-border: #2b8a3e;
  --card-lab-shadow: #0ca678;

  --card-online: linear-gradient(135deg, #f3d9fa 0%, #eebefa 100%);
  --card-online-border: #ae3ec9;
  
  --box-shadow-bevel: inset -1px -1px 0px #4a473f, inset 1px 1px 0px #ffffff, inset -2px -2px 0px #9e9a8e, inset 2px 2px 0px #ffffff;
  --box-shadow-sunken: inset 1px 1px 0px #4a473f, inset -1px -1px 0px #ffffff, inset 2px 2px 0px #9e9a8e, inset -2px -2px 0px #ffffff;
  --font-system: 'MS Sans Serif', Tahoma, Geneva, 'Segoe UI', sans-serif;
  --font-retro: 'VT323', monospace;
  --font-pixel: 'Press Start 2P', monospace;
  --border-radius: 4px;
}

body.theme-modern {
  /* ================== ТЕМА 2: МОСПОЛИТЕХ МОДЕРН (КИБЕРПАНК DARK) ================== */
  --bg-desktop: #060913 radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 40%), radial-gradient(circle at 90% 80%, rgba(217, 70, 239, 0.15) 0%, transparent 40%);
  --bg-desktop-size: 100% 100%;
  --win-bg: #0d1322;
  --win-face: #141d33;
  --win-header-from: #1e1b4b;
  --win-header-to: #0369a1;
  --win-text: #f1f5f9;
  --win-title-text: #38bdf8;
  --border-light: #334155;
  --border-dark: #1e293b;
  --border-darkest: #020617;
  --primary-accent: #0284c7;
  --primary-accent-hover: #0369a1;
  
  --card-lecture: linear-gradient(135deg, #1e293b 0%, #1e3a5f 100%);
  --card-lecture-border: #38bdf8;
  --card-lecture-shadow: rgba(56, 189, 248, 0.3);
  
  --card-practice: linear-gradient(135deg, #27272a 0%, #3f2f28 100%);
  --card-practice-border: #fb923c;
  --card-practice-shadow: rgba(251, 146, 60, 0.3);
  
  --card-lab: linear-gradient(135deg, #1e2e28 0%, #153e35 100%);
  --card-lab-border: #34d399;
  --card-lab-shadow: rgba(52, 211, 153, 0.3);

  --card-online: linear-gradient(135deg, #281e3a 0%, #381e4b 100%);
  --card-online-border: #c084fc;
  
  --box-shadow-bevel: 0 8px 32px rgba(0, 0, 0, 0.5);
  --box-shadow-sunken: inset 0 2px 4px rgba(0,0,0,0.6);
  --font-system: 'Inter', system-ui, sans-serif;
  --border-radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg-desktop);
  background-size: var(--bg-desktop-size);
  font-family: var(--font-system);
  color: var(--win-text);
  font-size: 13.5px;
  line-height: 1.45;
  height: 100vh;
  overflow: hidden;
  user-select: none;
}

/* Окно Личного кабинета */
.app-window {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--win-bg);
  box-shadow: var(--box-shadow-bevel);
  overflow: hidden;
}

/* Шапка Windows 98 / Modern */
.title-bar {
  background: linear-gradient(90deg, var(--win-header-from), var(--win-header-to));
  color: var(--win-title-text);
  padding: 8px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: bold;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--border-dark);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.title-bar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  font-size: 20px;
  filter: drop-shadow(1px 2px 3px rgba(0,0,0,0.4));
  animation: floatCat 3s ease-in-out infinite;
}

@keyframes floatCat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.title-name {
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.title-badge {
  background: linear-gradient(90deg, #ff007a, #ffbe0b);
  color: #000;
  font-size: 10px;
  font-weight: bold;
  font-family: var(--font-pixel);
  padding: 3px 8px;
  border: 1px solid #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(255, 0, 122, 0.4);
}

.title-bar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Переключатель тем */
.theme-switch-btn {
  background: var(--win-face);
  color: var(--win-text);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 4px 12px;
  cursor: pointer;
  font-size: 11px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.3);
  border-radius: var(--border-radius);
  transition: all 0.15s ease;
}
.theme-switch-btn:hover {
  transform: translateY(-1px);
  filter: brightness(1.05);
}
.theme-switch-btn:active {
  border-color: var(--border-darkest) var(--border-light) var(--border-light) var(--border-darkest);
  box-shadow: none;
  transform: translateY(1px);
}

/* Ретро кнопки в шапке */
.win-controls {
  display: flex;
  gap: 4px;
}
.win-btn {
  width: 22px;
  height: 22px;
  font-size: 11px;
  font-weight: bold;
  background: var(--win-face);
  color: #000;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: var(--border-radius);
  box-shadow: 1px 1px 0px rgba(0,0,0,0.2);
}
.win-btn:hover {
  background: #ff5252;
  color: #fff;
}

/* Верхний блок: Поиск, Слоган, Логотип */
.sub-header {
  background: var(--win-face);
  border-bottom: 2px solid var(--border-dark);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.polytech-logo {
  font-size: 20px;
  font-weight: 900;
  background: linear-gradient(135deg, #0038ff, #ff007a);
  color: #ffffff;
  padding: 6px 10px;
  border: 2px solid #ffffff;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.4);
  border-radius: var(--border-radius);
  letter-spacing: 1px;
}

.header-texts h2 {
  font-size: 14px;
  font-weight: 800;
  color: var(--win-text);
  letter-spacing: 0.3px;
}

.cat-slogan-banner {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: bold;
  color: #d6336c;
  background: #fff0f6;
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px dashed #f783ac;
  margin-top: 3px;
}

body.theme-modern .cat-slogan-banner {
  background: rgba(244, 63, 94, 0.15);
  color: #fb7185;
  border-color: rgba(244, 63, 94, 0.4);
}

/* Живой глобальный поиск */
.search-wrapper {
  position: relative;
  flex: 1;
  max-width: 500px;
}

.search-input-box {
  width: 100%;
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 2px solid;
  border-color: var(--border-dark) var(--border-light) var(--border-light) var(--border-dark);
  box-shadow: inset 1px 1px 3px rgba(0,0,0,0.15);
  padding: 6px 12px;
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}
.search-input-box:focus-within {
  border-color: var(--primary-accent);
  box-shadow: 0 0 8px rgba(0, 82, 204, 0.3);
}

body.theme-modern .search-input-box {
  background: #111827;
  border-color: #38bdf8;
}

.search-input-box input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-family: inherit;
  font-size: 12px;
  color: inherit;
}

/* Выпадающие подсказки поиска */
.search-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: var(--win-face);
  border: 2px solid var(--border-darkest);
  box-shadow: 3px 6px 16px rgba(0,0,0,0.25);
  z-index: 1000;
  display: none;
  max-height: 340px;
  overflow-y: auto;
  border-radius: var(--border-radius);
}

.search-dropdown.open {
  display: block;
}

.search-dropdown-item {
  padding: 10px 14px;
  border-bottom: 1px dotted var(--border-dark);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 3px;
  transition: background 0.15s ease;
}

.search-dropdown-item:hover {
  background: var(--primary-accent);
  color: #ffffff;
}

.search-item-cat {
  font-size: 9px;
  text-transform: uppercase;
  opacity: 0.85;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.search-item-q {
  font-weight: 700;
  font-size: 12px;
}

/* Основной лейаут: Левый сайдбар + Контент */
.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
  height: calc(100vh - 95px);
  position: relative;
}

/* Левая боковая панель (Sidebar) */
.sidebar {
  width: 290px;
  min-width: 290px;
  background: var(--win-face);
  border-right: 2px solid var(--border-dark);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 12px;
  gap: 10px;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1), min-width 0.25s cubic-bezier(0.4, 0, 0.2, 1), padding 0.25s ease, opacity 0.2s ease;
  position: relative;
}

/* Свёрнутый сайдбар (плашки скрыты) */
.sidebar.collapsed {
  width: 0px !important;
  min-width: 0px !important;
  padding: 0px !important;
  overflow: hidden !important;
  border-right: none !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* Плавающая кнопка разворачивания сайдбара */
.sidebar-open-btn {
  display: none;
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--win-face);
  color: var(--win-text);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
  z-index: 100;
  border-radius: var(--border-radius);
  align-items: center;
  gap: 6px;
}
.sidebar-open-btn:hover {
  background: var(--primary-accent);
  color: #fff;
}
.sidebar-open-btn.visible {
  display: flex;
}

/* Кнопка скрыть сайдбар вверху панели */
.sidebar-hide-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
}

.sidebar-collapse-btn {
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  color: var(--win-text);
  padding: 3px 8px;
  font-size: 10px;
  font-weight: bold;
  cursor: pointer;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 1px 1px 0px rgba(0,0,0,0.15);
  transition: all 0.15s ease;
}
.sidebar-collapse-btn:hover {
  background: #ff5252;
  color: #fff;
  border-color: #d32f2f;
}

/* Карточка студента вверху сайдбара */
.sidebar-user-card {
  background: #ffffff;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-radius: var(--border-radius);
  box-shadow: 1px 1px 0px rgba(0,0,0,0.2);
}

body.theme-modern .sidebar-user-card {
  background: #1e293b;
  border: 1px solid #334155;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.user-name {
  font-weight: bold;
  font-size: 12px;
}
.user-status-pill {
  font-size: 10px;
  color: #2b8a3e;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 4px;
}
body.theme-modern .user-status-pill { color: #4ade80; }

.status-dot {
  width: 7px;
  height: 7px;
  background: #20c997;
  border-radius: 50%;
  box-shadow: 0 0 6px #20c997;
  animation: pulse-dot 1.5s infinite;
}

@keyframes pulse-dot {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.8; }
}

.sidebar-section-title {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  color: #555;
  padding: 5px 8px;
  background: rgba(0,0,0,0.06);
  border-left: 3px solid var(--primary-accent);
  letter-spacing: 0.5px;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s ease;
}
.sidebar-section-title:hover {
  background: rgba(0,0,0,0.1);
}

body.theme-modern .sidebar-section-title {
  color: #94a3b8;
  background: rgba(255,255,255,0.06);
}

.section-collapse-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s ease;
}
.section-collapse-content.collapsed {
  display: none;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  list-style: none;
}

.nav-item {
  padding: 8px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid transparent;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--border-radius);
  transition: all 0.15s ease;
}

.nav-item:hover {
  background: rgba(0, 82, 204, 0.08);
  border-color: var(--border-dark);
  transform: translateX(2px);
}

.nav-item.active {
  background: var(--primary-accent);
  color: #ffffff !important;
  border: 2px solid;
  border-color: var(--border-darkest) var(--border-light) var(--border-light) var(--border-darkest);
  box-shadow: inset 1px 1px 0px #000;
  font-weight: bold;
}

body.theme-modern .nav-item.active {
  background: linear-gradient(135deg, #0284c7, #0369a1);
  border: 1px solid #38bdf8;
  box-shadow: 0 0 14px rgba(56, 189, 248, 0.4);
}

.nav-badge-num {
  font-size: 10px;
  background: rgba(0,0,0,0.18);
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: auto;
  font-weight: bold;
}

/* Нижняя часть сайдбара */
.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 10px;
  border-top: 1px dashed var(--border-dark);
}

.sidebar-clock-card {
  position: relative;
  background-color: #030712;
  background-image: 
    linear-gradient(180deg, rgba(3, 7, 18, 0.72) 0%, rgba(2, 6, 23, 0.94) 100%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 120' width='320' height='120'%3E%3Cdefs%3E%3ClinearGradient id='bgSky' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0%25' stop-color='%230f172a'/%3E%3Cstop offset='100%25' stop-color='%23020617'/%3E%3C/linearGradient%3E%3ClinearGradient id='glow' x1='0' y1='0' x2='1' y2='0'%3E%3Cstop offset='0%25' stop-color='%230284c7' stop-opacity='0.5'/%3E%3Cstop offset='100%25' stop-color='%2338bdf8' stop-opacity='0.2'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='320' height='120' fill='url(%23bgSky)'/%3E%3Ccircle cx='30' cy='20' r='1' fill='%23fff' opacity='0.8'/%3E%3Ccircle cx='95' cy='15' r='1.5' fill='%2338bdf8' opacity='0.9'/%3E%3Ccircle cx='180' cy='25' r='1' fill='%23fff' opacity='0.6'/%3E%3Ccircle cx='240' cy='12' r='1.5' fill='%23818cf8' opacity='0.9'/%3E%3Ccircle cx='290' cy='22' r='1' fill='%23fff' opacity='0.7'/%3E%3Cpath d='M0 120 L0 80 L20 80 L20 65 L28 65 L28 55 L36 55 L36 65 L44 65 L44 80 L70 80 L70 88 L95 88 L95 60 L105 45 L115 60 L115 88 L145 88 L145 75 L170 75 L170 70 L185 70 L185 75 L210 75 L210 82 L245 82 L245 72 L260 72 L260 82 L320 82 L320 120 Z' fill='%23091428' opacity='0.95'/%3E%3Cpath d='M8 120 L8 88 L16 88 L16 120 M55 120 L55 92 L63 92 L63 120 M125 120 L125 96 L135 96 L135 120 M195 120 L195 85 L203 85 L203 120 M275 120 L275 90 L285 90 L285 120' stroke='%2338bdf8' stroke-width='1.2' opacity='0.35'/%3E%3Cline x1='0' y1='119' x2='320' y2='119' stroke='url(%23glow)' stroke-width='2'/%3E%3C/svg%3E");
  background-size: cover;
  background-position: center bottom;
  border: 2px solid;
  border-color: var(--border-dark) var(--border-light) var(--border-light) var(--border-dark);
  padding: 10px 12px;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15);
  overflow: hidden;
  user-select: none;
  transition: transform 0.15s ease;
}
.sidebar-clock-card:hover {
  transform: translateY(-1px);
}
body.theme-modern .sidebar-clock-card {
  border: 1px solid #334155;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(56, 189, 248, 0.08);
}

.clock-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.clock-live-indicator {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 9px;
  font-weight: 800;
  color: #38bdf8;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.clock-pulse-dot {
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  box-shadow: 0 0 8px #22c55e;
  animation: clockPulse 1.8s infinite;
}
@keyframes clockPulse {
  0% { transform: scale(0.9); opacity: 0.6; }
  50% { transform: scale(1.25); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.6; }
}
.clock-campus-badge {
  font-size: 9px;
  background: rgba(255,255,255,0.1);
  color: #e2e8f0;
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid rgba(255,255,255,0.15);
}

.retro-clock {
  font-family: 'JetBrains Mono', var(--font-retro), monospace;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 3px;
  text-align: center;
  color: #00ff66;
  text-shadow: 0 0 10px rgba(0, 255, 102, 0.6);
  margin: 2px 0 6px 0;
}
body.theme-modern .retro-clock {
  color: #38bdf8;
  text-shadow: 0 0 16px rgba(56, 189, 248, 0.7);
}

.retro-date {
  font-size: 10px;
  color: #cbd5e1;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}

.clock-week-pill {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 9px;
  background: rgba(2, 132, 199, 0.2);
  border: 1px solid rgba(56, 189, 248, 0.35);
  color: #7dd3fc;
  padding: 2px 8px;
  border-radius: 10px;
  margin: 0 auto;
  max-width: fit-content;
  font-weight: bold;
}

.under-dev-badge {
  background: linear-gradient(135deg, #fff9db 0%, #ffec99 100%);
  border: 2px dashed #f59f00;
  color: #d9480f;
  padding: 6px;
  text-align: center;
  font-size: 10px;
  font-weight: bold;
  animation: pulse-y2k 2.5s infinite alternate;
  border-radius: var(--border-radius);
  box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

@keyframes pulse-y2k {
  0% { transform: scale(0.98); }
  100% { transform: scale(1.01); }
}

/* Центральная область (Контент) */
.content-area {
  flex: 1;
  background: var(--win-bg);
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
}

/* Вкладка: Расписание (2 колонки) */
.schedule-grid-wrap {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 18px;
  align-items: start;
}

/* Левая узкая колонка: Сводка дня */
.day-summary-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.summary-card {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 14px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.25);
  border-radius: var(--border-radius);
}

.summary-card h3 {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--primary-accent);
  border-bottom: 1px solid var(--border-dark);
  padding-bottom: 5px;
}

.lesson-mini {
  background: #ffffff;
  border-left: 4px solid var(--primary-accent);
  padding: 9px 12px;
  margin-bottom: 8px;
  font-size: 11px;
  box-shadow: 1px 2px 4px rgba(0,0,0,0.08);
  border-radius: var(--border-radius);
  transition: transform 0.15s ease;
}
.lesson-mini:hover {
  transform: translateX(2px);
}

body.theme-modern .lesson-mini {
  background: #1e293b;
}

.lesson-mini-time {
  font-weight: bold;
  color: #0052cc;
}
body.theme-modern .lesson-mini-time { color: #38bdf8; }

.lesson-mini-title {
  font-weight: 700;
  font-size: 12px;
  margin: 3px 0;
}

.lesson-mini-meta {
  color: #555;
  font-size: 11px;
}
body.theme-modern .lesson-mini-meta { color: #94a3b8; }

/* Правая широкая колонка: Календарь занятий */
.schedule-table-panel {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 14px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.25);
  border-radius: var(--border-radius);
}

.calendar-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 10px;
}

.week-selector-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.retro-btn {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 4px 12px;
  cursor: pointer;
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--border-radius);
  box-shadow: 1px 1px 0px rgba(0,0,0,0.2);
  transition: all 0.1s ease;
}
.retro-btn:hover {
  filter: brightness(1.08);
}
.retro-btn:active {
  border-color: var(--border-darkest) var(--border-light) var(--border-light) var(--border-darkest);
  box-shadow: none;
}
.retro-btn.active {
  background: #0052cc;
  color: #ffffff;
}

/* Сетка расписания: Дни (Пн-Сб) x Слоты звонков */
.timetable-grid {
  display: grid;
  grid-template-columns: 82px repeat(6, 1fr);
  gap: 6px;
  border: 1px solid var(--border-dark);
  padding: 8px;
  background: #ffffff;
  overflow-x: auto;
  border-radius: var(--border-radius);
}

body.theme-modern .timetable-grid {
  background: #090e17;
}

.time-header-cell, .day-header-cell {
  background: var(--win-bg);
  border: 1px solid var(--border-dark);
  padding: 8px 4px;
  text-align: center;
  font-weight: bold;
  font-size: 11px;
  border-radius: var(--border-radius);
}

.day-header-cell .campus-tag {
  display: block;
  font-size: 9px;
  font-weight: 600;
  color: #666;
  margin-top: 3px;
}
body.theme-modern .day-header-cell .campus-tag { color: #94a3b8; }

.slot-time-cell {
  background: #f1f3f5;
  font-size: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 1px solid var(--border-dark);
  padding: 6px 2px;
  border-radius: var(--border-radius);
}
body.theme-modern .slot-time-cell { background: #1e293b; color: #94a3b8; }

/* Сочные и аппетитные карточки пар */
.lesson-card {
  padding: 8px;
  font-size: 10px;
  border: 2px solid;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 92px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
  transition: all 0.15s ease;
}
.lesson-card:hover {
  transform: translateY(-2px);
  box-shadow: 3px 4px 8px rgba(0,0,0,0.25);
}

.lesson-card.lecture {
  background: var(--card-lecture);
  border-color: var(--card-lecture-border);
}

.lesson-card.practice {
  background: var(--card-practice);
  border-color: var(--card-practice-border);
}

.lesson-card.lab {
  background: var(--card-lab);
  border-color: var(--card-lab-border);
}

.lesson-card.online {
  background: var(--card-online);
  border-color: var(--card-online-border);
}

.lesson-badge {
  display: inline-block;
  padding: 2px 6px;
  font-size: 8px;
  font-weight: 800;
  text-transform: uppercase;
  border-radius: 3px;
  align-self: flex-start;
  margin-bottom: 3px;
  background: rgba(0,0,0,0.12);
  letter-spacing: 0.3px;
}

.lesson-card-name {
  font-weight: 800;
  font-size: 11px;
  line-height: 1.25;
  margin-bottom: 4px;
}

.lesson-card-info {
  font-size: 9px;
  color: #222;
  line-height: 1.3;
}
body.theme-modern .lesson-card-info { color: #e2e8f0; }

.lesson-card-empty {
  background: rgba(0,0,0,0.02);
  border: 1px dashed #ced4da;
  border-radius: var(--border-radius);
  min-height: 92px;
}

/* ================== РАЗДЕЛЫ БАЗЫ ЗНАНИЙ ================== */
.wiki-section-header {
  background: linear-gradient(90deg, #0038ff 0%, #7928ca 100%);
  color: #ffffff;
  padding: 14px 18px;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: var(--border-radius);
  box-shadow: 2px 2px 0px rgba(0,0,0,0.3);
}

.wiki-section-header h2 {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.5px;
  margin: 0;
}

.wiki-questions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.question-row {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 12px 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
  transition: all 0.15s ease;
  border-radius: var(--border-radius);
}

.question-row:hover {
  background: #ffffff;
  border-color: var(--primary-accent);
  transform: translateX(3px);
}
body.theme-modern .question-row:hover {
  background: #1e293b;
  border-color: #38bdf8;
}

.q-left {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.q-title {
  font-weight: 800;
  font-size: 13px;
}

.q-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.badge-tag {
  background: #e7f5ff;
  color: #1971c2;
  border: 1px solid #74c0fc;
  padding: 2px 8px;
  font-size: 10px;
  font-weight: 700;
  border-radius: 4px;
}

body.theme-modern .badge-tag {
  background: #0c4a6e;
  color: #38bdf8;
  border-color: #0284c7;
}

.arrow-icon {
  font-size: 18px;
  font-weight: bold;
  color: var(--primary-accent);
  transition: transform 0.2s ease;
}
.question-row:hover .arrow-icon {
  transform: translateX(4px);
}

/* Детальная карточка ответа Базы знаний */
.answer-detail-modal {
  display: none;
  background: var(--win-face);
  border: 3px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 18px;
  margin-top: 16px;
  box-shadow: 4px 6px 18px rgba(0,0,0,0.3);
  border-radius: var(--border-radius);
}

.answer-detail-modal.active {
  display: block;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.answer-top-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--border-dark);
  padding-bottom: 10px;
  margin-bottom: 14px;
}

.answer-short-box {
  background: #141824;
  color: #f8fafc;
  padding: 16px 20px;
  border-radius: var(--border-radius);
  margin-bottom: 14px;
  border-left: 6px solid #10b981;
  font-size: 13px;
  line-height: 1.6;
  box-shadow: inset 0 2px 6px rgba(0,0,0,0.4);
}

.answer-short-box strong.title {
  color: #10b981;
  display: block;
  font-size: 11px;
  letter-spacing: 1.5px;
  margin-bottom: 6px;
  font-family: var(--font-pixel);
}

.answer-sources-box {
  background: #ffffff;
  border: 1px solid var(--border-dark);
  padding: 12px 16px;
  margin-bottom: 14px;
  border-radius: var(--border-radius);
}
body.theme-modern .answer-sources-box { background: #0f172a; }

.similar-questions-box {
  margin-top: 10px;
}
.similar-btn {
  display: inline-block;
  margin: 4px;
  padding: 5px 10px;
  background: #e9ecef;
  border: 1px solid #adb5bd;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  border-radius: var(--border-radius);
  transition: all 0.15s ease;
}
.similar-btn:hover {
  background: #0052cc;
  color: #fff;
  border-color: #003d99;
}
body.theme-modern .similar-btn { background: #1e293b; border-color: #334155; }

/* ================== ВКЛАДКА: ДАШБОРД ================== */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 16px;
}

.dash-widget {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 16px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
  border-radius: var(--border-radius);
  transition: transform 0.15s ease;
}
.dash-widget:hover {
  transform: translateY(-2px);
}

.dash-widget h3 {
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--border-dark);
  padding-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Студенческий билет в Дашборде */
.student-id-card {
  background: linear-gradient(135deg, #002b80 0%, #0052cc 100%);
  color: #ffffff;
  padding: 14px;
  border-radius: 8px;
  border: 2px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}
.student-id-card::after {
  content: "МОСКОВСКИЙ ПОЛИТЕХ";
  position: absolute;
  right: -20px;
  bottom: -10px;
  font-size: 26px;
  font-weight: 900;
  opacity: 0.1;
  transform: rotate(-10deg);
}

/* Прогресс-бар БРС */
.brs-progress-wrap {
  margin: 10px 0;
}
.brs-progress-bar {
  width: 100%;
  height: 18px;
  background: #dee2e6;
  border: 2px solid #adb5bd;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}
.brs-progress-fill {
  height: 100%;
  width: 88%;
  background: linear-gradient(90deg, #51cf66, #20c997, #0ca678);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(32, 201, 151, 0.5);
}

/* ================== ЗАМЕТКИ И ДЕДЛАЙНЫ ================== */
.notes-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 780px;
}
.note-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  box-shadow: 1px 2px 0px rgba(0,0,0,0.15);
  transition: all 0.15s ease;
}
.note-item:hover {
  background: #ffffff;
}
body.theme-modern .note-item:hover {
  background: #1e293b;
}
.note-item.done {
  text-decoration: line-through;
  opacity: 0.6;
}

/* ================== СОЧНЫЙ ПЕРЕМЕЩАЕМЫЙ ИИ-ВИДЖЕТ (DRAGGABLE FAB) ================== */
.floating-ai-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: linear-gradient(135deg, #ff007a 0%, #7928ca 50%, #0038ff 100%);
  color: #ffffff;
  border: 3px solid #ffffff;
  border-radius: 30px;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: grab;
  box-shadow: 0 8px 24px rgba(255, 0, 122, 0.45);
  z-index: 9998;
  user-select: none;
  touch-action: none;
  animation: fabFloat 3.5s ease-in-out infinite;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.floating-ai-fab:active {
  cursor: grabbing;
  transform: scale(1.05);
}

@keyframes fabFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.floating-ai-fab:hover {
  box-shadow: 0 12px 30px rgba(255, 0, 122, 0.6);
}

.fab-icon {
  font-size: 22px;
  pointer-events: none;
}

.fab-label {
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.5px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
  pointer-events: none;
}

body.theme-modern .floating-ai-fab {
  background: linear-gradient(135deg, #06b6d4, #2563eb, #9333ea);
  border-color: #67e8f9;
  box-shadow: 0 0 25px rgba(6, 182, 212, 0.6);
}

/* Окно ИИ-чата (Перемещаемое и растягиваемое) */
.ai-chat-window {
  position: fixed;
  bottom: 85px;
  right: 24px;
  width: 420px;
  height: 550px;
  min-width: 320px;
  min-height: 380px;
  max-width: 95vw;
  max-height: 95vh;
  resize: both;
  background: var(--win-bg);
  border: 3px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  box-shadow: 6px 10px 30px rgba(0,0,0,0.4);
  z-index: 9999;
  display: none;
  flex-direction: column;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.chat-resize-handle-se {
  position: absolute;
  right: 2px;
  bottom: 2px;
  width: 16px;
  height: 16px;
  cursor: nwse-resize;
  z-index: 10005;
  user-select: none;
  touch-action: none;
  opacity: 0.5;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  pointer-events: auto;
  transition: opacity 0.15s ease;
}
.chat-resize-handle-se:hover {
  opacity: 1;
  color: #0052cc;
}

.chat-resize-handle-nw {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  cursor: nwse-resize;
  z-index: 10005;
  user-select: none;
  touch-action: none;
  opacity: 0.4;
  pointer-events: auto;
}
.chat-resize-handle-nw:hover {
  opacity: 0.9;
}

.ai-chat-window.open {
  display: flex;
  animation: slideUp 0.25s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(25px); }
  to { opacity: 1; transform: translateY(0); }
}

.chat-header {
  background: linear-gradient(90deg, #002b80, #0077ff);
  color: #ffffff;
  padding: 10px 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  cursor: grab;
  user-select: none;
}
.chat-header:active {
  cursor: grabbing;
}

body.theme-modern .chat-header {
  background: linear-gradient(90deg, #1e1b4b, #0369a1);
}

.chat-messages {
  flex: 1;
  padding: 14px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #ffffff;
}

body.theme-modern .chat-messages {
  background: #0b1120;
}

.chat-msg {
  max-width: 85%;
  padding: 9px 13px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.45;
}

/* ================== СТИЛИ МОДАЛКИ ПОДРОБНОСТЕЙ ПАРЫ ================== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.5);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(2px);
}
.modal-overlay.open {
  display: flex;
}
.modal-dialog {
  width: 520px;
  max-width: 90vw;
  background: var(--win-face);
  border: 3px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  box-shadow: 8px 12px 30px rgba(0,0,0,0.4);
  border-radius: var(--border-radius);
  overflow: hidden;
  animation: popIn 0.2s ease-out;
}
@keyframes popIn {
  from { transform: scale(0.92); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Модальное окно деталей пары */
.lesson-modal-body {
  padding: 16px 18px;
}
.lesson-modal-badge-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.lesson-modal-time-tag {
  background: #e7f5ff;
  color: #0052cc;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 4px;
}
body.theme-modern .lesson-modal-time-tag {
  background: rgba(14, 165, 233, 0.18);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
}

.lesson-modal-title {
  font-size: 17px;
  font-weight: 800;
  color: #002b80;
  margin-bottom: 12px;
  line-height: 1.35;
}
body.theme-modern .lesson-modal-title {
  color: #60a5fa !important;
}

.lesson-modal-card {
  background: #ffffff;
  border: 1px solid var(--border-dark);
  padding: 12px 14px;
  border-radius: var(--border-radius);
  font-size: 12px;
  line-height: 1.7;
  margin-bottom: 12px;
  color: #1a1a1a;
}
body.theme-modern .lesson-modal-card {
  background: #1e293b !important;
  border-color: #334155 !important;
  color: #f1f5f9 !important;
}
.lesson-modal-card p {
  margin-bottom: 4px;
}
.lesson-modal-card p:last-child {
  margin-bottom: 0;
}
.lesson-modal-card b {
  color: #002b80;
}
body.theme-modern .lesson-modal-card b {
  color: #93c5fd;
}
.lesson-modal-room {
  font-weight: bold;
  color: #0052cc;
}
body.theme-modern .lesson-modal-room {
  color: #38bdf8 !important;
}

.lesson-modal-route {
  background: #fff9db;
  border: 1px solid #f59f00;
  padding: 10px 14px;
  border-radius: var(--border-radius);
  font-size: 11px;
  line-height: 1.5;
  margin-bottom: 16px;
  color: #795548;
}
body.theme-modern .lesson-modal-route {
  background: rgba(245, 159, 0, 0.12) !important;
  border-color: rgba(245, 159, 0, 0.4) !important;
  color: #fef08a !important;
}

.lesson-modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
body.theme-modern a.retro-btn {
  color: #f1f5f9 !important;
}

/* Стили карточек Общежитий */
.dorm-card-title {
  font-size: 13px;
  font-weight: bold;
  color: #002b80;
}
body.theme-modern .dorm-card-title {
  color: #38bdf8 !important;
}
.dorm-price-tag {
  font-size: 10px;
  font-weight: bold;
  background: #e6fcf5;
  color: #0ca678;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #b2f2bb;
}
body.theme-modern .dorm-price-tag {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.3);
}

/* Таблицы Зачётки и Общежитий */
.retro-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  background: #ffffff;
  border: 1px solid var(--border-dark);
}
body.theme-modern .retro-table {
  background: #0f172a;
}
.retro-table th {
  background: var(--win-bg);
  border: 1px solid var(--border-dark);
  padding: 8px 10px;
  text-align: left;
  font-weight: 800;
  font-size: 11px;
}
.retro-table td {
  border: 1px solid var(--border-dark);
  padding: 8px 10px;
}
.retro-table tr:hover {
  background: rgba(0, 82, 204, 0.05);
}
  box-shadow: 1px 2px 4px rgba(0,0,0,0.06);
}

.chat-msg.bot {
  background: #e7f5ff;
  border: 1px solid #74c0fc;
  align-self: flex-start;
  color: #000;
}
body.theme-modern .chat-msg.bot {
  background: #1e293b;
  border-color: #38bdf8;
  color: #f1f5f9;
}

.chat-msg.user {
  background: linear-gradient(135deg, #d3f9d8, #b2f2bb);
  border: 1px solid #69db7c;
  align-self: flex-end;
  color: #000;
}
body.theme-modern .chat-msg.user {
  background: linear-gradient(135deg, #065f46, #047857);
  border-color: #34d399;
  color: #ffffff;
}

/* Чипсы быстрых подсказок */
.chat-chips {
  padding: 8px 12px;
  background: var(--win-face);
  border-top: 1px solid var(--border-dark);
  display: flex;
  gap: 6px;
  overflow-x: auto;
  white-space: nowrap;
}

.chip-btn {
  background: #ffffff;
  border: 1px solid var(--border-dark);
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  border-radius: 14px;
  box-shadow: 1px 1px 0px rgba(0,0,0,0.1);
  transition: all 0.15s ease;
  color: var(--win-text, #1a1a1a);
}
.chip-btn:hover {
  background: #0052cc;
  color: #fff;
}
body.theme-modern .chip-btn { 
  background: #1e293b; 
  border-color: #475569; 
  color: #e2e8f0; 
}
body.theme-modern .chip-btn:hover {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.deadline-presets-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--win-text, #555555);
  flex-wrap: wrap;
}
body.theme-modern .deadline-presets-bar {
  color: #cbd5e1;
}

.chat-input-area {
  padding: 10px;
  background: var(--win-face);
  border-top: 2px solid var(--border-dark);
  display: flex;
  gap: 8px;
}

.chat-input-area input {
  flex: 1;
  padding: 7px 12px;
  font-size: 12px;
  border: 2px solid;
  border-color: var(--border-dark) var(--border-light) var(--border-light) var(--border-dark);
  border-radius: var(--border-radius);
  outline: none;
}

/* Sound toggle button in title bar */
.sound-toggle-btn {
  background: var(--win-face);
  color: var(--win-text);
  border: 1px solid var(--border-dark);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--border-radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 1px 1px 0px rgba(0,0,0,0.15);
  transition: all 0.15s ease;
}
.sound-toggle-btn:hover {
  background: var(--border-light);
}

/* Notifications Bell and Popover */
.notifications-wrapper {
  position: relative;
  display: inline-block;
}
.notif-bell-btn {
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  font-size: 11px;
  padding: 2px 7px;
  border-radius: var(--border-radius);
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: bold;
  box-shadow: 1px 1px 0px rgba(0,0,0,0.15);
  transition: all 0.15s ease;
}
.notif-bell-btn:hover { background: #ffe066; }
.notif-badge-count {
  background: #fa5252;
  color: #fff;
  font-size: 9px;
  font-weight: bold;
  padding: 1px 5px;
  border-radius: 8px;
}
.notif-dropdown {
  display: none;
  position: absolute;
  top: 115%;
  right: 0;
  width: 340px;
  background: var(--win-face);
  color: #111111 !important;
  text-shadow: none !important;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  box-shadow: 3px 3px 14px rgba(0,0,0,0.4);
  border-radius: var(--border-radius);
  z-index: 1000;
}
.notif-dropdown.open { display: block; }
.notif-header {
  padding: 6px 10px;
  background: #000080;
  color: #fff !important;
  font-size: 11px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
body.theme-modern .notif-header { background: #1e293b; color: #fff !important; }
.notif-clear-btn {
  font-size: 9px;
  text-decoration: underline;
  cursor: pointer;
  opacity: 0.85;
}
.notif-clear-btn:hover { opacity: 1; }
.notif-list {
  max-height: 280px;
  overflow-y: auto;
  padding: 6px;
}
.notif-item {
  padding: 8px 10px;
  margin-bottom: 6px;
  background: #ffffff !important;
  color: #111111 !important;
  text-shadow: none !important;
  border: 1px solid var(--border-dark);
  border-radius: 4px;
  font-size: 11px;
  line-height: 1.4;
  position: relative;
  border-left: 4px solid #1971c2 !important;
}
.notif-item b {
  color: #000080 !important;
}
.notif-item.unread {
  background: #f0f7ff !important;
  border-left: 4px solid #0052cc !important;
}
.notif-item-time {
  font-size: 9px;
  color: #555555 !important;
  margin-top: 3px;
}

body.theme-modern .notif-dropdown {
  color: #f1f5f9 !important;
}
body.theme-modern .notif-item {
  background: #0f172a !important;
  border-color: #334155 !important;
  color: #f1f5f9 !important;
  border-left-color: #3b82f6 !important;
}
body.theme-modern .notif-item.unread {
  background: #1e293b !important;
}
body.theme-modern .notif-item b {
  color: #60a5fa !important;
}
body.theme-modern .notif-item-time {
  color: #94a3b8 !important;
}

/* Digital Student ID card modal */
.student-id-card {
  width: 100%;
  max-width: 480px;
  background: linear-gradient(135deg, #002b66 0%, #001533 100%);
  color: #fff;
  border: 3px solid #ffcc00;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 4px 4px 18px rgba(0,0,0,0.4);
  font-family: inherit;
  position: relative;
  overflow: hidden;
}
.student-id-card::after {
  content: "МОСКОВСКИЙ ПОЛИТЕХ";
  position: absolute;
  right: -20px;
  bottom: 20px;
  font-size: 38px;
  font-weight: 900;
  color: rgba(255,255,255,0.04);
  transform: rotate(-15deg);
  pointer-events: none;
}
.student-id-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255,204,0,0.5);
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.student-id-body {
  display: flex;
  gap: 14px;
}
.student-id-photo {
  width: 90px;
  height: 115px;
  background: #fff;
  border: 2px solid #ffcc00;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: #000;
  box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}
.student-id-info {
  flex: 1;
  font-size: 11px;
  line-height: 1.5;
}
.student-id-info b { color: #ffcc00; }
.student-id-barcode {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px dashed rgba(255,255,255,0.25);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: monospace;
  font-size: 10px;
  letter-spacing: 2px;
}

/* Стили вкладки Проектной деятельности */
.project-header-card {
  background: linear-gradient(90deg, #3b5bdb 0%, #7048e8 100%);
  color: #fff;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.15);
}
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
  margin-bottom: 16px;
}
.project-card {
  background: var(--card-bg);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 14px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.1);
}
.sprint-timeline {
  display: flex;
  gap: 8px;
  margin: 12px 0 0 0;
  overflow-x: auto;
  padding-bottom: 4px;
}
.sprint-step {
  flex: 1;
  min-width: 110px;
  padding: 8px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 4px;
  font-size: 10px;
  text-align: center;
}
.sprint-step.done {
  border-color: #51cf66;
  background: rgba(81,207,102,0.25);
}
.sprint-step.current {
  border-color: #ffd43b;
  background: rgba(255,212,59,0.3);
  font-weight: bold;
}

/* Стили вкладки Справки и Студофис */
.mfc-form-card {
  background: var(--card-bg);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 16px;
  margin-bottom: 16px;
}
.mfc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}
@media (max-width: 768px) {
  .mfc-grid { grid-template-columns: 1fr; }
}
.mfc-order-item {
  background: #fff;
  border: 1px solid var(--border-dark);
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
body.theme-modern .mfc-order-item { background: #1e293b; border-color: #334155; }

/* Стили вкладки Навигатора по аудиториям */
.nav-campus-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.nav-campus-btn {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  padding: 6px 12px;
  font-size: 11px;
  font-weight: bold;
  cursor: pointer;
  border-radius: var(--border-radius);
  transition: all 0.15s ease;
  color: var(--win-text, #1a1a1a);
}
.nav-campus-btn:hover {
  background: #d0d7de;
}
.nav-campus-btn.active {
  background: #000080;
  color: #fff;
}
body.theme-modern .nav-campus-btn {
  background: #1e293b;
  color: #f1f5f9;
  border-color: #475569;
}
body.theme-modern .nav-campus-btn:hover {
  background: #334155;
  color: #ffffff;
  border-color: #64748b;
}
body.theme-modern .nav-campus-btn.active { 
  background: #3b82f6; 
  color: #ffffff; 
  border-color: #60a5fa; 
}
.room-result-card {
  background: var(--card-bg);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 14px;
  margin-top: 10px;
}


/* Полоса живого трекера текущей пары */
.current-lesson-tracker-bar {
  background: #ffffff;
  border: 2px solid #000080;
  border-radius: var(--border-radius);
  padding: 8px 12px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.15);
  flex-wrap: wrap;
}
body.theme-modern .current-lesson-tracker-bar {
  background: #0f172a;
  border-color: #3b82f6;
  color: #f8fafc;
}
.tracker-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.tracker-status-pill.ongoing {
  background: #ff0055;
  color: #fff;
  animation: pulsePill 1.5s infinite;
}
.tracker-status-pill.break {
  background: #f59f00;
  color: #fff;
}
.tracker-status-pill.finished {
  background: #e7f5ff;
  color: #002b80;
}
body.theme-modern .tracker-status-pill.finished {
  background: #1e293b;
  color: #60a5fa;
}
@keyframes pulsePill {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.04); opacity: 0.85; }
  100% { transform: scale(1); opacity: 1; }
}
.tracker-progress-wrap {
  min-width: 150px;
  flex: 1;
  max-width: 240px;
}
.tracker-progress-bar-bg {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border: 1px solid var(--border-dark);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 3px;
}
body.theme-modern .tracker-progress-bar-bg { background: #1e293b; }
.tracker-progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff0055, #ff6b6b);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Стили для селектора недель */
.week-select-dropdown {
  font-weight: bold;
  font-size: 11px;
  padding: 3px 6px;
  border: 1px solid var(--border-dark);
  border-radius: var(--border-radius);
  background: #fff;
  max-width: 230px;
  cursor: pointer;
}
body.theme-modern .week-select-dropdown {
  background: #1e293b;
  color: #f1f5f9;
  border-color: #475569;
}

/* Фильтры исполнителей в проектной деятельности */
.assignee-filter-bar {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}
.assignee-filter-btn {
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  font-size: 10px;
  padding: 2px 7px;
  border-radius: 10px;
  cursor: pointer;
  white-space: nowrap;
}
.assignee-filter-btn.active {
  background: #000080;
  color: #fff;
  border-color: #000080;
}
body.theme-modern .assignee-filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
}


/* =========================================================================
   МОБИЛЬНАЯ АДАПТАЦИЯ И ОПТИМИЗАЦИЯ ДЛЯ СМАРТФОНОВ (<= 768px)
   ========================================================================= */

/* Кнопка гамбургер-меню в шапке */
.mobile-menu-toggle-btn {
  display: none;
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  color: var(--win-text);
  font-size: 15px;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: var(--border-radius);
  cursor: pointer;
  margin-right: 6px;
  box-shadow: 1px 1px 0px rgba(0,0,0,0.2);
  align-items: center;
  justify-content: center;
  touch-action: manipulation;
}

/* Затемняющий оверлей для бокового меню на смартфонах */
.sidebar-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(2px);
  z-index: 9998;
  opacity: 0;
  transition: opacity 0.25s ease;
}
.sidebar-backdrop.active {
  display: block;
  opacity: 1;
}

/* Нижняя панель навигации для телефонов (Mobile Bottom Bar) */
.mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--win-face);
  border-top: 2px solid var(--border-dark);
  box-shadow: 0 -3px 12px rgba(0,0,0,0.18);
  z-index: 9990;
  justify-content: space-around;
  align-items: center;
  padding: 0 4px;
  box-sizing: border-box;
}
body.theme-modern .mobile-bottom-nav {
  background: #0f172a;
  border-color: #334155;
  box-shadow: 0 -3px 18px rgba(0,0,0,0.45);
}

.mobile-nav-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  background: transparent;
  border: none;
  padding: 6px 2px;
  color: var(--win-text);
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.15s ease;
  user-select: none;
  touch-action: manipulation;
}
.mobile-nav-btn.active {
  color: #000080;
  font-weight: bold;
  background: rgba(0,0,128,0.08);
}
body.theme-modern .mobile-nav-btn.active {
  color: #38bdf8;
  background: rgba(56,189,248,0.12);
}
.mobile-nav-btn .mob-icon {
  font-size: 18px;
  line-height: 1;
}
.mobile-nav-btn .mob-label {
  font-size: 10px;
  letter-spacing: -0.2px;
}

/* Мобильный селектор дней в расписании */
.mobile-day-selector {
  display: none;
  gap: 6px;
  margin-bottom: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
}
.mob-day-chip {
  flex: 1;
  min-width: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6px 4px;
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  font-weight: bold;
  color: var(--win-text);
  box-shadow: 1px 1px 0px rgba(0,0,0,0.1);
  transition: all 0.15s ease;
  touch-action: manipulation;
}
.mob-day-chip.active {
  background: #000080;
  color: #ffffff;
  border-color: #000080;
  box-shadow: inset 1px 1px 3px rgba(0,0,0,0.3);
}
body.theme-modern .mob-day-chip.active {
  background: #3b82f6;
  border-color: #3b82f6;
}
.mob-day-chip .day-count {
  font-size: 9px;
  opacity: 0.85;
  font-weight: normal;
  margin-top: 1px;
}

/* Мобильный вертикальный список пар */
.mobile-day-feed {
  display: none;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}
.mobile-lesson-item {
  background: #ffffff;
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 12px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.12);
  cursor: pointer;
  transition: transform 0.15s ease;
}
.mobile-lesson-item:active {
  transform: scale(0.98);
}
body.theme-modern .mobile-lesson-item {
  background: #1e293b;
  border-color: #334155;
  color: #f8fafc;
}

/* Горизонтальная обёртка для сетки расписания */
.timetable-grid-wrapper {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border-radius: var(--border-radius);
}

/* Медиа-запросы для мобильных смартфонов (<= 680px) */
@media (max-width: 680px) {
  /* Шапка */
  .title-bar {
    padding: 6px 8px;
  }
  .title-bar-left {
    gap: 4px;
  }
  .title-name {
    font-size: 11px;
    max-width: 140px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .title-badge, .win-controls {
    display: none !important;
  }
  .title-bar-actions {
    gap: 4px;
  }
  .sound-toggle-btn span:last-child {
    display: none;
  }
  .theme-switch-btn span:last-child {
    display: none;
  }

  /* Подшапка и поиск */
  .sub-header {
    flex-direction: column;
    padding: 8px 10px;
    gap: 8px;
  }
  .header-brand {
    width: 100%;
  }
  .header-texts h2 {
    font-size: 13px;
  }
  .cat-slogan-banner {
    font-size: 9px;
  }
  .search-wrapper {
    max-width: 100%;
    width: 100%;
  }
  .mobile-menu-toggle-btn {
    display: inline-flex;
  }

  /* Выпадающее окно уведомлений */
  .notif-dropdown {
    width: calc(100vw - 20px) !important;
    right: -70px !important;
  }

  /* Сайдбар превращается в мобильную шторку (Drawer) */
  .main-layout {
    height: auto !important;
    min-height: calc(100vh - 140px) !important;
    overflow: visible !important;
  }
  .sidebar {
    position: fixed !important;
    top: 0 !important;
    bottom: 0 !important;
    left: -320px !important;
    width: 280px !important;
    min-width: 280px !important;
    z-index: 10000 !important;
    box-shadow: 6px 0 25px rgba(0,0,0,0.5) !important;
    transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    background: var(--win-face) !important;
  }
  .sidebar.mobile-open {
    left: 0 !important;
  }
  .sidebar-open-btn {
    display: none !important;
  }

  /* Контентная область с отступом под нижний мобильный бар */
  .content-area {
    padding: 10px 10px 80px 10px !important;
    overflow-y: visible !important;
    width: 100% !important;
  }

  /* Отображение мобильного нижнего бара */
  .mobile-bottom-nav {
    display: flex;
  }

  /* Плавающая кнопка ИИ над нижним баром */
  .floating-ai-fab {
    bottom: 70px !important;
    right: 12px !important;
    padding: 6px 12px !important;
    font-size: 11px !important;
  }

  /* Окно чата на весь экран снизу (Bottom Sheet) */
  .ai-chat-window {
    width: 100% !important;
    max-width: 100vw !important;
    height: 85vh !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    border-radius: 16px 16px 0 0 !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: none !important;
  }

  /* Расписание на телефоне */
  .schedule-grid-wrap {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  .day-summary-panel {
    display: block !important;
    width: 100% !important;
  }
  .calendar-top-bar {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
  }
  .week-selector-group {
    justify-content: space-between !important;
    width: 100% !important;
  }
  .week-select-dropdown {
    flex: 1 !important;
    max-width: none !important;
  }
  .mobile-day-selector {
    display: flex !important;
  }
  .mobile-day-feed {
    display: flex !important;
  }
  .timetable-grid-wrapper.mobile-hide-grid {
    display: none !important;
  }

  /* Сетка дашборда и виджеты */
  .dashboard-grid {
    grid-template-columns: 1fr !important;
  }
  .project-grid {
    grid-template-columns: 1fr !important;
  }
  .mfc-grid {
    grid-template-columns: 1fr !important;
  }

  /* Модальные окна */
  .modal-dialog {
    width: 95vw !important;
    max-height: 90vh !important;
    margin: 10px !important;
  }
  .student-id-card {
    padding: 12px !important;
  }
  .student-id-photo {
    width: 75px !important;
    height: 95px !important;
  }
}


/* =========================================================================
   ФИКСЫ ЦВЕТА ТЕКСТА И КОНТРАСТНОСТИ ДЛЯ ТЕМНОЙ ТЕМЫ (THEME MODERN)
   ========================================================================= */

/* Карточки объявлений на дашборде */
.dash-announcement-card {
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 11px;
  line-height: 1.5;
  border: 1px solid;
}
.dash-announcement-card.warning {
  background: #fff9db;
  border-color: #ffe066;
  color: #2b2b2b;
}
.dash-announcement-card.warning .announcement-title { color: #d9480f; }
.dash-announcement-card.info {
  background: #e7f5ff;
  border-color: #a5d8ff;
  color: #2b2b2b;
}
.dash-announcement-card.info .announcement-title { color: #1971c2; }
.dash-announcement-card.promo {
  background: #f3d9fa;
  border-color: #d0bfff;
  color: #2b2b2b;
}
.dash-announcement-card.promo .announcement-title { color: #7928ca; }

body.theme-modern .dash-announcement-card.warning {
  background: rgba(245, 159, 0, 0.15) !important;
  border-color: rgba(245, 159, 0, 0.45) !important;
  color: #fef08a !important;
}
body.theme-modern .dash-announcement-card.warning .announcement-title { color: #fbbf24 !important; }

body.theme-modern .dash-announcement-card.info {
  background: rgba(59, 130, 246, 0.15) !important;
  border-color: rgba(59, 130, 246, 0.45) !important;
  color: #bfdbfe !important;
}
body.theme-modern .dash-announcement-card.info .announcement-title { color: #60a5fa !important; }

body.theme-modern .dash-announcement-card.promo {
  background: rgba(168, 85, 247, 0.15) !important;
  border-color: rgba(168, 85, 247, 0.45) !important;
  color: #e9d5ff !important;
}
body.theme-modern .dash-announcement-card.promo .announcement-title { color: #c084fc !important; }

/* Карточки базы знаний (Скриншот 4) */
.wiki-cat-title {
  color: #000080;
  margin: 4px 0;
  font-size: 13px;
  font-weight: bold;
}
.wiki-cat-desc {
  font-size: 11px;
  color: #555555;
  margin: 4px 0;
}
.wiki-cat-link {
  margin-top: 8px;
  font-size: 10px;
  font-weight: bold;
  color: #1971c2;
}
body.theme-modern .dash-widget {
  background: #111827 !important;
  border-color: #374151 !important;
  color: #e5e7eb !important;
}

/* Карточка пары в дашборде */
.dash-pair-box {
  background: #e7f5ff;
  border: 1px solid #74c0fc;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 4px 0;
  transition: all 0.15s ease;
}
.dash-pair-time {
  color: #0052cc;
  font-weight: 800;
  font-size: 11px;
}
.dash-pair-name {
  font-weight: 700;
  font-size: 13px;
  margin: 2px 0;
  color: #1a1a1a;
}
.dash-pair-meta {
  font-size: 11px;
  color: #495057;
}
body.theme-modern .dash-pair-box {
  background: #1e293b !important;
  border-color: #38bdf8 !important;
}
body.theme-modern .dash-pair-time {
  color: #38bdf8 !important;
}
body.theme-modern .dash-pair-name {
  color: #f8fafc !important;
}
body.theme-modern .dash-pair-meta {
  color: #cbd5e1 !important;
}
body.theme-modern .wiki-cat-title {
  color: #60a5fa !important;
}
body.theme-modern .wiki-cat-desc {
  color: #94a3b8 !important;
}
body.theme-modern .wiki-cat-link {
  color: #38bdf8 !important;
}

/* Карточки навигатора по аудиториям (Скриншот 5) */
.room-badge {
  background: #000080;
  color: #ffffff;
  font-size: 12px;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: var(--border-radius);
  display: inline-block;
}
.room-card-title {
  margin: 6px 0 2px 0;
  font-size: 13px;
  font-weight: bold;
  color: #000080;
}
.room-card-meta {
  font-size: 10px;
  color: #555555;
}
.room-card-desc {
  font-size: 11px;
  margin: 8px 0;
  color: #333333;
  line-height: 1.4;
}
.room-card-route {
  background: var(--win-face);
  border: 1px solid var(--border-dark);
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 10px;
  color: var(--win-text);
}

body.theme-modern .room-result-card {
  background: #111827 !important;
  border-color: #374151 !important;
  color: #e5e7eb !important;
}
body.theme-modern .room-badge {
  background: #2563eb !important;
  color: #ffffff !important;
}
body.theme-modern .room-card-title {
  color: #60a5fa !important;
}
body.theme-modern .room-card-meta {
  color: #94a3b8 !important;
}
body.theme-modern .room-card-desc {
  color: #cbd5e1 !important;
}
body.theme-modern .room-card-route {
  background: #0f172a !important;
  border-color: #334155 !important;
  color: #e2e8f0 !important;
}
body.theme-modern #roomSearchInput {
  background: #0f172a !important;
  color: #f1f5f9 !important;
  border-color: #38bdf8 !important;
}

/* =========================================================================
   ПОИСКОВАЯ СТРОКА В СТИЛЕ GOOGLE С ИИ-АГЕНТОМ НА ГЛАВНОЙ
   ========================================================================= */
.ai-hero-search-box {
  background: var(--win-face);
  border: 2px solid;
  border-color: var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light);
  border-radius: var(--border-radius);
  padding: 16px 20px;
  margin-bottom: 16px;
  box-shadow: 2px 2px 0px rgba(0,0,0,0.15);
  position: relative;
}
body.theme-modern .ai-hero-search-box {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
  border-color: #3b82f6;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25);
}
.ai-hero-branding {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 8px;
}
.ai-hero-logo {
  font-size: 16px;
  font-weight: 900;
  color: #000080;
  display: flex;
  align-items: center;
  gap: 6px;
}
body.theme-modern .ai-hero-logo {
  color: #38bdf8;
}
.ai-hero-tag {
  font-size: 11px;
  color: #555;
}
body.theme-modern .ai-hero-tag {
  color: #94a3b8;
}
.ai-search-input-container {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 2px solid #0052cc;
  border-radius: 26px;
  padding: 4px 6px 4px 14px;
  box-shadow: 0 3px 12px rgba(0, 82, 204, 0.15);
  transition: all 0.2s ease;
}
.ai-search-input-container:focus-within {
  box-shadow: 0 4px 18px rgba(0, 82, 204, 0.35);
  border-color: #003d99;
}
body.theme-modern .ai-search-input-container {
  background: #0f172a;
  border-color: #38bdf8;
  box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);
}
.ai-search-lens {
  font-size: 16px;
  margin-right: 8px;
}
.ai-search-input-container input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-family: inherit;
  font-size: 12px;
  color: var(--win-text);
  padding: 8px 0;
}
body.theme-modern .ai-search-input-container input {
  color: #f1f5f9;
}
.ai-search-action-btn {
  background: linear-gradient(135deg, #0052cc, #0038ff);
  color: #ffffff;
  border: none;
  border-radius: 18px;
  padding: 7px 16px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  box-shadow: 1px 2px 6px rgba(0, 56, 255, 0.25);
  touch-action: manipulation;
}
.ai-search-action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 1px 4px 10px rgba(0, 56, 255, 0.45);
}
body.theme-modern .ai-search-action-btn {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  box-shadow: 0 0 12px rgba(6, 182, 212, 0.5);
}

.ai-hero-chips {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.hero-chip-btn {
  background: #ffffff;
  border: 1px solid var(--border-dark);
  border-radius: 14px;
  padding: 3px 10px;
  font-size: 11px;
  cursor: pointer;
  color: var(--win-text);
  transition: all 0.15s ease;
  touch-action: manipulation;
}
.hero-chip-btn:hover {
  background: #0052cc;
  color: #fff;
  border-color: #0052cc;
}
body.theme-modern .hero-chip-btn {
  background: #1e293b;
  border-color: #475569;
  color: #e2e8f0;
}
body.theme-modern .hero-chip-btn:hover {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #fff;
}

/* Карточка ответа ИИ прямо на Главной */
.ai-hero-answer-card {
  margin-top: 14px;
  background: #ffffff;
  border: 2px solid #0052cc;
  border-radius: 8px;
  padding: 14px;
  animation: fadeIn 0.25s ease-out;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
body.theme-modern .ai-hero-answer-card {
  background: #0f172a;
  border-color: #38bdf8;
  color: #f1f5f9;
}
.ai-hero-answer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-dark);
  padding-bottom: 6px;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: bold;
  color: #000080;
}
body.theme-modern .ai-hero-answer-top {
  color: #38bdf8;
  border-color: #334155;
}
.ai-hero-answer-content {
  font-size: 12px;
  line-height: 1.5;
  color: var(--win-text);
}
body.theme-modern .ai-hero-answer-content {
  color: #e2e8f0;
}
.ai-hero-answer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px dashed var(--border-dark);
  flex-wrap: wrap;
  gap: 8px;
}
body.theme-modern .ai-hero-answer-bottom {
  border-color: #334155;
}

</style>
</head>
<body>

<div class="app-window">
  <!-- ВЕРХНЯЯ ШАПКА ОКНА (TITLE BAR) -->
  <div class="title-bar">
    <div class="title-bar-left">
      <button class="mobile-menu-toggle-btn" onclick="toggleMobileMenu()" title="Открыть меню">☰</button>
      <span class="title-icon">🐱🎓</span>
      <span class="title-name">Московский Политех · Личный кабинет студента [v2.0.26]</span>
      <span class="title-badge">Y2K CYBER-EDITION</span>
    </div>
    <div class="title-bar-actions">
      <!-- Переключатель звука эффектов -->
      <button class="sound-toggle-btn" id="soundToggleBtn" onclick="toggleSound()" title="Включить/выключить звуковые эффекты ретро-кликов">
        <span id="soundBtnIcon">🔈</span> <span id="soundBtnText">Звук: ВЫКЛ</span>
      </button>

      <!-- Уведомления кампуса -->
      <div class="notifications-wrapper">
        <button class="notif-bell-btn" id="notifBellBtn" onclick="toggleNotifications()" title="Уведомления кампуса">
          🔔 <span class="notif-badge-count" id="notifBadge">3</span>
        </button>
        <div class="notif-dropdown" id="notifDropdown">
          <div class="notif-header">
            <span>📢 Уведомления кампуса</span>
            <span class="notif-clear-btn" onclick="clearNotifications()">Очистить</span>
          </div>
          <div class="notif-list" id="notifList">
            <div class="notif-item unread">
              <b>⭐ Баллы БРС обновлены:</b> Выставлены +15 б. по дисциплине «Веб-разработка». Итого: 88/100 б.
              <div class="notif-item-time">Сегодня, 11:20 · Деканат ФИТ</div>
            </div>
            <div class="notif-item unread">
              <b>🚀 Проектная деятельность (ДМ2026):</b> Напоминаем о необходимости сдать паспорт проекта КТ1 до 15 ноября!
              <div class="notif-item-time">Вчера, 16:45 · Центр проектной деятельности</div>
            </div>
            <div class="notif-item unread">
              <b>📄 Студенческий офис (А-101):</b> Справка об обучении №МП-2026-7120 готова к выдаче в окне №3.
              <div class="notif-item-time">05 ноября · Студофис</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Переключатель тем -->
      <button class="theme-switch-btn" id="themeToggleBtn" onclick="toggleTheme()">
        <span id="themeBtnIcon">💾</span> <span id="themeBtnText">Тема: Y2K Ретро</span>
      </button>
      <div class="win-controls">
        <div class="win-btn" title="Свернуть">_</div>
        <div class="win-btn" title="Развернуть">□</div>
        <div class="win-btn" title="Закрыть">✕</div>
      </div>
    </div>
  </div>

  <!-- ПОДШАПКА: Логотип, слоган с котиками, живой глобальный поиск -->
  <div class="sub-header">
    <div class="header-brand">
      <div class="polytech-logo">МП</div>
      <div class="header-texts">
        <h2>Моё расписание / Личный кабинет</h2>
        <div class="cat-slogan-banner">
          <span>✨</span>
          <span>Добро пожаловать на мою страничку! Котики делают жизнь лучше! 🐾💖</span>
        </div>
      </div>
    </div>

    <!-- Живой глобальный поиск по базе знаний с подсказками -->
    <div class="search-wrapper">
      <div class="search-input-box">
        <span style="margin-right:6px; font-size:14px;">🔍</span>
        <input type="text" id="globalSearchInput" placeholder="Живой поиск по базе знаний: общежитие, стипендия, ЕУЗ, пересдачи..." autocomplete="off">
      </div>
      <div class="search-dropdown" id="searchDropdown"></div>
    </div>
  </div>

  <!-- СЕТКА: Левый сайдбар + Центральная область -->
  <div class="main-layout">
    <!-- Плавающая кнопка для раскрытия сайдбара, когда он скрыт -->
    <button class="sidebar-open-btn" id="sidebarOpenBtn" onclick="toggleSidebar()">
      <span>☰</span> <span>Развернуть меню</span>
    </button>

    <!-- ЗАТЕМНЯЮЩИЙ БЭКДРОП ДЛЯ МОБИЛЬНОГО МЕНЮ -->
    <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="closeMobileMenu()"></div>

    <!-- ЛЕВАЯ ПАНЕЛЬ НАВИГАЦИИ (САЙДБАР) -->
    <div class="sidebar" id="appSidebar">
      <!-- Верхняя строка с кнопкой свернуть/скрыть -->
      <div class="sidebar-hide-bar">
        <span style="font-size:11px; font-weight:800; color:#555;">🧭 НАВИГАЦИЯ</span>
        <button class="sidebar-collapse-btn" onclick="toggleSidebar()" title="Скрыть боковую панель">
          <span>◀</span> <span>Скрыть панель</span>
        </button>
      </div>

      <!-- Карточка профиля студента -->
      <div class="sidebar-user-card" id="userProfileCard" onclick="openStudentIdModal()" title="Нажмите, чтобы открыть цифровой студенческий билет" style="cursor:pointer;">
        <div class="user-avatar">🐱</div>
        <div class="user-details">
          <div class="user-name">Алексей Смирнов 🪪</div>
          <div class="user-status-pill">
            <span class="status-dot"></span> 241-321 · Бюджет (2 курс)
          </div>
        </div>
      </div>

      <!-- Секция: Кабинет студента -->
      <div class="sidebar-section-title" onclick="toggleSectionContent('navCabinetList', 'chevCabinet')">
        <span>Кабинет студента</span>
        <span id="chevCabinet">▲</span>
      </div>
      <div class="section-collapse-content" id="navCabinetList">
        <ul class="nav-list">
          <li class="nav-item" id="nav-dashboard" onclick="switchTab('dashboard')">
            <span>🏠</span> <span>Главная / Дашборд</span>
          </li>
          <li class="nav-item active" id="nav-schedule" onclick="switchTab('schedule')">
            <span>📅</span> <span>Расписание занятий</span>
            <span class="nav-badge-num" id="currentGroupBadge">241-321</span>
          </li>
          <li class="nav-item" id="nav-projects" onclick="switchTab('projects')">
            <span>🚀</span> <span>Проектная деятельность (ПД)</span>
            <span class="nav-badge-num" style="background:#7928ca; color:#fff;">КТ1</span>
          </li>
          <li class="nav-item" id="nav-gradebook" onclick="switchTab('gradebook')">
            <span>🎓</span> <span>Зачётка и сессия</span>
            <span class="nav-badge-num" style="background:#2b8a3e; color:#fff;">88 б.</span>
          </li>
          <li class="nav-item" id="nav-services" onclick="switchTab('services')">
            <span>📄</span> <span>Справки и Студофис</span>
            <span class="nav-badge-num" style="background:#1971c2; color:#fff;">МФЦ</span>
          </li>
          <li class="nav-item" id="nav-navigator" onclick="switchTab('navigator')">
            <span>🗺️</span> <span>Навигатор по аудиториям</span>
          </li>
          <li class="nav-item" id="nav-dormitory" onclick="switchTab('dormitory')">
            <span>🏢</span> <span>Общежития и кампус</span>
          </li>
          <li class="nav-item" id="nav-notes" onclick="switchTab('notes')">
            <span>📝</span> <span>Заметки и дедлайны</span>
            <span class="nav-badge-num" id="notesCounterBadge" style="background:#fa5252; color:#fff;">3</span>
          </li>
          <li class="nav-item" id="nav-all-wiki" onclick="switchTab('all-wiki')">
            <span>📚</span> <span>Все разделы базы знаний</span>
          </li>
        </ul>
      </div>

      <!-- Секция: База знаний (8 тем) -->
      <div class="sidebar-section-title" style="margin-top:6px;" onclick="toggleSectionContent('sidebarFaqWrap', 'chevFaq')">
        <span>База знаний (8 тем)</span>
        <span id="chevFaq">▲</span>
      </div>
      <div class="section-collapse-content" id="sidebarFaqWrap">
        <ul class="nav-list" id="sidebarFaqList">
          <!-- 8 заглавных тем генерируются через JS -->
        </ul>
      </div>

      <!-- Подвал сайдбара со стильным виджетом времени и кампуса -->
      <div class="sidebar-footer">
        <div class="sidebar-clock-card" title="Московское время и текущая учебная неделя">
          <div class="clock-top-bar">
            <span class="clock-live-indicator">
              <span class="clock-pulse-dot"></span> МСК ОНЛАЙН
            </span>
            <span class="clock-campus-badge">🏛️ МосПолитех</span>
          </div>
          <div class="retro-clock" id="liveClock">00:00:00</div>
          <div class="retro-date" id="liveDate">Вторник · 17 ноября 2026</div>
          <div class="clock-week-pill" id="liveWeekBadge">🗓️ 6-я неделя · Чётная</div>
        </div>
        <div class="under-dev-badge">
          🚧 МОСКОВСКИЙ ПОЛИТЕХ 2026 🚧<br>
          <span style="font-size:9px; font-weight:normal;">Личный кабинет студента · Версия 2.4 Y2K</span>
        </div>
      </div>
    </div>

    <!-- ЦЕНТРАЛЬНАЯ РАБОЧАЯ ОБЛАСТЬ -->
    <div class="content-area" id="mainContentArea">
      <!-- Контент переключается динамически через JS -->
    </div>
  <!-- НИЖНЯЯ ПАНЕЛЬ НАВИГАЦИИ ДЛЯ СМАРТФОНОВ (MOBILE BOTTOM BAR) -->
  <div class="mobile-bottom-nav">
    <button class="mobile-nav-btn active" id="mob-schedule" onclick="switchTab('schedule')">
      <span class="mob-icon">📅</span>
      <span class="mob-label">Пары</span>
    </button>
    <button class="mobile-nav-btn" id="mob-dashboard" onclick="switchTab('dashboard')">
      <span class="mob-icon">🏠</span>
      <span class="mob-label">Главная</span>
    </button>
    <button class="mobile-nav-btn" id="mob-projects" onclick="switchTab('projects')">
      <span class="mob-icon">🚀</span>
      <span class="mob-label">Проекты</span>
    </button>
    <button class="mobile-nav-btn" id="mob-gradebook" onclick="switchTab('gradebook')">
      <span class="mob-icon">🎓</span>
      <span class="mob-label">Зачётка</span>
    </button>
    <button class="mobile-nav-btn" id="mob-more" onclick="toggleMobileMenu()">
      <span class="mob-icon">☰</span>
      <span class="mob-label">Ещё</span>
    </button>
  </div>
  </div>
</div>

<!-- МОДАЛЬНОЕ ОКНО ДЕТАЛЕЙ ПАРЫ -->
<div class="modal-overlay" id="lessonModal" onclick="closeLessonModal(event)">
  <div class="modal-dialog" id="lessonModalContent">
    <!-- Заполняется динамически -->
  </div>
</div>

<!-- ПОДВИЖНЫЙ СОЧНЫЙ ИИ-ВИДЖЕТ В ПРАВОМ НИЖНЕМ УГЛУ (DRAGGABLE FAB) -->
<div class="floating-ai-fab" id="aiFab" title="Потяните, чтобы переместить, или нажмите, чтобы открыть чат">
  <span class="fab-icon">🤖</span>
  <span class="fab-label">ИИ Помощник</span>
</div>

<!-- ОКНО ЧАТА С ИИ -->
<div class="ai-chat-window" id="aiChatWindow">
  <div class="chat-resize-handle-nw" id="chatResizeHandleNW" title="Потяните для изменения размера"></div>
  <div class="chat-header">
    <div style="display:flex; align-items:center; gap:8px;">
      <span style="font-size:18px;">🤖</span>
      <div>
        <div style="font-size:12px; font-weight:800;">ПолиГид AI · Консультант</div>
        <div style="font-size:9px; opacity:0.85;">🟢 В сети | Регламенты МосПолитеха 2026</div>
      </div>
    </div>
    <div style="display:flex; gap:4px; align-items:center;">
      <div class="win-btn" id="aiChatMaxBtn" onclick="toggleMaximizeAiChat()" title="Развернуть / Восстановить" style="color:#000; font-size:11px; line-height:1; padding:2px 6px;">🗖</div>
      <div class="win-btn" onclick="toggleAiChat()" title="Закрыть" style="color:#000; padding:2px 6px;">✕</div>
    </div>
  </div>

  <div class="chat-messages" id="chatMessages">
    <div class="chat-msg bot">
      👋 <b>Привет!</b> Я цифровой ассистент Московского Политеха. Чем могу помочь? Спроси про расписание, пары завтра, общежитие, стипендию или логин ЕУЗ!
    </div>
  </div>

  <!-- Быстрые чипсы-подсказки -->
  <div class="chat-chips">
    <button class="chip-btn" onclick="sendChip('Где узнать логин ЕУЗ?')">🔑 Логин ЕУЗ</button>
    <button class="chip-btn" onclick="sendChip('Сколько стоит общежитие?')">🏠 Общежитие</button>
    <button class="chip-btn" onclick="sendChip('Какие пары завтра?')">📅 Пары завтра</button>
    <button class="chip-btn" onclick="sendChip('Как заказать справку об обучении?')">📄 Справка</button>
    <button class="chip-btn" onclick="sendChip('Как получить автомат по БРС?')">📊 Автомат по БРС</button>
  </div>

  <div class="chat-input-area" style="position:relative;">
    <input type="text" id="aiChatInput" placeholder="Задайте вопрос..." onkeydown="handleChatKey(event)">
    <button class="retro-btn" onclick="sendChatMessage()">ОК</button>
    <div class="chat-resize-handle-se" id="chatResizeHandleSE" title="Потяните для изменения размера">
      <svg width="12" height="12" viewBox="0 0 12 12" style="display:block;">
        <path d="M11 2v9H2L11 2z" fill="currentColor" opacity="0.4"/>
        <path d="M11 6v5H6L11 6z" fill="currentColor" opacity="0.75"/>
      </svg>
    </div>
  </div>
</div>

<script>
// =========================================================================
// 1. ДАННЫЕ БАЗЫ ЗНАНИЙ (8 ЗАГЛАВНЫХ ТЕМ МОСКОВСКОГО ПОЛИТЕХА)
// =========================================================================
const WIKI_CATEGORIES = [
  {
    id: "cat_1",
    code: "01",
    title: "Поступление",
    desc: "документы, экзамены, приоритеты, зачисление",
    icon: "🎒",
    items: [
      {
        id: "q1_1",
        question: "Как подать документы для поступления в МосПолитех?",
        tags: ["По официальным источникам", "Приём 2026", "Абитуриенту"],
        verified: "25 октября 2026",
        short: "Подать документы можно через суперсервис «Поступление в вуз онлайн» на портале Госуслуг, в личном кабинете абитуриента на сайте e.mospolytech.ru или лично в Приёмной комиссии (ул. Б. Семёновская, 38, ауд. В-202).",
        sources: [
          { name: "Официальный портал приёма МосПолитеха", url: "https://mospolytech.ru/postupayushchim/" },
          { name: "Личный кабинет абитуриента e.mospolytech.ru", url: "https://online.mospolytech.ru/" }
        ],
        similar: ["Какие документы нужны для поступления?", "Предоставляется ли общежитие абитуриентам?"]
      },
      {
        id: "q1_2",
        question: "Какие документы нужны для подачи заявления?",
        tags: ["Приём 2026", "Документы"],
        verified: "18 октября 2026",
        short: "Паспорт гражданина РФ, документ об образовании с приложением (аттестат или диплом СПО), номер СНИЛС, 4 фотографии 3х4 и медицинская справка формы 086/у.",
        sources: [
          { name: "Правила приёма 2026 Московского Политеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как подать документы для поступления в МосПолитех?", "Сколько стоит общежитие для студентов?"]
      },
      {
        id: "q1_3",
        question: "Как работают приоритеты зачисления и оригинал аттестата?",
        tags: ["Приём 2026", "Конкурс"],
        verified: "10 октября 2026",
        short: "Зачисление происходит строго по наивысшему приоритету, на который абитуриент проходит по конкурсу баллов. Важно подать согласие и оригинал аттестата (через Госуслуги или лично) до дедлайна основного этапа.",
        sources: [
          { name: "Справочник абитуриента МосПолитеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как подать документы для поступления в МосПолитех?"]
      }
    ]
  },
  {
    id: "cat_2",
    code: "02",
    title: "Учёба",
    desc: "начало занятий, расписание и учебный план",
    icon: "📖",
    items: [
      {
        id: "q2_1",
        question: "Как устроена балльно-рейтинговая система (БРС) и зачёт?",
        tags: ["По официальным источникам", "Первый курс", "Сессия"],
        verified: "15 октября 2026",
        short: "Шкала оценивания — 100 баллов. Для допуска к экзамену/зачёту и успешной сдачи необходимо набрать не менее 60 баллов за семестр (текущая работа, тесты, лабораторные работы и контрольные точки).",
        sources: [
          { name: "Положение о БРС Московского Политеха", url: "https://mospolytech.ru/" },
          { name: "Личный кабинет: электронная зачётка", url: "https://online.mospolytech.ru/" }
        ],
        similar: ["Сколько пересдач даётся студенту при задолженности?"]
      },
      {
        id: "q2_2",
        question: "Сколько пересдач даётся студенту при задолженности?",
        tags: ["По официальным источникам", "Сессия"],
        verified: "12 октября 2026",
        short: "Студенту предоставляются ровно 2 пересдачи: первая — ведущему преподавателю дисциплины, вторая — комиссии кафедры. Сроки ликвидации хвостов объявляются приказом деканата.",
        sources: [
          { name: "Регламент ликвидации академических задолженностей", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как устроена балльно-рейтинговая система (БРС) и зачёт?"]
      },
      {
        id: "q2_3",
        question: "Где смотреть официальное актуальное расписание?",
        tags: ["Расписание", "Сервисы"],
        verified: "20 октября 2026",
        short: "Расписание доступно на официальном сервере rasp.dmami.ru по номеру группы (например, 241-321), а также в мобильном приложении и текущем Личном кабинете.",
        sources: [
          { name: "Официальный портал расписания rasp.dmami.ru", url: "https://rasp.dmami.ru/" }
        ],
        similar: ["Как получить логин и пароль ЕУЗ?"]
      }
    ]
  },
  {
    id: "cat_3",
    code: "03",
    title: "Документы и сервисы",
    desc: "личный кабинет, пропуск, студенческий и справки",
    icon: "🪪",
    items: [
      {
        id: "q3_1",
        question: "Как получить логин и пароль ЕУЗ (online.mospolytech.ru)?",
        tags: ["По официальным источникам", "Первый курс", "ЕУЗ"],
        verified: "14 октября 2026",
        short: "Логин ЕУЗ высылается первокурснику на e-mail, указанный при поступлении. Для восстановления пароля обратитесь с паспортом в Студенческий офис (Б. Семёновская, 38, ауд. А-101) или напишите на studentoffice@mospolytech.ru.",
        sources: [
          { name: "Студенческий офис Московского Политеха", url: "https://online.mospolytech.ru/" }
        ],
        similar: ["Как заказать справку об обучении?"]
      },
      {
        id: "q3_2",
        question: "Как заказать справку об обучении?",
        tags: ["Документы", "Сервисы"],
        verified: "21 октября 2026",
        short: "Заказ оформляется онлайн в Личном кабинете: раздел «Услуги и сервисы» -> «Справка об обучении». Срок изготовления: 1–3 рабочих дня. Готовый документ с печатью забирается в А-101.",
        sources: [
          { name: "Заказ справок в ЛК Студента", url: "https://online.mospolytech.ru/" }
        ],
        similar: ["Как восстановить утерянный электронный пропуск?"]
      },
      {
        id: "q3_3",
        question: "Как восстановить утерянный электронный пропуск?",
        tags: ["Кампус", "Пропуск"],
        verified: "05 октября 2026",
        short: "Обратитесь в Бюро пропусков главного корпуса (Б. Семёновская, 38, проходная). При себе иметь студенческий билет или паспорт. Перевыпуск занимает 10 минут.",
        sources: [
          { name: "Бюро пропусков МосПолитеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как получить логин и пароль ЕУЗ?"]
      }
    ]
  },
  {
    id: "cat_4",
    code: "04",
    title: "Деньги",
    desc: "оплата обучения, бюджетные места и стипендии",
    icon: "💰",
    items: [
      {
        id: "q4_1",
        question: "Как оплатить обучение материнским капиталом?",
        tags: ["По официальным источникам", "Оплата", "Родителям"],
        verified: "11 октября 2026",
        short: "Оформите дополнительное соглашение в Договорном отделе (ауд. А-210) и подайте заявление через Госуслуги или в Социальный фонд РФ (СФР). Средства поступят на лицевой счёт университета напрямую.",
        sources: [
          { name: "Договорной отдел Московского Политеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как оформить налоговый вычет 13% за обучение?"]
      },
      {
        id: "q4_2",
        question: "Кому и как выплачивается академическая стипендия?",
        tags: ["Стипендии", "Бюджет"],
        verified: "01 октября 2026",
        short: "Государственная академическая стипендия выплачивается студентам-бюджетникам, закрывшим сессию на «хорошо» и «отлично» без троек. Выплаты производятся ежемесячно на карту «МИР».",
        sources: [
          { name: "Положение о стипендиальном обеспечении", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как перевестись с платного обучения на бюджет?"]
      },
      {
        id: "q4_3",
        question: "Как оформить налоговый вычет 13% за обучение?",
        tags: ["Финансы", "Родителям"],
        verified: "09 октября 2026",
        short: "Закажите в Студенческом офисе копию лицензии вуза, справку об оплате за отчётный год и акт оказанных услуг, затем подайте декларацию 3-НДФЛ в личном кабинете налогоплательщика ФНС.",
        sources: [
          { name: "Регламент платного обучения", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как оплатить обучение материнским капиталом?"]
      }
    ]
  },
  {
    id: "cat_5",
    code: "05",
    title: "Общежитие",
    desc: "получение места, справки, заселение и быт",
    icon: "🏢",
    items: [
      {
        id: "q5_1",
        question: "Сколько стоит общежитие для студентов Московского Политеха?",
        tags: ["По официальным источникам", "Общежитие", "Первый курс"],
        verified: "15 октября 2026",
        short: "Стоимость проживания составляет от 950 до 1 850 рублей в месяц в зависимости от типа студгородка (коридорный/блочный тип). Оплата производится в личном кабинете online.mospolytech.ru или через банковское приложение.",
        sources: [
          { name: "Приказ об установлении платы за проживание в общежитиях", url: "https://mospolytech.ru/" },
          { name: "Управление студенческим городком МосПолитех", url: "https://mospolytech.ru/" }
        ],
        similar: ["Какие документы нужны для заселения в общежитие?", "Где расположены корпуса общежитий?"]
      },
      {
        id: "q5_2",
        question: "Какие документы нужны для заселения в общежитие?",
        tags: ["Общежитие", "Документы"],
        verified: "15 октября 2026",
        short: "Паспорт, действующая флюорография (срок до 11 месяцев), медицинская справка формы 086/у, 3 фотографии 3х4 и ордер на заселение из личного кабинета.",
        sources: [
          { name: "Памятка заселяющемуся в общежитие", url: "https://mospolytech.ru/" }
        ],
        similar: ["Сколько стоит общежитие для студентов Московского Политеха?"]
      },
      {
        id: "q5_3",
        question: "Где расположены студгородки и корпуса общежитий?",
        tags: ["Общежитие", "Кампус"],
        verified: "02 октября 2026",
        short: "Общежития МосПолитеха находятся по адресам: ул. Малая Переяславская 7/1, ул. Павла Корчагина 22, ул. Михалковская 7, ул. 7-я Парковая 9/26 и ул. Бориса Галушкина 9.",
        sources: [
          { name: "Карта общежитий Московского Политеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Сколько стоит общежитие для студентов Московского Политеха?"]
      }
    ]
  },
  {
    id: "cat_6",
    code: "06",
    title: "Здоровье и поддержка",
    desc: "медицинские документы и личные вопросы",
    icon: "🩺",
    items: [
      {
        id: "q6_1",
        question: "Что делать в случае болезни и как закрыть пропуски?",
        tags: ["По официальным источникам", "Здоровье", "Справки"],
        verified: "19 октября 2026",
        short: "Получите медицинскую справку формы 095/у в поликлинике, заверьте её в здравпункте Политеха (Б. Семёновская, 38) и предоставьте скан в Студенческий офис через ЛК в течение 3 дней после выхода.",
        sources: [
          { name: "Здравпункт Московского Политеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как обратиться в службу психологической поддержки?"]
      },
      {
        id: "q6_2",
        question: "Как обратиться в службу психологической поддержки?",
        tags: ["Поддержка", "Студенту"],
        verified: "17 октября 2026",
        short: "В Московском Политехе работает бесплатная анонимная психологическая служба. Запись доступна через форму в Личном кабинете или по почте psy@mospolytech.ru.",
        sources: [
          { name: "Центр психологической поддержки МосПолитеха", url: "https://mospolytech.ru/" }
        ],
        similar: ["Что делать в случае болезни и как закрыть пропуски?"]
      }
    ]
  },
  {
    id: "cat_7",
    code: "07",
    title: "Возможности",
    desc: "проекты, практика, работа и стажировки",
    icon: "🚀",
    items: [
      {
        id: "q7_1",
        question: "Как оценивается проектная деятельность (ДМ2026)?",
        tags: ["По официальным источникам", "Проекты", "ДМ2026"],
        verified: "24 октября 2026",
        short: "Оценка складывается из контрольных точек семестра: КТ1 (паспорт проекта), КТ2 (промежуточный отчет) и КТ3 (финальная защита перед экспертами). По регламенту ДМ2026 для зачёта необходимо набрать от 60 баллов.",
        sources: [
          { name: "Распоряжение №598-Р о проектной деятельности", url: "https://mospolytech.ru/" },
          { name: "Центр проектной деятельности ЦПД", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как найти стажировку через Центр карьеры?"]
      },
      {
        id: "q7_2",
        question: "Как найти стажировку через Центр карьеры?",
        tags: ["Карьера", "Стажировки"],
        verified: "20 октября 2026",
        short: "Вступайте в Telegram-канал Центра карьеры Политеха и посещайте ежегодную «Ярмарку вакансий». Партнеры: Сбер, Ростех, АвтоВАЗ, Яндекс.",
        sources: [
          { name: "Центр карьеры и трудоустройства", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как оценивается проектная деятельность (ДМ2026)?"]
      }
    ]
  },
  {
    id: "cat_8",
    code: "08",
    title: "Выпуск и смена планов",
    desc: "академ, перевод, отчисление и диплом",
    icon: "🎓",
    items: [
      {
        id: "q8_1",
        question: "Как оформить академический отпуск?",
        tags: ["По официальным источникам", "Академ"],
        verified: "16 октября 2026",
        short: "Академический отпуск предоставляется по медицинским показаниям, семейным обстоятельствам или призыву в армию сроком до 2 лет. Подайте заявление и подтверждающие справки в Студенческий офис (А-101).",
        sources: [
          { name: "Положение о порядке предоставления академических отпусков", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как восстановиться после отчисления?"]
      },
      {
        id: "q8_2",
        question: "Как восстановиться после отчисления по собственному желанию?",
        tags: ["Восстановление", "Учёба"],
        verified: "08 октября 2026",
        short: "Студент имеет право на восстановление в течение 5 лет после отчисления при наличии свободных мест с сохранением бюджетной основы обучения (если обучался на бюджете).",
        sources: [
          { name: "Регламент восстановления обучающихся", url: "https://mospolytech.ru/" }
        ],
        similar: ["Как оформить академический отпуск?"]
      }
    ]
  }
];

// =========================================================================
// 2. БАЗА ДАННЫХ РАСПИСАНИЯ ПО АКАДЕМИЧЕСКИМ ГРУППАМ МОСПОЛИТЕХА
// =========================================================================
const TIME_SLOTS = [
  { num: 1, start: "09:00", end: "10:30" },
  { num: 2, start: "10:40", end: "12:10" },
  { num: 3, start: "12:20", end: "13:50" },
  { num: 4, start: "14:30", end: "16:00" },
  { num: 5, start: "16:10", end: "17:40" }
];

const WEEK_DAYS = [
  { id: "mon", name: "Понедельник", campus: "Б. Семёновская, 38" },
  { id: "tue", name: "Вторник", campus: "Прянишникова, 2А" },
  { id: "wed", name: "Среда", campus: "Б. Семёновская, 38" },
  { id: "thu", name: "Четверг", campus: "Автозаводская, 16" },
  { id: "fri", name: "Пятница", campus: "Б. Семёновская, 38" },
  { id: "sat", name: "Суббота", campus: "Вебинар / Дистант" }
];

// Расписания разных групп Московского Политеха
const GROUPS_DATA = {
  "241-321": {
    faculty: "Факультет информационных технологий (ФИТ)",
    specialty: "09.03.04 Программная инженерия",
    schedule: {
      mon: {
        1: { name: "Проектная деятельность (ДМ2026)", type: "lab", typeName: "Лаб. работа", room: "Б-302", teacher: "Смирнов А. В.", desc: "Работа над паспортом проекта КТ1 и архитектурой приложения", moodle: "https://online.mospolytech.ru" },
        2: { name: "Веб-разработка и frontend", type: "lecture", typeName: "Лекция", room: "А-201", teacher: "д-р наук Ковалёв Д. И.", desc: "Современные frontend-фреймворки, Y2K-дизайн и React компоненты", moodle: "https://online.mospolytech.ru" },
        3: { name: "Базы данных и SQL", type: "practice", typeName: "Практика", room: "Н-412", teacher: "доц. Николаев С. П.", desc: "Нормализация БД, транзакции ACID и сложные JOIN-запросы", moodle: "https://online.mospolytech.ru" }
      },
      tue: {
        2: { name: "Архитектура информационных систем", type: "lecture", typeName: "Лекция", room: "П-304", teacher: "проф. Соколов М. Е.", desc: "Микросервисная архитектура и паттерны проектирования GoF", moodle: "https://online.mospolytech.ru" },
        3: { name: "Дискретная математика", type: "practice", typeName: "Практика", room: "П-210", teacher: "доц. Кузнецова Е. А.", desc: "Теория графов, деревья решений и алгоритмы Дейкстры", moodle: "https://online.mospolytech.ru" },
        4: { name: "Иностранный язык в проф. сфере", type: "practice", typeName: "Практика", room: "П-415", teacher: "Иванова Т. Н.", desc: "Technical English: Software Development & Git Documentation", moodle: "https://online.mospolytech.ru" }
      },
      wed: {
        1: { name: "Операционные системы и сети", type: "lecture", typeName: "Лекция", room: "Б-105", teacher: "Федоров К. С.", desc: "Процессы, потоки, планировщики Linux и модель TCP/IP", moodle: "https://online.mospolytech.ru" },
        2: { name: "Операционные системы (Лаб)", type: "lab", typeName: "Лаб. работа", room: "Н-308", teacher: "Федоров К. С.", desc: "Системные вызовы POSIX, пайпы и сокеты в ОС Linux", moodle: "https://online.mospolytech.ru" }
      },
      thu: {
        2: { name: "Физическая культура и спорт", type: "practice", typeName: "Практика", room: "Спортзал", teacher: "Морозов В. Г.", desc: "Общая физическая подготовка / секция волейбола", moodle: "https://online.mospolytech.ru" },
        3: { name: "Алгоритмы и структуры данных", type: "lecture", typeName: "Лекция", room: "А-1402", teacher: "доц. Васильев О. Д.", desc: "Асимптотическая сложность O(N), хеш-таблицы и красно-черные деревья", moodle: "https://online.mospolytech.ru" },
        4: { name: "Алгоритмы (Лаб)", type: "lab", typeName: "Лаб. работа", room: "А-1410", teacher: "доц. Васильев О. Д.", desc: "Реализация структур данных на C++ и тестирование", moodle: "https://online.mospolytech.ru" }
      },
      fri: {
        1: { name: "Разработка пользовательских интерфейсов", type: "lecture", typeName: "Лекция", room: "А-202", teacher: "Ковалёв Д. И.", desc: "UI/UX паттерны, адаптивность, анимации и доступность a11y", moodle: "https://online.mospolytech.ru" },
        2: { name: "Интерфейсы (Практика)", type: "practice", typeName: "Практика", room: "Н-416", teacher: "Ковалёв Д. И.", desc: "Разработка ретро-дэшборда и SPA на JavaScript", moodle: "https://online.mospolytech.ru" }
      },
      sat: {
        2: { name: "Цифровая культура (Онлайн-курс)", type: "online", typeName: "Онлайн", room: "Moodle / Teams", teacher: "Попова С. М.", desc: "Информационная безопасность и цифровая гигиена студента", moodle: "https://online.mospolytech.ru" }
      }
    }
  },
  "241-211": {
    faculty: "Транспортный факультет",
    specialty: "23.03.03 Эксплуатация транспортно-технологических комплексов",
    schedule: {
      mon: {
        1: { name: "Начертательная геометрия", type: "lecture", typeName: "Лекция", room: "А-105", teacher: "Козлов А. М.", desc: "Методы проецирования, комплексные чертежи точек и прямых", moodle: "https://online.mospolytech.ru" },
        2: { name: "Инженерная графика", type: "practice", typeName: "Практика", room: "Г-302", teacher: "Козлов А. М.", desc: "Выполнение рабочих чертежей деталей в среде КОМПАС-3D", moodle: "https://online.mospolytech.ru" }
      },
      tue: {
        2: { name: "Математический анализ", type: "practice", typeName: "Практика", room: "А-203", teacher: "Иванов А. В.", desc: "Интегральное исчисление и дифференциальные уравнения", moodle: "https://online.mospolytech.ru" },
        3: { name: "Введение в проектную деятельность", type: "practice", typeName: "Практика", room: "Н-405", teacher: "Кудрявцева Ю. С.", desc: "Инженерный проект болида для гоночной серии", moodle: "https://online.mospolytech.ru" }
      },
      wed: {
        2: { name: "Теоретическая механика", type: "lecture", typeName: "Лекция", room: "А-101", teacher: "Николаев В. Д.", desc: "Статика, кинематика и динамика материальной точки", moodle: "https://online.mospolytech.ru" }
      },
      thu: {
        1: { name: "Иностранный язык", type: "practice", typeName: "Практика", room: "Б-205", teacher: "Смирнова Л. А.", desc: "Автомобилестроение и терминология двигателей", moodle: "https://online.mospolytech.ru" },
        2: { name: "Информатика", type: "lab", typeName: "Лаб. работа", room: "В-401", teacher: "Семенов В. В.", desc: "Основы языка Python для инженерных расчетов", moodle: "https://online.mospolytech.ru" }
      },
      fri: {
        3: { name: "Элективная физическая культура", type: "practice", typeName: "Практика", room: "Спортзал", teacher: "Кафедра ФВиС", desc: "Легкая атлетика и общефизическая подготовка", moodle: "https://online.mospolytech.ru" }
      },
      sat: {}
    }
  },
  "231-161": {
    faculty: "Факультет машиностроения",
    specialty: "15.03.01 Машиностроение и робототехника",
    schedule: {
      mon: {
        2: { name: "Материаловедение и ТКМ", type: "lecture", typeName: "Лекция", room: "А-212", teacher: "проф. Белов В. В.", desc: "Диаграмма железо-углерод, термообработка сталей и сплавов", moodle: "https://online.mospolytech.ru" },
        3: { name: "Материаловедение (Лаб)", type: "lab", typeName: "Лаб. работа", room: "Л-104", teacher: "Белов В. В.", desc: "Микроструктурный анализ сплавов и измерение твердости", moodle: "https://online.mospolytech.ru" }
      },
      tue: {
        1: { name: "Сопротивление материалов", type: "lecture", typeName: "Лекция", room: "А-301", teacher: "доц. Романов Г. И.", desc: "Расчет балок на изгиб и кручение, эпюры напряжений", moodle: "https://online.mospolytech.ru" },
        2: { name: "Сопротивление материалов (Практ)", type: "practice", typeName: "Практика", room: "Б-203", teacher: "Романов Г. И.", desc: "Решение расчетно-графических работ РГР", moodle: "https://online.mospolytech.ru" }
      },
      wed: {
        2: { name: "Проектная деятельность (ЦПД)", type: "practice", typeName: "Практика", room: "Н-401", teacher: "Куратор ЦПД", desc: "Проектирование захвата для промышленного робота-манипулятора", moodle: "https://online.mospolytech.ru" }
      },
      thu: {
        3: { name: "Гидравлика и гидропневмопривод", type: "lecture", typeName: "Лекция", room: "А-102", teacher: "Марков С. А.", desc: "Уравнение Бернулли, гидроцилиндры и клапаны управления", moodle: "https://online.mospolytech.ru" }
      },
      fri: {
        1: { name: "Программирование ЧПУ", type: "lab", typeName: "Лаб. работа", room: "В-305", teacher: "Алексеев Д. П.", desc: "G-код и наладка фрезерного станка с ЧПУ", moodle: "https://online.mospolytech.ru" }
      },
      sat: {}
    }
  },
  "221-811": {
    faculty: "Полиграфический институт (Институт издательского дела и журналистики)",
    specialty: "42.03.02 Журналистика и медиатехнологии",
    schedule: {
      mon: {
        1: { name: "Компьютерная верстка и типографика", type: "lab", typeName: "Лаб. работа", room: "П-104", teacher: "Ларионова Е. К.", desc: "Модульные сетки и верстка книжно-журнальных полос в InDesign", moodle: "https://online.mospolytech.ru" },
        2: { name: "История отечественной журналистики", type: "lecture", typeName: "Лекция", room: "П-201", teacher: "проф. Дмитриев Ю. С.", desc: "Периодическая печать XIX–XX веков", moodle: "https://online.mospolytech.ru" }
      },
      tue: {
        2: { name: "Технологии полиграфического производства", type: "lecture", typeName: "Лекция", room: "П-302", teacher: "Чернов В. А.", desc: "Офсетная, цифровая и трафаретная печать, цветоделение CMYK", moodle: "https://online.mospolytech.ru" }
      },
      wed: {
        1: { name: "Медиадизайн и инфографика", type: "practice", typeName: "Практика", room: "П-402", teacher: "Гордеева А. С.", desc: "Визуализация данных для цифровых СМИ и лонгридов", moodle: "https://online.mospolytech.ru" }
      },
      thu: {
        2: { name: "Проектная мастерская медиа", type: "practice", typeName: "Практика", room: "П-215", teacher: "Куратор медиа", desc: "Выпуск студенческого университетского подкаста и журнала", moodle: "https://online.mospolytech.ru" }
      },
      fri: {
        3: { name: "Иностранный язык для медиа", type: "practice", typeName: "Практика", room: "П-310", teacher: "Григорьева Н. И.", desc: "Media Literacy & International Journalism", moodle: "https://online.mospolytech.ru" }
      },
      sat: {}
    }
  }
};

let currentSelectedGroup = "241-321";

function changeSelectedGroup(newGroup) {
  if (GROUPS_DATA[newGroup]) {
    currentSelectedGroup = newGroup;
    const badge = document.getElementById("currentGroupBadge");
    if (badge) badge.textContent = newGroup;
    renderScheduleTab(document.getElementById("mainContentArea"));
  }
}

// Открытие модального окна подробностей пары
function openLessonModal(dayId, slotNum) {
  const grpData = GROUPS_DATA[currentSelectedGroup];
  if (!grpData || !grpData.schedule[dayId] || !grpData.schedule[dayId][slotNum]) return;
  const l = grpData.schedule[dayId][slotNum];
  const day = WEEK_DAYS.find(d => d.id === dayId);
  const slot = TIME_SLOTS.find(s => s.num === slotNum);

  const modal = document.getElementById("lessonModal");
  const content = document.getElementById("lessonModalContent");

  content.innerHTML = `
    <div class="title-bar" style="cursor:default;">
      <div class="title-bar-left">
        <span>📖</span>
        <span>Информация об учебном занятии</span>
      </div>
      <div class="win-btn" onclick="closeLessonModal()" title="Закрыть (Esc)">✕</div>
    </div>
    <div class="lesson-modal-body">
      <div class="lesson-modal-badge-row">
        <span class="lesson-modal-time-tag">Пара №${slot.num} · ${slot.start} — ${slot.end}</span>
        <span class="lesson-badge">${l.typeName}</span>
      </div>

      <h3 class="lesson-modal-title">${l.name}</h3>

      <div class="lesson-modal-card">
        <p>👤 <b>Преподаватель:</b> ${l.teacher}</p>
        <p>📍 <b>Аудитория:</b> <span class="lesson-modal-room">${l.room}</span> (${day.campus})</p>
        <p>🎓 <b>Группа:</b> ${currentSelectedGroup} (${grpData.faculty})</p>
        <p>📝 <b>Тема занятия:</b> ${l.desc || 'Плановое занятие по рабочей программе дисциплины'}</p>
      </div>

      <div class="lesson-modal-route">
        💡 <b>Как добраться:</b> Корпус <i>${day.campus}</i>. На входе приложите студенческий пропуск к турникету.
      </div>

      <div class="lesson-modal-footer">
        <button class="retro-btn" onclick="addNoteFromLesson('${l.name}')">📝 Добавить в заметки</button>
        <div style="display:flex; gap:8px;">
          <a href="${l.moodle}" target="_blank" class="retro-btn" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">🌐 СДО Moodle</a>
          <button class="retro-btn active" onclick="closeLessonModal()">Понятно</button>
        </div>
      </div>
    </div>
  `;

  modal.classList.add("open");
}

function closeLessonModal(e) {
  // Если событие клика передано:
  if (e && e.target) {
    const isOverlay = e.target.id === "lessonModal";
    const isCloseBtn = e.target.closest(".win-btn") || 
                       e.target.closest(".retro-btn") || 
                       e.target.closest("button") ||
                       (e.target.classList && (e.target.classList.contains("win-btn") || e.target.classList.contains("retro-btn")));
    // Если кликнули внутри диалогового окна не по кнопке закрытия — не закрываем
    if (!isOverlay && !isCloseBtn) {
      return;
    }
  }
  const modal = document.getElementById("lessonModal");
  if (modal) {
    modal.classList.remove("open");
    playRetroSound("click");
  }
}

// Закрытие модального окна по клавише Escape
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") {
    const modal = document.getElementById("lessonModal");
    if (modal && modal.classList.contains("open")) {
      closeLessonModal();
    }
  }
});

function addNoteFromLesson(lessonName) {
  const notes = getStoredNotes();
  notes.push({
    id: Date.now(),
    text: `Подготовиться к паре: ${lessonName}`,
    deadline: "К следующему занятию",
    done: false
  });
  saveStoredNotes(notes);
  document.getElementById("lessonModal").classList.remove("open");
  alert(`Задача по предмету «${lessonName}» добавлена в раздел «Заметки и дедлайны»! ✨`);
}

// =========================================================================
// 3. ИНИЦИАЛИЗАЦИЯ И РЕНДЕРИНГ САЙДБАРА
// =========================================================================
function initSidebarFaq() {
  const container = document.getElementById("sidebarFaqList");
  container.innerHTML = "";
  WIKI_CATEGORIES.forEach(cat => {
    const li = document.createElement("li");
    li.className = "nav-item";
    li.id = `nav-${cat.id}`;
    li.onclick = () => switchTab(cat.id);
    li.innerHTML = `<span>${cat.icon}</span> <span>${cat.code}. ${cat.title}</span>`;
    container.appendChild(li);
  });
}

// =========================================================================
// 4. ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК И СВЕРТЫВАНИЕ САЙДБАРА
// =========================================================================
let currentTabId = "schedule";


// =========================================================================
// МОБИЛЬНАЯ НАВИГАЦИЯ И МОБИЛЬНОЕ РАСПИСАНИЕ ПО ДНЯМ
// =========================================================================
let mobileScheduleTab = "mon";
// Автоопределение сегодняшнего дня недели для мобильного вида
try {
  const curDayIdx = new Date().getDay();
  const dayKeysMap = ["mon", "mon", "tue", "wed", "thu", "fri", "sat"];
  mobileScheduleTab = dayKeysMap[curDayIdx] || "mon";
} catch(e) {}

let mobileScheduleView = "feed"; // "feed" (карточки дня) или "grid" (полная сетка)

function selectMobileScheduleDay(dayId) {
  mobileScheduleTab = dayId;
  mobileScheduleView = "feed";
  playRetroSound("click");
  renderScheduleTab(document.getElementById("mainContentArea"));
}

function setMobileScheduleView(view) {
  mobileScheduleView = view;
  playRetroSound("click");
  renderScheduleTab(document.getElementById("mainContentArea"));
}

function toggleMobileMenu() {
  const sidebar = document.getElementById("appSidebar");
  const backdrop = document.getElementById("sidebarBackdrop");
  if (!sidebar) return;
  const isOpen = sidebar.classList.toggle("mobile-open");
  if (backdrop) backdrop.classList.toggle("active", isOpen);
  playRetroSound("click");
}

function closeMobileMenu() {
  const sidebar = document.getElementById("appSidebar");
  const backdrop = document.getElementById("sidebarBackdrop");
  if (sidebar) sidebar.classList.remove("mobile-open");
  if (backdrop) backdrop.classList.remove("active");
}

function switchTab(tabId) {
  currentTabId = tabId;
  // Закрываем мобильное меню при переходе
  closeMobileMenu();

  // Снимаем активность со всех пунктов меню
  document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
  const targetNav = document.getElementById(`nav-${tabId}`);
  if (targetNav) targetNav.classList.add("active");

  // Обновляем активную кнопку в мобильном нижнем баре
  document.querySelectorAll(".mobile-nav-btn").forEach(b => b.classList.remove("active"));
  const mobBtn = document.getElementById(`mob-${tabId}`);
  if (mobBtn) mobBtn.classList.add("active");

  const contentArea = document.getElementById("mainContentArea");

  playRetroSound("click");
  if (tabId === "schedule") {
    renderScheduleTab(contentArea);
  } else if (tabId === "dashboard") {
    renderDashboardTab(contentArea);
  } else if (tabId === "projects") {
    renderProjectsTab(contentArea);
  } else if (tabId === "gradebook") {
    renderGradebookTab(contentArea);
  } else if (tabId === "services") {
    renderServicesTab(contentArea);
  } else if (tabId === "navigator") {
    renderNavigatorTab(contentArea);
  } else if (tabId === "dormitory") {
    renderDormitoryTab(contentArea);
  } else if (tabId === "notes") {
    renderNotesTab(contentArea);
  } else if (tabId === "all-wiki") {
    renderAllWikiTab(contentArea);
  } else if (tabId.startsWith("cat_")) {
    const cat = WIKI_CATEGORIES.find(c => c.id === tabId);
    if (cat) renderCategoryWikiTab(contentArea, cat);
  }
}

// Сворачивание и скрытие левой панели (сайдбара)
let isSidebarCollapsed = false;

function toggleSidebar() {
  isSidebarCollapsed = !isSidebarCollapsed;
  const sidebar = document.getElementById("appSidebar");
  const openBtn = document.getElementById("sidebarOpenBtn");

  if (isSidebarCollapsed) {
    sidebar.classList.add("collapsed");
    openBtn.classList.add("visible");
  } else {
    sidebar.classList.remove("collapsed");
    openBtn.classList.remove("visible");
  }
  try {
    localStorage.setItem("poly_sidebar_collapsed", isSidebarCollapsed ? "1" : "0");
  } catch(e) {}
}

// Аккордеон сворачивания плашек внутри сайдбара
function toggleSectionContent(wrapId, chevId) {
  const wrap = document.getElementById(wrapId);
  const chev = document.getElementById(chevId);
  if (!wrap) return;

  wrap.classList.toggle("collapsed");
  if (chev) {
    chev.textContent = wrap.classList.contains("collapsed") ? "▼" : "▲";
  }
}

// =========================================================================
// 4.1 РЕНДЕР ВКЛАДКИ РАСПИСАНИЯ С ВЫБОРОМ ГРУПП И КЛИКОМ ПО ПАРАМ
// =========================================================================
let currentWeekIndex = 10; // 11-я неделя по умолчанию (текущая)
const WEEKS_LIST = [
  { num: 1, label: "1-я нед (01–06 сен)", parity: "Нечётная" },
  { num: 2, label: "2-я нед (08–13 сен)", parity: "Чётная" },
  { num: 3, label: "3-я нед (15–20 сен)", parity: "Нечётная" },
  { num: 4, label: "4-я нед (22–27 сен)", parity: "Чётная" },
  { num: 5, label: "5-я нед (29 сен–04 окт)", parity: "Нечётная" },
  { num: 6, label: "6-я нед (06–11 окт)", parity: "Чётная" },
  { num: 7, label: "7-я нед (13–18 окт)", parity: "Нечётная" },
  { num: 8, label: "8-я нед (20–25 окт)", parity: "Чётная" },
  { num: 9, label: "9-я нед (27 окт–01 ноя)", parity: "Нечётная" },
  { num: 10, label: "10-я нед (03–08 ноя)", parity: "Чётная" },
  { num: 11, label: "11-я нед (10–15 ноя · ТЕКУЩАЯ)", parity: "Нечётная" },
  { num: 12, label: "12-я нед (17–22 ноя)", parity: "Чётная" },
  { num: 13, label: "13-я нед (24–29 ноя)", parity: "Нечётная" },
  { num: 14, label: "14-я нед (01–06 дек)", parity: "Чётная" },
  { num: 15, label: "15-я нед (08–13 дек)", parity: "Нечётная" },
  { num: 16, label: "16-я нед (15–20 дек)", parity: "Чётная" },
  { num: 17, label: "17-я нед (22–27 дек · Зачёты)", parity: "Нечётная" },
  { num: 18, label: "Зимняя сессия (11–25 янв 2026)", parity: "Экзамены" }
];

function setWeekIndex(idx) {
  currentWeekIndex = idx;
  playRetroSound("click");
  renderScheduleTab(document.getElementById("mainContentArea"));
}
let selectedCampusFilter = "all";

function changeWeek(delta) {
  currentWeekIndex = (currentWeekIndex + delta + WEEKS_LIST.length) % WEEKS_LIST.length;
  renderScheduleTab(document.getElementById("mainContentArea"));
}

function setCampusFilter(campusKey) {
  selectedCampusFilter = campusKey;
  renderScheduleTab(document.getElementById("mainContentArea"));
}


// =========================================================================
// ЖИВОЙ ТРЕКЕР ТЕКУЩЕЙ ПАРЫ В РАСПИСАНИИ
// =========================================================================
function getLiveLessonStatusHtml() {
  const now = new Date();
  const dayIndex = now.getDay(); // 0=Sun, 1=Mon, ..., 6=Sat
  const dayKeys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  const dayKey = dayKeys[dayIndex];
  const dayNames = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
  const todayName = dayNames[dayIndex];

  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const grpData = GROUPS_DATA[currentSelectedGroup] || GROUPS_DATA["241-321"];
  const sched = grpData.schedule;
  const todaySched = sched[dayKey] || {};

  // Выходной день (Воскресенье)
  if (dayIndex === 0) {
    return `
      <div class="current-lesson-tracker-bar">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="tracker-status-pill finished">🛌 ВЫХОДНОЙ ДЕНЬ</span>
          <span style="font-size:12px;">Сегодня <b>${todayName}</b> — занятий нет. Отдыхайте перед учебной неделей!</span>
        </div>
        <div style="font-size:11px; color:#666;">Ближайшие пары: Понедельник в 09:00 (Пара 1)</div>
      </div>
    `;
  }

  const slotsWithMins = [
    { num: 1, startM: 540, endM: 630, start: "09:00", end: "10:30" },
    { num: 2, startM: 640, endM: 730, start: "10:40", end: "12:10" },
    { num: 3, startM: 740, endM: 830, start: "12:20", end: "13:50" },
    { num: 4, startM: 870, endM: 960, start: "14:30", end: "16:00" },
    { num: 5, startM: 970, endM: 1060, start: "16:10", end: "17:40" },
    { num: 6, startM: 1070, endM: 1160, start: "17:50", end: "19:20" }
  ];

  // До 09:00
  if (currentMinutes < 540) {
    const firstLesson = todaySched[1];
    return `
      <div class="current-lesson-tracker-bar">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="tracker-status-pill finished">🌅 ДО НАЧАЛА ЗАНЯТИЙ</span>
          <span style="font-size:12px;">Сегодня <b>${todayName}</b>. Первая пара начнётся в <b>09:00</b>${firstLesson ? `: <b>«${firstLesson.name}»</b> (ауд. ${firstLesson.room})` : ''}</span>
        </div>
        <div style="font-size:11px; color:#0052cc;">Группа ${currentSelectedGroup}</div>
      </div>
    `;
  }

  // После окончания всех пар (после 17:40 / 19:20)
  if (currentMinutes >= 1060) {
    return `
      <div class="current-lesson-tracker-bar">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="tracker-status-pill finished">🌙 ПАРЫ ЗАВЕРШЕНЫ</span>
          <span style="font-size:12px;">Все учебные занятия группы <b>${currentSelectedGroup}</b> на сегодня окончены.</span>
        </div>
        <div style="font-size:11px; color:#2b8a3e; font-weight:bold;">Отличного вечера! 🎉</div>
      </div>
    `;
  }

  // Проверка попадания внутрь слота пары
  for (let s of slotsWithMins) {
    if (currentMinutes >= s.startM && currentMinutes < s.endM) {
      const lesson = todaySched[s.num];
      const elapsed = currentMinutes - s.startM;
      const total = s.endM - s.startM;
      const remaining = s.endM - currentMinutes;
      const pct = Math.min(100, Math.round((elapsed / total) * 100));

      if (lesson) {
        return `
          <div class="current-lesson-tracker-bar" style="border-left: 6px solid #ff0055;">
            <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:280px;">
              <span class="tracker-status-pill ongoing">🔴 ИДЕТ ${s.num}-Я ПАРА</span>
              <div>
                <div style="font-size:12px; font-weight:bold; color:#000080;">
                  ${lesson.name} <span style="font-size:11px; font-weight:normal; color:#444;">(${lesson.typeName})</span>
                </div>
                <div style="font-size:11px; color:#555;">
                  📍 ауд. <b>${lesson.room}</b> · ${lesson.teacher} · ⏰ ${s.start} — ${s.end}
                </div>
              </div>
            </div>

            <div class="tracker-progress-wrap">
              <div style="display:flex; justify-content:space-between; font-size:10px; font-weight:bold;">
                <span>Осталось: <span style="color:#ff0055;">${remaining} мин</span></span>
                <span>${pct}%</span>
              </div>
              <div class="tracker-progress-bar-bg">
                <div class="tracker-progress-bar-fill" style="width:${pct}%;"></div>
              </div>
            </div>
          </div>
        `;
      } else {
        return `
          <div class="current-lesson-tracker-bar">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="tracker-status-pill break">🪟 ОКНО В РАСПИСАНИИ</span>
              <span style="font-size:12px;">Сейчас идёт ${s.num}-я пара (${s.start} — ${s.end}), но у группы <b>${currentSelectedGroup}</b> эта пара свободна!</span>
            </div>
            <div style="font-size:11px; color:#555;">Отличное время заглянуть в коворкинг или столовую ☕</div>
          </div>
        `;
      }
    }
  }

  // Перемена между парами
  const nextSlot = slotsWithMins.find(s => s.startM > currentMinutes);
  if (nextSlot) {
    const nextLesson = todaySched[nextSlot.num];
    const minsUntil = nextSlot.startM - currentMinutes;
    return `
      <div class="current-lesson-tracker-bar" style="border-left: 6px solid #f59f00;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="tracker-status-pill break">☕ ПЕРЕМЕНА</span>
          <span style="font-size:12px;">
            Следующая пара №${nextSlot.num} (${nextSlot.start})${nextLesson ? `: <b>«${nextLesson.name}»</b> (ауд. ${nextLesson.room})` : ''} · до звонка: <b>${minsUntil} мин</b>
          </span>
        </div>
        <div style="font-size:11px; color:#d9480f; font-weight:bold;">Звонок на пару в ${nextSlot.start} 🔔</div>
      </div>
    `;
  }

  return "";
}

function renderScheduleTab(container) {
  const currentWeek = WEEKS_LIST[currentWeekIndex];
  const grpData = GROUPS_DATA[currentSelectedGroup] || GROUPS_DATA["241-321"];
  const sched = grpData.schedule;

  // Определение реального дня недели по локальному календарю
  const now = new Date();
  const dayIdx = now.getDay(); // 0=Вс, 1=Пн, 2=Вт, 3=Ср, 4=Чт, 5=Пт, 6=Сб
  const dayKeysMap = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  const dayNamesMap = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
  const todayKey = dayKeysMap[dayIdx];
  const todayName = dayNamesMap[dayIdx];

  // Следующий день (Завтра)
  const nextDayIdx = (dayIdx + 1) % 7;
  const tomorrowKey = dayKeysMap[nextDayIdx];
  const tomorrowName = dayNamesMap[nextDayIdx];

  // Данные для Сегодня
  const todayLessons = sched[todayKey] || {};
  const todayLessonNums = Object.keys(todayLessons).sort((a,b) => parseInt(a) - parseInt(b));
  const isSundayToday = dayIdx === 0;

  // Данные для Завтра
  const tomorrowLessons = sched[tomorrowKey] || {};
  const tomorrowLessonNums = Object.keys(tomorrowLessons).sort((a,b) => parseInt(a) - parseInt(b));
  const isSundayTomorrow = nextDayIdx === 0;
  const tomorrowDayObj = WEEK_DAYS.find(d => d.id === tomorrowKey);
  const tomorrowCampus = tomorrowDayObj ? tomorrowDayObj.campus : "Кампус Политеха";

  // Список дней для блока "Дальше по расписанию" (исключая сегодня и завтра)
  const upcomingDays = WEEK_DAYS.filter(d => d.id !== todayKey && d.id !== tomorrowKey);

  container.innerHTML = `
    <div class="schedule-grid-wrap">
      <!-- ЛЕВАЯ КОЛОНКА: СВОДКА ДНЯ (ДИНАМИЧЕСКИ ПО РЕАЛЬНОМУ КАЛЕНДАРЮ) -->
      <div class="day-summary-panel">
        <div class="summary-card">
          <h3>📌 СЕГОДНЯ (${todayName.toUpperCase()})</h3>
          ${isSundayToday ? `
            <div style="font-size:11px; margin-bottom:8px; color:#f59f00; font-weight:bold;">🛌 Выходной день · Занятий нет</div>
            <div style="font-size:11px; opacity:0.8; padding:4px 0;">Сегодня воскресенье — день отдыха и подготовки к новой учебной неделе!</div>
          ` : `
            <div style="font-size:11px; margin-bottom:8px; color:#2b8a3e; font-weight:bold;">🟢 Идут занятия · Группа ${currentSelectedGroup}</div>
            
            ${todayLessonNums.length > 0 ? todayLessonNums.map(sNum => {
              const l = todayLessons[sNum];
              const slot = TIME_SLOTS.find(s => s.num === parseInt(sNum));
              return `
                <div class="lesson-mini" onclick="openLessonModal('${todayKey}', ${sNum})" style="cursor:pointer;" title="Нажмите для подробностей">
                  <span class="lesson-mini-time">${slot ? slot.start + ' — ' + slot.end : ''} (Пара ${sNum})</span>
                  <div class="lesson-mini-title">${l.name}</div>
                  <div class="lesson-mini-meta">📍 ауд. <b>${l.room}</b> · ${l.teacher}</div>
                </div>
              `;
            }).join('') : '<div style="font-size:11px; opacity:0.8; padding:4px 0;">На сегодня пар по расписанию нет 🎉</div>'}
          `}
        </div>

        <div class="summary-card">
          <h3>🌅 ЗАВТРА (${tomorrowName.toUpperCase()})</h3>
          ${isSundayTomorrow ? `
            <div style="font-size:11px; margin-bottom:6px; color:#f59f00; font-weight:bold;">🛌 Завтра воскресенье · Выходной день</div>
            <div style="font-size:11px; opacity:0.8; padding:4px 0;">Занятий нет, библиотеки и коворкинги работают по расписанию выходного дня.</div>
          ` : `
            <div style="font-size:11px; margin-bottom:6px;"><b>Всего пар:</b> ${tomorrowLessonNums.length} · <b>Корпус:</b> ${tomorrowCampus}</div>
            ${tomorrowLessonNums.length > 0 ? tomorrowLessonNums.map(sNum => {
              const l = tomorrowLessons[sNum];
              const slot = TIME_SLOTS.find(s => s.num === parseInt(sNum));
              return `
                <div class="lesson-mini" onclick="openLessonModal('${tomorrowKey}', ${sNum})" style="cursor:pointer;" title="Нажмите для подробностей">
                  <span class="lesson-mini-time">${slot ? slot.start + ' — ' + slot.end : ''} (Пара ${sNum})</span>
                  <div class="lesson-mini-title">${l.name}</div>
                  <div class="lesson-mini-meta">📍 ауд. <b>${l.room}</b> · ${l.teacher}</div>
                </div>
              `;
            }).join('') : '<div style="font-size:11px; opacity:0.8; padding:4px 0;">Завтра пар нет — день самостоятельной работы</div>'}
            <div style="font-size:10px; opacity:0.8; padding-left:4px; margin-top:6px;">💡 Нажмите на любую пару в таблице для открытия карты и материалов</div>
          `}
        </div>

        <div class="summary-card">
          <h3>⏩ ДАЛЬШЕ ПО РАСПИСАНИЮ</h3>
          <div style="font-size:11px; line-height:1.7;">
            ${upcomingDays.map(d => {
              const dLessons = sched[d.id] ? Object.keys(sched[d.id]).length : 0;
              return `• <b>${d.name}:</b> ${dLessons > 0 ? dLessons + ' пар' : 'Пар нет'} · ${d.campus}`;
            }).join('<br>')}
          </div>
        </div>
      </div>

      <!-- ПРАВАЯ КОЛОНКА: СЕТКА КАЛЕНДАРЯ -->
      <div class="schedule-table-panel">
        <div class="calendar-top-bar">
          <div class="week-selector-group">
            <button class="retro-btn" onclick="changeWeek(-1)" title="Предыдущая неделя">◀</button>
            <select onchange="setWeekIndex(parseInt(this.value))" class="week-select-dropdown">
              ${WEEKS_LIST.map((w, idx) => `
                <option value="${idx}" ${idx === currentWeekIndex ? 'selected' : ''}>
                  🗓️ ${w.label} [${w.parity}]
                </option>
              `).join('')}
            </select>
            <button class="retro-btn" onclick="changeWeek(1)" title="Следующая неделя">▶</button>
            <span class="badge-tag" style="margin-left:4px;">${currentWeek.parity}</span>
          </div>

          <!-- Выбор группы и корпуса -->
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <div style="display:flex; align-items:center; gap:4px;">
              <span style="font-size:11px; font-weight:bold;">Группа:</span>
              <select onchange="changeSelectedGroup(this.value)" style="font-size:11px; font-weight:bold; padding:4px 8px; border:2px solid #0052cc; border-radius:var(--border-radius); background:#fff; color:#002b80;">
                <option value="241-321" ${currentSelectedGroup==='241-321'?'selected':''}>241-321 (ФИТ - Программная инженерия)</option>
                <option value="241-211" ${currentSelectedGroup==='241-211'?'selected':''}>241-211 (Транспортный факультет)</option>
                <option value="231-161" ${currentSelectedGroup==='231-161'?'selected':''}>231-161 (Машиностроение / Роботы)</option>
                <option value="221-811" ${currentSelectedGroup==='221-811'?'selected':''}>221-811 (Полиграф / Медиа)</option>
              </select>
            </div>

            <div style="display:flex; align-items:center; gap:4px;">
              <span style="font-size:11px; color:#555;">Корпус:</span>
              <select onchange="setCampusFilter(this.value)" style="font-size:11px; padding:3px 6px; border:1px solid var(--border-dark); border-radius:var(--border-radius);">
                <option value="all" ${selectedCampusFilter==='all'?'selected':''}>Все корпуса</option>
                <option value="sem" ${selectedCampusFilter==='sem'?'selected':''}>Б. Семёновская, 38</option>
                <option value="pryan" ${selectedCampusFilter==='pryan'?'selected':''}>Прянишникова, 2А</option>
                <option value="avto" ${selectedCampusFilter==='avto'?'selected':''}>Автозаводская, 16</option>
              </select>
            </div>
          </div>
        </div>

        <div style="font-size:11px; color:#666; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>Направление: <b>${grpData.specialty}</b> · <span style="font-size:10px; color:#0052cc;">🖱️ Кликните пару для аудитории и материалов</span></div>
          <button class="retro-btn" onclick="exportScheduleToIcs()" title="Скачать календарь расписания .ics для смартфона" style="font-size:10px; padding:3px 8px; display:flex; align-items:center; gap:4px; font-weight:bold;">
            <span>📅</span> <span>Экспорт в iCal (.ics)</span>
          </button>
        </div>

        <!-- ЖИВАЯ ПОЛОСА ТЕКУЩЕЙ ПАРЫ -->
        ${getLiveLessonStatusHtml()}

        <!-- МОБИЛЬНЫЙ СЕЛЕКТОР ДНЕЙ НЕДЕЛИ -->
        <div class="mobile-day-selector">
          ${WEEK_DAYS.map(day => {
            const count = sched[day.id] ? Object.keys(sched[day.id]).length : 0;
            return `
              <button class="mob-day-chip ${mobileScheduleTab === day.id ? 'active' : ''}" onclick="selectMobileScheduleDay('${day.id}')">
                <span class="day-short">${day.name.slice(0, 2)}</span>
                <span class="day-count">${count} пар</span>
              </button>
            `;
          }).join('')}
        </div>

        <!-- МОБИЛЬНЫЙ ПЕРЕКЛЮЧАТЕЛЬ: ПО ДНЯМ / ТАБЛИЦА -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:11px; font-weight:bold; color:#000080;">
            ${mobileScheduleView === 'feed' ? `📅 ${WEEK_DAYS.find(d=>d.id===mobileScheduleTab).name} (${WEEK_DAYS.find(d=>d.id===mobileScheduleTab).campus})` : '📊 Полная сетка расписания'}
          </span>
          <div style="display:flex; gap:4px;">
            <button class="retro-btn" onclick="setMobileScheduleView('feed')" style="font-size:10px; padding:2px 8px; font-weight:${mobileScheduleView==='feed'?'bold':'normal'};">📱 По дням</button>
            <button class="retro-btn" onclick="setMobileScheduleView('grid')" style="font-size:10px; padding:2px 8px; font-weight:${mobileScheduleView==='grid'?'bold':'normal'};">📊 Таблица</button>
          </div>
        </div>

        <!-- МОБИЛЬНЫЙ ВЕРТИКАЛЬНЫЙ СПИСОК ПАР ВЫБРАННОГО ДНЯ -->
        <div class="mobile-day-feed" style="${mobileScheduleView === 'grid' ? 'display:none;' : ''}">
          ${(() => {
            const dayObj = WEEK_DAYS.find(d => d.id === mobileScheduleTab);
            const dayLessons = sched[mobileScheduleTab] || {};
            const lessonSlots = Object.keys(dayLessons).sort((a,b) => parseInt(a) - parseInt(b));

            if (lessonSlots.length === 0) {
              return `
                <div style="background:var(--win-face); border:1px solid var(--border-dark); padding:16px; border-radius:6px; text-align:center;">
                  <div style="font-size:24px; margin-bottom:4px;">🎉</div>
                  <b style="color:#000080;">В этот день пар нет!</b>
                  <div style="font-size:11px; color:#666; margin-top:4px;">Свободный день для отдыха, библиотеки или проектной деятельности.</div>
                </div>
              `;
            }

            return lessonSlots.map(sNum => {
              const l = dayLessons[sNum];
              const slot = TIME_SLOTS.find(s => s.num === parseInt(sNum));
              return `
                <div class="mobile-lesson-item" onclick="openLessonModal('${mobileScheduleTab}', ${sNum})">
                  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                    <span class="badge-tag" style="background:#000080; color:#fff; font-size:10px; font-weight:bold;">
                      №${sNum} · ${slot ? slot.start + ' — ' + slot.end : ''}
                    </span>
                    <span class="lesson-badge ${l.type}">${l.typeName}</span>
                  </div>
                  <div style="font-size:13px; font-weight:bold; color:#000080; margin-bottom:4px;">
                    ${l.name}
                  </div>
                  <div style="font-size:11px; color:#444; line-height:1.4;">
                    📍 <b>ауд. ${l.room}</b> · ${dayObj.campus}<br>
                    👤 ${l.teacher}
                  </div>
                  <div style="margin-top:6px; font-size:10px; color:#0052cc; display:flex; justify-content:flex-end; font-weight:bold;">
                    Подробнее / Moodle ➔
                  </div>
                </div>
              `;
            }).join('');
          })()}
        </div>

        <!-- ГОРИЗОНТАЛЬНАЯ ОБЕРТКА ДЛЯ ТАБЛИЦЫ С СВАЙПОМ -->
        <div class="timetable-grid-wrapper ${mobileScheduleView === 'feed' ? 'mobile-hide-grid' : ''}">
          <div class="timetable-grid" style="min-width:760px;">
          <!-- Заголовок времени -->
          <div class="time-header-cell">Время</div>
          <!-- Заголовки дней -->
          ${WEEK_DAYS.map(day => `
            <div class="day-header-cell">
              <div>${day.name}</div>
              <span class="campus-tag">${day.campus}</span>
            </div>
          `).join('')}

          <!-- Строки по 5 слотам звонков -->
          ${TIME_SLOTS.map(slot => `
            <div class="slot-time-cell">
              <span style="font-size:11px; color:#000080;">№${slot.num}</span>
              <span>${slot.start}</span>
              <span>${slot.end}</span>
            </div>
            ${WEEK_DAYS.map(day => {
              const lesson = sched[day.id] ? sched[day.id][slot.num] : null;
              if (lesson) {
                // Фильтрация по выбранному корпусу
                if (selectedCampusFilter === "sem" && !day.campus.includes("Семёновская")) return `<div class="lesson-card-empty" style="opacity:0.3;"></div>`;
                if (selectedCampusFilter === "pryan" && !day.campus.includes("Прянишникова")) return `<div class="lesson-card-empty" style="opacity:0.3;"></div>`;
                if (selectedCampusFilter === "avto" && !day.campus.includes("Автозаводская")) return `<div class="lesson-card-empty" style="opacity:0.3;"></div>`;

                return `
                  <div class="lesson-card ${lesson.type}" onclick="openLessonModal('${day.id}', ${slot.num})" style="cursor:pointer;" title="Нажмите, чтобы открыть подробности">
                    <span class="lesson-badge">${lesson.typeName}</span>
                    <div class="lesson-card-name">${lesson.name}</div>
                    <div class="lesson-card-info">
                      📍 <b>${lesson.room}</b><br>
                      👤 ${lesson.teacher}
                    </div>
                  </div>
                `;
              } else {
                return `<div class="lesson-card-empty"></div>`;
              }
            }).join('')}
          `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
}

// =========================================================================
// 4.1.1 НОВАЯ ВКЛАДКА: ЭЛЕКТРОННАЯ ЗАЧЁТКА И СЕССИЯ
// =========================================================================
function renderGradebookTab(container) {
  container.innerHTML = `
    <div style="margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h2 style="display:flex; align-items:center; gap:8px;">
          <span>🎓</span> <span>Электронная зачётная книжка · №241321042</span>
        </h2>
        <div style="color:#666; font-size:12px;">Студент: Алексей Смирнов · Группа 241-321 · 2 курс (Осенний семестр 2026)</div>
      </div>
      <button class="retro-btn" onclick="alert('Электронная выписка БРС сформирована и подписана ЭЦП Студофиса!')">🖨️ Скачать выписку БРС (PDF)</button>
    </div>

    <!-- Сводная статистика успеваемости -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-bottom:16px;">
      <div style="background:#ffffff; border:2px solid var(--border-dark); padding:12px; border-radius:var(--border-radius); text-align:center;">
        <div style="font-size:10px; color:#666; text-transform:uppercase; font-weight:bold;">Средний балл (GPA)</div>
        <div style="font-size:26px; font-weight:900; color:#0052cc;">4.85 / 5.0</div>
        <div style="font-size:10px; color:#2b8a3e;">✓ Претендует на повышенную стипендию</div>
      </div>
      <div style="background:#ffffff; border:2px solid var(--border-dark); padding:12px; border-radius:var(--border-radius); text-align:center;">
        <div style="font-size:10px; color:#666; text-transform:uppercase; font-weight:bold;">Общий рейтинг БРС</div>
        <div style="font-size:26px; font-weight:900; color:#2b8a3e;">88 / 100</div>
        <div style="font-size:10px; color:#555;">Порог зачета пройден (>60)</div>
      </div>
      <div style="background:#ffffff; border:2px solid var(--border-dark); padding:12px; border-radius:var(--border-radius); text-align:center;">
        <div style="font-size:10px; color:#666; text-transform:uppercase; font-weight:bold;">Допуск к экзаменам</div>
        <div style="font-size:26px; font-weight:900; color:#10b981;">ПОЛУЧЕН</div>
        <div style="font-size:10px; color:#555;">Задолженностей: 0 предметов</div>
      </div>
      <div style="background:#ffffff; border:2px solid var(--border-dark); padding:12px; border-radius:var(--border-radius); text-align:center;">
        <div style="font-size:10px; color:#666; text-transform:uppercase; font-weight:bold;">Зимняя сессия 2026</div>
        <div style="font-size:26px; font-weight:900; color:#d9480f;">11 — 25 ЯНВ</div>
        <div style="font-size:10px; color:#555;">Всего 4 экзамена, 3 зачёта</div>
      </div>
    </div>

    <!-- Таблица дисциплин текущего семестра -->
    <div style="background:var(--win-face); border:2px solid; border-color:var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light); padding:14px; border-radius:var(--border-radius); margin-bottom:16px;">
      <h3 style="margin-bottom:10px; font-size:13px; font-weight:800; color:#002b80;">📚 Дисциплины текущего семестра и баллы БРС</h3>
      <table class="retro-table">
        <thead>
          <tr>
            <th>Дисциплина</th>
            <th>Преподаватель</th>
            <th>БРС (из 100)</th>
            <th>Форма контроля</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Проектная деятельность (ДМ2026)</b></td>
            <td>Смирнов А. В.</td>
            <td><b style="color:#2b8a3e;">88 б.</b></td>
            <td>Дифф. зачёт</td>
            <td><span class="badge-tag" style="background:#d3f9d8; color:#2b8a3e;">КТ1 сдана (30/30)</span></td>
          </tr>
          <tr>
            <td><b>Веб-разработка и frontend-технологии</b></td>
            <td>Ковалёв Д. И.</td>
            <td><b style="color:#2b8a3e;">92 б.</b></td>
            <td>Экзамен</td>
            <td><span class="badge-tag" style="background:#ffe8cc; color:#d9480f;">Автомат «Отлично» 🌟</span></td>
          </tr>
          <tr>
            <td><b>Базы данных и SQL</b></td>
            <td>Николаев С. П.</td>
            <td><b style="color:#0052cc;">85 б.</b></td>
            <td>Экзамен</td>
            <td><span class="badge-tag" style="background:#e7f5ff; color:#0052cc;">Допущен к экзамену</span></td>
          </tr>
          <tr>
            <td><b>Архитектура информационных систем</b></td>
            <td>Соколов М. Е.</td>
            <td><b style="color:#0052cc;">79 б.</b></td>
            <td>Экзамен</td>
            <td><span class="badge-tag" style="background:#e7f5ff; color:#0052cc;">Допущен к экзамену</span></td>
          </tr>
          <tr>
            <td><b>Дискретная математика</b></td>
            <td>Кузнецова Е. А.</td>
            <td><b style="color:#2b8a3e;">81 б.</b></td>
            <td>Зачёт</td>
            <td><span class="badge-tag" style="background:#d3f9d8; color:#2b8a3e;">Зачтено автоматически</span></td>
          </tr>
          <tr>
            <td><b>Иностранный язык (профессиональный)</b></td>
            <td>Иванова Т. Н.</td>
            <td><b style="color:#2b8a3e;">90 б.</b></td>
            <td>Зачёт с оценкой</td>
            <td><span class="badge-tag" style="background:#d3f9d8; color:#2b8a3e;">Оценка «Отлично»</span></td>
          </tr>
          <tr>
            <td><b>Физическая культура и спорт</b></td>
            <td>Морозов В. Г.</td>
            <td><b style="color:#2b8a3e;">100 б.</b></td>
            <td>Зачёт</td>
            <td><span class="badge-tag" style="background:#d3f9d8; color:#2b8a3e;">Зачтено (100% посещений)</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- График экзаменационной сессии -->
    <div style="background:var(--win-face); border:2px solid; border-color:var(--border-light) var(--border-darkest) var(--border-darkest) var(--border-light); padding:14px; border-radius:var(--border-radius);">
      <h3 style="margin-bottom:10px; font-size:13px; font-weight:800; color:#d9480f;">📅 Расписание экзаменов и консультаций (Зимняя сессия 2026)</h3>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; font-size:11px;">
        <div style="background:#ffffff; border:1px solid var(--border-dark); padding:10px; border-radius:6px;">
          <div style="font-weight:bold; color:#002b80;">14 января (Среда) · 10:00</div>
          <div style="font-weight:700; font-size:12px; margin:2px 0;">Архитектура ИС (Экзамен)</div>
          <div style="color:#555;">📍 ауд. <b>А-201</b> (Б. Семёновская, 38) · проф. Соколов М. Е.</div>
          <div style="color:#888; font-size:10px; margin-top:4px;">Консультация: 12 января в 12:00 (MS Teams)</div>
        </div>
        <div style="background:#ffffff; border:1px solid var(--border-dark); padding:10px; border-radius:6px;">
          <div style="font-weight:bold; color:#002b80;">18 января (Воскресенье) · 10:00</div>
          <div style="font-weight:700; font-size:12px; margin:2px 0;">Базы данных и SQL (Экзамен)</div>
          <div style="color:#555;">📍 ауд. <b>Н-412</b> (Б. Семёновская, 38) · доц. Николаев С. П.</div>
          <div style="color:#888; font-size:10px; margin-top:4px;">Консультация: 16 января в 14:00 (ауд. Н-412)</div>
        </div>
        <div style="background:#ffffff; border:1px solid var(--border-dark); padding:10px; border-radius:6px;">
          <div style="font-weight:bold; color:#002b80;">22 января (Четверг) · 11:00</div>
          <div style="font-weight:700; font-size:12px; margin:2px 0;">Защита проекта (ДМ2026)</div>
          <div style="color:#555;">📍 ауд. <b>Н-401</b> (Б. Семёновская, 38) · Комиссия ЦПД</div>
          <div style="color:#888; font-size:10px; margin-top:4px;">Загрузка презентации в систему: до 20 января 23:59</div>
        </div>
      </div>
    </div>
  `;
}

// =========================================================================
// 4.1.2 ВКЛАДКА: ОБЩЕЖИТИЯ И СТУДГОРОДОК МОСПОЛИТЕХА (ВСЕ 10 ОБЩЕЖИТИЙ)
// =========================================================================
const ALL_DORMITORIES = [
  {
    num: 1,
    name: "Студгородок «Малая Переяславская»",
    district: "cacao",
    metro: "м. Проспект Мира",
    address: "ул. Малая Переяславская, д. 7/1",
    type: "Блочный тип (2–3 человека в комнате)",
    desc: "Комфортные жилые блоки с санузлом, спортивный и читальный залы с Wi-Fi, прачечная со стиральными и сушильными машинами, кухни на этажах.",
    route: "✓ 20 минут на метро до главного корпуса (Б. Семёновская, 38).",
    director: "Волкова Татьяна Сергеевна",
    phone: "доб. 1421",
    priceBudget: "1 050 ₽/мес.",
    priceContract: "1 650 ₽/мес."
  },
  {
    num: 2,
    name: "Студгородок «Павла Корчагина, 20А»",
    district: "svao",
    metro: "м. ВДНХ / м. Алексеевская",
    address: "ул. Павла Корчагина, д. 20А, корп. 3",
    type: "Коридорный тип (2–3 человека)",
    desc: "Уютный студгородок в зелёной зоне возле парка «Сокольники». Кухни на этажах, тихие комнаты самоподготовки, камера хранения.",
    route: "✓ 15 минут пешком до корпуса на Корчагина / 25 минут до Б. Семёновской.",
    director: "Григорьев Михаил Олегович",
    phone: "доб. 1422",
    priceBudget: "950 ₽/мес.",
    priceContract: "1 500 ₽/мес."
  },
  {
    num: 3,
    name: "Студгородок «Павла Корчагина, 22»",
    district: "svao",
    metro: "м. ВДНХ / ст. Маленковская",
    address: "ул. Павла Корчагина, д. 22",
    type: "Блочный и коридорный тип",
    desc: "Студенческое кафе, камера хранения, спортивные площадки, велопарковка, терминалы оплаты и банкоматы в холле.",
    route: "✓ Прямой выезд к проспекту Мира, быстрый доступ к транспорту.",
    director: "Смирнов Андрей Викторович",
    phone: "доб. 1423",
    priceBudget: "1 100 ₽/мес.",
    priceContract: "1 600 ₽/мес."
  },
  {
    num: 4,
    name: "Студгородок «Бориса Галушкина»",
    district: "svao",
    metro: "м. ВДНХ / Ростокино",
    address: "ул. Бориса Галушкина, д. 9",
    type: "Блочный тип повышенной комфортности",
    desc: "Зона коворкинга, оптоволоконный скоростной интернет, современные душевые, охраняемая территория и система контроля доступа СКУД.",
    route: "✓ 10 минут на трамвае до метро ВДНХ, рядом парки Сокольники и ВДНХ.",
    director: "Федоров Дмитрий Сергеевич",
    phone: "доб. 1424",
    priceBudget: "1 250 ₽/мес.",
    priceContract: "1 850 ₽/мес."
  },
  {
    num: 5,
    name: "Студгородок «Михалковская»",
    district: "sao",
    metro: "м. Войковская / МЦК Коптево",
    address: "ул. Михалковская, д. 7, корп. 3",
    type: "Блочный тип (2–3 человека)",
    desc: "Просторные комнаты, тренажерный зал, библиотека с зонами Wi-Fi, прачечная самообслуживания, студенческий совет общежития.",
    route: "✓ В пешей доступности от кампуса на Михалковской (Текстильный институт).",
    director: "Лебедева Ольга Николаевна",
    phone: "доб. 1425",
    priceBudget: "1 150 ₽/мес.",
    priceContract: "1 700 ₽/мес."
  },
  {
    num: 6,
    name: "Студгородок «7-я Парковая»",
    district: "vao",
    metro: "м. Первомайская",
    address: "ул. 7-я Парковая, д. 9/26",
    type: "Коридорный тип (2–3 человека)",
    desc: "Кухни на каждом этаже, гладильные и сушильные комнаты, благоустроенный зеленый район Измайлово, спортивная площадка.",
    route: "✓ Прямая Арбатско-Покровская ветка метро до Электрозаводской / Семёновской (всего 15 минут!).",
    director: "Смирнова Анна Павловна",
    phone: "доб. 1426",
    priceBudget: "950 ₽/мес.",
    priceContract: "1 550 ₽/мес."
  },
  {
    num: 7,
    name: "Студгородок «1-я Дубровская»",
    district: "cacao",
    metro: "м. Дубровка / Пролетарская",
    address: "ул. 1-я Дубровская, д. 16А, стр. 2",
    type: "Блочный тип",
    desc: "Ближайшее общежитие к кампусу на Автозаводской! Современные кухни, спортивная комната, высокоскоростной интернет, комната отдыха.",
    route: "✓ 10 минут на транспорте или пешком до корпуса Автозаводская, 16 (Транспортный факультет).",
    director: "Козлова Наталья Ивановна",
    phone: "доб. 1427",
    priceBudget: "1 200 ₽/мес.",
    priceContract: "1 800 ₽/мес."
  },
  {
    num: 8,
    name: "Студгородок «800-летия Москвы»",
    district: "sao",
    metro: "м. Селигерская / Яхромская",
    address: "ул. 800-летия Москвы, д. 28, корп. 1",
    type: "Коридорный тип (2–3 человека)",
    desc: "Светлые комнаты, новые стеклопакеты, спортивная площадка во дворе, продуктовые магазины и аптеки в шаговой доступности.",
    route: "✓ Быстрый проезд до кампуса на Прянишникова (Институт графики и книги).",
    director: "Николаев Сергей Петрович",
    phone: "доб. 1428",
    priceBudget: "980 ₽/мес.",
    priceContract: "1 500 ₽/мес."
  },
  {
    num: 9,
    name: "Студгородок «Прянишникова»",
    district: "sao",
    metro: "м. Тимирязевская / МЦД Лихоборы",
    address: "ул. Прянишникова, д. 2А, стр. 2",
    type: "Блочный тип (учебный городок Прянишникова)",
    desc: "Расположено непосредственно на территории учебного городка Прянишникова! 1 минута до учебных корпусов, столовой и библиотеки.",
    route: "✓ 0 минут до учебных занятий на Прянишникова, 35 мин до Б. Семёновской.",
    director: "Зайцева Елена Васильевна",
    phone: "доб. 1429",
    priceBudget: "1 200 ₽/мес.",
    priceContract: "1 750 ₽/мес."
  },
  {
    num: 10,
    name: "Студгородок «Рижский проезд»",
    district: "svao",
    metro: "м. Алексеевская / пл. Маленковская",
    address: "Рижский проезд, д. 15, корп. 2",
    type: "Коридорный тип",
    desc: "Тихий район возле парка «Лосиный остров», комнаты для самостоятельных занятий, настольный теннис, прачечная.",
    route: "✓ 15 минут пешком до метро Алексеевская, удобная транспортная доступность.",
    director: "Соловьев Виктор Аркадьевич",
    phone: "доб. 1430",
    priceBudget: "950 ₽/мес.",
    priceContract: "1 500 ₽/мес."
  }
];

let selectedDormFilter = "all";

function setDormFilter(fKey) {
  selectedDormFilter = fKey;
  playRetroSound("click");
  renderDormitoryTab(document.getElementById("mainContentArea"));
}

function renderDormitoryTab(container) {
  const inputEl = document.getElementById("dormSearchInput");
  const q = (inputEl ? inputEl.value : "").trim().toLowerCase();

  let filtered = ALL_DORMITORIES.filter(d => {
    const matchesFilter = selectedDormFilter === "all" || d.district === selectedDormFilter;
    const matchesQuery = !q || 
      d.name.toLowerCase().includes(q) || 
      d.address.toLowerCase().includes(q) || 
      d.metro.toLowerCase().includes(q) ||
      d.desc.toLowerCase().includes(q) ||
      String(d.num).includes(q);
    return matchesFilter && matchesQuery;
  });

  container.innerHTML = `
    <div style="margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div>
        <h2 style="display:flex; align-items:center; gap:8px;">
          <span>🏢</span> <span>Общежития и студенческий городок МосПолитеха</span>
        </h2>
        <div style="color:var(--win-text); opacity:0.8; font-size:12px;">Управление студгородком: ул. Малая Семёновская, д. 12, корп. 1 · Тел. +7 (495) 223-05-23 доб. 1420</div>
      </div>
      <button class="retro-btn active" onclick="alert('Форма электронной подачи заявки на общежитие открыта в ЛК: online.mospolytech.ru')">📝 Заявка на заселение / переселение</button>
    </div>

    <!-- Информационная плашка стоимости (с поддержкой темной темы) -->
    <div style="background:var(--win-face); border:2px solid var(--border-light); border-left:6px solid #0052cc; padding:12px 16px; border-radius:var(--border-radius); margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; box-shadow:1px 2px 6px rgba(0,0,0,0.1);">
      <div>
        <b style="color:var(--primary-accent); font-size:12px;">💡 Тарифы на проживание для студентов 2026/2027 уч. года:</b>
        <div style="font-size:11px; opacity:0.9; margin-top:3px;">
          Бюджетная основа: <b>от 950 до 1 250 ₽/мес.</b> · Договорная основа: <b>от 1 500 до 1 850 ₽/мес.</b> (коммунальные услуги и Wi-Fi включены).
        </div>
      </div>
      <span class="badge-tag" style="background:#000080; color:#fff; font-size:11px; padding:4px 10px;">Оплата в ЛК онлайн</span>
    </div>

    <!-- Фильтры по районам и поиск -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
      <div class="nav-campus-tabs" style="margin-bottom:0;">
        <button class="nav-campus-btn ${selectedDormFilter==='all'?'active':''}" onclick="setDormFilter('all')">🌐 Все 10 общежитий</button>
        <button class="nav-campus-btn ${selectedDormFilter==='svao'?'active':''}" onclick="setDormFilter('svao')">🚇 СВАО / ВДНХ (№2, 3, 4, 10)</button>
        <button class="nav-campus-btn ${selectedDormFilter==='sao'?'active':''}" onclick="setDormFilter('sao')">🚇 САО / Прянишникова (№5, 8, 9)</button>
        <button class="nav-campus-btn ${selectedDormFilter==='vao'?'active':''}" onclick="setDormFilter('vao')">🚇 ВАО / Измайлово (№6)</button>
        <button class="nav-campus-btn ${selectedDormFilter==='cacao'?'active':''}" onclick="setDormFilter('cacao')">🚇 ЦАО / ЮВАО (№1, 7)</button>
      </div>

      <div style="min-width:240px; flex:1; max-width:320px;">
        <input type="text" id="dormSearchInput" value="${q}" placeholder="Поиск по адресу, метро, номеру..." style="width:100%; padding:6px 10px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius); outline:none;" oninput="renderDormitoryTab(document.getElementById('mainContentArea'))">
      </div>
    </div>

    <!-- Сетка карточек всех 10 общежитий -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(310px, 1fr)); gap:14px;">
      ${filtered.length > 0 ? filtered.map(d => `
        <div class="dash-widget" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
              <h3 class="dorm-card-title">📍 ${d.name}</h3>
              <span class="badge-tag" style="background:#0052cc; color:#fff;">${d.metro}</span>
            </div>
            
            <p style="font-size:11px; margin:4px 0;"><b>Адрес:</b> ${d.address}</p>
            <p style="font-size:11px; margin:4px 0;"><b>Тип:</b> ${d.type}</p>
            <p style="font-size:11px; margin:4px 0; opacity:0.9;"><b>Удобства:</b> ${d.desc}</p>
            <p style="font-size:11px; margin:4px 0;"><b>Комендант:</b> ${d.director} · <code>${d.phone}</code></p>
            
            <div style="display:flex; gap:6px; margin:8px 0; flex-wrap:wrap;">
              <span class="dorm-price-tag">Бюджет: ${d.priceBudget}</span>
              <span class="dorm-price-tag" style="background:#fff3bf; color:#d9480f; border-color:#ffe066;">Платно: ${d.priceContract}</span>
            </div>
          </div>

          <div style="margin-top:10px; border-top:1px dashed var(--border-dark); padding-top:8px; font-size:11px; color:#2b8a3e; font-weight:bold;">
            ${d.route}
          </div>
        </div>
      `).join('') : '<div style="grid-column: 1 / -1; padding:24px; text-align:center; color:#888;">Общежития по вашему запросу не найдены. Попробуйте выбрать «Все 10 общежитий».</div>'}
    </div>
  `;
}

// 4.2 РЕНДЕР ВКЛАДКИ КОНКРЕТНОГО РАЗДЕЛА БАЗЫ ЗНАНИЙ
function renderCategoryWikiTab(container, cat) {
  container.innerHTML = `
    <div class="wiki-section-header">
      <div>
        <h2>${cat.code}. РАЗДЕЛ — ${cat.title.toUpperCase()}</h2>
        <div style="font-size:11px; opacity:0.9;">${cat.desc}</div>
      </div>
      <div style="font-size:24px;">${cat.icon}</div>
    </div>

    <div class="wiki-questions-list">
      ${cat.items.map(item => `
        <div class="question-row" onclick="openAnswerCard('${cat.id}', '${item.id}')">
          <div class="q-left">
            <div class="q-title">${item.question}</div>
            <div class="q-tags">
              ${item.tags.map(t => `<span class="badge-tag">${t}</span>`).join('')}
            </div>
          </div>
          <div class="arrow-icon">➔</div>
        </div>
      `).join('')}
    </div>

    <!-- Карточка детального ответа (открывается при клике) -->
    <div class="answer-detail-modal" id="answerDetailBox"></div>
  `;
}

// 4.3 ОТКРЫТИЕ КАРТОЧКИ ОТВЕТА БАЗЫ ЗНАНИЙ
function openAnswerCard(catId, qId) {
  const cat = WIKI_CATEGORIES.find(c => c.id === catId);
  if (!cat) return;
  const item = cat.items.find(q => q.id === qId);
  if (!item) return;

  const box = document.getElementById("answerDetailBox");
  if (!box) return;

  box.innerHTML = `
    <div class="answer-top-meta">
      <div>
        <span style="font-size:11px; text-transform:uppercase; color:#000080; font-weight:bold;">Раздел: ${cat.title}</span>
        <h3 style="font-size:15px; margin-top:2px;">${item.question}</h3>
      </div>
      <div style="text-align:right;">
        <span style="font-size:10px; background:#d3f9d8; color:#2b8a3e; padding:2px 6px; border:1px solid #40c057; font-weight:bold;">
          ✓ Проверено: ${item.verified}
        </span>
      </div>
    </div>

    <!-- Тёмный блок КОРОТКО -->
    <div class="answer-short-box">
      <strong class="title">⚡ КОРОТКО</strong>
      ${item.short}
    </div>

    <!-- Официальные источники -->
    <div class="answer-sources-box">
      <b style="font-size:11px; color:#495057;">📜 ОФИЦИАЛЬНЫЕ ИСТОЧНИКИ:</b>
      <ul style="margin: 6px 0 0 16px; font-size:11px;">
        ${item.sources.map(s => `
          <li><a href="${s.url}" target="_blank" style="color:#000080; font-weight:600; text-decoration:underline;">${s.name}</a></li>
        `).join('')}
      </ul>
    </div>

    <!-- Похожие вопросы -->
    ${item.similar && item.similar.length > 0 ? `
      <div class="similar-questions-box">
        <span style="font-size:11px; font-weight:bold; color:#495057;">🔗 ПОХОЖИЕ ВОПРОСЫ:</span>
        <div style="margin-top:4px;">
          ${item.similar.map(sq => `<button class="similar-btn" onclick="searchByQuestion('${sq}')">❓ ${sq}</button>`).join('')}
        </div>
      </div>
    ` : ''}

    <div style="margin-top:12px; text-align:right;">
      <button class="retro-btn" onclick="document.getElementById('answerDetailBox').classList.remove('active')">Закрыть ответ</button>
    </div>
  `;

  box.classList.add("active");
  box.scrollIntoView({ behavior: "smooth" });
}

// 4.4 РЕНДЕР ВКЛАДКИ ДАШБОРД (СОЧНЫЙ РЕТРО-ДАШБОРД С ID-КАРТОЙ И БРС)
function getDashboardUpcomingPairHtml() {
  const now = new Date();
  const dayIdx = now.getDay();
  const dKeys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  const dNames = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
  const curKey = dKeys[dayIdx];
  const curName = dNames[dayIdx];
  const grpSched = (GROUPS_DATA[currentSelectedGroup] || GROUPS_DATA["241-321"]).schedule;
  const todayPairs = grpSched[curKey] || {};
  const pairKeys = Object.keys(todayPairs).sort((a,b) => parseInt(a) - parseInt(b));

  if (dayIdx === 0 || pairKeys.length === 0) {
    const nextKey = dayIdx === 0 ? "mon" : dKeys[(dayIdx + 1) % 7];
    const nextDayObj = WEEK_DAYS.find(d => d.id === nextKey);
    const nextPairs = grpSched[nextKey] || {};
    const nextFirstNum = Object.keys(nextPairs).sort((a,b) => parseInt(a) - parseInt(b))[0];
    const nextPair = nextFirstNum ? nextPairs[nextFirstNum] : null;
    const nextSlot = nextFirstNum ? TIME_SLOTS.find(s => s.num === parseInt(nextFirstNum)) : null;

    return `
      <div class="dash-pair-box">
        <div class="dash-pair-time">🛌 Сегодня ${curName} — пар нет</div>
        ${nextPair ? `
          <div class="dash-pair-name">Ближайшее занятие: ${nextPair.name}</div>
          <div class="dash-pair-meta">📅 ${nextDayObj ? nextDayObj.name : 'Следующий учебный день'} (${nextSlot ? nextSlot.start : '09:00'}) · ауд. <b>${nextPair.room}</b></div>
          <div class="dash-pair-meta">👤 Преподаватель: ${nextPair.teacher}</div>
        ` : `
          <div class="dash-pair-name">Свободный день / Самостоятельная работа</div>
          <div class="dash-pair-meta">Отличная возможность повторить материалы в Moodle!</div>
        `}
      </div>
      <div style="margin-top:8px; font-size:11px; color:#2b8a3e; font-weight:bold;">
        ✨ Набирайтесь сил перед следующими занятиями!
      </div>
    `;
  }

  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const slotsWithMins = [
    { num: 1, startM: 540, endM: 630, start: "09:00", end: "10:30" },
    { num: 2, startM: 640, endM: 730, start: "10:40", end: "12:10" },
    { num: 3, startM: 740, endM: 830, start: "12:20", end: "13:50" },
    { num: 4, startM: 870, endM: 960, start: "14:30", end: "16:00" },
    { num: 5, startM: 970, endM: 1060, start: "16:10", end: "17:40" },
    { num: 6, startM: 1070, endM: 1160, start: "17:50", end: "19:20" }
  ];

  let targetSlotNum = pairKeys[0];
  let slotObj = slotsWithMins.find(s => s.num === parseInt(targetSlotNum));
  for (const sNum of pairKeys) {
    const s = slotsWithMins.find(x => x.num === parseInt(sNum));
    if (s && currentMinutes <= s.endM) {
      targetSlotNum = sNum;
      slotObj = s;
      break;
    }
  }

  const p = todayPairs[targetSlotNum];
  const dayObj = WEEK_DAYS.find(d => d.id === curKey);
  const campus = dayObj ? dayObj.campus : "Кампус Политеха";

  return `
    <div class="dash-pair-box" onclick="openLessonModal('${curKey}', ${targetSlotNum})" style="cursor:pointer;" title="Нажмите для подробностей">
      <div class="dash-pair-time">${slotObj ? slotObj.start + ' — ' + slotObj.end : '09:00 — 10:30'} (СЕГОДНЯ, ${curName.toUpperCase()})</div>
      <div class="dash-pair-name">${p.name}</div>
      <div class="dash-pair-meta">📍 ауд. <b>${p.room}</b> (${campus})</div>
      <div class="dash-pair-meta">👤 Преподаватель: ${p.teacher}</div>
    </div>
    <div style="margin-top:8px; font-size:11px; color:#d9480f; font-weight:bold;">
      ${slotObj && currentMinutes < slotObj.startM ? `⏳ До звонка осталось: ${slotObj.startM - currentMinutes} мин! Не забудьте студенческий пропуск!` : `🟢 Занятие в расписании · ауд. ${p.room}`}
    </div>
  `;
}

function renderDashboardTab(container) {
  container.innerHTML = `
    <div style="margin-bottom:16px;">
      <h2 style="display:flex; align-items:center; gap:8px;">
        <span>🏠</span> <span>Главная · Цифровой кабинет студента</span>
        <span class="badge-tag" style="background:#e6fcf5; color:#0ca678; border-color:#63e6be;">Семестр: Осенний 2026</span>
      </h2>
      <div style="color:#666; font-size:12px;">Единое окно контроля успеваемости, пар, дедлайнов и документов</div>
    </div>

    <!-- Студенческий билет (ID CARD) -->
    <div class="student-id-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div style="display:flex; gap:14px; align-items:center;">
          <div style="width:54px; height:54px; background:linear-gradient(135deg, #ffd43b, #ff922b); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; border:2px solid #fff; box-shadow:0 3px 8px rgba(0,0,0,0.3);">
            🐱
          </div>
          <div>
            <div style="font-size:10px; text-transform:uppercase; opacity:0.8; letter-spacing:1px; font-weight:800;">МОСКОВСКИЙ ПОЛИТЕХ · СТУДЕНЧЕСКИЙ БИЛЕТ №241321042</div>
            <div style="font-size:18px; font-weight:900; letter-spacing:0.5px; margin:2px 0;">Смирнов Алексей Викторович</div>
            <div style="font-size:11px; opacity:0.95;">Факультет информационных технологий (ФИТ) · Группа <b>241-321</b> (2 курс)</div>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:10px; background:rgba(255,255,255,0.2); padding:3px 8px; border-radius:4px; font-weight:bold; border:1px solid rgba(255,255,255,0.4);">
            ФОРМА: ОЧНАЯ (БЮДЖЕТ)
          </div>
          <div style="font-size:10px; margin-top:4px; color:#a5d8ff;">Пропуск: АКТИВЕН 🟢</div>
        </div>
      </div>
    </div>


    <!-- ПОИСКОВАЯ СТРОКА В СТИЛЕ GOOGLE С ИИ-АГЕНТОМ ПОЛИГИД AI -->
    <div class="ai-hero-search-box">
      <div class="ai-hero-branding">
        <span class="ai-hero-logo">🤖 ПолиГид <span style="color:#0052cc;">AI</span></span>
        <span class="ai-hero-tag">Умный поиск по расписанию, сессии, общежитиям, стипендиям и регламентам Политеха</span>
      </div>

      <div class="ai-search-input-container">
        <span class="ai-search-lens">🔍</span>
        <input type="text" id="dashboardAiSearchInput" placeholder="Спросите ИИ о чём угодно: пары завтра, автомат по БРС, общага, пересдачи, заказ справок..." onkeydown="handleHeroSearchKey(event)">
        <button class="ai-search-action-btn" onclick="submitHeroAiSearch()">
          <span>Спросить</span> ✨
        </button>
      </div>

      <div class="ai-hero-chips">
        <span style="font-size:11px; opacity:0.8; margin-right:2px;">Частые вопросы:</span>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Какие пары завтра у группы 241-321?')">📅 Пары завтра</button>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Как получить автомат по БРС?')">🎯 Автомат по БРС</button>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Сколько стоит общежитие и где подать заявление?')">🏠 Общежития</button>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Где находится ауд. А-101 и Студофис?')">🏢 Студофис А-101</button>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Как заказать справку об обучении с печатью?')">📄 Заказ справки</button>
        <button class="hero-chip-btn" onclick="triggerHeroChip('Когда начнётся зимняя сессия 2026?')">⏳ Сессия 2026</button>
      </div>

      <!-- Встроенная карточка мгновенного ответа ИИ прямо на главной -->
      <div class="ai-hero-answer-card" id="heroAiAnswerCard" style="display:none;">
        <div class="ai-hero-answer-top">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:18px;">🤖</span>
            <b>Ответ ПолиГид AI:</b>
          </div>
          <button class="win-btn" onclick="closeHeroAiAnswer()" style="width:20px; height:20px; font-size:10px;">✕</button>
        </div>
        <div class="ai-hero-answer-content" id="heroAiAnswerContent"></div>
        <div class="ai-hero-answer-bottom">
          <span style="font-size:10px; opacity:0.75;">Ответ сгенерирован по официальным регламентам МосПолитеха</span>
          <button class="retro-btn" onclick="continueInFullChat()" style="font-size:10px; padding:2px 8px;">Открыть диалог в полном чате 💬</button>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- Виджет успеваемости БРС -->
      <div class="dash-widget">
        <h3>📊 Успеваемость и рейтинг (БРС)</h3>
        <div style="display:flex; justify-content:space-between; font-size:12px; margin-top:4px;">
          <span>Текущий балл: <b style="color:#2b8a3e; font-size:14px;">88 / 100</b></span>
          <span style="color:#1971c2; font-weight:bold;">Статус: Отличник 🌟</span>
        </div>
        <div class="brs-progress-wrap">
          <div class="brs-progress-bar">
            <div class="brs-progress-fill"></div>
          </div>
        </div>
        <div style="font-size:11px; color:#555; display:flex; justify-content:space-between;">
          <span>Минимум: 60 (Зачёт)</span>
          <span>До автомата: <b>12 баллов</b> 🎯</span>
        </div>
        <div style="margin-top:10px; font-size:11px; border-top:1px dashed var(--border-dark); padding-top:6px;">
          • Стипендия: <b>2 900 ₽</b> (ГАС, карта МИР)<br>
          • Пропусков по неуважительной: <b>0 часов</b>
        </div>
      </div>

      <!-- Виджет ближайшей пары -->
      <div class="dash-widget">
        <h3>⏰ Ближайшая пара</h3>
        ${getDashboardUpcomingPairHtml()}
      </div>

      <!-- Виджет кампуса и погоды -->
      <div class="dash-widget">
        <h3>📍 Кампус и погода</h3>
        <div style="font-size:12px; line-height:1.6;">
          🌤️ <b>Москва (Соколиная гора):</b> +6°C, облачно с прояснениями<br>
          ☕ <b>Столовая (Корпус А, 1 этаж):</b> Открыта до 17:30 (комплексный обед 220 ₽)<br>
          📖 <b>Коворкинг ЦПД:</b> Б. Семёновская, 38, ауд. Н-401 / Н-405 (Wi-Fi, пуфы)<br>
          ⏳ <b>До зимней сессии:</b> <b style="color:#0052cc;">48 дней</b> (с 11 января)
        </div>
      </div>

      <!-- Важные объявления деканата -->
      <div class="dash-widget" style="grid-column: 1 / -1;">
        <h3>📢 Важные объявления и дедлайны института</h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; font-size:11px;">
          <div class="dash-announcement-card warning">
            <b class="announcement-title">🔥 Проектная деятельность (ДМ2026):</b><br>
            До 15 ноября необходимо утвердить паспорт проекта КТ1 и состав команды на портале.
          </div>
          <div class="dash-announcement-card info">
            <b class="announcement-title">📄 Справки в военкомат (Приложение 4):</b><br>
            Оформляются во 2-м отделе (ауд. А-220, Пн-Пт 10:00–16:00). При себе иметь приписное.
          </div>
          <div class="dash-announcement-card promo">
            <b class="announcement-title">🏎️ Гоночная команда FDR Moscow:</b><br>
            Открыт набор первокурсников и второкурсников в команду Formula Student Polytech!
          </div>
        </div>
      </div>
    </div>
  `;
}

// 4.5 РЕНДЕР ВКЛАДКИ ЗАМЕТОК И ДЕДЛАЙНОВ (С СОХРАНЕНИЕМ В LOCALSTORAGE)
const DEFAULT_NOTES = [
  { id: 1, text: "Проектная деятельность (ДМ2026): Загрузить паспорт проекта и цели КТ1", deadline: "15 ноября 23:59", done: false },
  { id: 2, text: "Веб-разработка: Доделать макет личного кабинета Y2K в Figma", deadline: "10 ноября", done: false },
  { id: 3, text: "Студофис: Заказать справку об обучении для налогового вычета", deadline: "Выполнено · Справка в А-101", done: true }
];

function getStoredNotes() {
  try {
    const s = localStorage.getItem("poly_notes_storage");
    return s ? JSON.parse(s) : DEFAULT_NOTES;
  } catch(e) { return DEFAULT_NOTES; }
}

function saveStoredNotes(notes) {
  try {
    localStorage.setItem("poly_notes_storage", JSON.stringify(notes));
  } catch(e) {}
  updateNotesBadge();
}


function updateNotesBadge() {
  const notes = getStoredNotes();
  const uncompleted = notes.filter(n => !n.done).length;
  const badge = document.getElementById("notesCounterBadge");
  if (badge) {
    badge.textContent = uncompleted;
    badge.style.display = uncompleted > 0 ? "inline-block" : "none";
  }
}

function setDeadlinePreset(val) {
  const el = document.getElementById("newNoteDeadline");
  if (el) {
    el.value = val;
    playRetroSound("click");
  }
}

function renderNotesTab(container) {
  const notes = getStoredNotes();
  container.innerHTML = `
    <div style="margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h2>📝 Заметки и дедлайны студента</h2>
        <div style="color:var(--win-text); opacity:0.75;">Задачи сохраняются автоматически в памяти браузера</div>
      </div>
      <button class="retro-btn" onclick="resetDefaultNotes()">Сбросить список</button>
    </div>

    <div class="notes-container" id="notesListContainer">
      ${notes.map(n => `
        <div class="note-item ${n.done ? 'done' : ''}" id="note-item-${n.id}">
          <input type="checkbox" ${n.done ? 'checked' : ''} onchange="toggleNoteDone(${n.id})">
          <div style="flex:1;">
            <b>${n.text}</b>
            <div style="font-size:10px; color:${n.done ? '#2b8a3e' : '#d9480f'}; font-weight:bold; margin-top:2px;">
              ⏰ ${n.deadline}
            </div>
          </div>
          <button class="win-btn" onclick="deleteNote(${n.id})" title="Удалить" style="width:22px; height:22px; font-size:10px;">✕</button>
        </div>
      `).join('')}

      <!-- Форма добавления заметки со сроком / дедлайном -->
      <div style="background:var(--win-face); border:1px solid var(--border-dark); padding:10px; border-radius:var(--border-radius); margin-top:14px;">
        <div style="font-size:11px; font-weight:bold; margin-bottom:6px;">➕ Новая задача с дедлайном:</div>
        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
          <input type="text" id="newNoteInput" placeholder="Что нужно сделать (напр. Сдать лабу по БД, Заполнить паспорт ПД)..." style="flex:2; min-width:200px; padding:7px 10px; font-size:12px; border:2px solid; border-color:var(--border-dark) var(--border-light) var(--border-light) var(--border-dark);" onkeydown="if(event.key==='Enter') addNewNote()">
          <input type="text" id="newNoteDeadline" placeholder="Дедлайн (напр. 15 ноября 23:59)" style="flex:1; min-width:140px; padding:7px 10px; font-size:12px; border:2px solid; border-color:var(--border-dark) var(--border-light) var(--border-light) var(--border-dark);" onkeydown="if(event.key==='Enter') addNewNote()">
          <button class="retro-btn" onclick="addNewNote()" style="font-weight:bold; background:#000080; color:#fff;">+ Добавить задачу</button>
        </div>
        <div class="deadline-presets-bar">
          <span>Быстрый срок:</span>
          <button class="chip-btn" type="button" onclick="setDeadlinePreset('Сегодня к 23:59')">Сегодня</button>
          <button class="chip-btn" type="button" onclick="setDeadlinePreset('Завтра к 1-й паре')">Завтра</button>
          <button class="chip-btn" type="button" onclick="setDeadlinePreset('До конца недели')">До конца недели</button>
          <button class="chip-btn" type="button" onclick="setDeadlinePreset('До сессии (11 янв)')">К сессии</button>
        </div>
      </div>
    </div>
  `;
}

function toggleNoteDone(id) {
  const notes = getStoredNotes();
  const n = notes.find(x => x.id === id);
  if (n) {
    n.done = !n.done;
    saveStoredNotes(notes);
    const item = document.getElementById(`note-item-${id}`);
    if (item) item.classList.toggle('done');
  }
}

function deleteNote(id) {
  let notes = getStoredNotes();
  notes = notes.filter(x => x.id !== id);
  saveStoredNotes(notes);
  renderNotesTab(document.getElementById("mainContentArea"));
}

function resetDefaultNotes() {
  saveStoredNotes(DEFAULT_NOTES);
  renderNotesTab(document.getElementById("mainContentArea"));
}

function addNewNote() {
  const input = document.getElementById("newNoteInput");
  if (!input || !input.value.trim()) return;
  const deadlineEl = document.getElementById("newNoteDeadline");
  const deadlineVal = (deadlineEl && deadlineEl.value.trim()) ? deadlineEl.value.trim() : "Дедлайн: без срока";
  const notes = getStoredNotes();
  const newObj = {
    id: Date.now(),
    text: input.value.trim(),
    deadline: deadlineVal,
    done: false
  };
  notes.push(newObj);
  saveStoredNotes(notes);
  playRetroSound("success");
  renderNotesTab(document.getElementById("mainContentArea"));
}

// 4.6 РЕНДЕР ВСЕХ 8 РАЗДЕЛОВ
function renderAllWikiTab(container) {
  container.innerHTML = `
    <div style="margin-bottom:14px;">
      <h2>📚 Интерактивная База знаний Московского Политеха</h2>
      <div style="color:#666;">Выберите один из 8 тематических разделов для перехода к вопросам и регламентам:</div>
    </div>

    <div class="dashboard-grid">
      ${WIKI_CATEGORIES.map(c => `
        <div class="dash-widget wiki-category-card" style="cursor:pointer;" onclick="switchTab('${c.id}')">
          <div style="font-size:24px; margin-bottom:4px;">${c.icon}</div>
          <h3 class="wiki-cat-title">${c.code}. ${c.title}</h3>
          <p class="wiki-cat-desc">${c.desc}</p>
          <div class="wiki-cat-link">Вопросов в разделе: ${c.items.length} ➔</div>
        </div>
      `).join('')}
    </div>
  `;
}

// =========================================================================
// 5. ЖИВОЙ ГЛОБАЛЬНЫЙ ПОИСК С ВЫПАДАЮЩИМИ ПОДСКАЗКАМИ
// =========================================================================
const searchInput = document.getElementById("globalSearchInput");
const searchDropdown = document.getElementById("searchDropdown");

searchInput.addEventListener("input", function() {
  const val = this.value.trim().toLowerCase();
  if (!val) {
    searchDropdown.classList.remove("open");
    return;
  }

  const results = [];
  WIKI_CATEGORIES.forEach(cat => {
    cat.items.forEach(item => {
      if (item.question.toLowerCase().includes(val) || item.short.toLowerCase().includes(val)) {
        results.push({ cat, item });
      }
    });
  });

  if (results.length === 0) {
    searchDropdown.innerHTML = `<div style="padding:10px; font-size:11px; color:#888;">Ничего не найдено по запросу «${val}»</div>`;
  } else {
    searchDropdown.innerHTML = results.slice(0, 6).map(res => `
      <div class="search-dropdown-item" onclick="selectSearchResult('${res.cat.id}', '${res.item.id}')">
        <span class="search-item-cat">${res.cat.code}. ${res.cat.title}</span>
        <span class="search-item-q">${res.item.question}</span>
      </div>
    `).join('');
  }
  searchDropdown.classList.add("open");
});

function selectSearchResult(catId, qId) {
  searchDropdown.classList.remove("open");
  searchInput.value = "";
  switchTab(catId);
  setTimeout(() => openAnswerCard(catId, qId), 150);
}

function searchByQuestion(qText) {
  searchInput.value = qText;
  searchInput.dispatchEvent(new Event("input"));
}

document.addEventListener("click", function(e) {
  if (!e.target.closest(".search-wrapper")) {
    searchDropdown.classList.remove("open");
  }
});

// =========================================================================
// 6. ВСПОМОГАТЕЛЬНЫЙ ПЛАВАЮЩИЙ ИИ-ЧАТ И ПЕРЕМЕЩЕНИЕ (DRAGGABLE FAB)
// =========================================================================
function toggleAiChat() {
  const win = document.getElementById("aiChatWindow");
  win.classList.toggle("open");
  if (win.classList.contains("open")) {
    document.getElementById("aiChatInput").focus();
  }
}

function askAiAboutQuestion(qText) {
  const win = document.getElementById("aiChatWindow");
  win.classList.add("open");
  const input = document.getElementById("aiChatInput");
  input.value = qText;
  sendChatMessage();
}

function handleChatKey(e) {
  if (e.key === "Enter") sendChatMessage();
}

function sendChip(text) {
  document.getElementById("aiChatInput").value = text;
  sendChatMessage();
}


// =========================================================================
// ОБЩИЙ ГЕНЕРАТОР ОТВЕТОВ ИИ-АГЕНТА ПО РЕГЛАМЕНТАМ МОСПОЛИТЕХА
// =========================================================================
function generateSmartAiResponse(text) {
  const query = (text || "").toLowerCase();
  let reply = "";

  if (query.includes("еуз") || query.includes("логин") || query.includes("пароль")) {
    reply = "🔑 <b>Логин и пароль ЕУЗ:</b> высылаются на почту при зачислении. Восстановить доступ можно в <b>Студенческом офисе (корпус А, ауд. А-101)</b> или написав на <code>studentoffice@mospolytech.ru</code> с паспортом.";
  } else if (query.includes("общежит") || query.includes("стоит") || query.includes("комнат") || query.includes("заселен")) {
    reply = "🏠 <b>Общежития МосПолитеха:</b> стоимость проживания от <b>950 до 1 850 руб./мес.</b> Доступны 5 студгородков (Малая Переяславская, Павла Корчагина, Михалковская, 7-я Парковая, Б. Галушкина). Заселение и ордер оформляются через ЛК <code>online.mospolytech.ru</code>. Подробнее во вкладке «Общежития и кампус».";
  } else if (query.includes("пар") || query.includes("завтра") || query.includes("расписан") || query.includes("звонк")) {
    reply = `📅 <b>Расписание занятий:</b> Сейчас выбрана группа <b>${currentSelectedGroup}</b>. Расписание пар доступно во вкладке «Расписание занятий» и на сервере <code>rasp.dmami.ru</code>. Первая пара начинается в 09:00. Для переключения группы воспользуйтесь селектором в шапке расписания!`;
  } else if (query.includes("справк") || query.includes("обучен") || query.includes("вычет")) {
    reply = "📄 <b>Справка об обучении:</b> заказывается онлайн прямо в нашем Личном кабинете (вкладка «Справки и Студофис») либо на <code>online.mospolytech.ru</code>. Готовность от 1 до 3 рабочих дней, забирать оригинал с гербовой печатью в ауд. А-101 (окно №3).";
  } else if (query.includes("автомат") || query.includes("брс") || query.includes("зачет") || query.includes("оценк")) {
    reply = "📊 <b>Автомат по БРС:</b> Для получения автомата необходимо набрать от <b>85 баллов</b> (на усмотрение преподавателя) и выполнить все контрольные точки. Порог допуска к экзамену — <b>60 баллов</b>. Проверьте свои баллы во вкладке «Зачётка и сессия»!";
  } else if (query.includes("проект") || query.includes("дм2026") || query.includes("цпд")) {
    reply = "🚀 <b>Проектная деятельность (ДМ2026):</b> Контрольная точка КТ1 (паспорт проекта) закрывается до 15 ноября. Для успешного зачета необходимо набрать не менее 60 баллов. Центр проектной деятельности (ЦПД): ул. Большая Семёновская, 38, корпус Н, 4-й этаж (Точка кипения, ауд. Н-401).";
  } else if (query.includes("стипенд") || query.includes("выплат") || query.includes("деньг")) {
    reply = "💰 <b>Стипендии:</b> Государственная академическая стипендия (ГАС) выплачивается бюджетникам без троек по итогам сессии (от 2 900 руб.). Повышенная стипендия (ПГАС) назначается за научные, спортивные и творческие достижения (до 14 000 руб.).";
  } else if (query.includes("бюджет") || query.includes("перевод")) {
    reply = "🎯 <b>Перевод на бюджет:</b> возможен при наличии вакантных бюджетных мест после сдачи двух сессий подряд на «отлично» и «хорошо» без троек и академических задолженностей.";
  } else if (query.includes("арми") || query.includes("военкомат") || query.includes("отсрочк")) {
    reply = "🎖️ <b>Отсрочка от службы в армии:</b> справка для военкомата (Приложение №4) оформляется во <b>Втором (мобилизационном) отделе</b>: корпус А, ауд. А-220 при предъявлении приписного удостоверения.";
  } else if (query.includes("сесси") || query.includes("пересдач") || query.includes("экзамен")) {
    reply = "📊 <b>Зимняя сессия 2026:</b> продлится с 11 по 25 января. Подробный график экзаменов доступен во вкладке «Зачётка и сессия». При задолженности даётся ровно 2 пересдачи: первая преподавателю, вторая — комиссии кафедры.";
  } else if (query.includes("а-101") || query.includes("студофис") || query.includes("где")) {
    reply = "📍 <b>Единый студенческий офис (А-101):</b> Главный корпус (ул. Б. Семёновская, 38), корпус А, 1 этаж. Сразу направо от центральных турникетов главного входа. Время работы: Пн-Пт 09:00–19:00, Сб 10:00–15:00.";
  } else {
    reply = `📚 По запросу <b>«${text}»</b>: ПолиГид AI рекомендует обратиться в Единый студенческий офис (корпус А, ауд. А-101, тел. <code>+7 (495) 223-05-23 доб. 1200</code>) либо воспользоваться поиском по 8 разделам нашей Базы знаний!`;
  }
  return reply;
}

// Функции для работы с Google-поисковой строкой на Дашборде
function submitHeroAiSearch() {
  const input = document.getElementById("dashboardAiSearchInput");
  if (!input || !input.value.trim()) return;
  executeHeroSearch(input.value.trim());
}

function handleHeroSearchKey(e) {
  if (e.key === "Enter") submitHeroAiSearch();
}

function triggerHeroChip(text) {
  const input = document.getElementById("dashboardAiSearchInput");
  if (input) input.value = text;
  executeHeroSearch(text);
}

function executeHeroSearch(query) {
  playRetroSound("click");
  const card = document.getElementById("heroAiAnswerCard");
  const content = document.getElementById("heroAiAnswerContent");
  if (!card || !content) return;

  card.style.display = "block";
  content.innerHTML = "<em>🤖 ПолиГид AI ищет ответ в базе знаний и регламентах МосПолитеха...</em>";

  setTimeout(() => {
    const answer = generateSmartAiResponse(query);
    content.innerHTML = answer;
    playRetroSound("success");
    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, 250);
}

function closeHeroAiAnswer() {
  const card = document.getElementById("heroAiAnswerCard");
  if (card) card.style.display = "none";
}

function continueInFullChat() {
  const input = document.getElementById("dashboardAiSearchInput");
  const q = input ? input.value : "";
  toggleAiChat();
  if (q) {
    const chatInp = document.getElementById("aiChatInput");
    if (chatInp) chatInp.value = q;
  }
}

function sendChatMessage() {
  const input = document.getElementById("aiChatInput");
  const text = input.value.trim();
  if (!text) return;

  const msgs = document.getElementById("chatMessages");

  // Добавляем сообщение пользователя
  const userMsg = document.createElement("div");
  userMsg.className = "chat-msg user";
  userMsg.textContent = text;
  msgs.appendChild(userMsg);
  input.value = "";
  msgs.scrollTop = msgs.scrollHeight;

  // Индикатор печати
  const typingIndicator = document.createElement("div");
  typingIndicator.className = "chat-msg bot";
  typingIndicator.id = "aiTypingIndicator";
  typingIndicator.innerHTML = "<em>🤖 ПолиГид AI ищет в регламентах...</em>";
  msgs.appendChild(typingIndicator);
  msgs.scrollTop = msgs.scrollHeight;

  // Имитация умного поиска по регламентам МосПолитеха
  setTimeout(() => {
    const indicator = document.getElementById("aiTypingIndicator");
    if (indicator) indicator.remove();

    const botMsg = document.createElement("div");
    botMsg.className = "chat-msg bot";
    botMsg.innerHTML = generateSmartAiResponse(text);
    msgs.appendChild(botMsg);
    msgs.scrollTop = msgs.scrollHeight;
  }, 350);
}

// =========================================================================
// ПОЛНОЦЕННОЕ ПЕРЕМЕЩЕНИЕ КНОПКИ ИИ-ПОМОЩНИКА (DRAGGABLE FAB)
// =========================================================================

// =========================================================================
// ФИКС ПОЗИЦИОНИРОВАНИЯ ИИ-КНОПКИ ПРИ ИЗМЕНЕНИИ / СЖАТИИ ЭКРАНА
// =========================================================================
function clampFabPosition() {
  const fab = document.getElementById("aiFab");
  if (!fab) return;

  // На экранах мобильных устройств (<= 768px) всегда фиксируем в безопасной зоне над нижним баром
  if (window.innerWidth <= 768) {
    fab.style.left = "auto";
    fab.style.top = "auto";
    fab.style.bottom = "70px";
    fab.style.right = "14px";
    return;
  }

  // Если были заданы абсолютные координаты left / top, проверяем, чтобы кнопка не улетела за правый/нижний край
  if (fab.style.left && fab.style.left !== "auto") {
    const fabWidth = fab.offsetWidth || 135;
    const fabHeight = fab.offsetHeight || 44;
    const currentLeft = parseFloat(fab.style.left) || 0;
    const currentTop = parseFloat(fab.style.top) || 0;

    const maxLeft = Math.max(10, window.innerWidth - fabWidth - 14);
    const maxTop = Math.max(10, window.innerHeight - fabHeight - 14);

    const clampedLeft = Math.max(10, Math.min(maxLeft, currentLeft));
    const clampedTop = Math.max(10, Math.min(maxTop, currentTop));

    fab.style.left = `${clampedLeft}px`;
    fab.style.top = `${clampedTop}px`;
    fab.style.right = "auto";
    fab.style.bottom = "auto";
  }
}

window.addEventListener("resize", clampFabPosition);

function initDraggableFab() {
  const fab = document.getElementById("aiFab");
  if (!fab) return;

  // Восстановление позиции из localStorage с валидацией границ видимости
  try {
    if (window.innerWidth > 768) {
      const saved = localStorage.getItem("poly_fab_pos");
      if (saved) {
        const pos = JSON.parse(saved);
        const l = parseFloat(pos.left);
        const t = parseFloat(pos.top);
        const maxL = window.innerWidth - 140;
        const maxT = window.innerHeight - 50;
        if (!isNaN(l) && !isNaN(t) && l > 0 && l < maxL && t > 0 && t < maxT) {
          fab.style.bottom = "auto";
          fab.style.right = "auto";
          fab.style.left = `${l}px`;
          fab.style.top = `${t}px`;
        }
      }
    }
  } catch(e) {}
  clampFabPosition();

  let isDragging = false;
  let startX, startY, initialX, initialY;

  fab.addEventListener("mousedown", (e) => {
    isDragging = false;
    startX = e.clientX;
    startY = e.clientY;
    const rect = fab.getBoundingClientRect();
    initialX = rect.left;
    initialY = rect.top;

    function onMouseMove(moveEvent) {
      const dx = moveEvent.clientX - startX;
      const dy = moveEvent.clientY - startY;
      if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
        isDragging = true;
        fab.style.bottom = "auto";
        fab.style.right = "auto";
        const newLeft = Math.max(10, Math.min(window.innerWidth - fab.offsetWidth - 10, initialX + dx));
        const newTop = Math.max(10, Math.min(window.innerHeight - fab.offsetHeight - 10, initialY + dy));
        fab.style.left = `${newLeft}px`;
        fab.style.top = `${newTop}px`;
      }
    }

    function onMouseUp() {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      if (!isDragging) {
        toggleAiChat();
      } else {
        clampFabPosition();
        try {
          localStorage.setItem("poly_fab_pos", JSON.stringify({ left: fab.style.left, top: fab.style.top }));
        } catch(e) {}
      }
    }

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  });

  // Поддержка сенсорных экранов / Touch
  fab.addEventListener("touchstart", (e) => {
    isDragging = false;
    const t = e.touches[0];
    startX = t.clientX;
    startY = t.clientY;
    const rect = fab.getBoundingClientRect();
    initialX = rect.left;
    initialY = rect.top;

    function onTouchMove(moveEvent) {
      const touch = moveEvent.touches[0];
      const dx = touch.clientX - startX;
      const dy = touch.clientY - startY;
      if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
        isDragging = true;
        fab.style.bottom = "auto";
        fab.style.right = "auto";
        const newLeft = Math.max(10, Math.min(window.innerWidth - fab.offsetWidth - 10, initialX + dx));
        const newTop = Math.max(10, Math.min(window.innerHeight - fab.offsetHeight - 10, initialY + dy));
        fab.style.left = `${newLeft}px`;
        fab.style.top = `${newTop}px`;
      }
    }

    function onTouchEnd() {
      document.removeEventListener("touchmove", onTouchMove);
      document.removeEventListener("touchend", onTouchEnd);
      if (!isDragging) {
        toggleAiChat();
      }
    }

    document.addEventListener("touchmove", onTouchMove, { passive: true });
    document.addEventListener("touchend", onTouchEnd);
  });
}

// ПЕРЕТАСКИВАНИЕ ОКНА ЧАТА ЗА ЗАГОЛОВОК
function initDraggableChatWindow() {
  const win = document.getElementById("aiChatWindow");
  const header = document.querySelector(".chat-header");
  if (!win || !header) return;

  let isDragging = false;
  let startX, startY, initialX, initialY;

  header.addEventListener("mousedown", (e) => {
    if (e.target.classList.contains("win-btn") || isAiChatMaximized) return;
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    const rect = win.getBoundingClientRect();
    initialX = rect.left;
    initialY = rect.top;

    function onMouseMove(moveEvent) {
      if (!isDragging) return;
      const dx = moveEvent.clientX - startX;
      const dy = moveEvent.clientY - startY;
      win.style.bottom = "auto";
      win.style.right = "auto";
      const newLeft = Math.max(10, Math.min(window.innerWidth - win.offsetWidth - 10, initialX + dx));
      const newTop = Math.max(10, Math.min(window.innerHeight - win.offsetHeight - 10, initialY + dy));
      win.style.left = `${newLeft}px`;
      win.style.top = `${newTop}px`;
    }

    function onMouseUp() {
      isDragging = false;
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    }

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  });
}

// МАКСИМИЗАЦИЯ И ВОССТАНОВЛЕНИЕ ОКНА ЧАТА
let isAiChatMaximized = false;
let prevAiChatGeometry = null;

function toggleMaximizeAiChat() {
  const win = document.getElementById("aiChatWindow");
  const maxBtn = document.getElementById("aiChatMaxBtn");
  if (!win) return;

  if (!isAiChatMaximized) {
    const rect = win.getBoundingClientRect();
    prevAiChatGeometry = {
      width: win.style.width || `${rect.width}px`,
      height: win.style.height || `${rect.height}px`,
      left: win.style.left || `${rect.left}px`,
      top: win.style.top || `${rect.top}px`,
      right: win.style.right,
      bottom: win.style.bottom
    };
    win.style.left = "24px";
    win.style.top = "24px";
    win.style.right = "24px";
    win.style.bottom = "24px";
    win.style.width = "auto";
    win.style.height = "auto";
    if (maxBtn) maxBtn.textContent = "🗗";
    isAiChatMaximized = true;
  } else {
    if (prevAiChatGeometry) {
      win.style.left = prevAiChatGeometry.left;
      win.style.top = prevAiChatGeometry.top;
      win.style.right = prevAiChatGeometry.right;
      win.style.bottom = prevAiChatGeometry.bottom;
      win.style.width = prevAiChatGeometry.width;
      win.style.height = prevAiChatGeometry.height;
    } else {
      win.style.left = "auto";
      win.style.top = "auto";
      win.style.right = "24px";
      win.style.bottom = "85px";
      win.style.width = "420px";
      win.style.height = "550px";
    }
    if (maxBtn) maxBtn.textContent = "🗖";
    isAiChatMaximized = false;
  }
}

// РАСТЯГИВАНИЕ ОКНА ЧАТА (RESIZABLE И С РУЧКАМИ И С КЛАВИАТУРОЙ/МЫШЬЮ)
function initResizableChatWindow() {
  const win = document.getElementById("aiChatWindow");
  const handleSE = document.getElementById("chatResizeHandleSE");
  const handleNW = document.getElementById("chatResizeHandleNW");
  if (!win) return;

  function startResize(e, direction) {
    e.preventDefault();
    e.stopPropagation();

    if (isAiChatMaximized) {
      toggleMaximizeAiChat();
    }

    const isTouch = e.type.startsWith("touch");
    const clientX = isTouch ? e.touches[0].clientX : e.clientX;
    const clientY = isTouch ? e.touches[0].clientY : e.clientY;

    const startRect = win.getBoundingClientRect();
    const startW = startRect.width;
    const startH = startRect.height;
    const startX = clientX;
    const startY = clientY;
    const startLeft = startRect.left;
    const startTop = startRect.top;

    win.style.left = `${startLeft}px`;
    win.style.top = `${startTop}px`;
    win.style.right = "auto";
    win.style.bottom = "auto";

    function onPointerMove(moveEvent) {
      const curX = isTouch ? (moveEvent.touches ? moveEvent.touches[0].clientX : clientX) : moveEvent.clientX;
      const curY = isTouch ? (moveEvent.touches ? moveEvent.touches[0].clientY : clientY) : moveEvent.clientY;
      const dx = curX - startX;
      const dy = curY - startY;

      if (direction === "se") {
        const newW = Math.max(300, Math.min(window.innerWidth - startLeft - 10, startW + dx));
        const newH = Math.max(360, Math.min(window.innerHeight - startTop - 10, startH + dy));
        win.style.width = `${newW}px`;
        win.style.height = `${newH}px`;
      } else if (direction === "nw") {
        const newW = Math.max(300, Math.min(startLeft + startW - 10, startW - dx));
        const newH = Math.max(360, Math.min(startTop + startH - 10, startH - dy));
        const newLeft = startLeft + (startW - newW);
        const newTop = startTop + (startH - newH);
        win.style.width = `${newW}px`;
        win.style.height = `${newH}px`;
        win.style.left = `${newLeft}px`;
        win.style.top = `${newTop}px`;
      }
    }

    function onPointerUp() {
      document.removeEventListener(isTouch ? "touchmove" : "mousemove", onPointerMove);
      document.removeEventListener(isTouch ? "touchend" : "mouseup", onPointerUp);
    }

    document.addEventListener(isTouch ? "touchmove" : "mousemove", onPointerMove, { passive: false });
    document.addEventListener(isTouch ? "touchend" : "mouseup", onPointerUp);
  }

  if (handleSE) {
    handleSE.addEventListener("mousedown", (e) => startResize(e, "se"));
    handleSE.addEventListener("touchstart", (e) => startResize(e, "se"), { passive: false });
  }
  if (handleNW) {
    handleNW.addEventListener("mousedown", (e) => startResize(e, "nw"));
    handleNW.addEventListener("touchstart", (e) => startResize(e, "nw"), { passive: false });
  }
}

// =========================================================================
// 7. ЖИВЫЕ ЧАСЫ И ДАТА В САЙДБАРЕ
// =========================================================================
function updateClock() {
  const clock = document.getElementById("liveClock");
  const dateEl = document.getElementById("liveDate");
  const badgeEl = document.getElementById("liveWeekBadge");
  const now = new Date();
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  const s = String(now.getSeconds()).padStart(2, '0');
  if (clock) clock.textContent = `${h}:${m}:${s}`;

  if (dateEl) {
    const days = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
    const months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"];
    const dayName = days[now.getDay()];
    const d = now.getDate();
    const mon = months[now.getMonth()];
    dateEl.textContent = `${dayName}, ${d} ${mon} ${now.getFullYear()}`;
  }

  if (badgeEl && typeof WEEKS_LIST !== "undefined" && typeof currentWeekIndex !== "undefined") {
    const curW = WEEKS_LIST[currentWeekIndex];
    if (curW) {
      badgeEl.textContent = `🗓️ ${curW.label} [${curW.parity}]`;
    }
  }
}
setInterval(updateClock, 1000);
updateClock();

// =========================================================================
// 8. ПЕРЕКЛЮЧАТЕЛЬ ТЕМ (Y2K РЕТРО <-> МОСПОЛИТЕХ МОДЕРН)
// =========================================================================
let isModern = false;
function toggleTheme() {
  isModern = !isModern;
  const body = document.body;
  const btnIcon = document.getElementById("themeBtnIcon");
  const btnText = document.getElementById("themeBtnText");

  if (isModern) {
    body.classList.add("theme-modern");
    btnIcon.textContent = "⚡";
    btnText.textContent = "Тема: Модерн";
  } else {
    body.classList.remove("theme-modern");
    btnIcon.textContent = "💾";
    btnText.textContent = "Тема: Y2K Ретро";
  }
}

// Сайдбар по умолчанию открыт и виден
isSidebarCollapsed = false;

// Запуск приложения

// =========================================================================
// ЗВУКОВЫЕ ЭФФЕКТЫ РЕТРО (WEB AUDIO API SYNTHESIZER)
// =========================================================================
let isSoundEnabled = false;
let audioCtx = null;

function getAudioContext() {
  if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioCtx;
}

function playRetroSound(type = "click") {
  if (!isSoundEnabled) return;
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    const now = ctx.currentTime;
    if (type === "click") {
      osc.type = "square";
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(400, now + 0.04);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
      osc.start(now);
      osc.stop(now + 0.04);
    } else if (type === "success") {
      osc.type = "sine";
      osc.frequency.setValueAtTime(523.25, now);
      osc.frequency.setValueAtTime(659.25, now + 0.08);
      osc.frequency.setValueAtTime(783.99, now + 0.16);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
      osc.start(now);
      osc.stop(now + 0.28);
    } else if (type === "notify") {
      osc.type = "triangle";
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.start(now);
      osc.stop(now + 0.18);
    }
  } catch(e) {}
}

function toggleSound() {
  isSoundEnabled = !isSoundEnabled;
  const btnIcon = document.getElementById("soundBtnIcon");
  const btnText = document.getElementById("soundBtnText");
  if (isSoundEnabled) {
    btnIcon.textContent = "🔊";
    btnText.textContent = "Звук: ВКЛ";
    playRetroSound("success");
  } else {
    btnIcon.textContent = "🔈";
    btnText.textContent = "Звук: ВЫКЛ";
  }
  try {
    localStorage.setItem("poly_sound_enabled", isSoundEnabled ? "1" : "0");
  } catch(e) {}
}

// =========================================================================
// ЦЕНТР УВЕДОМЛЕНИЙ КАМПУСА
// =========================================================================
function toggleNotifications() {
  const dd = document.getElementById("notifDropdown");
  if (!dd) return;
  dd.classList.toggle("open");
  playRetroSound("click");
}

function clearNotifications() {
  const list = document.getElementById("notifList");
  const badge = document.getElementById("notifBadge");
  if (list) list.innerHTML = '<div style="padding:16px; text-align:center; font-size:11px; color:#888;">Все уведомления прочитаны</div>';
  if (badge) badge.style.display = 'none';
  playRetroSound("click");
}

document.addEventListener("click", function(e) {
  if (!e.target.closest(".notifications-wrapper")) {
    const dd = document.getElementById("notifDropdown");
    if (dd) dd.classList.remove("open");
  }
});

// =========================================================================
// ЦИФРОВОЙ СТУДЕНЧЕСКИЙ БИЛЕТ (МОДАЛЬНОЕ ОКНО)
// =========================================================================
function openStudentIdModal() {
  playRetroSound("click");
  const modal = document.getElementById("lessonModal");
  const content = document.getElementById("lessonModalContent");
  if (!modal || !content) return;

  content.innerHTML = `
    <div class="title-bar" style="cursor:default;">
      <div class="title-bar-left">
        <span>🪪</span>
        <span>Электронный студенческий билет Московского Политеха</span>
      </div>
      <div class="win-btn" onclick="closeLessonModal()" title="Закрыть (Esc)">✕</div>
    </div>
    <div class="modal-body" style="display:flex; justify-content:center; align-items:center; padding:18px;">
      <div class="student-id-card">
        <div class="student-id-header">
          <div>
            <div style="font-size:9px; color:#ffcc00; letter-spacing:1px; font-weight:800;">МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РФ</div>
            <div style="font-size:14px; font-weight:900; color:#fff; letter-spacing:0.5px;">МОСКОВСКИЙ ПОЛИТЕХ</div>
          </div>
          <div style="font-size:24px;">🎓</div>
        </div>
        
        <div class="student-id-body">
          <div class="student-id-photo">
            <span>🐱</span>
            <span style="font-size:8px; font-weight:bold; margin-top:2px; color:#555;">ФОТО</span>
          </div>
          <div class="student-id-info">
            <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:4px;">СМИРНОВ Алексей Дмитриевич</div>
            <div><b>Билет №:</b> 241-321-0428</div>
            <div><b>Факультет:</b> Информационных технологий (ФИТ)</div>
            <div><b>Направление:</b> 09.03.01 Информатика и ВТ</div>
            <div><b>Форма:</b> Очная (Бюджетная основа)</div>
            <div><b>Курс / Группа:</b> 2 курс · гр. 241-321</div>
            <div><b>Действителен:</b> до 30.06.2028 г.</div>
          </div>
        </div>

        <div class="student-id-barcode">
          <span>||| | ||||| || |||| || ||| ||||||| |</span>
          <span>#MP-2413210428-2026</span>
          <span style="color:#51cf66; font-weight:bold;">🟢 АКТИВЕН</span>
        </div>
      </div>
    </div>
    <div class="modal-footer" style="padding:10px 16px; display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-dark); background:var(--win-face);">
      <span style="font-size:11px; opacity:0.8;">При предъявлении на КПП кампуса и в библиотеке</span>
      <button class="retro-btn" onclick="closeLessonModal()">Закрыть</button>
    </div>
  `;
  modal.classList.add("open");
}

// =========================================================================
// ЭКСПОРТ РАСПИСАНИЯ В ICALENDAR (.ICS)
// =========================================================================
function exportScheduleToIcs() {
  const grpData = GROUPS_DATA[currentSelectedGroup] || GROUPS_DATA["241-321"];
  const sched = grpData.schedule;

  let icsLines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//MosPolytech//Student Assistant//RU",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    `X-WR-CALNAME:Расписание МосПолитех ${currentSelectedGroup}`,
    "X-WR-TIMEZONE:Europe/Moscow"
  ];

  const dayOffsets = { mon: 1, tue: 2, wed: 3, thu: 4, fri: 5, sat: 6 };
  const baseDate = new Date(2026, 10, 9); // Понедельник 9 ноября 2026

  Object.keys(sched).forEach(dayKey => {
    const dayData = sched[dayKey];
    const offset = (dayOffsets[dayKey] || 1) - 1;
    const eventDate = new Date(baseDate);
    eventDate.setDate(baseDate.getDate() + offset);

    const y = eventDate.getFullYear();
    const m = String(eventDate.getMonth() + 1).padStart(2, '0');
    const d = String(eventDate.getDate()).padStart(2, '0');

    Object.keys(dayData).forEach(sNum => {
      const l = dayData[sNum];
      const slot = TIME_SLOTS.find(s => s.num === parseInt(sNum));
      if (!slot) return;

      const startParts = slot.start.split(':');
      const endParts = slot.end.split(':');
      const dtStart = `${y}${m}${d}T${startParts[0]}${startParts[1]}00`;
      const dtEnd = `${y}${m}${d}T${endParts[0]}${endParts[1]}00`;

      icsLines.push("BEGIN:VEVENT");
      icsLines.push(`UID:poly-${currentSelectedGroup}-${dayKey}-${sNum}-${y}${m}${d}@mospolytech.ru`);
      icsLines.push(`DTSTAMP:${y}${m}${d}T000000Z`);
      icsLines.push(`DTSTART;TZID=Europe/Moscow:${dtStart}`);
      icsLines.push(`DTEND;TZID=Europe/Moscow:${dtEnd}`);
      icsLines.push(`SUMMARY:${l.name} (${l.type})`);
      icsLines.push(`LOCATION:Московский Политех, ауд. ${l.room}, ${l.campus}`);
      icsLines.push(`DESCRIPTION:Преподаватель: ${l.teacher}\\nГруппа: ${currentSelectedGroup}\\n${l.desc || ''}`);
      icsLines.push("STATUS:CONFIRMED");
      icsLines.push("END:VEVENT");
    });
  });

  icsLines.push("END:VCALENDAR");
  const icsBlob = new Blob([icsLines.join("\r\n")], { type: "text/calendar;charset=utf-8" });
  const url = URL.createObjectURL(icsBlob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `mospolytech_${currentSelectedGroup}_schedule.ics`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  playRetroSound("success");
  alert(`✅ Расписание группы ${currentSelectedGroup} успешно экспортировано в файл mospolytech_${currentSelectedGroup}_schedule.ics!`);
}

// =========================================================================
// 4.7 РЕНДЕР ВКЛАДКИ ПРОЕКТНОЙ ДЕЯТЕЛЬНОСТИ (ПД / ДМ2026)
// =========================================================================
const DEFAULT_PROJECT_TASKS = [
  { id: 1, text: "Утвердить паспорт проекта КТ1 и состав команды на портале ЦПД", assignee: "Алексей С.", done: true },
  { id: 2, text: "Собрать регламенты и вопросы первокурсников для Базы знаний", assignee: "Екатерина В.", done: true },
  { id: 3, text: "Разработать кликабельный Y2K интерфейс и переключатель тем", assignee: "Алексей С.", done: true },
  { id: 4, text: "Интегрировать расписание rasp.dmami.ru и модалки пар", assignee: "Максим М.", done: false },
  { id: 5, text: "Подготовить слайды презентации к Демо-дню ДМ2026", assignee: "Дарья С.", done: false }
];

function getStoredProjectTasks() {
  try {
    const s = localStorage.getItem("poly_project_tasks");
    return s ? JSON.parse(s) : DEFAULT_PROJECT_TASKS;
  } catch(e) { return DEFAULT_PROJECT_TASKS; }
}

function saveStoredProjectTasks(tasks) {
  try {
    localStorage.setItem("poly_project_tasks", JSON.stringify(tasks));
  } catch(e) {}
}


let currentProjectAssigneeFilter = "all";

function setProjectAssigneeFilter(filter) {
  currentProjectAssigneeFilter = filter;
  playRetroSound("click");
  renderProjectsTab(document.getElementById("mainContentArea"));
}

function getAssigneeColor(assignee) {
  if (assignee.includes("Алексей")) return "#1971c2";
  if (assignee.includes("Дарья")) return "#7928ca";
  if (assignee.includes("Максим")) return "#2b8a3e";
  if (assignee.includes("Екатерина")) return "#d9480f";
  return "#099268";
}

function cycleAssignee(id) {
  const members = ["Алексей С.", "Дарья С.", "Максим М.", "Екатерина В.", "Вся команда"];
  const tasks = getStoredProjectTasks();
  const t = tasks.find(x => x.id === id);
  if (t) {
    const currIdx = members.indexOf(t.assignee);
    const nextIdx = (currIdx + 1) % members.length;
    t.assignee = members[nextIdx];
    saveStoredProjectTasks(tasks);
    playRetroSound("click");
    renderProjectsTab(document.getElementById("mainContentArea"));
  }
}

function renderProjectsTab(container) {
  const tasks = getStoredProjectTasks();
  container.innerHTML = `
    <!-- Заголовок и карточка проекта -->
    <div class="project-header-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
        <div>
          <span style="background:rgba(255,255,255,0.2); padding:2px 8px; border-radius:4px; font-size:10px; font-weight:bold; letter-spacing:1px;">ПД-2026 · ИТ-ТРЕК</span>
          <h2 style="margin:6px 0 4px 0; color:#fff; font-size:18px;">🚀 Интеллектуальный кампусный ассистент и База знаний МосПолитех</h2>
          <div style="font-size:12px; opacity:0.9;">Кафедра «Информационные технологии» · Куратор: к.т.н., доц. Смирнов А.В.</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:24px; font-weight:900; color:#ffcc00;">93 / 100 б.</div>
          <div style="font-size:10px; color:#e0e7ff;">Прогнозируемая оценка: <b>ОТЛИЧНО (АВТОМАТ)</b></div>
        </div>
      </div>

      <div class="sprint-timeline">
        <div class="sprint-step done">
          <b>КТ 1 (20 б.)</b><br>Паспорт проекта ✅<br><span style="color:#51cf66; font-weight:bold;">20 / 20</span>
        </div>
        <div class="sprint-step done">
          <b>КТ 2 (25 б.)</b><br>Архитектура & UX ✅<br><span style="color:#51cf66; font-weight:bold;">25 / 25</span>
        </div>
        <div class="sprint-step current">
          <b>КТ 3 (30 б.)</b><br>Фронтенд & Чат-бот 🔄<br><span style="color:#ffd43b; font-weight:bold;">28 / 30</span>
        </div>
        <div class="sprint-step">
          <b>КТ 4 (50 б.)</b><br>Демо-день & Защита ⏳<br><span style="opacity:0.8;">22 дек 2026</span>
        </div>
      </div>
    </div>

    <!-- Сетка: Команда и Интерактивный бэклог задач -->
    <div class="project-grid">
      <!-- Карточка команды -->
      <div class="project-card">
        <h3>👥 Состав проектной команды</h3>
        <div style="margin-top:10px; display:flex; flex-direction:column; gap:8px; font-size:11px;">
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; background:var(--win-face); border:1px solid var(--border-dark); border-radius:4px;">
            <div><b>🐱 Алексей Смирнов (Вы)</b><br><span style="color:#666; font-size:10px;">Team Lead · Frontend & UI/UX</span></div>
            <span class="badge-tag" style="background:#e7f5ff; color:#1971c2;">Лидер</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; background:var(--win-face); border:1px solid var(--border-dark); border-radius:4px;">
            <div><b>🎨 Дарья Соколова</b><br><span style="color:#666; font-size:10px;">Дизайн систем & Графика Y2K</span></div>
            <span class="badge-tag" style="background:#f3d9fa; color:#7928ca;">Дизайн</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; background:var(--win-face); border:1px solid var(--border-dark); border-radius:4px;">
            <div><b>⚙️ Максим Морозов</b><br><span style="color:#666; font-size:10px;">Backend & Интеграция rasp.dmami.ru</span></div>
            <span class="badge-tag" style="background:#ebfbee; color:#2b8a3e;">Backend</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; background:var(--win-face); border:1px solid var(--border-dark); border-radius:4px;">
            <div><b>🔍 Екатерина Волкова</b><br><span style="color:#666; font-size:10px;">Тестирование & Контент Базы знаний</span></div>
            <span class="badge-tag" style="background:#fff3bf; color:#f08c00;">QA & Анализ</span>
          </div>
        </div>

        <div style="margin-top:14px; padding-top:10px; border-top:1px dashed var(--border-dark); font-size:11px;">
          <b>📍 Локация команды:</b> Кампус Б. Семёновская, ауд. Н-401 (Точка кипения / Коворкинг ПД).
        </div>
      </div>

      <!-- Интерактивный бэклог задач спринта -->
      <div class="project-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <h3>📋 Задачи спринта (Бэклог)</h3>
          <span style="font-size:10px; color:#666;">Назначение людей на задачи</span>
        </div>

        <!-- Фильтр по исполнителю -->
        <div class="assignee-filter-bar">
          <button class="assignee-filter-btn ${currentProjectAssigneeFilter==='all'?'active':''}" onclick="setProjectAssigneeFilter('all')">Все (${tasks.length})</button>
          <button class="assignee-filter-btn ${currentProjectAssigneeFilter==='Алексей С.'?'active':''}" onclick="setProjectAssigneeFilter('Алексей С.')">Мои (Алексей)</button>
          <button class="assignee-filter-btn ${currentProjectAssigneeFilter==='Дарья С.'?'active':''}" onclick="setProjectAssigneeFilter('Дарья С.')">Дарья С.</button>
          <button class="assignee-filter-btn ${currentProjectAssigneeFilter==='Максим М.'?'active':''}" onclick="setProjectAssigneeFilter('Максим М.')">Максим М.</button>
          <button class="assignee-filter-btn ${currentProjectAssigneeFilter==='Екатерина В.'?'active':''}" onclick="setProjectAssigneeFilter('Екатерина В.')">Екатерина В.</button>
        </div>

        <div style="display:flex; flex-direction:column; gap:6px; max-height:220px; overflow-y:auto; padding-right:4px;">
          ${tasks.filter(t => currentProjectAssigneeFilter === 'all' || t.assignee.includes(currentProjectAssigneeFilter)).map(t => `
            <div class="note-item ${t.done ? 'done' : ''}" style="margin-bottom:2px; padding:6px 8px; display:flex; align-items:center; gap:8px;">
              <input type="checkbox" ${t.done ? 'checked' : ''} onchange="toggleProjectTask(${t.id})">
              <div style="flex:1; font-size:11px;">
                <span>${t.text}</span>
              </div>
              <span class="badge-tag" onclick="cycleAssignee(${t.id})" style="cursor:pointer; font-size:10px; padding:2px 6px; background:${getAssigneeColor(t.assignee)}; color:#fff;" title="Нажмите, чтобы переназначить исполнителя">
                👤 ${t.assignee} ▾
              </span>
              <button class="win-btn" onclick="deleteProjectTask(${t.id})" title="Удалить задачу" style="width:18px; height:18px; font-size:9px;">✕</button>
            </div>
          `).join('')}
        </div>

        <!-- Форма добавления задачи с выбором исполнителя -->
        <div style="display:flex; gap:6px; margin-top:10px; flex-wrap:wrap;">
          <input type="text" id="newProjectTaskInput" placeholder="Новая задача для проекта..." style="flex:2; min-width:180px; padding:5px 8px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius);" onkeydown="if(event.key==='Enter') addProjectTask()">
          <select id="newProjectTaskAssignee" style="flex:1; min-width:130px; padding:5px 6px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius); background:#fff;">
            <option value="Алексей С.">🐱 Алексей С. (Вы)</option>
            <option value="Дарья С.">🎨 Дарья С. (Дизайн)</option>
            <option value="Максим М.">⚙️ Максим М. (Backend)</option>
            <option value="Екатерина В.">🔍 Екатерина В. (QA)</option>
            <option value="Вся команда">👥 Вся команда</option>
          </select>
          <button class="retro-btn" onclick="addProjectTask()">+ Добавить</button>
        </div>
      </div>
    </div>

    <!-- Ресурсы и регламенты ДМ2026 -->
    <div class="dash-widget">
      <h3>📚 Полезные ресурсы и документы Проектной деятельности</h3>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-top:8px; font-size:11px;">
        <a href="https://mospolytech.ru/" target="_blank" style="text-decoration:none; color:inherit; background:var(--win-face); border:1px solid var(--border-dark); padding:8px 10px; border-radius:4px; display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">📑</span>
          <div><b>Регламент ДМ2026</b><br><span style="font-size:9px; color:#666;">Критерии оценивания и защиты</span></div>
        </a>
        <a href="https://online.mospolytech.ru/" target="_blank" style="text-decoration:none; color:inherit; background:var(--win-face); border:1px solid var(--border-dark); padding:8px 10px; border-radius:4px; display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🌐</span>
          <div><b>Портал проектов ЦПД</b><br><span style="font-size:9px; color:#666;">Загрузка отчетов и файлов</span></div>
        </a>
        <a href="https://github.com/" target="_blank" style="text-decoration:none; color:inherit; background:var(--win-face); border:1px solid var(--border-dark); padding:8px 10px; border-radius:4px; display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🐙</span>
          <div><b>Репозиторий GitHub</b><br><span style="font-size:9px; color:#666;">Исходный код кампусного ассистента</span></div>
        </a>
      </div>
    </div>
  `;
}

function toggleProjectTask(id) {
  playRetroSound("click");
  const tasks = getStoredProjectTasks();
  const t = tasks.find(x => x.id === id);
  if (t) {
    t.done = !t.done;
    saveStoredProjectTasks(tasks);
    renderProjectsTab(document.getElementById("mainContentArea"));
  }
}

function deleteProjectTask(id) {
  playRetroSound("click");
  let tasks = getStoredProjectTasks();
  tasks = tasks.filter(x => x.id !== id);
  saveStoredProjectTasks(tasks);
  renderProjectsTab(document.getElementById("mainContentArea"));
}

function addProjectTask() {
  const inp = document.getElementById("newProjectTaskInput");
  if (!inp || !inp.value.trim()) return;
  const assigneeEl = document.getElementById("newProjectTaskAssignee");
  const assignee = assigneeEl ? assigneeEl.value : "Алексей С.";
  const tasks = getStoredProjectTasks();
  tasks.push({
    id: Date.now(),
    text: inp.value.trim(),
    assignee: assignee,
    done: false
  });
  saveStoredProjectTasks(tasks);
  playRetroSound("success");
  renderProjectsTab(document.getElementById("mainContentArea"));
}

// =========================================================================
// 4.8 РЕНДЕР ВКЛАДКИ СПРАВОК И СТУДОФИСА (МФЦ)
// =========================================================================
const DEFAULT_ORDERS = [
  { id: "МП-2026-7120", type: "Справка об обучении с гербовой печатью", target: "В налоговую для вычета", format: "Бумажный оригинал (А-101)", status: "Готова к выдаче", date: "05.11.2026", ready: true },
  { id: "МП-2026-6944", type: "Справка в военкомат (Приложение №4)", target: "Военный комиссариат", format: "Второй отдел (А-220)", status: "На подписи у руководства", date: "02.11.2026", ready: false }
];

function getStoredOrders() {
  try {
    const s = localStorage.getItem("poly_services_orders");
    return s ? JSON.parse(s) : DEFAULT_ORDERS;
  } catch(e) { return DEFAULT_ORDERS; }
}

function saveStoredOrders(orders) {
  try {
    localStorage.setItem("poly_services_orders", JSON.stringify(orders));
  } catch(e) {}
}

function renderServicesTab(container) {
  const orders = getStoredOrders();
  container.innerHTML = `
    <div style="margin-bottom:14px;">
      <h2>📄 Заказ справок и Единый Студенческий Офис (МФЦ)</h2>
      <div style="color:#666;">Заказывайте официальные документы университета онлайн без очередей в деканате:</div>
    </div>

    <!-- Форма заказа справки -->
    <div class="mfc-form-card">
      <h3 style="color:#000080; margin-bottom:10px;">📝 Новая заявка на документ</h3>
      <div class="mfc-grid">
        <div>
          <label style="display:block; font-size:11px; font-weight:bold; margin-bottom:4px;">Тип справки / документа:</label>
          <select id="mfcDocType" style="width:100%; padding:6px 8px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius); background:#fff;">
            <option value="Справка об обучении с гербовой печатью">Справка об обучении с гербовой печатью (для работы / льгот)</option>
            <option value="Справка в военный комиссариат (Приложение №4)">Справка в военный комиссариат (Приложение №4)</option>
            <option value="Справка о стипендии и доходах (форма 2-НДФЛ)">Справка о стипендии и доходах (форма 2-НДФЛ / для соцзащиты)</option>
            <option value="Дубликат электронного пропуска">Дубликат электронного пропуска (взамен утерянного)</option>
            <option value="Выписка из зачётной ведомости (БРС)">Выписка из зачётной ведомости (БРС за все семестры)</option>
          </select>
        </div>

        <div>
          <label style="display:block; font-size:11px; font-weight:bold; margin-bottom:4px;">Цель / Куда предоставляется:</label>
          <select id="mfcDocTarget" style="width:100%; padding:6px 8px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius); background:#fff;">
            <option value="По месту требования">По месту требования</option>
            <option value="Налоговая инспекция (налоговый вычет)">Налоговая инспекция (налоговый вычет)</option>
            <option value="Военный комиссариат (отсрочка)">Военный комиссариат (отсрочка)</option>
            <option value="Пенсионный фонд РФ">Пенсионный фонд РФ</option>
            <option value="Посольство / Для визы">Посольство / Для визы</option>
          </select>
        </div>

        <div>
          <label style="display:block; font-size:11px; font-weight:bold; margin-bottom:4px;">Способ получения:</label>
          <select id="mfcDocFormat" style="width:100%; padding:6px 8px; font-size:11px; border:1px solid var(--border-dark); border-radius:var(--border-radius); background:#fff;">
            <option value="Бумажный оригинал с печатью (ауд. А-101)">Бумажный оригинал с синей гербовой печатью (каб. А-101)</option>
            <option value="Электронный скан с усиленной ЭЦП (на e-mail)">Электронный скан с усиленной ЭЦП (на корпоративный e-mail)</option>
          </select>
        </div>

        <div style="display:flex; align-items:flex-end;">
          <button class="retro-btn" onclick="submitMfcOrder()" style="width:100%; padding:8px 12px; font-weight:bold; background:#000080; color:#fff;">
            🚀 Заказать документ онлайн
          </button>
        </div>
      </div>
      <div style="font-size:10px; color:#666;">
        ⏱️ Срок изготовления: от 1 до 3 рабочих дней. Уведомление о готовности придет в личный кабинет и на электронную почту.
      </div>
    </div>

    <!-- Список активных и выданных заявок -->
    <div class="dash-widget" style="margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <h3>📋 Мои заказы документов</h3>
        <span style="font-size:11px; color:#666;">Всего заявок: ${orders.length}</span>
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        ${orders.map(o => `
          <div class="mfc-order-item">
            <div style="flex:1;">
              <div style="display:flex; align-items:center; gap:8px;">
                <b>${o.type}</b>
                <span class="badge-tag" style="font-family:monospace;">${o.id}</span>
              </div>
              <div style="font-size:11px; color:#555; margin-top:2px;">
                🎯 Цель: ${o.target} · 📦 Формат: ${o.format} · Дата: ${o.date}
              </div>
            </div>
            <div style="text-align:right;">
              <span class="badge-tag" style="background:${o.ready ? '#ebfbee' : '#fff3bf'}; color:${o.ready ? '#2b8a3e' : '#f08c00'}; font-weight:bold;">
                ${o.ready ? '🟢 Готова к выдаче' : '🟡 В обработке'}
              </span>
              ${o.ready ? `
                <div style="font-size:10px; color:#2b8a3e; margin-top:3px; font-weight:bold;">
                  📍 Забрать: ауд. А-101 (окно 3)
                </div>
              ` : ''}
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Информационная плашка Студофиса -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px;">
      <div class="summary-card">
        <h3>🏢 Единый студенческий офис (А-101)</h3>
        <div style="font-size:11px; line-height:1.6; margin-top:6px;">
          📍 <b>Адрес:</b> ул. Б. Семёновская, 38, корпус А, ауд. А-101<br>
          ⏰ <b>Часы приёма:</b> Пн–Пт с 09:00 до 19:00, Сб с 10:00 до 15:00<br>
          📞 <b>Телефон:</b> +7 (495) 223-05-23 доб. 1200 / 1201<br>
          📧 <b>Email:</b> studentoffice@mospolytech.ru
        </div>
      </div>

      <div class="summary-card">
        <h3>🎖️ Второй отдел (Воинский учёт)</h3>
        <div style="font-size:11px; line-height:1.6; margin-top:6px;">
          📍 <b>Адрес:</b> ул. Б. Семёновская, 38, корпус А, ауд. А-220<br>
          ⏰ <b>Часы приёма:</b> Пн, Вт, Чт с 10:00 до 16:30 (перерыв 13:00–14:00)<br>
          📄 <b>При себе иметь:</b> Паспорт РФ и приписное удостоверение (или военный билет)<br>
          💡 Справка в военкомат выдается строго лично в руки!
        </div>
      </div>
    </div>
  `;
}

function submitMfcOrder() {
  const type = document.getElementById("mfcDocType").value;
  const target = document.getElementById("mfcDocTarget").value;
  const format = document.getElementById("mfcDocFormat").value;

  const orders = getStoredOrders();
  const rndCode = Math.floor(1000 + Math.random() * 9000);
  const now = new Date();
  const dateStr = `${String(now.getDate()).padStart(2,'0')}.${String(now.getMonth()+1).padStart(2,'0')}.${now.getFullYear()}`;

  const newOrder = {
    id: `МП-2026-${rndCode}`,
    type: type,
    target: target,
    format: format,
    status: "В обработке деканатом",
    date: dateStr,
    ready: false
  };

  orders.unshift(newOrder);
  saveStoredOrders(orders);
  playRetroSound("success");
  alert(`✅ Заявка на документ «${type}» успешно отправлена!\nНомер обращения: ${newOrder.id}\nСтатус можно отслеживать в этом разделе.`);
  renderServicesTab(document.getElementById("mainContentArea"));
}

// =========================================================================
// 4.9 РЕНДЕР ВКЛАДКИ НАВИГАТОРА ПО АУДИТОРИЯМ И КОРПУСАМ
// =========================================================================
let selectedNavCampus = "sem";

const ROOMS_DB = [
  // БОЛЬШАЯ СЕМЁНОВСКАЯ, 38 (ГЛАВНЫЙ КАМПУС)
  { room: "Н-401", campus: "sem", title: "Дирекция Центра проектной деятельности (ЦПД) & Точка кипения", floor: "4 этаж", building: "Корпус Н", desc: "Главный штаб проектной деятельности МосПолитеха (ДМ2026), защита паспортов и презентаций КТ1/КТ2, переговорные залы.", route: "На скоростном лифте корпуса Н на 4 этаж, направо от турникетов Точки кипения." },
  { room: "Н-405", campus: "sem", title: "Проектный коворкинг FabLab и зона прототипирования", floor: "4 этаж", building: "Корпус Н", desc: "Открытое рабочее пространство для команд проектной деятельности: 3D-принтеры, лазерный раскрой, Wi-Fi, маркерные доски и пуфы.", route: "Корпус Н, 4 этаж, зона коворкинга напротив эскалатора." },
  { room: "А-101", campus: "sem", title: "Единый студенческий офис (МФЦ МосПолитеха)", floor: "1 этаж", building: "Корпус А", desc: "Приём заявлений, заказ и выдача всех видов справок, переводы, восстановление документов, продление студенческих билетов.", route: "Сразу направо от центральных турникетов главного входа кампуса." },
  { room: "А-220", campus: "sem", title: "Второй (мобилизационный) отдел", floor: "2 этаж", building: "Корпус А", desc: "Воинский учёт студентов, выдача справок Приложение №4 для военкомата, оформление отсрочки от призыва.", route: "По центральной лестнице корпуса А на 2 этаж, направо по коридору." },
  { room: "А-412", campus: "sem", title: "Деканат Факультета информационных технологий (ФИТ)", floor: "4 этаж", building: "Корпус А", desc: "Учебная часть ФИТ: кураторы направлений 09.03.01 и 09.03.02, академические ведомости, вопросы практик.", route: "Корпус А, 4 этаж, центральное крыло." },
  { room: "Б-204", campus: "sem", title: "Компьютерный класс кафедры ИТ", floor: "2 этаж", building: "Корпус Б", desc: "Лаборатория прикладного программирования, системного администрирования, ОС Linux и сетевых технологий.", route: "Корпус Б, 2 этаж, левое крыло." },
  { room: "Б-305", campus: "sem", title: "Лаборатория баз данных и веб-разработки", floor: "3 этаж", building: "Корпус Б", desc: "30 современных рабочих станций, сервер тестовых сред PostgreSQL/Redis, интерактивная доска.", route: "Корпус Б, 3 этаж, возле лестничного пролёта." },
  { room: "В-202", campus: "sem", title: "Приёмная комиссия / Большой конференц-зал", floor: "2 этаж", building: "Корпус В", desc: "Зал Учёного совета, университетские хакатоны, презентации индустриальных партнёров и дни открытых дверей.", route: "Через переход из корпуса А в корпус В, 2 этаж." },
  { room: "В-302", campus: "sem", title: "Поточная лекционная аудитория им. В. В. Бахирева", floor: "3 этаж", building: "Корпус В", desc: "Большой мультимедийный амфитеатр на 150 мест со сдвоенными проекторами и акустической системой.", route: "Корпус В, 3 этаж, напротив кафедры математики." },
  { room: "Н-102", campus: "sem", title: "Главная столовая и кофе-пойнт кампуса", floor: "1 этаж", building: "Корпус Н", desc: "Горячие комплексные студенческие обеды от 220 руб., салаты, супы, свежая выпечка и кофейный корнер.", route: "1 этаж корпуса Н, прямо по холлу атриума." },

  // АВТОЗАВОДСКАЯ, 16 (ТРАНСПОРТНЫЙ ФАКУЛЬТЕТ)
  { room: "АВ-204", campus: "avto", title: "Деканат Транспортного факультета", floor: "2 этаж", building: "Корпус 1 (Автозаводская)", desc: "Учебная часть транспортных специальностей, ведомости успеваемости, консультации по практикам на автозаводах.", route: "Центральный вход, подняться по парадной лестнице на 2 этаж, кабинет 204." },
  { room: "АВ-1102", campus: "avto", title: "Инженерно-гоночный бокс FDR Moscow (Formula Student)", floor: "1 этаж", building: "Ангар 2 (Автозаводская)", desc: "Штаб-квартира гоночной инженерной команды Moscow Polytech: проектирование и сборка гоночных болидов и электрокаров.", route: "Внутренний двор кампуса Автозаводская, ангар 2 инженерно-спортивных команд." },
  { room: "АВ-105", campus: "avto", title: "Лаборатория тяговых электроприводов и электромобилей", floor: "1 этаж", building: "Корпус 1 (Автозаводская)", desc: "Испытательные стенды электродвигателей, высоковольтных тяговых батарей и контроллеров для беспилотников.", route: "1 этаж главного корпуса, левое крыло." },
  { room: "АВ-112", campus: "avto", title: "Лаборатория двигателей внутреннего сгорания (ДВС)", floor: "1 этаж", building: "Лабораторный корпус", desc: "Моторные испытательные боксы, нагрузочные стенды, газоанализ и эко-контроль автомобильных силовых установок.", route: "1 этаж лабораторного корпуса, северный въезд." },
  { room: "АВ-308", campus: "avto", title: "Компьютерный класс САПР и транспортного дизайна", floor: "3 этаж", building: "Корпус 1 (Автозаводская)", desc: "3D-моделирование кузовов и агрегатов (Siemens NX, Компас-3D), цифровая гидроаэродинамика в ANSYS Fluent.", route: "3 этаж главного корпуса, направо по коридору до ауд. 308." },
  { room: "СК-Авто", campus: "avto", title: "Спортивный комплекс кампуса (бассейн и залы)", floor: "1–2 этажи", building: "Спорткомплекс", desc: "Плавательный бассейн 25 метров (5 дорожек), тренажёрный зал, секции волейбола, баскетбола и единоборств.", route: "Отдельный вход слева от центрального КПП кампуса Автозаводская." },
  { room: "АВ-101", campus: "avto", title: "Студенческая столовая Автозаводская", floor: "1 этаж", building: "Корпус 1 (Автозаводская)", desc: "Горячее питание, комплексные обеды для студентов и сотрудников, выпечка, чай и кофе.", route: "1 этаж главного корпуса, справа от вестибюля." },

  // ПРЯНИШНИКОВА, 2А (ИНСТИТУТ ГРАФИКИ И ИСКУССТВА КНИГИ)
  { room: "ПР-215", campus: "pryan", title: "Медиа-лаборатория графики и типографики", floor: "2 этаж", building: "ул. Прянишникова, 2А", desc: "Институт графики и искусства книги им. В.А. Фаворского: графические планшеты Wacom, профессиональная вёрстка книг и журналов.", route: "Главный корпус на Прянишникова, 2 этаж, правое крыло." },
  { room: "ПР-102", campus: "pryan", title: "Мастерская эстампа, линогравюры и офорта", floor: "1 этаж", building: "ул. Прянишникова, 2А", desc: "Офортные и печатные станки для глубокой печати, литографские камни, ванны травления и сушилки.", route: "1 этаж, налево от поста охраны, мастерские художественной печати." },
  { room: "ПР-201", campus: "pryan", title: "Деканат Института графики и искусства книги", floor: "2 этаж", building: "ул. Прянишникова, 2А", desc: "Учебная часть, оформление справок, кураторы творческих направлений: книжный дизайн, иллюстрация, анимация.", route: "2 этаж, напротив центрального лестничного холла." },
  { room: "ПР-304", campus: "pryan", title: "Поточная аудитория медиаиндустрии и рекламы", floor: "3 этаж", building: "ул. Прянишникова, 2А", desc: "Мультимедийная лекционная аудитория издательского дела, журналистики и рекламы.", route: "3 этаж главного корпуса, центральная галерея." },
  { room: "ПР-Буфет", campus: "pryan", title: "Студенческий буфет и арт-коворкинг", floor: "1 этаж", building: "ул. Прянишникова, 2А", desc: "Зона отдыха и перекусов студентов творческих специальностей, кофе, сэндвичи, столы для эскизирования.", route: "1 этаж, рядом с гардеробом." },

  // ПАВЛА КОРЧАГИНА, 22 (ХИМИКО-ТЕХНОЛОГИЧЕСКИЙ ФАКУЛЬТЕТ)
  { room: "ПК-210", campus: "korch", title: "Лаборатория аналитической и органической химии", floor: "2 этаж", building: "ул. Павла Корчагина, 22", desc: "Институт химической технологии и биотехнологий: вытяжные шкафы, спектрофотометры, синтез органических соединений.", route: "Центральный вход, 2 этаж, левое лабораторное крыло." },
  { room: "ПК-114", campus: "korch", title: "Лаборатория композиционных и полимерных материалов", floor: "1 этаж", building: "Лабораторный корпус", desc: "Оборудование для формования углепластиков, экструдеры, гидравлические прессы и разрывные испытательные машины.", route: "1 этаж, крытый переход в лабораторный корпус." },
  { room: "ПК-301", campus: "korch", title: "Деканат Факультета химтехнологий и биотехнологий", floor: "3 этаж", building: "ул. Павла Корчагина, 22", desc: "Студенческий офис химических и биотехнологических профилей, заявления, консультации по стипендиям.", route: "3 этаж главного корпуса, направо от центральной лестницы." },
  { room: "ПК-Актовый", campus: "korch", title: "Исторический актовый зал кампуса Корчагина", floor: "2 этаж", building: "ул. Павла Корчагина, 22", desc: "Торжественные мероприятия, студенческие научные конференции, ректорские награждения и концерты.", route: "2 этаж, центральный парадный холл." },

  // МИХАЛКОВСКАЯ, 7 (ИНСТИТУТ ТЕКСТИЛЯ И МОДЫ)
  { room: "МХ-105", campus: "mikh", title: "Швейная лаборатория и дизайн-мастерская моды", floor: "1 этаж", building: "ул. Михалковская, 7", desc: "Промышленные прямострочные швейные машины Juki, оверлоки, манекены всех типоразмеров и раскройные столы.", route: "1 этаж, правое крыло здания." },
  { room: "МХ-204", campus: "mikh", title: "Деканат Факультета дизайна и моды", floor: "2 этаж", building: "ул. Михалковская, 7", desc: "Учебный отдел текстильных специальностей, конструирования изделий лёгкой промышленности и моды.", route: "2 этаж, налево по коридору, кабинет 204." },
  { room: "МХ-302", campus: "mikh", title: "Компьютерный класс САПР Грация и Clo3D", floor: "3 этаж", building: "ул. Михалковская, 7", desc: "Параметрическое цифровое моделирование лекал, виртуальная примерка одежды на 3D-аватарах.", route: "3 этаж, аудитория 302." }
];

function setNavCampus(campKey) {
  selectedNavCampus = campKey;
  playRetroSound("click");
  renderNavigatorTab(document.getElementById("mainContentArea"));
}

function renderNavigatorTab(container) {
  const inputEl = document.getElementById("roomSearchInput");
  const q = (inputEl ? inputEl.value : "").trim().toLowerCase();

  let filtered = ROOMS_DB.filter(r => {
    const matchesCampus = selectedNavCampus === "all" || r.campus === selectedNavCampus;
    const matchesQuery = !q || r.room.toLowerCase().includes(q) || r.title.toLowerCase().includes(q) || r.desc.toLowerCase().includes(q) || r.building.toLowerCase().includes(q);
    return matchesCampus && matchesQuery;
  });

  container.innerHTML = `
    <div style="margin-bottom:14px;">
      <h2>🗺️ Интерактивный навигатор по кампусам и аудиториям</h2>
      <div style="color:#666;">Быстрый поиск аудиторий, деканатов, коворкингов и столовых:</div>
    </div>

    <!-- Переключатель кампусов -->
    <div class="nav-campus-tabs">
      <button class="nav-campus-btn ${selectedNavCampus==='sem'?'active':''}" onclick="setNavCampus('sem')">🏢 Б. Семёновская, 38 (Главный)</button>
      <button class="nav-campus-btn ${selectedNavCampus==='avto'?'active':''}" onclick="setNavCampus('avto')">🏎️ Автозаводская, 16</button>
      <button class="nav-campus-btn ${selectedNavCampus==='pryan'?'active':''}" onclick="setNavCampus('pryan')">🎨 Прянишникова, 2А</button>
      <button class="nav-campus-btn ${selectedNavCampus==='korch'?'active':''}" onclick="setNavCampus('korch')">🔬 Павла Корчагина, 22</button>
      <button class="nav-campus-btn ${selectedNavCampus==='mikh'?'active':''}" onclick="setNavCampus('mikh')">🧵 Михалковская, 7</button>
      <button class="nav-campus-btn ${selectedNavCampus==='all'?'active':''}" onclick="setNavCampus('all')">🌐 Все корпуса</button>
    </div>

    <!-- Поисковая строка -->
    <div style="display:flex; gap:8px; margin-bottom:14px;">
      <div style="flex:1; position:relative;">
        <input type="text" id="roomSearchInput" value="${q}" placeholder="Введите номер аудитории (напр. А-101, В-202, Б-305, Н-401, столовая, коворкинг)..." style="width:100%; padding:8px 12px; font-size:12px; border:2px solid var(--border-dark); border-radius:var(--border-radius); outline:none;" oninput="renderNavigatorTab(document.getElementById('mainContentArea'))">
      </div>
    </div>

    <!-- Список найденных аудиторий -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:12px;">
      ${filtered.length > 0 ? filtered.map(r => `
        <div class="room-result-card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <span class="room-badge">${r.room}</span>
              <h4 class="room-card-title">${r.title}</h4>
              <div class="room-card-meta">📍 ${r.building} · ${r.floor}</div>
            </div>
            <span style="font-size:20px;">🚪</span>
          </div>

          <p class="room-card-desc">${r.desc}</p>

          <div class="room-card-route">
            <b>🚶 Как пройти:</b> ${r.route}
          </div>
        </div>
      `).join('') : '<div style="grid-column: 1 / -1; padding:20px; text-align:center; color:#888;">Аудитория не найдена. Попробуйте изменить запрос или выбрать «Все корпуса».</div>'}
    </div>
  `;
}

initSidebarFaq();
switchTab("schedule");
initDraggableFab();
initDraggableChatWindow();
initResizableChatWindow();
</script>
</body>
</html>
'''

# Отображение через Streamlit Components
components.html(HTML_FRONTEND, height=980, scrolling=True)
