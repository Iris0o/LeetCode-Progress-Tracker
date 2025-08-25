# 📊 LeetCode Progress Tracker

<div align="center">

![LeetCode Progress Tracker](images/1.png)

[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](README_en.md)
[![Русский](https://img.shields.io/badge/README-%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-red?style=for-the-badge)](README_ru.md)

</div>

> Система для отслеживания прогресса решения задач на LeetCode с красивым веб-интерфейсом и графиками.

## ✨ Особенности

- 📈 Интерактивные графики прогресса
- 👥 Сравнение нескольких пользователей
- 🎯 Отслеживание по уровням сложности (Easy, Medium, Hard)
- 🔄 Автоматическое обновление данных
- 🌐 Современный веб-интерфейс
- 📱 Адаптивный дизайн
- 🌍 Поддержка нескольких языков (Русский/English)

## Компоненты

### 1. Скрипт сбора данных (`data_collector.py`)
Собирает статистику пользователей LeetCode и сохраняет в CSV файл.

### 2. Веб-приложение (`app.py`)
FastAPI приложение для отображения графиков и статистики.

### 3. Конфигурация (`config.py`)
Настройки для обоих компонентов.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка пользователей

Отредактируйте `config.py` и укажите нужных пользователей LeetCode:

```python
USERNAMES = ["your_username", "friend_username"]
```

### 3. Сбор данных

```bash
python data_collector.py
```

💡 **Совет**: Настройте автоматический запуск для регулярного обновления данных.

### 4. Запуск веб-приложения

```bash
python app.py
```

Или используя uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

🌐 Откройте браузер: http://localhost:8000

## 📋 API Endpoints

| Endpoint | Описание |
|----------|----------|
| `GET /` | Главная страница с графиками |
| `GET /plot/progress` | График прогресса (PNG) |
| `GET /plot/total` | График общего количества (PNG) |
| `GET /api/stats` | Статистика в JSON |

## ⚙️ Настройка конфигурации

В файле `config.py` настройте основные параметры:

```python
# Пользователи LeetCode для отслеживания
USERNAMES = ["your_username", "friend_username"]

# Файлы данных
CSV_FILE = "leetcode_progress.csv"

# Настройки запросов
REQUEST_TIMEOUT = 10  # Таймаут в секундах
```

## 🔄 Автоматизация

Для автоматического обновления данных настройте запуск `data_collector.py`:

### Windows (Task Scheduler)
1. Откройте Task Scheduler
2. Создайте новую задачу
3. Установите расписание (например, каждый час)
4. Укажите команду: `python "path\to\your\data_collector.py"`

### Linux/macOS (cron)
```bash
# Добавить в crontab для запуска каждый час
0 * * * * cd /path/to/project && python data_collector.py
```

## 📁 Структура проекта

```
leetcode-graph/
├── 📄 app.py                        # Веб-приложение FastAPI
├── 📊 data_collector.py             # Скрипт сбора данных
├── ⚙️ config.py                     # Конфигурация
├── 📋 requirements.txt              # Python зависимости
├── � pyproject.toml                # Метаданные проекта
├── �📈 leetcode_progress.csv         # Данные (автоматически)
├── 📂 modules/                      # Модули приложения
│   ├── __init__.py
│   ├── api_routes.py               # API маршруты
│   ├── chart_creator.py            # Создание графиков
│   ├── data_processor.py           # Обработка данных
│   ├── i18n.py                     # Интернационализация
│   ├── utils.py                    # Утилиты
│   └── web_views.py                # Веб-представления
├── 📂 static/                       # Статические файлы
│   ├── css/style.css               # Стили
│   └── js/app.js                   # JavaScript
├── 📂 templates/                    # HTML шаблоны
│   ├── index.html                  # Главная страница
│   └── error.html                  # Страница ошибки
├── 📂 locales/                      # Переводы
│   ├── en.json                     # Английские переводы
│   └── ru.json                     # Русские переводы
└── 📂 images/                       # Изображения
    └── 1.png                       # Скриншоты
```

## 🌍 Поддержка языков

Приложение поддерживает несколько языков:

- **Русский** - Язык по умолчанию
- **English** - Английский язык

Файлы переводов находятся в директории `locales/`. Вы можете легко добавить больше языков, создав новые JSON файлы по той же структуре.

## ⚙️ Настройка конфигурации

В файле `config.py` настройте основные параметры:

```python
# Пользователи LeetCode для отслеживания
USERNAMES = ["your_username", "friend_username"]

# Файлы данных
CSV_FILE = "leetcode_progress.csv"

# Настройки запросов
REQUEST_TIMEOUT = 10  # Таймаут в секундах
```

## API Endpoints

- `GET /` - Главная страница с графиками
- `GET /plot/progress` - График прогресса (PNG)
- `GET /plot/total` - График общего количества (PNG)
- `GET /api/stats` - Статистика в JSON формате

## ❗ Решение проблем

### Пользователь не найден
Убедитесь, что имена пользователей в `config.py` указаны правильно и соответствуют профилям на LeetCode.

### Файл с данными не найден  
Запустите `data_collector.py` хотя бы один раз для создания файла с данными.

### Проблемы с графиками
Убедитесь, что установлены все зависимости из `requirements.txt`.

---

## 📝 Лицензия

MIT License

## 🤝 Вклад в проект

Приветствуются Pull Request'ы и Issues! Не стесняйтесь предлагать улучшения.

### Руководство для разработчиков
1. Сделайте форк репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Добавить потрясающую функцию'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Стиль кода
- Следуйте PEP 8 для Python кода
- Используйте осмысленные имена переменных и функций
- Добавляйте docstring для функций и классов
- Пишите тесты для новых функций

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.

## 🙏 Благодарности

- Спасибо LeetCode за предоставление платформы и API
- FastAPI за отличный веб-фреймворк
- Matplotlib за возможности создания графиков
- Всем участникам, которые помогли улучшить этот проект

## ⭐ Поддержка

Если проект оказался полезным, поставьте звездочку! ⭐

## 📞 Контакты

- GitHub: [@Iris0o](https://github.com/Iris0o)
- Ссылка на проект: [https://github.com/Iris0o/LeetCode-Progress-Tracker](https://github.com/Iris0o/LeetCode-Progress-Tracker)

---

<div align="center">
Сделано с ❤️ сообществом
</div>
