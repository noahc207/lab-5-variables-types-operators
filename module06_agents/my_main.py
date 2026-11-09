# my_main.py
# Author: Noah Chavez

from my_assistant import RepairHelper
from my_tool import RepairBoard
from ollama_model import OllamaModel

TICKETS = {
    "R101": "in the repair stand",
    "R102": "ready for pickup",
    "R103": "waiting on a part",
}

INSTRUCTIONS = """You are Gears, an assistant for a bike repair shop.
Answer in one short sentence.
The shop is at 12 Main Street.
Bring your claim ticket when you pick up your bike.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to the shop manager."""

repair_board = RepairBoard(TICKETS)
model = OllamaModel("granite4.1:3b")
helper = RepairHelper("Gears", INSTRUCTIONS, repair_board, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
