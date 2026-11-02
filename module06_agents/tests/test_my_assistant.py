# test_my_assistant.py
# Author: Noah Chavez

from my_assistant import RepairHelper
from my_tool import RepairBoard


def make_helper():
    """Build a fresh helper with its own tool for each test."""
    board = RepairBoard({"R101": "in the repair stand", "R102": "ready for pickup"})
    return RepairHelper("Gears", board)


def test_status_question_uses_the_tool():
    helper = make_helper()
    assert helper.respond("status of R102") == "Ticket R102: ready for pickup."


def test_unknown_ticket_gets_a_helpful_reply():
    helper = make_helper()
    assert "couldn't find" in helper.respond("status of R999")


def test_refund_goes_to_a_human():
    helper = make_helper()
    assert "shop manager" in helper.respond("I want a refund")


def test_unknown_request_gets_a_safe_reply():
    helper = make_helper()
    assert "not sure" in helper.respond("do you sell helmets")


def test_history_grows_by_two_each_turn():
    helper = make_helper()
    helper.respond("hello")
    helper.respond("status of R101")
    assert len(helper.history) == 4
