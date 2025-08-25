"""Модуль для загрузки и обработки данных LeetCode."""

import pandas as pd
import os
from fastapi import HTTPException
from config import CSV_FILE


def load_and_process_data():
    """Загружает данные, преобразует их и вычисляет прогресс."""
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="Файл с данными не найден. Запустите скрипт обновления данных.")

    try:
        # Загружаем все данные
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            raise HTTPException(status_code=404, detail="Файл с данными пуст.")
            
        # Преобразуем строку с timestamp в объект datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Проверяем, есть ли новые колонки (детализация по сложности)
        has_difficulty_columns = all(col in df.columns for col in ['easy_solved', 'medium_solved', 'hard_solved'])
        
        if has_difficulty_columns:
            # Новый формат с детализацией
            # Преобразуем в широкий формат для каждого типа метрик
            df_total = df.pivot_table(index='timestamp', columns='username', values='total_solved')
            df_easy = df.pivot_table(index='timestamp', columns='username', values='easy_solved')
            df_medium = df.pivot_table(index='timestamp', columns='username', values='medium_solved')
            df_hard = df.pivot_table(index='timestamp', columns='username', values='hard_solved')
        else:
            # Старый формат - только общее количество
            df_total = df.pivot_table(index='timestamp', columns='username', values='total_solved')
            df_easy = pd.DataFrame()
            df_medium = pd.DataFrame()
            df_hard = pd.DataFrame()
        
        if df_total.empty:
            raise HTTPException(status_code=404, detail="Нет данных для обработки.")
        
        # Вычисляем прогресс относительно первого замера для каждого пользователя
        def calculate_progress(col):
            if col.dropna().empty:
                return col
            first_value = col.loc[col.first_valid_index()]
            return (col - first_value).astype('float64')
        
        df_progress_total = df_total.apply(calculate_progress, axis=0)
        
        # Прогресс для каждого уровня сложности
        if has_difficulty_columns:
            df_progress_easy = df_easy.apply(calculate_progress, axis=0)
            df_progress_medium = df_medium.apply(calculate_progress, axis=0)
            df_progress_hard = df_hard.apply(calculate_progress, axis=0)
        else:
            df_progress_easy = pd.DataFrame()
            df_progress_medium = pd.DataFrame()
            df_progress_hard = pd.DataFrame()
        
        # Приводим все к float64
        df_total = df_total.astype('float64')
        if has_difficulty_columns:
            df_easy = df_easy.astype('float64')
            df_medium = df_medium.astype('float64')
            df_hard = df_hard.astype('float64')
        
        return {
            'progress_total': df_progress_total,
            'total': df_total,
            'easy': df_easy,
            'medium': df_medium,
            'hard': df_hard,
            'progress_easy': df_progress_easy,
            'progress_medium': df_progress_medium,
            'progress_hard': df_progress_hard,
            'has_difficulty_data': has_difficulty_columns
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка при обработке данных: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка обработки данных: {str(e)}")
