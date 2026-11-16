# repair_toolbox.py
# Author: Noah Chavez


class RepairToolbox:
    """Every tool request from the model passes through this one checked door."""

    def __init__(self, repair_board, rush_queue):
        """Hold the tools the model may ask for."""
        self.repair_board = repair_board
        self.rush_queue = rush_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [self.repair_board.check_status, self.rush_queue.request_rush]

    def run(self, name, arguments, history):
        """Check one request. Run the tool only if every check passes."""
        if name == "check_status":
            ticket = self.clean(arguments, "ticket")
            if ticket == "":
                return "The ticket ID is missing. Ask the customer for it."
            if not self.customer_typed(history, ticket):
                return "The customer never typed that ticket ID. Ask them for it."
            return self.repair_board.check_status(ticket)
        if name == "request_rush":
            ticket = self.clean(arguments, "ticket")
            customer = self.clean(arguments, "customer")
            if ticket == "" or customer == "":
                return "Both the ticket ID and the customer's name are needed."
            if not self.customer_typed(history, ticket):
                return "The customer never typed that ticket ID. Ask them for it."
            if not self.customer_typed(history, customer):
                return "The customer never typed that name. Ask them for it."
            return self.rush_queue.request_rush(ticket, customer)
        return f"No tool called {name} exists here."

    def clean(self, arguments, key):
        """Return one argument as trimmed text, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_typed(self, history, text):
        """Return True if text appears in something the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
