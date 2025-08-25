"""API роутеры для LeetCode Progress Tracker."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import subprocess
import sys

from modules.data_processor import load_and_process_data
from modules.chart_creator import (
    create_progress_plot_data, create_total_plot_data,
    create_difficulty_breakdown_data, create_daily_progress_data,
    create_difficulty_total_data, create_difficulty_progress_data,
    create_weekly_heatmap_data, create_progress_plot, create_total_plot
)
from config import USERNAMES

# Создаем роутер для API
api_router = APIRouter(prefix="/api")

# Роутер для статических графиков (PNG)
plot_router = APIRouter(prefix="/plot")


@api_router.get("/plot/progress")
async def get_progress_plot_data():
    """Возвращает данные для интерактивного графика прогресса."""
    try:
        data_dict = load_and_process_data()
        if data_dict['progress_total'].empty:
            raise HTTPException(status_code=404, detail="Нет данных для построения графика прогресса")
        
        chart_config = create_progress_plot_data(data_dict['progress_total'])
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания графика прогресса: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/total")
async def get_total_plot_data():
    """Возвращает данные для интерактивного графика общего количества."""
    try:
        data_dict = load_and_process_data()
        if data_dict['total'].empty:
            raise HTTPException(status_code=404, detail="Нет данных для построения графика общего количества")
        
        chart_config = create_total_plot_data(data_dict['total'])
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания графика общего количества: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/difficulty-breakdown")
async def get_difficulty_breakdown_plot_data():
    """Возвращает данные для графика распределения по уровням сложности."""
    try:
        data_dict = load_and_process_data()
        if data_dict['easy'].empty or data_dict['medium'].empty or data_dict['hard'].empty:
            raise HTTPException(status_code=404, detail="Данные о сложности недоступны. Обновите данные для получения детальной статистики.")
        
        chart_config = create_difficulty_breakdown_data(data_dict['easy'], data_dict['medium'], data_dict['hard'])
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания графика по сложности: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/daily-progress")
async def get_daily_progress_plot_data():
    """Возвращает данные для графика прогресса по дням."""
    try:
        data_dict = load_and_process_data()
        if data_dict['total'].empty:
            raise HTTPException(status_code=404, detail="Нет данных для построения дневного графика")
        
        chart_config = create_daily_progress_data(data_dict)
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания дневного графика: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/difficulty-total")
async def get_difficulty_total_plot_data():
    """Возвращает данные для графика общего количества задач по уровням сложности."""
    try:
        data_dict = load_and_process_data()
        if data_dict['easy'].empty or data_dict['medium'].empty or data_dict['hard'].empty:
            raise HTTPException(status_code=404, detail="Данные о сложности недоступны. Обновите данные для получения детальной статистики.")
        
        chart_config = create_difficulty_total_data(data_dict['easy'], data_dict['medium'], data_dict['hard'])
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания графика общего количества по сложности: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/difficulty-progress")
async def get_difficulty_progress_plot_data():
    """Возвращает данные для графика прогресса по уровням сложности."""
    try:
        data_dict = load_and_process_data()
        if data_dict['progress_easy'].empty or data_dict['progress_medium'].empty or data_dict['progress_hard'].empty:
            raise HTTPException(status_code=404, detail="Данные о сложности недоступны. Обновите данные для получения детальной статистики.")
        
        chart_config = create_difficulty_progress_data(data_dict['progress_easy'], data_dict['progress_medium'], data_dict['progress_hard'])
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания графика прогресса по сложности: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.get("/plot/weekly-heatmap")
async def get_weekly_heatmap_plot_data():
    """Возвращает данные для тепловой карты активности."""
    try:
        data_dict = load_and_process_data()
        if data_dict['total'].empty:
            raise HTTPException(status_code=404, detail="Нет данных для построения тепловой карты")
        
        chart_config = create_weekly_heatmap_data(data_dict)
        
        return JSONResponse(content=chart_config)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка создания тепловой карты: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@api_router.post("/update")
async def update_data():
    """API endpoint для обновления данных."""
    try:
        # Запускаем скрипт data_collector.py
        result = subprocess.run([sys.executable, "data_collector.py"], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Данные успешно обновлены",
                "output": result.stdout
            }
        else:
            return {
                "success": False,
                "message": "Ошибка при обновлении данных",
                "error": result.stderr
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Ошибка выполнения скрипта: {str(e)}"
        }


@api_router.get("/stats")
async def get_stats():
    """API endpoint для получения статистики в JSON формате."""
    try:
        data_dict = load_and_process_data()
        
        stats = {}
        for username in USERNAMES:
            if username in data_dict['total'].columns:
                latest_total = data_dict['total'][username].dropna().iloc[-1] if not data_dict['total'][username].dropna().empty else 0
                latest_progress = data_dict['progress_total'][username].dropna().iloc[-1] if not data_dict['progress_total'][username].dropna().empty else 0
                
                user_stats = {
                    'total_solved': int(latest_total),
                    'progress_from_start': int(latest_progress)
                }
                
                # Добавляем детализацию по сложности, если доступна
                latest_easy = data_dict['easy'][username].dropna().iloc[-1] if not data_dict['easy'].empty and username in data_dict['easy'].columns and not data_dict['easy'][username].dropna().empty else 0
                latest_medium = data_dict['medium'][username].dropna().iloc[-1] if not data_dict['medium'].empty and username in data_dict['medium'].columns and not data_dict['medium'][username].dropna().empty else 0
                latest_hard = data_dict['hard'][username].dropna().iloc[-1] if not data_dict['hard'].empty and username in data_dict['hard'].columns and not data_dict['hard'][username].dropna().empty else 0
                
                user_stats.update({
                    'easy_solved': int(latest_easy),
                    'medium_solved': int(latest_medium),
                    'hard_solved': int(latest_hard)
                })
                
                stats[username] = user_stats
            else:
                base_stats = {
                    'total_solved': 0,
                    'progress_from_start': 0,
                    'easy_solved': 0,
                    'medium_solved': 0,
                    'hard_solved': 0
                }
                
                stats[username] = base_stats
        
        # Последнее обновление
        if not data_dict['total'].empty:
            last_update = data_dict['total'].index[-1].isoformat()
        else:
            last_update = None
            
        return {
            'stats': stats,
            'last_update': last_update,
            'total_users': len(USERNAMES),
            'has_difficulty_data': not data_dict['easy'].empty or not data_dict['medium'].empty or not data_dict['hard'].empty
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


@plot_router.get("/progress")
async def get_progress_plot():
    """Возвращает график прогресса в формате PNG."""
    try:
        data_dict = load_and_process_data()
        img = create_progress_plot(data_dict['progress_total'])
        return StreamingResponse(img, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")


@plot_router.get("/total")
async def get_total_plot():
    """Возвращает график общего количества решенных задач в формате PNG."""
    try:
        data_dict = load_and_process_data()
        img = create_total_plot(data_dict['total'])
        return StreamingResponse(img, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания графика: {str(e)}")
