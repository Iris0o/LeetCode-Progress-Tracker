"""Веб-страницы для LeetCode Progress Tracker."""

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.data_processor import load_and_process_data
from config import USERNAMES

templates = Jinja2Templates(directory="templates")

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
                latest_total = data_dict['total'][username].dropna().iloc[-1] if not data_dict['total'][username].dropna().empty else 0
                latest_progress = data_dict['progress_total'][username].dropna().iloc[-1] if not data_dict['progress_total'][username].dropna().empty else 0
                
                # Детальная статистика по сложности, если доступна
                if data_dict['has_difficulty_data']:
                    latest_easy = data_dict['easy'][username].dropna().iloc[-1] if not data_dict['easy'][username].dropna().empty else 0
                    latest_medium = data_dict['medium'][username].dropna().iloc[-1] if not data_dict['medium'][username].dropna().empty else 0
                    latest_hard = data_dict['hard'][username].dropna().iloc[-1] if not data_dict['hard'][username].dropna().empty else 0
                else:
                    latest_easy = latest_medium = latest_hard = 0
                
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
        if data_dict['has_difficulty_data']:
            for stat in stats:
                easy_progress = 0
                medium_progress = 0
                hard_progress = 0
                
                if stat['username'] in data_dict['progress_easy'].columns:
                    easy_progress = int(data_dict['progress_easy'][stat['username']].dropna().iloc[-1]) if not data_dict['progress_easy'][stat['username']].dropna().empty else 0
                if stat['username'] in data_dict['progress_medium'].columns:
                    medium_progress = int(data_dict['progress_medium'][stat['username']].dropna().iloc[-1]) if not data_dict['progress_medium'][stat['username']].dropna().empty else 0
                if stat['username'] in data_dict['progress_hard'].columns:
                    hard_progress = int(data_dict['progress_hard'][stat['username']].dropna().iloc[-1]) if not data_dict['progress_hard'][stat['username']].dropna().empty else 0
                
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
            "has_difficulty_data": data_dict['has_difficulty_data']
        })
        
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"Произошла ошибка при загрузке данных: {str(e)}",
            "suggestion": "Убедитесь, что скрипт обновления данных был запущен хотя бы один раз."
        })
