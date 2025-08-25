// LeetCode Progress Tracker - ApexCharts Integration

// Конфигурация загрузки
const loadingConfig = {
    showLoading: false,         // Показывать индикатор загрузки (false = мгновенная загрузка)
    useSkeletonLoading: true,   // Использовать skeleton loading вместо спиннера
    preloadCharts: true,        // Предзагружать популярные графики
    fastSwitch: true            // Быстрое переключение между табами
};

// Карта соответствия endpoints и контейнеров для графиков
const chartEndpoints = {
    'progress': '/api/plot/progress',
    'total': '/api/plot/total',
    'daily': '/api/plot/daily-progress',
    'difficulty-breakdown': '/api/plot/difficulty-breakdown',
    'difficulty-total': '/api/plot/difficulty-total',
    'difficulty-progress': '/api/plot/difficulty-progress',
    'heatmap': '/api/plot/weekly-heatmap'
};

const chartContainers = {
    'progress': 'progressChart',
    'total': 'totalChart',
    'daily': 'dailyChart',
    'difficulty-breakdown': 'difficultyBreakdownChart',
    'difficulty-total': 'difficultyTotalChart',
    'difficulty-progress': 'difficultyProgressChart',
    'heatmap': 'heatmapChart'
};

// Кэш для хранения созданных диаграмм
let chartsCache = {};

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeTabs();
    initializeTooltips();
    
    // Загружаем первый график без задержки
    const activeTab = document.querySelector('.tab-btn.active');
    let initialChartType = 'progress'; // По умолчанию
    
    if (activeTab) {
        const chartType = activeTab.dataset.chart;
        console.log('Found active tab with chart type:', chartType);
        
        // Проверяем что такой тип графика существует
        if (chartEndpoints[chartType]) {
            initialChartType = chartType;
        } else {
            console.error('Chart type not found in endpoints:', chartType);
        }
    } else {
        console.log('No active tab found, using default progress chart');
    }
    
    // Показываем контейнер и загружаем график
    showChart(initialChartType);
    loadChart(initialChartType);
    
    // Предзагружаем следующие популярные графики в фоне с небольшой задержкой
    if (loadingConfig.preloadCharts) {
        setTimeout(() => {
            const preloadCharts = ['total', 'daily'];
            preloadCharts.forEach(type => {
                if (type !== initialChartType && chartEndpoints[type]) {
                    loadChart(type);
                }
            });
        }, 500);
    }
});

// Инициализация табов
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const chartType = this.dataset.chart;
            
            // Обновляем активные табы
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Показываем соответствующий контейнер графика
            showChart(chartType);
            
            // Загружаем график если не загружен (асинхронно, не блокируя UI)
            if (!chartsCache[chartType]) {
                loadChart(chartType);
            }
        });
    });
}

// Показать контейнер графика
function showChart(chartType) {
    const chartContainersElements = document.querySelectorAll('.chart');
    
    // Скрываем все контейнеры
    chartContainersElements.forEach(container => {
        container.classList.remove('active');
    });
    
    // Показываем нужный контейнер по составному ID (chartType + '-chart')
    const targetContainer = document.getElementById(chartType + '-chart');
    if (targetContainer) {
        targetContainer.classList.add('active');
        console.log(`Showing chart container: ${chartType}-chart`);
    } else {
        console.error(`Container ${chartType}-chart not found`);
    }
}

