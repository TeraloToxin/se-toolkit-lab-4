"""Unit tests for learner model edge cases."""

from app.models.learner import Learner, LearnerCreate


class TestLearnerCreateEdgeCases:
    """Tests for LearnerCreate schema edge cases."""

    def test_valid_learner_create(self) -> None:
        """Test creating a valid LearnerCreate instance."""
        learner = LearnerCreate(name="John Doe", email="john@example.com")
        assert learner.name == "John Doe"
        assert learner.email == "john@example.com"

    def test_learner_create_long_name(self) -> None:
        """Test LearnerCreate accepts very long names (boundary: 500 chars)."""
        long_name = "A" * 500
        learner = LearnerCreate(name=long_name, email="test@example.com")
        assert len(learner.name) == 500


class TestLearnerModelEdgeCases:
    """Tests for Learner database model edge cases."""

    def test_learner_with_none_enrolled_at(self) -> None:
        """Test Learner model with None enrolled_at (optional field)."""
        learner = Learner(id=1, name="John", email="john@example.com", enrolled_at=None)
        assert learner.enrolled_at is None

    def test_learner_without_enrolled_at_uses_default(self) -> None:
        """Test Learner model defaults enrolled_at to None."""
        learner = Learner(id=1, name="John", email="john@example.com")
        assert learner.enrolled_at is None

    def test_learner_with_special_characters_in_name(self) -> None:
        """Test Learner model accepts special characters in name."""
        learner = Learner(id=1, name="John <>&\"' Doe", email="test@example.com")
        assert learner.name == "John <>&\"' Doe"
