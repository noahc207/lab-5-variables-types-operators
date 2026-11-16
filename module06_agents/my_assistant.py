# my_assistant.py
# Author: Noah Chavez

HANDOFF_WORDS = ["refund", "cancel", "complaint"]
MAX_TOOL_ROUNDS = 3


class RepairHelper:
    """A repair helper. The model decides. The toolbox checks every request."""

    def __init__(self, name, instructions, tools, model):
        """Set up one helper with its name, instructions, tools, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Send money matters to the shop manager. Give the rest to the model."""
        if self.needs_human(user_message.lower()):
            return "I can't handle money or cancellations. I'm passing you to the shop manager."
        return self.model_reply()

    def needs_human(self, text):
        """Return True if the message involves refunds, cancellations, or complaints."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run any tool it requests and ask again, up to a limit."""
        for _ in range(MAX_TOOL_ROUNDS):
            decision = self.model.decide(
                self.instructions, self.history, self.tools.tool_list()
            )
            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."
            if "text" in decision:
                return decision["text"]
            result = self.tools.run(
                decision["tool"], decision["arguments"], self.history
            )
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": decision["tool"],
                    "arguments": decision["arguments"],
                    "content": result,
                }
            )
        return "Sorry, I couldn't finish that. I'm passing you to the shop manager."
