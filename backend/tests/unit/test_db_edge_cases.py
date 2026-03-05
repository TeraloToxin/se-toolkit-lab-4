"""Unit tests for database operations edge cases."""

from unittest.mock import AsyncMock, MagicMock

from app.db.items import update_item
from app.db.learners import read_learners
from app.models.item import ItemRecord
from app.models.learner import Learner


class TestUpdateItemEdgeCases:
    """Tests for update_item function edge cases."""

    def test_update_nonexistent_item_returns_none(self) -> None:
        """Test updating a non-existent item returns None."""
        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=None)

        import asyncio
        result = asyncio.run(update_item(mock_session, item_id=999, title="New", description="Desc"))

        assert result is None
        mock_session.get.assert_called_once_with(ItemRecord, 999)
        mock_session.add.assert_not_called()

    def test_update_item_with_empty_description(self) -> None:
        """Test updating an item with empty description is allowed."""
        mock_item = ItemRecord(id=1, type="step", title="Old", description="Old desc")
        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=mock_item)
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        import asyncio
        result = asyncio.run(update_item(mock_session, item_id=1, title="New", description=""))

        assert result is not None
        assert result.description == ""
        mock_session.add.assert_called_once()


class TestReadLearnersEdgeCases:
    """Tests for read_learners function edge cases."""

    def test_read_learners_with_none_enrolled_after(self) -> None:
        """Test read_learners with enrolled_after=None returns all learners."""
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = [
            Learner(id=1, name="John", email="john@example.com"),
            Learner(id=2, name="Jane", email="jane@example.com"),
        ]
        mock_session = MagicMock()
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        import asyncio
        result = asyncio.run(read_learners(mock_session, enrolled_after=None))

        assert len(result) == 2

    def test_read_learners_with_enrolled_after_filters(self) -> None:
        """Test read_learners with enrolled_after applies filter."""
        from datetime import datetime, timezone
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = [
            Learner(id=1, name="John", email="john@example.com"),
        ]
        mock_session = MagicMock()
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        import asyncio
        cutoff_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        result = asyncio.run(read_learners(mock_session, enrolled_after=cutoff_date))

        assert len(result) == 1
        mock_session.exec.assert_called_once()
