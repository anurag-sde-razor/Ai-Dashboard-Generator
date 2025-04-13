import pandas as pd
import PyPDF2
from typing import Union, Dict, Any
import requests
from io import StringIO, BytesIO

class DataLoader:
    @staticmethod
    def load_csv(file_path: Union[str, BytesIO]) -> pd.DataFrame:
        """Load data from CSV file"""
        return pd.read_csv(file_path)

    @staticmethod
    def load_excel(file_path: Union[str, BytesIO]) -> pd.DataFrame:
        """Load data from Excel file"""
        return pd.read_excel(file_path)

    @staticmethod
    def load_pdf(file_path: Union[str, BytesIO]) -> pd.DataFrame:
        """Load data from PDF file"""
        # TODO: Implement PDF data extraction
        # This is a placeholder - actual implementation would need
        # more sophisticated PDF parsing logic
        pdf_reader = PyPDF2.PdfReader(file_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return pd.DataFrame({'text': [text]})

    @staticmethod
    def load_from_api(url: str, params: Dict[str, Any] = None) -> pd.DataFrame:
        """Load data from API endpoint"""
        response = requests.get(url, params=params)
        response.raise_for_status()
        return pd.read_json(StringIO(response.text))

    @staticmethod
    def load_data(file_path: Union[str, BytesIO], file_type: str = None) -> pd.DataFrame:
        """Load data from various file types"""
        # Handle Streamlit uploaded file
        if hasattr(file_path, 'name'):
            file_type = file_path.name.split('.')[-1].lower()
        elif file_type is None and isinstance(file_path, str):
            file_type = file_path.split('.')[-1].lower()

        loaders = {
            'csv': DataLoader.load_csv,
            'xlsx': DataLoader.load_excel,
            'xls': DataLoader.load_excel,
            'pdf': DataLoader.load_pdf
        }

        if file_type not in loaders:
            raise ValueError(f"Unsupported file type: {file_type}")

        return loaders[file_type](file_path) 