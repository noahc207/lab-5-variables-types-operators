# my_assistant.py
# Author: Noah Chavez

HANDOFF_WORDS = ["refund", "cancel", "complaint"]


class RepairHelper:
    """A mock repair-status helper. Replies come from keyword rules, not AI."""

    def __init__(self, name, repair_board):
        """Set up one helper with its own name, tool, and history."""
        self.name = name
        self.repair_board = repair_board
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't handle money or cancellations. I'm passing you to the shop manager."
        if (
            "status" in text
            or "ready" in text
            or self.repair_board.looks_like_ticket(user_message)
        ):
            return self.status_reply(user_message)
        if "hello" in text or "hi" in text.split():
            return f"Hi! I'm {self.name}. Send me a ticket ID like R101 and I'll check your repair."
        return "I'm not sure how to help with that. I can check a repair status."

    def needs_human(self, text):
        """Return True if the message involves refunds or cancellations."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def status_reply(self, user_message):
        """Use the repair board to answer a status question."""
        ticket_id = self.repair_board.find_ticket(user_message)
        if ticket_id is not None:
            return f"Ticket {ticket_id}: {self.repair_board.status_for(ticket_id)}."
        if self.repair_board.looks_like_ticket(user_message):
            return "I couldn't find that ticket. Please double check the ID."
        return "Which ticket? Please send an ID like R101."
