"""
ingestor.py

This module provides functionality to ingest quotes
from various file formats.
"""

import os
import subprocess
import shutil  # Added import for shutil
from typing import List
from abc import ABC, abstractmethod
import pandas as pd
from docx import Document
from QuoteEngine.quote_model import QuoteModel


class IngestorInterface(ABC):
    """Class to ingest quotes from different file formats."""
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Determine if the ingestor can ingest the specified file type."""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the specified file and return a list of QuoteModel objects."""


class TextIngestor(IngestorInterface):
    """Class to ingest quotes from txt file formats."""
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as file:  # Specify encoding
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split('-')
                        if len(parts) == 2:
                            body = parts[0].strip()
                            author = parts[1].strip()
                            quotes.append(QuoteModel(body, author))
        except FileNotFoundError:
            print(f"File not found: {path}")
        except IOError as error:  # Renamed variable
            print(f"I/O error occurred: {error}")
        return quotes


class CSVIngestor(IngestorInterface):
    """Class to ingest quotes from csv file formats."""
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        dataframe = pd.read_csv(path)
        for _, row in dataframe.iterrows():  # Use underscore for unused index
            quotes.append(QuoteModel(row['body'], row['author']))
        return quotes


class DocxIngestor(IngestorInterface):
    """Class to ingest quotes from docx file formats."""
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        try:
            doc = Document(path)
            for paragraph in doc.paragraphs:
                line = paragraph.text.strip()
                if line:
                    parts = line.split('-')
                    if len(parts) == 2:
                        body = parts[0].strip()
                        author = parts[1].strip()
                        quotes.append(QuoteModel(body, author))
        except FileNotFoundError as error:
            print(f"File not found: {error}")
        except ValueError as error:
            print(f"Value error: {error}")
        return quotes


class PDFIngestor(IngestorInterface):
    """Class to ingest quotes from pdf file formats."""
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        temp_text_file = path.replace('.pdf', '.txt')  # Temporary text file name
        if not shutil.which('pdftotext'):
            print("pdftotext command not found. Please install it to use PDF ingestion.")
            return []

        # Step 1: Use pdftotext to convert PDF to text
        command = ['pdftotext', path, temp_text_file]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as error:
            print(f"An error occurred while processing the PDF: {error}")
            return []

        # Step 2: Read the text from the temporary file
        with open(temp_text_file, 'r', encoding='utf-8') as file:  # Specify encoding
            text = file.read()
            lines = text.splitlines()
            for line in lines:
                # Assuming quotes are in the format "Quote - Author"
                if ' - ' in line:
                    body, author = line.rsplit(' - ', 1)
                    quotes.append(QuoteModel(body.strip(), author.strip()))

        # Step 3: Clean up the temporary text file
        os.remove(temp_text_file)

        return quotes


class Ingestor:
    """Class to ingest quotes from all ingestor formats."""
    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """ parse the path" """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        print(f"No ingestor found for the file type of {path}")
        return []
