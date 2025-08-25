// LeetCode Progress Tracker - ApexCharts Integration

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
    
    // Загружаем первый график
    loadChart('progress');
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
            
            // Загружаем график если не загружен
            if (!chartsCache[chartType]) {
                loadChart(chartType);
            }
        });
    });
}

// Показать контейнер графика
function showChart(chartType) {
    const chartContainersElements = document.querySelectorAll('.chart');
    const targetContainer = document.getElementById(chartType + '-chart');
    
    // Скрываем все контейнеры
    chartContainersElements.forEach(container => {
        container.classList.remove('active');
    });
    
    // Показываем нужный
    if (targetContainer) {
        targetContainer.classList.add('active');
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
    
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container ${containerId} not found`);
        return;
    }
    
    try {
        // Показываем индикатор загрузки
        container.innerHTML = '<div class="chart-loading">📊 Загрузка графика...</div>';
        
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const chartConfig = await response.json();
        
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

// Экспорт функций для глобального доступа
window.updateData = updateData;
window.loadChart = loadChart;
window.debugChartData = debugChartData;
window.toggleDifficultyLevel = toggleDifficultyLevel;
