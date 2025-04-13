import os
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

class LLMHandler:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Try different model names
        try:
            self.model = genai.GenerativeModel('gemini-1.0-pro')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except:
                # Fallback to a simple response if model loading fails
                self.model = None

    def parse_dashboard_spec(self, spec_text: str) -> Dict[str, Any]:
        """Parse natural language dashboard specification into structured format"""
        if self.model is None:
            # Fallback to a simple response if model is not available
            return {
                "dashboard_title": "Sample Dashboard",
                "data_sources": [
                    {"type": "csv", "path": "data.csv"}
                ],
                "charts": [
                    {
                        "title": "Sales by Industry",
                        "type": "bar",
                        "x_field": "Industry",
                        "y_field": "Sales",
                        "color_field": "Region",
                        "interactive": True
                    },
                    {
                        "title": "Sales by Region",
                        "type": "pie",
                        "labels_field": "Region",
                        "values_field": "Sales"
                    },
                    {
                        "title": "Sales Over Time",
                        "type": "time_series",
                        "time_field": "Date",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Product Statistics",
                        "type": "statistics",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Total Sales",
                        "type": "gauge",
                        "value_field": "Sales"
                    },
                    {
                        "title": "Top Products",
                        "type": "table",
                        "columns": ["Product", "Sales", "Region"]
                    }
                ],
                "layout": {
                    "rows": 3,
                    "columns": 2,
                    "chart_positions": [
                        {"chart": "Sales by Industry", "row": 1, "column": 1},
                        {"chart": "Sales by Region", "row": 1, "column": 2},
                        {"chart": "Sales Over Time", "row": 2, "column": 1},
                        {"chart": "Product Statistics", "row": 2, "column": 2},
                        {"chart": "Total Sales", "row": 3, "column": 1},
                        {"chart": "Top Products", "row": 3, "column": 2}
                    ]
                },
                "filters": ["Industry", "Region", "Product"],
                "notes": "Sample dashboard with all chart types"
            }

        try:
            prompt = f"""
            You are a professional dashboard specification analyzer.
            Parse the following dashboard specification into a structured JSON format:

            {spec_text}

            Return ONLY the JSON object with the following structure:
            {{
                "dashboard_title": "string",
                "data_sources": [
                    {{ "type": "string", "path": "string" }}
                ],
                "charts": [
                    {{
                        "title": "string",
                        "type": "string",
                        "x_field": "string",
                        "y_field": "string",
                        "color_field": "string",
                        "interactive": boolean
                    }}
                ],
                "layout": {{
                    "rows": number,
                    "columns": number,
                    "chart_positions": [
                        {{"chart": "string", "row": number, "column": number}}
                    ]
                }},
                "filters": ["string"],
                "notes": "string"
            }}

            The chart types can be one of the following:
            - "bar": Requires x_field and y_field
            - "pie": Requires labels_field and values_field
            - "line": Requires x_field and y_field
            - "scatter": Requires x_field and y_field
            - "time_series": Requires time_field and value_field
            - "statistics": Requires value_field (and optionally group_field)
            - "gauge": Requires value_field
            - "table": No required fields, but can have columns field

            Examples:
            - Bar chart: {{"title": "Sales by Product", "type": "bar", "x_field": "Product", "y_field": "Sales"}}
            - Pie chart: {{"title": "Sales by Region", "type": "pie", "labels_field": "Region", "values_field": "Sales"}}
            - Time series: {{"title": "Sales Over Time", "type": "time_series", "time_field": "Date", "value_field": "Sales", "group_field": "Product"}}
            - Statistics: {{"title": "Product Statistics", "type": "statistics", "value_field": "Sales", "group_field": "Product"}}
            - Gauge: {{"title": "Total Sales", "type": "gauge", "value_field": "Sales"}}
            - Table: {{"title": "Top Products", "type": "table", "columns": ["Product", "Sales", "Region"]}}

            IMPORTANT: Make sure to include at least one example of each chart type in your response.
            """

            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                try:
                    spec = json.loads(json_str)
                    return spec
                except json.JSONDecodeError:
                    print(f"Error parsing JSON: {json_str}")
            
            # If we couldn't extract valid JSON, return a default specification
            return {
                "dashboard_title": "Sample Dashboard",
                "data_sources": [
                    {"type": "csv", "path": "data.csv"}
                ],
                "charts": [
                    {
                        "title": "Sales by Industry",
                        "type": "bar",
                        "x_field": "Industry",
                        "y_field": "Sales",
                        "color_field": "Region",
                        "interactive": True
                    },
                    {
                        "title": "Sales by Region",
                        "type": "pie",
                        "labels_field": "Region",
                        "values_field": "Sales"
                    },
                    {
                        "title": "Sales Over Time",
                        "type": "time_series",
                        "time_field": "Date",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Product Statistics",
                        "type": "statistics",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Total Sales",
                        "type": "gauge",
                        "value_field": "Sales"
                    },
                    {
                        "title": "Top Products",
                        "type": "table",
                        "columns": ["Product", "Sales", "Region"]
                    }
                ],
                "layout": {
                    "rows": 3,
                    "columns": 2,
                    "chart_positions": [
                        {"chart": "Sales by Industry", "row": 1, "column": 1},
                        {"chart": "Sales by Region", "row": 1, "column": 2},
                        {"chart": "Sales Over Time", "row": 2, "column": 1},
                        {"chart": "Product Statistics", "row": 2, "column": 2},
                        {"chart": "Total Sales", "row": 3, "column": 1},
                        {"chart": "Top Products", "row": 3, "column": 2}
                    ]
                },
                "filters": ["Industry", "Region", "Product"],
                "notes": "Sample dashboard with all chart types"
            }
        except Exception as e:
            print(f"Error in LLM parsing: {str(e)}")
            # Return a simple response if parsing fails
            return {
                "dashboard_title": "Sample Dashboard",
                "data_sources": [
                    {"type": "csv", "path": "data.csv"}
                ],
                "charts": [
                    {
                        "title": "Sales by Industry",
                        "type": "bar",
                        "x_field": "Industry",
                        "y_field": "Sales",
                        "color_field": "Region",
                        "interactive": True
                    },
                    {
                        "title": "Sales by Region",
                        "type": "pie",
                        "labels_field": "Region",
                        "values_field": "Sales"
                    },
                    {
                        "title": "Sales Over Time",
                        "type": "time_series",
                        "time_field": "Date",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Product Statistics",
                        "type": "statistics",
                        "value_field": "Sales",
                        "group_field": "Product"
                    },
                    {
                        "title": "Total Sales",
                        "type": "gauge",
                        "value_field": "Sales"
                    },
                    {
                        "title": "Top Products",
                        "type": "table",
                        "columns": ["Product", "Sales", "Region"]
                    }
                ],
                "layout": {
                    "rows": 3,
                    "columns": 2,
                    "chart_positions": [
                        {"chart": "Sales by Industry", "row": 1, "column": 1},
                        {"chart": "Sales by Region", "row": 1, "column": 2},
                        {"chart": "Sales Over Time", "row": 2, "column": 1},
                        {"chart": "Product Statistics", "row": 2, "column": 2},
                        {"chart": "Total Sales", "row": 3, "column": 1},
                        {"chart": "Top Products", "row": 3, "column": 2}
                    ]
                },
                "filters": ["Industry", "Region", "Product"],
                "notes": "Sample dashboard with all chart types"
            }

    def suggest_chart_type(self, data_description: str, visualization_goal: str) -> str:
        """Suggest the most appropriate chart type based on data and goal"""
        if self.model is None:
            return "bar"  # Default to bar chart

        try:
            prompt = f"""
            Based on the following data description and visualization goal, suggest the most appropriate chart type.
            Choose from: bar, pie, line, scatter, time_series, statistics, gauge, or table.

            Data description: {data_description}
            Visualization goal: {visualization_goal}

            Return ONLY the chart type as a string.
            """

            response = self.model.generate_content(prompt)
            return response.text.strip().lower()
        except Exception as e:
            print(f"Error in chart type suggestion: {str(e)}")
            return "bar"  # Default to bar chart

    def generate_chart_title(self, chart_type: str, fields: list) -> str:
        """Generate a descriptive title for a chart based on its type and fields"""
        if self.model is None:
            return f"{chart_type.capitalize()} Chart of {', '.join(fields)}"

        try:
            prompt = f"""
            Generate a concise, descriptive title for a {chart_type} chart that uses the following fields: {', '.join(fields)}.

            Return ONLY the title as a string.
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error in title generation: {str(e)}")
            return f"{chart_type.capitalize()} Chart of {', '.join(fields)}" 