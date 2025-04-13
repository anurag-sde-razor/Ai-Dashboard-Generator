document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('fileInput');
  const fileLabel = document.querySelector('.file-label');
  const fileInfo = document.querySelector('.file-info');
  const description = document.getElementById('description');
  const chartType = document.getElementById('chartType');
  const colorScheme = document.getElementById('colorScheme');
  const generateBtn = document.getElementById('generateBtn');
  const status = document.getElementById('status');
  const dashboard = document.getElementById('dashboard');
  const historyList = document.getElementById('historyList');
  const toggleBtn = document.getElementById('toggleSidebar');
  const sidebar = document.querySelector('.sidebar');
  
  let currentFile = null;
  let dashboardHistory = [];
  
  fileInput.addEventListener('change', handleFileSelect);
  generateBtn.addEventListener('click', generateDashboard);
  toggleBtn.addEventListener('click', toggleSidebar);
  
  loadHistory();
  
  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      currentFile = file;
      fileLabel.textContent = file.name;
      fileInfo.textContent = `Size: ${formatFileSize(file.size)}`;
    }
  }
  
  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  
  function toggleSidebar() {
    sidebar.classList.toggle('collapsed');
    toggleBtn.textContent = sidebar.classList.contains('collapsed') ? '▶' : '◀';
  }
  
  function loadHistory() {
    chrome.storage.local.get(['dashboardHistory'], (result) => {
      dashboardHistory = result.dashboardHistory || [];
      renderHistory();
    });
  }
  
  function saveHistory(dashboardData) {
    const historyItem = {
      id: Date.now(),
      title: dashboardData.title,
      description: dashboardData.description,
      date: new Date().toLocaleString(),
      chartCount: dashboardData.charts.length,
      filterCount: dashboardData.filters.length,
      data: dashboardData
    };
    
    dashboardHistory.unshift(historyItem);
    if (dashboardHistory.length > 10) {
      dashboardHistory.pop();
    }
    
    chrome.storage.local.set({ dashboardHistory }, () => {
      renderHistory();
    });
  }
  
  function renderHistory() {
    if (dashboardHistory.length === 0) {
      historyList.innerHTML = '<div class="empty-history">No previous dashboards</div>';
      return;
    }
    
    historyList.innerHTML = dashboardHistory.map(item => `
      <div class="history-item" data-id="${item.id}">
        <div class="history-item-content">
          <div class="history-item-title">${item.title}</div>
          <div class="history-item-date">${item.date}</div>
          <div class="history-item-details">
            <span class="history-item-tag">${item.chartCount} charts</span>
            <span class="history-item-tag">${item.filterCount} filters</span>
          </div>
        </div>
        <div class="history-item-actions">
          <button class="history-btn edit-btn" title="Edit Dashboard">✏️</button>
          <button class="history-btn delete-btn" title="Delete Dashboard">🗑️</button>
        </div>
      </div>
    `).join('');
    
    document.querySelectorAll('.history-item').forEach(item => {
      item.addEventListener('click', (e) => {
        if (e.target.classList.contains('history-btn')) {
          return;
        }
        const id = parseInt(item.dataset.id);
        const dashboardData = dashboardHistory.find(h => h.id === id);
        if (dashboardData) {
          displayDashboard(dashboardData.data);
          document.querySelectorAll('.history-item').forEach(i => i.classList.remove('active'));
          item.classList.add('active');
        }
      });
    });

    document.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = parseInt(btn.closest('.history-item').dataset.id);
        const dashboardData = dashboardHistory.find(h => h.id === id);
        if (dashboardData) {
          description.value = dashboardData.description;
          chartType.value = dashboardData.data.options?.chartType || 'auto';
          colorScheme.value = dashboardData.data.options?.colorScheme || 'default';
          layout.value = dashboardData.data.options?.layout || '2';
          showStatus('Dashboard loaded for editing', 'success');
        }
      });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = parseInt(btn.closest('.history-item').dataset.id);
        if (confirm('Are you sure you want to delete this dashboard?')) {
          dashboardHistory = dashboardHistory.filter(h => h.id !== id);
          chrome.storage.local.set({ dashboardHistory }, () => {
            renderHistory();
            showStatus('Dashboard deleted', 'success');
          });
        }
      });
    });
  }
  
  function generateDashboard() {
    if (!currentFile) {
      showStatus('Please select a file first', 'error');
      return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
      const fileContent = e.target.result;
      const data = {
        fileContent: fileContent,
        fileName: currentFile.name,
        fileType: currentFile.type,
        chartType: chartType.value,
        colorScheme: colorScheme.value,
        description: description.value.trim()
      };
      
      showStatus('Generating dashboard...', 'success');
      generateBtn.disabled = true;
      
      chrome.runtime.sendMessage({ action: 'generateDashboard', data }, (response) => {
        generateBtn.disabled = false;
        
        if (response && response.error) {
          showStatus(response.error, 'error');
          return;
        }
        
        if (response && response.dashboard) {
          saveHistory(response.dashboard);
          displayDashboard(response.dashboard);
          showStatus('Dashboard generated successfully!', 'success');
        } else {
          showStatus('Failed to generate dashboard', 'error');
        }
      });
    };
    
    reader.readAsText(currentFile);
  }
  
  function displayDashboard(dashboardData) {
    if (!dashboardData) {
      showStatus('No dashboard data available', 'error');
      return;
    }

    // Ensure we have the required properties
    const title = dashboardData.title || 'Untitled Dashboard';
    const description = dashboardData.description || 'No description available';
    const filters = dashboardData.filters || [];
    const charts = dashboardData.charts || [];

    dashboard.innerHTML = `
      <h2>${title}</h2>
      <p>${description}</p>
      
      <div class="filters-container">
        <div class="filters-title">Filters</div>
        <div class="filters-list">
          ${filters.map(filter => {
            if (!filter || !filter.name || !filter.values) return '';
            return `
              <div class="filter-group">
                <label>${filter.name}</label>
                <select class="filter-select" data-filter="${filter.name}">
                  <option value="">All</option>
                  ${filter.values.map(value => `
                    <option value="${value}">${value}</option>
                  `).join('')}
                </select>
              </div>
            `;
          }).join('')}
        </div>
      </div>
      
      <div class="charts-grid">
        ${charts.map(chart => {
          if (!chart || !chart.type) return '';
          
          if (chart.type === 'bar' && chart.data) {
            return `
              <div class="chart-container">
                <div class="chart-title">${chart.title || 'Bar Chart'}</div>
                <div class="chart-content">
                  <canvas class="chart-canvas" data-type="bar" 
                    data-x="${chart.xAxis || ''}"
                    data-y="${chart.yAxis || ''}"
                    data-values='${JSON.stringify(chart.data)}'>
                  </canvas>
                </div>
              </div>
            `;
          } else if (chart.type === 'pie' && chart.data) {
            return `
              <div class="chart-container">
                <div class="chart-title">${chart.title || 'Pie Chart'}</div>
                <div class="chart-content">
                  <canvas class="chart-canvas" data-type="pie"
                    data-category="${chart.category || ''}"
                    data-value="${chart.value || ''}"
                    data-values='${JSON.stringify(chart.data)}'>
                  </canvas>
                </div>
              </div>
            `;
          }
          return '';
        }).join('')}
      </div>
    `;
    
    // Initialize charts
    initializeCharts();
    
    // Add filter event listeners
    document.querySelectorAll('.filter-select').forEach(select => {
      select.addEventListener('change', () => {
        applyFilters();
      });
    });
  }
  
  function initializeCharts() {
    document.querySelectorAll('.chart-canvas').forEach(canvas => {
      try {
        const ctx = canvas.getContext('2d');
        const type = canvas.dataset.type;
        const data = JSON.parse(canvas.dataset.values || '[]');
        
        if (!data || !Array.isArray(data)) {
          console.error('Invalid chart data');
          return;
        }
        
        if (type === 'bar') {
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.map(d => d.x || ''),
              datasets: [{
                label: canvas.dataset.y || 'Value',
                data: data.map(d => d.y || 0),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
        } else if (type === 'pie') {
          new Chart(ctx, {
            type: 'pie',
            data: {
              labels: data.map(d => d.category || ''),
              datasets: [{
                data: data.map(d => d.value || 0),
                backgroundColor: [
                  'rgba(255, 99, 132, 0.5)',
                  'rgba(54, 162, 235, 0.5)',
                  'rgba(255, 206, 86, 0.5)',
                  'rgba(75, 192, 192, 0.5)',
                  'rgba(153, 102, 255, 0.5)'
                ],
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false
            }
          });
        }
      } catch (error) {
        console.error('Error initializing chart:', error);
      }
    });
  }
  
  function applyFilters() {
    const filters = {};
    document.querySelectorAll('.filter-select').forEach(select => {
      if (select.value) {
        filters[select.dataset.filter] = select.value;
      }
    });
    
    // Update charts based on filters
    document.querySelectorAll('.chart-canvas').forEach(canvas => {
      const chart = Chart.getChart(canvas);
      if (chart) {
        // Apply filters to chart data
        // This is a simplified version - you might want to add more complex filtering logic
        chart.update();
      }
    });
  }
  
  function showStatus(message, type) {
    status.textContent = message;
    status.className = `status ${type}`;
    setTimeout(() => {
      status.className = 'status';
    }, 3000);
  }
}); 