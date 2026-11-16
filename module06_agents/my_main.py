# my_main.py
# Author: Noah Chavez

from my_assistant import RepairHelper
from my_tool import RepairBoard
from ollama_model import OllamaModel
from repair_toolbox import RepairToolbox
from rush_queue import RushQueue

TICKETS = {
    "R101": "in the repair stand",
    "R102": "ready for pickup",
    "R103": "waiting on a part",
}

INSTRUCTIONS = """You are Gears, an assistant for a bike repair shop.
Answer in one short sentence.
If the customer only says hello, greet them and ask how you can help.
The shop is at 12 Main Street.
Bring your claim ticket when you pick up your bike.
To request a rush you need the ticket ID and the customer's full name.
Only state facts that appear in these instructions or in tool results.
If you do not know, say you do not know and offer to pass the customer to the shop manager."""

repair_board = RepairBoard(TICKETS)
rush_queue = RushQueue(repair_board)
tools = RepairToolbox(repair_board, rush_queue)
model = OllamaModel("granite4.1:3b")
helper = RepairHelper("Gears", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")

print("Shop manager review")
for entry in rush_queue.waiting():
    number = entry["number"]
    print(f"Rush request {number}: {entry['customer']}, ticket {entry['ticket']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(rush_queue.approve(number))
    else:
        print(rush_queue.reject(number))

print(f"Repairs rushed: {len(rush_queue.rushed)}")
