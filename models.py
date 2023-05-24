import re
from pydantic import BaseModel, validator


class News(BaseModel):
    """
    Model representing a news item.
    """

    title: str
    date: str
    search_phrase: str
    description: str = None
    filename: str = None
    count: int = None
    contains_amount: bool = False

    @validator('count')
    def get_keyword_counts(cls, count: int, values: dict):
        """
        Calculates the count of occurrences of the search phrase in the news title.

        Returns:
            int: The updated count of keyword occurrences.
        """
        title = values.get('title')
        search_phrase = values.get('search_phrase')
        count = title.count(search_phrase)
        return count

    @validator('contains_amount')
    def check_contains_amount(cls, contains_amount: bool, values: dict):
        """
        Checks if the news title or description contains a monetary amount.

        Returns:
            bool: True if the news contains an amount, False otherwise.
        """
        title = values.get('title')
        description = values.get('description')
        pattern = r'\\$\d+\.?\d*|\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\b\d+\s+dollars\b|\b\d+\s+USD\b'
        match = re.search(pattern, title + ' ' + description)
        if match:
            return True
        else:
            return False
