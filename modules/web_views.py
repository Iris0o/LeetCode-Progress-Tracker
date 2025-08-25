"""Веб-страницы для LeetCode Progress Tracker."""

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.data_processor import load_and_process_data
from config import USERNAMES

templates = Jinja2Templates(directory="templates")


def get_latest_value(dataframe, username):
    """Получить последнее значение для пользователя из DataFrame."""
    if (dataframe.empty or 
        username not in dataframe.columns or 
        dataframe[username].dropna().empty):
        return 0
    return dataframe[username].dropna().iloc[-1]

# Создаем роутер для веб-страниц
web_router = APIRouter()


@web_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница с графиками."""
    try:
        data_dict = load_and_process_data()
        
        # Получаем статистику
        stats = []
        for username in USERNAMES:
            if username in data_dict['total'].columns:
                latest_total = get_latest_value(data_dict['total'], username)
                latest_progress = get_latest_value(data_dict['progress_total'], username)
                
                # Детальная статистика по сложности, если доступна
                latest_easy = get_latest_value(data_dict['easy'], username)
                latest_medium = get_latest_value(data_dict['medium'], username)
                latest_hard = get_latest_value(data_dict['hard'], username)
                
                stats.append({
                    'username': username,
                    'total': int(latest_total),
                    'progress': int(latest_progress),
                    'easy': int(latest_easy),
                    'medium': int(latest_medium),
                    'hard': int(latest_hard)
                })
            else:
                stats.append({
                    'username': username,
                    'total': 0,
                    'progress': 0,
                    'easy': 0,
                    'medium': 0,
                    'hard': 0
                })
        
        # Добавляем прогресс по сложности в статистику
        for stat in stats:
            easy_progress = int(get_latest_value(data_dict['progress_easy'], stat['username']))
            medium_progress = int(get_latest_value(data_dict['progress_medium'], stat['username']))
            hard_progress = int(get_latest_value(data_dict['progress_hard'], stat['username']))
            
            stat['easy_progress'] = easy_progress
            stat['medium_progress'] = medium_progress
            stat['hard_progress'] = hard_progress

        # Последнее обновление
        if not data_dict['total'].empty:
            last_update = data_dict['total'].index[-1].strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_update = "Нет данных"
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "stats": stats,
            "last_update": last_update,
            "has_difficulty_data": (not data_dict['easy'].empty or 
                                  not data_dict['medium'].empty or 
                                  not data_dict['hard'].empty)
        })
        
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"Произошла ошибка при загрузке данных: {str(e)}",
            "suggestion": "Убедитесь, что скрипт обновления данных был запущен хотя бы один раз."
        })
