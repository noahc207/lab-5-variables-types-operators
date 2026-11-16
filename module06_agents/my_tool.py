# my_tool.py
# Author: Noah Chavez


class RepairBoard:
    """A tool that knows the status of each repair ticket at a bike shop."""

    def __init__(self, tickets):
        """Store the tickets this tool can look up."""
        self.tickets = tickets

    def find_ticket(self, text):
        """Return the first known ticket ID mentioned in text, or None."""
        for ticket_id in self.tickets:
            if ticket_id.lower() in text.lower():
                return ticket_id
        return None

    def status_for(self, ticket_id):
        """Return the status for one ticket, or None if it is unknown."""
        return self.tickets.get(ticket_id)

    def looks_like_ticket(self, text):
        """Return True if any word looks like a ticket ID such as R999."""
        for word in text.split():
            word = word.strip("?.,!")
            if len(word) == 4 and word[0].lower() == "r" and word[1:].isdigit():
                return True
        return False

    def check_status(self, ticket):
        """Look up the status of one repair ticket.

        Args:
            ticket: The ticket ID, like R101.
        """
        ticket_id = self.find_ticket(ticket)
        if ticket_id is None:
            return "No ticket matched that ID. Ticket IDs look like R101."
        return f"Ticket {ticket_id} is {self.status_for(ticket_id)}."
