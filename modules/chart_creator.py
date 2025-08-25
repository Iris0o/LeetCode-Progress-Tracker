"""Модуль для создания интерактивных графиков с помощью ApexCharts.js."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from datetime import datetime
from config import FIGURE_SIZE, PLOT_STYLE, MARKER_SIZE, TITLE_FONT_SIZE, AXIS_FONT_SIZE, LEGEND_FONT_SIZE


def create_progress_plot_data(df):
    """Создает конфигурацию для интерактивного графика прогресса с ApexCharts."""
    series = []

    for username in df.columns:
        # Убираем NaN значения для корректного отображения
        clean_data = df[username].dropna()
        if not clean_data.empty:
            # Подготавливаем данные для ApexCharts
            data_points = []
            for timestamp, value in clean_data.items():
                data_points.append({
                    # Timestamp в миллисекундах
                    'x': int(timestamp.timestamp() * 1000),
                    'y': float(value)
                })

            series.append({
                'name': str(username),
                'data': data_points
            })

    # Конфигурация для ApexCharts
    chart_config = {
        'chart': {
            'type': 'line',
            'height': 500,
            'toolbar': {
                'show': True
            },
            'animations': {
                'enabled': True
            }
        },
        'series': series,
        'xaxis': {
            'type': 'datetime',
            'title': {
                'text': 'Дата и время'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Решено задач (относительно старта)'
            }
        },
        'title': {
            'text': 'Прогресс на LeetCode (с начала отслеживания)',
            'align': 'center'
        },
        'stroke': {
            'width': 2,
            'curve': 'smooth'
        },
        'markers': {
            'size': 4
        },
        'tooltip': {
            'x': {
                'format': 'dd/MM/yyyy HH:mm'
            }
        },
        'legend': {
            'position': 'top'
        }
    }

    return chart_config


def create_total_plot_data(df):
    """Создает конфигурацию для интерактивного графика общего количества задач с ApexCharts."""
    series = []

    for username in df.columns:
        # Убираем NaN значения для корректного отображения
        clean_data = df[username].dropna()
        if not clean_data.empty:
            # Подготавливаем данные для ApexCharts
            data_points = []
            for timestamp, value in clean_data.items():
                data_points.append({
                    # Timestamp в миллисекундах
                    'x': int(timestamp.timestamp() * 1000),
                    'y': float(value)
                })

            series.append({
                'name': str(username),
                'data': data_points
            })

    # Конфигурация для ApexCharts
    chart_config = {
        'chart': {
            'type': 'line',
            'height': 500,
            'toolbar': {
                'show': True
            },
            'animations': {
                'enabled': True
            }
        },
        'series': series,
        'xaxis': {
            'type': 'datetime',
            'title': {
                'text': 'Дата и время'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Общее количество решенных задач'
            }
        },
        'title': {
            'text': 'Общее количество решенных задач на LeetCode',
            'align': 'center'
        },
        'stroke': {
            'width': 2,
            'curve': 'smooth'
        },
        'markers': {
            'size': 4
        },
        'tooltip': {
            'x': {
                'format': 'dd/MM/yyyy HH:mm'
            }
        },
        'legend': {
            'position': 'top'
        }
    }

    return chart_config


def create_difficulty_breakdown_data(df_easy, df_medium, df_hard):
    """Создает конфигурацию для интерактивного графика распределения задач по уровням сложности."""
    categories = []
    easy_data = []
    medium_data = []
    hard_data = []

    for username in df_easy.columns:
        if username in df_medium.columns and username in df_hard.columns:
            categories.append(str(username))

            # Данные для последнего замера
            latest_easy = df_easy[username].dropna(
            ).iloc[-1] if not df_easy[username].dropna().empty else 0
            latest_medium = df_medium[username].dropna(
            ).iloc[-1] if not df_medium[username].dropna().empty else 0
            latest_hard = df_hard[username].dropna(
            ).iloc[-1] if not df_hard[username].dropna().empty else 0

            easy_data.append(float(latest_easy))
            medium_data.append(float(latest_medium))
            hard_data.append(float(latest_hard))

    # Конфигурация для ApexCharts
    chart_config = {
        'chart': {
            'type': 'bar',
            'height': 500,
            'stacked': True,
            'toolbar': {
                'show': True
            }
        },
        'series': [
            {
                'name': 'Easy',
                'data': easy_data,
                'color': '#4CAF50'
            },
            {
                'name': 'Medium',
                'data': medium_data,
                'color': '#FF9800'
            },
            {
                'name': 'Hard',
                'data': hard_data,
                'color': '#F44336'
            }
        ],
        'xaxis': {
            'categories': categories,
            'title': {
                'text': 'Пользователи'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Количество задач'
            }
        },
        'title': {
            'text': 'Распределение решенных задач по уровням сложности',
            'align': 'center'
        },
        'legend': {
            'position': 'top'
        },
        'plotOptions': {
            'bar': {
                'horizontal': False
            }
        }
    }

    return chart_config


def create_daily_progress_data(data_dict):
    """Создает конфигурацию для графика прогресса с группировкой по дням."""
    df_total = data_dict['total']

    if df_total.empty:
        return {'series': [], 'chart': {'type': 'line'}}

    # Группируем по дням
    df_daily = df_total.groupby(df_total.index.date).last()
    df_daily.index = pd.to_datetime(df_daily.index)

    series = []

    for username in df_daily.columns:
        clean_data = df_daily[username].dropna()
        if not clean_data.empty:
            data_points = []
            for timestamp, value in clean_data.items():
                data_points.append({
                    'x': int(timestamp.timestamp() * 1000),
                    'y': float(value)
                })

            series.append({
                'name': str(username),
                'data': data_points
            })

    chart_config = {
        'chart': {
            'type': 'line',
            'height': 500,
            'toolbar': {
                'show': True
            }
        },
        'series': series,
        'xaxis': {
            'type': 'datetime',
            'title': {
                'text': 'Дата'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Общее количество решенных задач'
            }
        },
        'title': {
            'text': 'Прогресс по дням',
            'align': 'center'
        },
        'stroke': {
            'width': 2,
            'curve': 'smooth'
        },
        'markers': {
            'size': 6
        },
        'tooltip': {
            'x': {
                'format': 'dd/MM/yyyy'
            }
        },
        'legend': {
            'position': 'top'
        }
    }

    return chart_config


def create_difficulty_total_data(df_easy, df_medium, df_hard):
    """Создает конфигурацию для графика общего количества задач по каждому уровню сложности."""
    series = []

    colors = {
        'easy': '#4CAF50',
        'medium': '#FF9800',
        'hard': '#F44336'
    }

    # Добавляем данные для каждого уровня сложности
    difficulty_data = [
        (df_easy, 'Easy', colors['easy']),
        (df_medium, 'Medium', colors['medium']),
        (df_hard, 'Hard', colors['hard'])
    ]

    for df, level, color in difficulty_data:
        if not df.empty:
            for username in df.columns:
                clean_data = df[username].dropna()
                if not clean_data.empty:
                    data_points = []
                    for timestamp, value in clean_data.items():
                        data_points.append({
                            'x': int(timestamp.timestamp() * 1000),
                            'y': float(value)
                        })

                    series.append({
                        'name': f'{username} ({level})',
                        'data': data_points,
                        'color': color
                    })

    chart_config = {
        'chart': {
            'type': 'line',
            'height': 600,
            'toolbar': {
                'show': True
            }
        },
        'series': series,
        'xaxis': {
            'type': 'datetime',
            'title': {
                'text': 'Дата и время'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Общее количество решенных задач'
            }
        },
        'title': {
            'text': 'Общее количество задач по уровням сложности',
            'align': 'center'
        },
        'stroke': {
            'width': 2,
            'curve': 'smooth'
        },
        'markers': {
            'size': 4
        },
        'tooltip': {
            'x': {
                'format': 'dd/MM/yyyy HH:mm'
            }
        },
        'legend': {
            'position': 'top',
            'onItemClick': {
                'toggleDataSeries': False
            }
        }
    }

    return chart_config


def create_difficulty_progress_data(
        df_progress_easy, df_progress_medium, df_progress_hard):
    """Создает конфигурацию для графика прогресса по каждому уровню сложности."""
    series = []

    colors = {
        'easy': '#4CAF50',
        'medium': '#FF9800',
        'hard': '#F44336'
    }

    # Добавляем данные для каждого уровня сложности
    difficulty_data = [
        (df_progress_easy, 'Easy', colors['easy']),
        (df_progress_medium, 'Medium', colors['medium']),
        (df_progress_hard, 'Hard', colors['hard'])
    ]

    for df, level, color in difficulty_data:
        if not df.empty:
            for username in df.columns:
                clean_data = df[username].dropna()
                if not clean_data.empty:
                    data_points = []
                    for timestamp, value in clean_data.items():
                        data_points.append({
                            'x': int(timestamp.timestamp() * 1000),
                            'y': float(value)
                        })

                    series.append({
                        'name': f'{username} ({level})',
                        'data': data_points,
                        'color': color
                    })

    chart_config = {
        'chart': {
            'type': 'line',
            'height': 600,
            'toolbar': {
                'show': True
            }
        },
        'series': series,
        'xaxis': {
            'type': 'datetime',
            'title': {
                'text': 'Дата и время'
            }
        },
        'yaxis': {
            'title': {
                'text': 'Прогресс решенных задач (относительно старта)'
            }
        },
        'title': {
            'text': 'Прогресс по уровням сложности (с начала отслеживания)',
            'align': 'center'
        },
        'stroke': {
            'width': 2,
            'curve': 'smooth'
        },
        'markers': {
            'size': 4
        },
        'tooltip': {
            'x': {
                'format': 'dd/MM/yyyy HH:mm'
            }
        },
        'legend': {
            'position': 'top',
            'onItemClick': {
                'toggleDataSeries': False
            }
        }
    }

    return chart_config


def create_weekly_heatmap_data(data_dict):
    """Создает конфигурацию для тепловой карты активности по дням недели и часам."""
    df_total = data_dict['total']

    if df_total.empty:
        return {'series': [], 'chart': {'type': 'heatmap'}}

    # Создаем DataFrame для всех пользователей с временными метками
    activity_data = []

    for username in df_total.columns:
        user_data = df_total[username].dropna()
        if not user_data.empty:
            # Вычисляем разности (активность)
            activity = user_data.diff().fillna(0)
            activity = activity[activity > 0]  # Только положительные изменения

            for timestamp, value in activity.items():
                activity_data.append({
                    'username': username,
                    'timestamp': timestamp,
                    'activity': value,
                    'hour': timestamp.hour,
                    'day_of_week': timestamp.strftime('%A'),
                    'weekday': timestamp.weekday()
                })

    if not activity_data:
        return {'series': [], 'chart': {'type': 'heatmap'}}

    activity_df = pd.DataFrame(activity_data)

    # Группируем по дням недели и часам
    heatmap_data = activity_df.groupby(['day_of_week', 'weekday', 'hour'])[
        'activity'].sum().reset_index()

    # Создаем серии данных для тепловой карты
    days_order = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday']
    series = []

    for day in days_order:
        day_data = []
        for hour in range(24):
            activity = heatmap_data[
                (heatmap_data['day_of_week'] == day) &
                (heatmap_data['hour'] == hour)
            ]['activity'].sum()
            day_data.append({
                'x': f'{hour}:00',
                'y': float(activity)
            })

        series.append({
            'name': day,
            'data': day_data
        })

    chart_config = {
        'chart': {
            'type': 'heatmap',
            'height': 400,
            'toolbar': {
                'show': True
            }
        },
        'series': series,
        'xaxis': {
            'title': {
                'text': 'Час дня'
            }
        },
        'yaxis': {
            'title': {
                'text': 'День недели'
            }
        },
        'title': {
            'text': 'Тепловая карта активности по дням недели и часам',
            'align': 'center'
        },
        'plotOptions': {
            'heatmap': {
                'shadeIntensity': 0.5,
                'colorScale': {
                    'ranges': [{
                        'from': 0,
                        'to': 5,
                        'name': 'низкая',
                        'color': '#FFF3E0'
                    }, {
                        'from': 6,
                        'to': 20,
                        'name': 'средняя',
                        'color': '#FF9800'
                    }, {
                        'from': 21,
                        'to': 50,
                        'name': 'высокая',
                        'color': '#F57C00'
                    }]
                }
            }
        }
    }

    return chart_config


def create_progress_plot(df):
    """Создает график прогресса и возвращает его в виде байтов."""
    plt.style.use(PLOT_STYLE)
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    for username in df.columns:
        ax.plot(
            df.index,
            df[username],
            marker='o',
            linestyle='-',
            markersize=MARKER_SIZE,
            label=username)

    ax.set_title(
        'Прогресс на LeetCode (с начала отслеживания)',
        fontsize=TITLE_FONT_SIZE,
        pad=20)
    ax.set_xlabel('Дата и время', fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel(
        'Решено задач (относительно старта)',
        fontsize=AXIS_FONT_SIZE)
    ax.legend(title='Участники', fontsize=LEGEND_FONT_SIZE)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Улучшенное форматирование оси X
    fig.autofmt_xdate(rotation=30, ha='right')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.tight_layout()

    # Сохраняем график в BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150)
    img.seek(0)
    plt.close()  # Важно закрыть фигуру для освобождения памяти

    return img


def create_total_plot(df):
    """Создает график общего количества решенных задач."""
    plt.style.use(PLOT_STYLE)
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    for username in df.columns:
        ax.plot(
            df.index,
            df[username],
            marker='o',
            linestyle='-',
            markersize=MARKER_SIZE,
            label=username)

    ax.set_title(
        'Общее количество решенных задач на LeetCode',
        fontsize=TITLE_FONT_SIZE,
        pad=20)
    ax.set_xlabel('Дата и время', fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel('Общее количество решенных задач', fontsize=AXIS_FONT_SIZE)
    ax.legend(title='Участники', fontsize=LEGEND_FONT_SIZE)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Улучшенное форматирование оси X
    fig.autofmt_xdate(rotation=30, ha='right')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.tight_layout()

    # Сохраняем график в BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150)
    img.seek(0)
    plt.close()

    return img
