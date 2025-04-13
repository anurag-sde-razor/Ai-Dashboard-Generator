import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class ChartGenerator:
    @staticmethod
    def create_bar_chart(
        data: pd.DataFrame,
        x_field: str,
        y_field: str,
        color_field: str = None,
        title: str = None
    ) -> go.Figure:
        """Create a bar chart"""
        fig = px.bar(
            data,
            x=x_field,
            y=y_field,
            color=color_field,
            title=title
        )
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig

    @staticmethod
    def create_pie_chart(
        data: pd.DataFrame,
        labels_field: str,
        values_field: str,
        title: str = None
    ) -> go.Figure:
        """Create a pie chart"""
        fig = px.pie(
            data,
            names=labels_field,
            values=values_field,
            title=title
        )
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig

    @staticmethod
    def create_line_chart(
        data: pd.DataFrame,
        x_field: str,
        y_field: str,
        color_field: str = None,
        title: str = None
    ) -> go.Figure:
        """Create a line chart"""
        fig = px.line(
            data,
            x=x_field,
            y=y_field,
            color=color_field,
            title=title
        )
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig

    @staticmethod
    def create_scatter_plot(
        data: pd.DataFrame,
        x_field: str,
        y_field: str,
        color_field: str = None,
        size_field: str = None,
        title: str = None
    ) -> go.Figure:
        """Create a scatter plot"""
        fig = px.scatter(
            data,
            x=x_field,
            y=y_field,
            color=color_field,
            size=size_field,
            title=title
        )
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig
        
    @staticmethod
    def create_time_series(
        data: pd.DataFrame,
        time_field: str,
        value_field: str,
        group_field: str = None,
        title: str = None
    ) -> go.Figure:
        """Create a time series chart"""
        # Ensure time field is datetime
        if not pd.api.types.is_datetime64_any_dtype(data[time_field]):
            try:
                data[time_field] = pd.to_datetime(data[time_field])
            except:
                # If conversion fails, use as is
                pass
                
        fig = px.line(
            data,
            x=time_field,
            y=value_field,
            color=group_field,
            title=title
        )
        
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50),
            xaxis_title="Time",
            yaxis_title=value_field
        )
        
        return fig
        
    @staticmethod
    def create_statistics(
        data: pd.DataFrame,
        value_field: str,
        group_field: str = None,
        title: str = None
    ) -> go.Figure:
        """Create a statistics chart showing mean, median, min, max"""
        if group_field:
            # Group by the specified field
            grouped_data = data.groupby(group_field)[value_field].agg(['mean', 'median', 'min', 'max']).reset_index()
            
            # Create a figure with subplots
            fig = go.Figure()
            
            # Add traces for each statistic
            fig.add_trace(go.Bar(
                name='Mean',
                x=grouped_data[group_field],
                y=grouped_data['mean'],
                marker_color='rgba(55, 83, 109, 0.7)'
            ))
            
            fig.add_trace(go.Bar(
                name='Median',
                x=grouped_data[group_field],
                y=grouped_data['median'],
                marker_color='rgba(26, 118, 255, 0.7)'
            ))
            
            fig.add_trace(go.Bar(
                name='Min',
                x=grouped_data[group_field],
                y=grouped_data['min'],
                marker_color='rgba(0, 255, 0, 0.7)'
            ))
            
            fig.add_trace(go.Bar(
                name='Max',
                x=grouped_data[group_field],
                y=grouped_data['max'],
                marker_color='rgba(255, 0, 0, 0.7)'
            ))
            
            fig.update_layout(
                barmode='group',
                title=title or f"Statistics for {value_field} by {group_field}",
                xaxis_title=group_field,
                yaxis_title=value_field,
                template="plotly_white",
                margin=dict(t=50, l=50, r=50, b=50)
            )
        else:
            # Calculate statistics for the entire dataset
            stats = {
                'Mean': data[value_field].mean(),
                'Median': data[value_field].median(),
                'Min': data[value_field].min(),
                'Max': data[value_field].max(),
                'Std Dev': data[value_field].std()
            }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(stats.keys()),
                    y=list(stats.values()),
                    marker_color='rgba(55, 83, 109, 0.7)'
                )
            ])
            
            fig.update_layout(
                title=title or f"Statistics for {value_field}",
                xaxis_title="Statistic",
                yaxis_title="Value",
                template="plotly_white",
                margin=dict(t=50, l=50, r=50, b=50)
            )
            
        return fig
        
    @staticmethod
    def create_gauge(
        data: pd.DataFrame,
        value_field: str,
        title: str = None,
        min_value: float = None,
        max_value: float = None
    ) -> go.Figure:
        """Create a gauge chart"""
        # Calculate the value (use mean if multiple rows)
        value = data[value_field].mean()
        
        # Determine min and max if not provided
        if min_value is None:
            min_value = data[value_field].min() * 0.9  # 10% below min
        if max_value is None:
            max_value = data[value_field].max() * 1.1  # 10% above max
            
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title or value_field},
            gauge={
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [min_value, min_value + (max_value - min_value) * 0.33], 'color': "lightgray"},
                    {'range': [min_value + (max_value - min_value) * 0.33, min_value + (max_value - min_value) * 0.66], 'color': "gray"},
                    {'range': [min_value + (max_value - min_value) * 0.66, max_value], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
        
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return fig
        
    @staticmethod
    def create_table(
        data: pd.DataFrame,
        columns: List[str] = None,
        title: str = None,
        max_rows: int = 10
    ) -> go.Figure:
        """Create a table visualization"""
        # If columns not specified, use all columns
        if columns is None:
            columns = data.columns.tolist()
            
        # Limit data to specified columns and rows
        table_data = data[columns].head(max_rows)
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=columns,
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[table_data[col] for col in columns],
                fill_color='lavender',
                align='left',
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title=title or "Data Table",
            template="plotly_white",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return fig 