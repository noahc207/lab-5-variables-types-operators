# rush_queue.py
# Author: Noah Chavez


class RushQueue:
    """Rush requests waiting for the shop manager. No repair moves until approval."""

    def __init__(self, repair_board):
        """Start with no requests and no rushed repairs."""
        self.repair_board = repair_board
        self.requests = []
        self.rushed = []

    def request_rush(self, ticket, customer):
        """Ask the shop manager to move one repair to the front of the line.

        Args:
            ticket: The ticket ID, like R101.
            customer: The customer's full name.
        """
        ticket_id = self.repair_board.find_ticket(ticket)
        if ticket_id is None:
            return "No ticket matched that ID. Ticket IDs look like R101."
        number = len(self.requests) + 1
        self.requests.append(
            {
                "number": number,
                "ticket": ticket_id,
                "customer": customer,
                "state": "waiting",
            }
        )
        return f"Rush request {number} was sent to the shop manager. No repair has been moved yet."

    def waiting(self):
        """Return the requests that still need a decision."""
        return [entry for entry in self.requests if entry["state"] == "waiting"]

    def find(self, number):
        """Return the request with this number, or None."""
        for entry in self.requests:
            if entry["number"] == number:
                return entry
        return None

    def approve(self, number):
        """Approve one waiting request. This is the only place a repair gets rushed."""
        entry = self.find(number)
        if entry is None:
            return f"There is no rush request {number}."
        if entry["state"] != "waiting":
            return f"Rush request {number} is already {entry['state']}."
        entry["state"] = "approved"
        self.rushed.append(entry["ticket"])
        return f"Rush request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is rushed."""
        entry = self.find(number)
        if entry is None:
            return f"There is no rush request {number}."
        if entry["state"] != "waiting":
            return f"Rush request {number} is already {entry['state']}."
        entry["state"] = "rejected"
        return f"Rush request {number} rejected."
