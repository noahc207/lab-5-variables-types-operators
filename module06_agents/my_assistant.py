# my_assistant.py
# Author: Noah Chavez

HANDOFF_WORDS = ["refund", "cancel", "complaint"]


class RepairHelper:
    """A repair-status helper. Rules handle the repair board. A model handles the rest."""

    def __init__(self, name, instructions, repair_board, model):
        """Set up one helper with its own name, instructions, tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.repair_board = repair_board
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't handle money or cancellations. I'm passing you to the shop manager."
        if (
            "status" in text
            or "ready" in text
            or self.repair_board.looks_like_ticket(user_message)
        ):
            return self.status_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply

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