// Загрузка и отображение графика
async function loadChart(chartType) {
    const endpoint = chartEndpoints[chartType];
    const containerId = chartContainers[chartType];
    
    if (!endpoint || !containerId) {
        console.error(`Chart type ${chartType} not found`);
        return;
    }
    
    // Если график уже загружен, не загружаем повторно
    if (chartsCache[chartType]) {
        return chartsCache[chartType];
    }
    
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container ${containerId} not found`);
        return;
    }
    
    try {
        // Показываем индикатор загрузки в зависимости от настроек
        if (loadingConfig.showLoading) {
            if (loadingConfig.useSkeletonLoading) {
                container.innerHTML = `
                    <div class="chart-skeleton">
                        <div class="skeleton-header"></div>
                        <div class="skeleton-chart"></div>
                    </div>
                `;
            } else {
                container.innerHTML = '<div class="chart-loading"></div>';
            }
        }
        
        // Используем Promise.race для таймаута если нужно
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const chartConfig = await response.json();
        
        // Очищаем контейнер от индикатора загрузки
        container.innerHTML = '';
        
        // Создаем новый график
        const chart = new ApexCharts(container, chartConfig);
        await chart.render();
        
        // Сохраняем в кэш
        chartsCache[chartType] = chart;
        
        // Инициализируем кнопки управления для графиков уровней сложности
        if (chartType === 'difficulty-total' || chartType === 'difficulty-progress') {
            initializeDifficultyControls(chartType);
        }
        
        console.log(`Chart ${chartType} loaded successfully`);
    } catch (error) {
        console.error(`Error loading chart ${chartType}:`, error);
        container.innerHTML = `
            <div class="chart-error">
                ❌ Ошибка загрузки графика: ${error.message}
                <br>
                <button onclick="loadChart('${chartType}')" class="retry-btn">🔄 Попробовать снова</button>
            </div>
        `;
    }
}

// Инициализация всех графиков (предзагрузка)
function initializeCharts() {
    // Инициализируем только активные вкладки при первой загрузке
    console.log('Charts initialized');
}

// Инициализация тултипов
function initializeTooltips() {
    // Добавляем обработчики для тултипов если они есть
    const tooltipElements = document.querySelectorAll('[data-tooltip="true"]');
    tooltipElements.forEach(element => {
        const tooltipContent = element.querySelector('.tooltip-content');
        if (tooltipContent) {
            element.addEventListener('mouseenter', () => {
                tooltipContent.style.display = 'block';
            });
            element.addEventListener('mouseleave', () => {
                tooltipContent.style.display = 'none';
            });
        }
    });
    console.log('Tooltips initialized');
}

// Обновление данных
async function updateData() {
    const updateBtn = document.getElementById('updateBtn');
    const loading = document.getElementById('loading');
    const message = document.getElementById('message');
    
    // Показываем индикатор загрузки
    updateBtn.disabled = true;
    loading.style.display = 'block';
    message.innerHTML = '';
    
    try {
        const response = await fetch('/api/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            message.innerHTML = '<p class="success">✅ ' + result.message + '</p>';
            
            // Очищаем кэш и перезагружаем текущий график
            Object.keys(chartsCache).forEach(chartType => {
                if (chartsCache[chartType]) {
                    chartsCache[chartType].destroy();
                    delete chartsCache[chartType];
                }
            });
            
            // Перезагружаем страницу для обновления статистики
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            message.innerHTML = '<p class="error">❌ ' + result.message + '</p>';
            if (result.error) {
                console.error('Update error:', result.error);
            }
        }
    } catch (error) {
        console.error('Update request failed:', error);
        message.innerHTML = '<p class="error">❌ Ошибка сети: ' + error.message + '</p>';
    } finally {
        updateBtn.disabled = false;
        loading.style.display = 'none';
    }
}

// Функция для переключения видимости уровня сложности
function toggleDifficultyLevel(chartType, difficulty) {
    const chart = chartsCache[chartType];
    if (!chart) {
        console.error(`Chart ${chartType} not found in cache`);
        return;
    }
    
    const button = document.querySelector(`#${chartType}-chart .difficulty-btn[data-difficulty="${difficulty}"]`);
    if (!button) {
        console.error(`Button for difficulty ${difficulty} not found`);
        return;
    }
    
    const isActive = button.classList.contains('active');
    const difficultyLevel = difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
    
    // Получаем все серии данных для данного уровня сложности
    const seriesToToggle = chart.w.globals.seriesNames.filter(name => 
        name.includes(`(${difficultyLevel})`)
    );
    
    if (isActive) {
        // Скрываем линии данного уровня сложности
        seriesToToggle.forEach(seriesName => {
            chart.hideSeries(seriesName);
        });
        button.classList.remove('active');
    } else {
        // Показываем линии данного уровня сложности
        seriesToToggle.forEach(seriesName => {
            chart.showSeries(seriesName);
        });
        button.classList.add('active');
    }
}

// Функция для инициализации кнопок управления после загрузки графика
function initializeDifficultyControls(chartType) {
    const chartContainer = document.getElementById(`${chartType}-chart`);
    if (!chartContainer) return;
    
    const controlsContainer = chartContainer.querySelector('.difficulty-controls');
    if (!controlsContainer) return;
    
    // Убеждаемся, что все кнопки изначально активны
    const buttons = controlsContainer.querySelectorAll('.difficulty-btn');
    buttons.forEach(button => {
        if (!button.classList.contains('active')) {
            button.classList.add('active');
        }
    });
}

// Обработка ошибок глобально
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Вспомогательные функции для отладки
function debugChartData(chartType) {
    const endpoint = chartEndpoints[chartType];
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            console.log(`Chart data for ${chartType}:`, data);
        })
        .catch(error => {
            console.error(`Error fetching ${chartType} data:`, error);
        });
}

// Функция для изменения настроек загрузки
function configureLoading(options = {}) {
    Object.assign(loadingConfig, options);
    console.log('Loading configuration updated:', loadingConfig);
}

// Быстрые предустановки
function disableLoading() {
    configureLoading({ showLoading: false });
}

function enableFastLoading() {
    configureLoading({ 
        showLoading: true,
        useSkeletonLoading: false,
        preloadCharts: true,
        fastSwitch: true 
    });
}

function enableSkeletonLoading() {
    configureLoading({ 
        showLoading: true,
        useSkeletonLoading: true,
        preloadCharts: true 
    });
}

// Экспорт функций для глобального доступа
window.updateData = updateData;
window.loadChart = loadChart;
window.debugChartData = debugChartData;
window.toggleDifficultyLevel = toggleDifficultyLevel;
window.configureLoading = configureLoading;
window.disableLoading = disableLoading;
window.enableFastLoading = enableFastLoading;
window.enableSkeletonLoading = enableSkeletonLoading;
