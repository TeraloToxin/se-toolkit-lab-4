"""Unit tests for item model edge cases."""

from app.models.item import ItemCreate, ItemUpdate, ItemRecord


class TestItemCreateEdgeCases:
    """Tests for ItemCreate schema edge cases."""

    def test_valid_item_create(self) -> None:
        """Test creating a valid ItemCreate instance."""
        item = ItemCreate(type="lab", parent_id=1, title="Test Lab", description="A test")
        assert item.type == "lab"
        assert item.parent_id == 1
        assert item.title == "Test Lab"
        assert item.description == "A test"

    def test_item_create_defaults(self) -> None:
        """Test ItemCreate uses default values for optional fields."""
        item = ItemCreate(title="Test")
        assert item.type == "step"
        assert item.parent_id is None
        assert item.description == ""

    def test_item_create_long_title(self) -> None:
        """Test ItemCreate accepts very long titles (boundary: 1000 chars)."""
        long_title = "A" * 1000
        item = ItemCreate(title=long_title)
        assert len(item.title) == 1000


class TestItemRecordEdgeCases:
    """Tests for ItemRecord database model edge cases."""

    def test_item_record_with_none_parent_id(self) -> None:
        """Test ItemRecord with None parent_id (root level item in tree)."""
        item = ItemRecord(id=1, type="course", parent_id=None, title="Course")
        assert item.parent_id is None

    def test_item_record_empty_attributes_dict(self) -> None:
        """Test ItemRecord with empty attributes dict."""
        item = ItemRecord(id=1, type="step", parent_id=None, title="Step", attributes={})
        assert item.attributes == {}

    def test_item_record_with_special_characters_in_title(self) -> None:
        """Test ItemRecord accepts special characters in title."""
        item = ItemRecord(id=1, type="step", parent_id=None, title="Test <>&\"' Title")
        assert item.title == "Test <>&\"' Title"
