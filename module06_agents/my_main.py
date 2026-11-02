# my_main.py
# Author: Noah Chavez

from my_assistant import RepairHelper
from my_tool import RepairBoard

TICKETS = {
    "R101": "in the repair stand",
    "R102": "ready for pickup",
    "R103": "waiting on a part",
}

repair_board = RepairBoard(TICKETS)
helper = RepairHelper("Gears", repair_board)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
