# AI Dashboard Generator

Transform your data into beautiful dashboards using natural language! This application uses AI to understand your dashboard requirements and automatically generates interactive visualizations.

## Features

- 📊 Natural language dashboard specification
- 🤖 AI-powered chart type suggestion
- 📈 Multiple chart types (bar, line, pie, scatter)
- 📁 Support for various data sources (CSV, Excel, PDF)
- 🎨 Interactive and responsive visualizations
- 🔄 Real-time dashboard updates

## Tech Stack

- Python
- Streamlit (Web interface)
- Pandas/NumPy (Data handling)
- Plotly (Interactive charts)
- Google Generative AI (Gemini)
- LangChain (LLM interaction)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-dashboard-generator.git
cd ai-dashboard-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload your data file (CSV, Excel, or PDF)
2. Describe your dashboard requirements in natural language
3. Click "Generate Dashboard" to create your visualization
4. Interact with the generated charts and filters

## Example Specification

```
I want a sales dashboard that includes a bar chart showing sales per product category, grouped by region. 
Also add a pie chart to show total sales by region.

The data will come from a CSV file I will upload. I want filters for region and product category.

The layout should be 2 charts side by side on the top row.
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 