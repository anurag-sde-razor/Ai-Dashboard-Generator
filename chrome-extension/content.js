// Listen for messages from the background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageData') {
    // Extract data from the current page
    const pageData = extractPageData();
    sendResponse({ success: true, data: pageData });
  }
  return true;
});

// Function to extract data from the current page
function extractPageData() {
  // Get all tables on the page
  const tables = document.getElementsByTagName('table');
  const tableData = [];
  
  for (let i = 0; i < tables.length; i++) {
    const table = tables[i];
    const headers = [];
    const rows = [];
    
    // Extract headers
    const headerCells = table.getElementsByTagName('th');
    for (let j = 0; j < headerCells.length; j++) {
      headers.push(headerCells[j].textContent.trim());
    }
    
    // If no headers found, try to get them from the first row
    if (headers.length === 0) {
      const firstRow = table.rows[0];
      if (firstRow) {
        const cells = firstRow.cells;
        for (let j = 0; j < cells.length; j++) {
          headers.push(cells[j].textContent.trim());
        }
      }
    }
    
    // Extract data rows
    const dataRows = table.getElementsByTagName('tr');
    for (let j = 1; j < dataRows.length; j++) { // Start from 1 to skip header row
      const row = dataRows[j];
      const cells = row.cells;
      const rowData = {};
      
      for (let k = 0; k < cells.length; k++) {
        if (headers[k]) {
          rowData[headers[k]] = cells[k].textContent.trim();
        }
      }
      
      if (Object.keys(rowData).length > 0) {
        rows.push(rowData);
      }
    }
    
    if (headers.length > 0 && rows.length > 0) {
      tableData.push({
        headers,
        data: rows
      });
    }
  }
  
  // Get all lists on the page
  const lists = document.getElementsByTagName('ul');
  const listData = [];
  
  for (let i = 0; i < lists.length; i++) {
    const list = lists[i];
    const items = [];
    
    // Extract list items
    const listItems = list.getElementsByTagName('li');
    for (let j = 0; j < listItems.length; j++) {
      items.push(listItems[j].textContent.trim());
    }
    
    if (items.length > 0) {
      listData.push(items);
    }
  }
  
  // Get all paragraphs on the page
  const paragraphs = document.getElementsByTagName('p');
  const paragraphData = [];
  
  for (let i = 0; i < paragraphs.length; i++) {
    const text = paragraphs[i].textContent.trim();
    if (text) {
      paragraphData.push(text);
    }
  }
  
  return {
    tables: tableData,
    lists: listData,
    paragraphs: paragraphData,
    url: window.location.href,
    title: document.title
  };
}

// Function to inject a dashboard into the page
function injectDashboard(dashboard) {
  // Create container for the dashboard
  const container = document.createElement('div');
  container.id = 'ai-dashboard-container';
  container.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    width: 400px;
    max-height: 80vh;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    overflow-y: auto;
    z-index: 10000;
  `;
  
  // Add close button
  const closeButton = document.createElement('button');
  closeButton.textContent = '×';
  closeButton.style.cssText = `
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
  `;
  closeButton.onclick = () => container.remove();
  container.appendChild(closeButton);
  
  // Add title
  const title = document.createElement('h2');
  title.textContent = dashboard.title;
  title.style.cssText = `
    margin: 0 0 20px 0;
    padding-right: 30px;
    font-size: 18px;
    color: #333;
  `;
  container.appendChild(title);
  
  // Add charts container
  const chartsContainer = document.createElement('div');
  chartsContainer.style.cssText = `
    display: grid;
    grid-template-columns: repeat(${dashboard.layout.columns}, 1fr);
    gap: 20px;
    margin-bottom: 20px;
  `;
  
  // Add each chart
  dashboard.charts.forEach(chart => {
    const chartElement = document.createElement('div');
    chartElement.style.cssText = `
      background: #f8f9fa;
      border-radius: 6px;
      padding: 15px;
    `;
    
    const chartTitle = document.createElement('h3');
    chartTitle.textContent = chart.title;
    chartTitle.style.cssText = `
      margin: 0 0 10px 0;
      font-size: 16px;
      color: #444;
    `;
    chartElement.appendChild(chartTitle);
    
    // Add chart placeholder (in a real implementation, you would use a charting library)
    const chartPlaceholder = document.createElement('div');
    chartPlaceholder.style.cssText = `
      height: 200px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 4px;
    `;
    chartPlaceholder.innerHTML = `
      <div style="font-size: 14px; color: #666; margin-bottom: 10px;">${chart.type.toUpperCase()} CHART</div>
      <div style="font-size: 12px; color: #888;">
        <div>X-Axis: ${chart.x_field}</div>
        <div>Y-Axis: ${chart.y_field}</div>
        ${chart.color_field ? `<div>Color: ${chart.color_field}</div>` : ''}
      </div>
    `;
    chartElement.appendChild(chartPlaceholder);
    
    chartsContainer.appendChild(chartElement);
  });
  
  container.appendChild(chartsContainer);
  
  // Add filters if specified
  if (dashboard.filters && dashboard.filters.length > 0) {
    const filtersContainer = document.createElement('div');
    filtersContainer.style.cssText = `
      background: #f8f9fa;
      border-radius: 6px;
      padding: 15px;
    `;
    
    const filtersTitle = document.createElement('h3');
    filtersTitle.textContent = 'Filters';
    filtersTitle.style.cssText = `
      margin: 0 0 10px 0;
      font-size: 16px;
      color: #444;
    `;
    filtersContainer.appendChild(filtersTitle);
    
    const filtersList = document.createElement('ul');
    filtersList.style.cssText = `
      margin: 0;
      padding: 0 0 0 20px;
      list-style-type: none;
    `;
    
    dashboard.filters.forEach(filter => {
      const filterItem = document.createElement('li');
      filterItem.textContent = filter;
      filterItem.style.cssText = `
        margin-bottom: 5px;
        font-size: 14px;
        color: #666;
      `;
      filtersList.appendChild(filterItem);
    });
    
    filtersContainer.appendChild(filtersList);
    container.appendChild(filtersContainer);
  }
  
  // Add the dashboard to the page
  document.body.appendChild(container);
} 