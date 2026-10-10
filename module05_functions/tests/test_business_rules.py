from business_rules import (
    calculate_total,
    requires_review,
    get_approval_tier,
    apply_discount,
)


def test_requires_review_over():
    assert requires_review(1500) is True


def test_requires_review_under():
    assert requires_review(500) is False


def test_boundary_limit():
    # Exactly 1000 should NOT require review (> not >=)
    assert requires_review(1000) is False


def test_total_includes_tax():
    assert round(calculate_total(100.0, 2), 2) == 214.0


def test_tier_auto():
    assert get_approval_tier(400) == "auto"


def test_tier_boundary():
    assert get_approval_tier(1500) == "manager"


def test_tier_upper_boundary():
    assert get_approval_tier(2000) == "manager"


def test_discount_ten():
    assert round(apply_discount(100.0, 10), 2) == 90.0
