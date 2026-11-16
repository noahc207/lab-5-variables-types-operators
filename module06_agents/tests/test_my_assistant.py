# test_my_assistant.py
# Author: Noah Chavez

from fake_model import FakeModel
from my_assistant import RepairHelper
from my_tool import RepairBoard
from repair_toolbox import RepairToolbox
from rush_queue import RushQueue


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_helper(model):
    """Build a fresh helper with its own tools and the model it is given."""
    board = RepairBoard({"R101": "in the repair stand", "R102": "ready for pickup"})
    queue = RushQueue(board)
    return RepairHelper("Gears", "Be clear.", RepairToolbox(board, queue), model)


def rush(ticket, customer):
    """Build the decision a model returns when it wants a rush request."""
    return {
        "tool": "request_rush",
        "arguments": {"ticket": ticket, "customer": customer},
    }


def test_model_can_ask_for_a_status():
    model = FakeModel(
        [
            {"tool": "check_status", "arguments": {"ticket": "R102"}},
            {"text": "It is ready."},
        ]
    )
    helper = make_helper(model)
    helper.respond("Is R102 ready?")
    assert helper.history[1]["content"] == "Ticket R102 is ready for pickup."


def test_rush_request_waits_for_the_manager():
    model = FakeModel([rush("R101", "Dana Cruz"), {"text": "Sent."}])
    helper = make_helper(model)
    helper.respond("Please rush R101, my name is Dana Cruz")
    assert len(helper.tools.rush_queue.waiting()) == 1
    assert helper.tools.rush_queue.rushed == []


def test_made_up_name_is_refused():
    model = FakeModel([rush("R101", "Jane Doe"), {"text": "Name?"}])
    helper = make_helper(model)
    helper.respond("Please rush R101")
    assert "never typed that name" in helper.history[1]["content"]
    assert helper.tools.rush_queue.waiting() == []


def test_approval_rushes_a_repair_only_once():
    board = RepairBoard({"R101": "in the repair stand"})
    queue = RushQueue(board)
    queue.request_rush("R101", "Dana Cruz")
    queue.approve(1)
    queue.approve(1)
    assert queue.rushed == ["R101"]


def test_refund_goes_to_the_shop_manager():
    helper = make_helper(FakeModel([]))
    assert "shop manager" in helper.respond("I want a refund")


def test_safe_reply_when_the_model_has_no_answer():
    helper = make_helper(SilentModel())
    assert "try again" in helper.respond("do you sell helmets")


def test_history_grows_by_two_each_turn():
    model = FakeModel([{"text": "Hi!"}, {"text": "Sure."}])
    helper = make_helper(model)
    helper.respond("hello")
    helper.respond("thanks")
    assert len(helper.history) == 4
