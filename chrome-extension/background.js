// API Key for Google Generative AI
const API_KEY = 'YOUR_API_KEY';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'generateDashboard') {
    generateDashboard(request.data)
      .then(dashboard => sendResponse({ dashboard }))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Will respond asynchronously
  }
});

async function generateDashboard(data) {
  try {
    // Parse the file data
    const parsedData = await parseFileData(data.fileContent, data.fileType);
    
    // Generate dashboard specification using AI
    const dashboardSpec = await generateDashboardSpec(parsedData, data.description);
    
    // Return the dashboard specification
    return {
      title: dashboardSpec.title,
      description: data.description,
      charts: dashboardSpec.charts,
      filters: dashboardSpec.filters,
      options: {
        chartType: data.chartType,
        colorScheme: data.colorScheme,
        layout: data.layout
      }
    };
  } catch (error) {
    console.error('Error generating dashboard:', error);
    throw new Error('Failed to generate dashboard: ' + error.message);
  }
}

async function parseFileData(content, fileType) {
  // For CSV files
  if (fileType === 'text/csv') {
    return parseCSV(content);
  }
  // For Excel files
  else if (fileType.includes('excel') || fileType.includes('spreadsheet')) {
    return parseExcel(content);
  }
  // For PDF files
  else if (fileType === 'application/pdf') {
    return parsePDF(content);
  }
  else {
    throw new Error('Unsupported file type');
  }
}

function parseCSV(content) {
  const lines = content.split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  const data = [];
  
  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    const values = lines[i].split(',').map(v => v.trim());
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index];
    });
    data.push(row);
  }
  
  return {
    headers,
    data,
    type: 'csv'
  };
}

function parseExcel(content) {
  // For now, we'll just parse as CSV
  // In a real implementation, you'd use a library like SheetJS
  return parseCSV(content);
}

function parsePDF(content) {
  // For now, we'll return a simple structure
  // In a real implementation, you'd use a PDF parsing library
  return {
    headers: ['text'],
    data: [{ text: content }],
    type: 'pdf'
  };
}

async function generateDashboardSpec(parsedData, description) {
  // Extract numeric and categorical columns
  const numericColumns = parsedData.headers.filter(header => {
    return parsedData.data.some(row => !isNaN(parseFloat(row[header])));
  });
  
  const categoricalColumns = parsedData.headers.filter(header => {
    return parsedData.data.some(row => isNaN(parseFloat(row[header])));
  });
  
  // Generate charts based on available data
  const charts = [];
  
  // If we have numeric data, create a bar chart
  if (numericColumns.length >= 2) {
    const xAxis = numericColumns[0];
    const yAxis = numericColumns[1];
    
    // Calculate aggregated data for the chart
    const aggregatedData = {};
    parsedData.data.forEach(row => {
      const xValue = row[xAxis];
      const yValue = parseFloat(row[yAxis]) || 0;
      aggregatedData[xValue] = (aggregatedData[xValue] || 0) + yValue;
    });
    
    charts.push({
      type: 'bar',
      title: `${yAxis} by ${xAxis}`,
      xAxis: xAxis,
      yAxis: yAxis,
      data: Object.entries(aggregatedData).map(([x, y]) => ({ x, y }))
    });
  }
  
  // If we have categorical and numeric data, create a pie chart
  if (categoricalColumns.length > 0 && numericColumns.length > 0) {
    const category = categoricalColumns[0];
    const value = numericColumns[0];
    
    // Calculate aggregated data for the pie chart
    const aggregatedData = {};
    parsedData.data.forEach(row => {
      const categoryValue = row[category];
      const numericValue = parseFloat(row[value]) || 0;
      aggregatedData[categoryValue] = (aggregatedData[categoryValue] || 0) + numericValue;
    });
    
    charts.push({
      type: 'pie',
      title: `${value} by ${category}`,
      category: category,
      value: value,
      data: Object.entries(aggregatedData).map(([category, value]) => ({ category, value }))
    });
  }
  
  // Generate filters based on categorical columns
  const filters = categoricalColumns.map(col => ({
    name: col,
    values: [...new Set(parsedData.data.map(row => row[col]))]
  }));
  
  return {
    title: `Data Analysis Dashboard`,
    description: description || 'Analyzing your data...',
    charts: charts,
    filters: filters,
    rawData: parsedData.data
  };
} 