# stock_tool.py
# Author: Noah Chavez


class StockLookup:
    """A tool that knows how many of each product are in stock."""

    def __init__(self, stock_counts):
        """Store the stock counts this tool can look up."""
        self.stock_counts = stock_counts

    def find_product(self, text):
        """Return the first known product mentioned in text, or None."""
        for product in self.stock_counts:
            if product in text.lower():
                return product
        return None

    def count_for(self, product):
        """Return how many of one product are in stock."""
        return self.stock_counts[product]
