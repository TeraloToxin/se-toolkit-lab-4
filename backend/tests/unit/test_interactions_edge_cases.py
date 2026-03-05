"""Unit tests for interaction filtering edge cases."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_no_matches_returns_empty_list() -> None:
    """Test filtering when no interactions match the given item_id."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_multiple_matches_returns_all_matching() -> None:
    """Test filtering returns all interactions with matching learner_id."""
    interactions = [
        _make_log(1, 1, 10),
        _make_log(2, 2, 20),
        _make_log(3, 1, 30),
        _make_log(4, 3, 40),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_single_item_list_match() -> None:
    """Test filtering a single-item list when item matches."""
    interactions = [_make_log(1, 1, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_with_zero_item_id() -> None:
    """Test filtering with item_id=0 (edge case for falsy value)."""
    interactions = [_make_log(1, 0, 0), _make_log(2, 1, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1
