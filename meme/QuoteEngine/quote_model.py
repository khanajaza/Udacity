"""
quote_model.py

This module defines the QuoteModel class for representing quotes with authors.
"""

class QuoteModel:
    """Class representing a quote with its author."""

    def __init__(self, body: str, author: str):
        """Initialize a QuoteModel instance.

        Args:
            body (str): The text of the quote.
            author (str): The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return a string representation of the quote."""
        return f'"{self.body}" - {self.author}'
