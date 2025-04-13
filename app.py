import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from modules.data_loader import DataLoader
from modules.spec_parser import ChartSpecParser
from modules.chart_generator import ChartGenerator
from custom_css import get_custom_css

# Load environment variables
load_dotenv()

# Set page config with full width
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS with gradient background
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Add custom CSS to remove any remaining gaps
st.markdown("""
<style>
    /* Remove any remaining gaps */
    .reportview-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Make sure the main content takes full width */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Remove any padding from the app */
    .stApp {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Make sure columns take full width */
    .row-widget.stHorizontal {
        width: 100% !important;
    }
    
    /* Remove any padding from columns */
    .row-widget.stHorizontal > div {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for demonstration"""
    # Create sample data
    np.random.seed(42)
    
    # Generate dates
    dates = [datetime.now() - timedelta(days=x) for x in range(100)]
    
    # Generate products
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    
    # Generate regions
    regions = ['North', 'South', 'East', 'West']
    
    # Generate industries
    industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']
    
    # Generate data
    data = []
    for date in dates:
        for product in products:
            for region in regions:
                for industry in industries:
                    if np.random.random() > 0.7:  # Only include some combinations
                        sales = np.random.randint(100, 1000)
                        profit = sales * np.random.uniform(0.1, 0.3)
                        data.append({
                            'Date': date,
                            'Product': product,
                            'Region': region,
                            'Industry': industry,
                            'Sales': sales,
                            'Profit': profit,
                            'Units': np.random.randint(10, 100)
                        })
    
    return pd.DataFrame(data)

def main():
    # Sidebar with app info
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/dashboard.png", width=80)
        st.title("AI Dashboard Generator")
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Transform your data into beautiful dashboards using natural language!
        
        Simply upload your data or use our sample data, then describe the dashboard you want to create.
        """)
        st.markdown("---")
        st.markdown("### Tips")
        st.markdown("""
        - Use clear, descriptive language
        - Specify chart types and data fields
        - Try different chart combinations
        """)
    
    # Main content
    st.markdown("<h1 style='text-align: center;'>📊 AI Dashboard Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Transform your data into beautiful dashboards using natural language!</p>", unsafe_allow_html=True)
    
    # Data section
    st.markdown("## 📁 Data")
    
    # Add custom CSS for file upload section
    st.markdown("""
        <style>
        .file-upload-container {
            padding-left: 2rem;
            margin-left: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create columns with adjusted ratios to move content more to the right
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Data source selection with improved styling
        st.markdown('<div class="file-upload-container">', unsafe_allow_html=True)
        st.markdown("### Select Data Source")
        data_source = st.radio(
            "",
            ["Upload File", "Use Sample Data"],
            horizontal=True
        )
        
        df = None
        
        if data_source == "Upload File":
            # File uploader with improved styling
            st.markdown("### Upload Your Data")
            uploaded_file = st.file_uploader("", type=['csv', 'xlsx', 'pdf'])
            
            if uploaded_file is not None:
                try:
                    # Load data
                    data_loader = DataLoader()
                    df = data_loader.load_data(uploaded_file)
                    st.success("Data loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        else:
            # Generate sample data
            df = generate_sample_data()
            st.success("Sample data generated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data preview section
    if df is not None:
        st.markdown("### Data Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        # Show column names to help with specification
        st.markdown("### Available Columns")
        st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>{', '.join(df.columns.tolist())}</div>", unsafe_allow_html=True)
    
    # Dashboard specification input
    st.markdown("## 📝 Dashboard Specification")
    
    # Create a container with specific width for the textbox
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        spec_input = st.text_area(
            "Describe your dashboard",
            placeholder="Example: Create a bar chart showing sales by product and a pie chart showing sales by region.",
            height=100
        )
    
    # Generate button
    if st.button("🚀 Generate Dashboard", key="generate_all", use_container_width=True):
        if df is None:
            st.error("Please upload a data file or use sample data first!")
        elif not spec_input:
            st.error("Please provide a description for your dashboard!")
        else:
            try:
                # Parse specification
                spec_parser = ChartSpecParser()
                spec = spec_parser.parse_specification(spec_input)
                
                # Create charts based on specification
                chart_generator = ChartGenerator()
                
                # Create columns for layout
                cols = st.columns(spec['layout']['columns'])
                
                # Generate each chart
                for i, chart_spec in enumerate(spec['charts']):
                    col_idx = i % spec['layout']['columns']
                    with cols[col_idx]:
                        if chart_spec['type'] == 'bar':
                            fig = chart_generator.create_bar_chart(
                                df,
                                chart_spec['x_field'],
                                chart_spec['y_field'],
                                chart_spec.get('color_field'),
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'pie':
                            fig = chart_generator.create_pie_chart(
                                df,
                                chart_spec['labels_field'],
                                chart_spec['values_field'],
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'line':
                            fig = chart_generator.create_line_chart(
                                df,
                                chart_spec['x_field'],
                                chart_spec['y_field'],
                                chart_spec.get('color_field'),
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'scatter':
                            fig = chart_generator.create_scatter_plot(
                                df,
                                chart_spec['x_field'],
                                chart_spec['y_field'],
                                chart_spec.get('color_field'),
                                chart_spec.get('size_field'),
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'time_series':
                            fig = chart_generator.create_time_series(
                                df,
                                chart_spec['time_field'],
                                chart_spec['value_field'],
                                chart_spec.get('group_field'),
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'statistics':
                            fig = chart_generator.create_statistics(
                                df,
                                chart_spec['value_field'],
                                chart_spec.get('group_field'),
                                chart_spec['title']
                            )
                        elif chart_spec['type'] == 'gauge':
                            fig = chart_generator.create_gauge(
                                df,
                                chart_spec['value_field'],
                                chart_spec['title'],
                                chart_spec.get('min_value'),
                                chart_spec.get('max_value')
                            )
                        elif chart_spec['type'] == 'table':
                            fig = chart_generator.create_table(
                                df,
                                chart_spec.get('columns'),
                                chart_spec['title'],
                                chart_spec.get('max_rows', 10)
                            )
                        
                        # Add zoom and download features to the chart
                        fig.update_layout(
                            height=500,
                            width=1500,  # Increased width even more
                            margin=dict(l=20, r=20, t=40, b=20),  # Reduced side margins
                            hovermode='closest',
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        # Add download button for each chart
                        chart_title = chart_spec.get('title', f"Chart {i+1}")
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label=f"Download {chart_title}",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name=f"{chart_title.replace(' ', '_').lower()}.html",
                            mime="text/html",
                            key=f"download_{i}"
                        )
                
                # Add filters if specified
                if 'filters' in spec and spec['filters']:
                    st.sidebar.header("Filters")
                    for filter_field in spec['filters']:
                        if filter_field in df.columns:
                            unique_values = df[filter_field].unique()
                            selected_values = st.sidebar.multiselect(
                                f"Select {filter_field}",
                                options=unique_values,
                                default=unique_values
                            )
            
            except Exception as e:
                st.error(f"Error generating dashboard: {str(e)}")
                st.error("Please check your data and specification format.")
                st.error("Make sure the fields mentioned in your specification exist in your data.")
    
    # Quick chart generation section
    st.markdown("## 📈 Quick Chart Generation")
    st.markdown("Generate individual charts with a single click")
    
    # Create a row of buttons for each chart type with wider spacing
    chart_buttons = st.columns(4)
    
    with chart_buttons[0]:
        if st.button("📈 Bar Chart", key="bar_chart"):
            if df is not None:
                try:
                    # Get numeric columns for y-axis
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    # Get categorical columns for x-axis
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if numeric_cols and categorical_cols:
                        # Create a bar chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_bar_chart(
                            df,
                            categorical_cols[0],  # Use first categorical column as x
                            numeric_cols[0],      # Use first numeric column as y
                            None,                 # No color grouping
                            f"Bar Chart: {numeric_cols[0]} by {categorical_cols[0]}"
                        )
                        
                        # Add zoom and download features with wider layout
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            hovermode='closest',
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        # Use full container width for the chart
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Bar Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="bar_chart.html",
                            mime="text/html",
                            key="download_bar"
                        )
                    else:
                        st.error("Need both numeric and categorical columns for a bar chart")
                except Exception as e:
                    st.error(f"Error creating bar chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons[1]:
        if st.button("🥧 Pie Chart", key="pie_chart"):
            if df is not None:
                try:
                    # Get numeric columns for values
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    # Get categorical columns for labels
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if numeric_cols and categorical_cols:
                        # Create a pie chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_pie_chart(
                            df,
                            categorical_cols[0],  # Use first categorical column as labels
                            numeric_cols[0],      # Use first numeric column as values
                            f"Pie Chart: {numeric_cols[0]} by {categorical_cols[0]}"
                        )
                        
                        # Add zoom and download features
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Pie Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="pie_chart.html",
                            mime="text/html",
                            key="download_pie"
                        )
                    else:
                        st.error("Need both numeric and categorical columns for a pie chart")
                except Exception as e:
                    st.error(f"Error creating pie chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons[2]:
        if st.button("📉 Line Chart", key="line_chart"):
            if df is not None:
                try:
                    # Get numeric columns for y-axis
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    # Get categorical columns for x-axis
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if numeric_cols and categorical_cols:
                        # Create a line chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_line_chart(
                            df,
                            categorical_cols[0],  # Use first categorical column as x
                            numeric_cols[0],      # Use first numeric column as y
                            None,                 # No color grouping
                            f"Line Chart: {numeric_cols[0]} by {categorical_cols[0]}"
                        )
                        
                        # Add zoom and download features
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            hovermode='closest',
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Line Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="line_chart.html",
                            mime="text/html",
                            key="download_line"
                        )
                    else:
                        st.error("Need both numeric and categorical columns for a line chart")
                except Exception as e:
                    st.error(f"Error creating line chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons[3]:
        if st.button("🔍 Scatter Plot", key="scatter_plot"):
            if df is not None:
                try:
                    # Get numeric columns for x and y axes
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if len(numeric_cols) >= 2:
                        # Create a scatter plot
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_scatter_plot(
                            df,
                            numeric_cols[0],      # Use first numeric column as x
                            numeric_cols[1],      # Use second numeric column as y
                            None,                 # No color grouping
                            None,                 # No size field
                            f"Scatter Plot: {numeric_cols[1]} vs {numeric_cols[0]}"
                        )
                        
                        # Add zoom and download features
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            hovermode='closest',
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Scatter Plot",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="scatter_plot.html",
                            mime="text/html",
                            key="download_scatter"
                        )
                    else:
                        st.error("Need at least two numeric columns for a scatter plot")
                except Exception as e:
                    st.error(f"Error creating scatter plot: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")

    # Second row of buttons
    chart_buttons2 = st.columns(4)
    
    with chart_buttons2[0]:
        if st.button("⏱️ Time Series", key="time_series"):
            if df is not None:
                try:
                    # Check if there's a date column
                    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
                    # Get numeric columns for values
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if date_cols and numeric_cols:
                        # Create a time series chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_time_series(
                            df,
                            date_cols[0],         # Use first date column as time field
                            numeric_cols[0],      # Use first numeric column as value field
                            None,                 # No group field
                            f"Time Series: {numeric_cols[0]} over time"
                        )
                        
                        # Add zoom and download features with wider layout
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            hovermode='closest',
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        # Use full container width for the chart
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Time Series Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="time_series_chart.html",
                            mime="text/html",
                            key="download_time_series"
                        )
                    else:
                        st.error("Need a date column and a numeric column for a time series chart")
                except Exception as e:
                    st.error(f"Error creating time series chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons2[1]:
        if st.button("📊 Statistics", key="statistics"):
            if df is not None:
                try:
                    # Get numeric columns for statistics
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if numeric_cols:
                        # Create a statistics chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_statistics(
                            df,
                            numeric_cols[0],      # Use first numeric column for statistics
                            None,                 # No group field
                            f"Statistics for {numeric_cols[0]}"
                        )
                        
                        # Add zoom and download features
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Statistics Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="statistics_chart.html",
                            mime="text/html",
                            key="download_statistics"
                        )
                    else:
                        st.error("Need at least one numeric column for statistics")
                except Exception as e:
                    st.error(f"Error creating statistics chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons2[2]:
        if st.button("🎯 Gauge", key="gauge"):
            if df is not None:
                try:
                    # Get numeric columns for gauge
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if numeric_cols:
                        # Create a gauge chart
                        chart_generator = ChartGenerator()
                        fig = chart_generator.create_gauge(
                            df,
                            numeric_cols[0],      # Use first numeric column for gauge
                            f"Gauge: {numeric_cols[0]}",
                            None,                 # No min value
                            None                  # No max value
                        )
                        
                        # Add zoom and download features
                        fig.update_layout(
                            height=500,
                            width=1800,  # Increased width even more
                            margin=dict(l=10, r=10, t=40, b=10),  # Reduced side margins even more
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.download_button(
                            label="Download Gauge Chart",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name="gauge_chart.html",
                            mime="text/html",
                            key="download_gauge"
                        )
                    else:
                        st.error("Need at least one numeric column for a gauge chart")
                except Exception as e:
                    st.error(f"Error creating gauge chart: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    with chart_buttons2[3]:
        if st.button("📋 Table", key="table"):
            if df is not None:
                try:
                    # Create a table
                    chart_generator = ChartGenerator()
                    fig = chart_generator.create_table(
                        df,
                        None,                    # Use all columns
                        "Data Table",
                        10                       # Show first 10 rows
                    )
                    
                    # Add zoom and download features
                    fig.update_layout(
                        height=500,
                        width=1800,  # Increased width even more
                        margin=dict(l=10, r=10, t=40, b=10)  # Reduced side margins even more
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.download_button(
                        label="Download Table",
                        data=fig.to_html(include_plotlyjs='cdn'),
                        file_name="data_table.html",
                        mime="text/html",
                        key="download_table"
                    )
                except Exception as e:
                    st.error(f"Error creating table: {str(e)}")
            else:
                st.error("Please upload a data file or use sample data first!")
    
    # Add a footer
    st.markdown("<div class='footer'>© 2023 AI Dashboard Generator | Created with ❤️</div>", unsafe_allow_html=True)

    # Add custom CSS to make charts wider
    st.markdown("""
        <style>
        /* Make charts wider */
        .stPlotlyChart {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Make chart containers wider */
        .element-container {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Ensure plotly charts take full width */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Make sure the main content takes full width */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Remove any remaining gaps */
        .reportview-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* Make sure columns take full width */
        .row-widget.stHorizontal {
            width: 100% !important;
        }
        
        /* Remove any padding from columns */
        .row-widget.stHorizontal > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Make sure the app takes full width */
        .stApp {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Make sure the sidebar doesn't take too much space */
        .css-1d391kg {
            width: 20% !important;
        }
        
        /* Make sure the main content takes more space */
        .css-1wrcr25 {
            width: 80% !important;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 