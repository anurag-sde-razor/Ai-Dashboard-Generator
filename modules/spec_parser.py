import json
from typing import Dict, Any, List
from .llm_handler import LLMHandler

class ChartSpecParser:
    def __init__(self):
        self.llm_handler = LLMHandler()

    def parse_specification(self, spec_text: str) -> Dict[str, Any]:
        """Parse natural language specification into structured format"""
        try:
            # Get structured JSON from LLM
            json_str = self.llm_handler.parse_dashboard_spec(spec_text)
            
            # If the response is already a dictionary, return it
            if isinstance(json_str, dict):
                spec = json_str
            else:
                # Try to parse the JSON string
                try:
                    spec = json.loads(json_str)
                except json.JSONDecodeError:
                    # If JSON parsing fails, use the default specification
                    spec = {
                        "dashboard_title": "Sample Dashboard",
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
                            }
                        ],
                        "layout": {
                            "rows": 2,
                            "columns": 2,
                            "chart_positions": [
                                {"chart": "Sales by Industry", "row": 1, "column": 1},
                                {"chart": "Sales by Region", "row": 1, "column": 2}
                            ]
                        },
                        "filters": ["Industry", "Region"]
                    }
            
            # Validate the specification
            self._validate_spec(spec)
            
            return spec
        except Exception as e:
            print(f"Error in specification parsing: {str(e)}")
            # Return a default specification
            return {
                "dashboard_title": "Sample Dashboard",
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
                    }
                ],
                "layout": {
                    "rows": 2,
                    "columns": 2,
                    "chart_positions": [
                        {"chart": "Sales by Industry", "row": 1, "column": 1},
                        {"chart": "Sales by Region", "row": 1, "column": 2}
                    ]
                },
                "filters": ["Industry", "Region"]
            }

    def _validate_spec(self, spec: Dict[str, Any]) -> None:
        """Validate the dashboard specification"""
        required_fields = ['dashboard_title', 'charts', 'layout']
        for field in required_fields:
            if field not in spec:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(spec['charts'], list):
            raise ValueError("'charts' must be a list")

        for chart in spec['charts']:
            self._validate_chart_spec(chart)

        self._validate_layout(spec['layout'])

    def _validate_chart_spec(self, chart: Dict[str, Any]) -> None:
        """Validate a chart specification"""
        required_fields = ['title', 'type']
        for field in required_fields:
            if field not in chart:
                raise ValueError(f"Chart missing required field: {field}")

        chart_type = chart['type']
        
        # Validate based on chart type
        if chart_type == 'bar':
            required_fields = ['x_field', 'y_field']
        elif chart_type == 'pie':
            required_fields = ['labels_field', 'values_field']
        elif chart_type == 'line':
            required_fields = ['x_field', 'y_field']
        elif chart_type == 'scatter':
            required_fields = ['x_field', 'y_field']
        elif chart_type == 'time_series':
            required_fields = ['time_field', 'value_field']
        elif chart_type == 'statistics':
            required_fields = ['value_field']
        elif chart_type == 'gauge':
            required_fields = ['value_field']
        elif chart_type == 'table':
            required_fields = []  # No required fields for table, columns are optional
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        for field in required_fields:
            if field not in chart:
                raise ValueError(f"Chart of type '{chart_type}' missing required field: {field}")

    def _validate_layout(self, layout: Dict[str, Any]) -> None:
        """Validate the layout specification"""
        required_fields = ['rows', 'columns']
        for field in required_fields:
            if field not in layout:
                raise ValueError(f"Layout missing required field: {field}")

        if not isinstance(layout['rows'], int) or layout['rows'] < 1:
            raise ValueError("'rows' must be a positive integer")

        if not isinstance(layout['columns'], int) or layout['columns'] < 1:
            raise ValueError("'columns' must be a positive integer") 