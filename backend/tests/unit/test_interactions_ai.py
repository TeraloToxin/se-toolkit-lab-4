"""AI-generated unit tests for interactions."""

from datetime import datetime

import pytest
from app.models.interaction import InteractionLog, InteractionLogCreate, InteractionModel


class TestInteractionLogCreate:
    """Tests for InteractionLogCreate request schema."""

    def test_create_valid_interaction_log(self):
        """Test creating a valid interaction log."""
        log = InteractionLogCreate(learner_id=1, item_id=2, kind="view")
        assert log.learner_id == 1
        assert log.item_id == 2
        assert log.kind == "view"

    def test_create_interaction_log_with_empty_kind(self):
        """Test that empty kind string is accepted."""
        log = InteractionLogCreate(learner_id=1, item_id=1, kind="")
        assert log.kind == ""


class TestInteractionModel:
    """Tests for InteractionModel response schema."""

    def test_interaction_model_with_created_at(self):
        """Test InteractionModel correctly uses created_at field."""
        now = datetime.now()
        model = InteractionModel(
            id=1,
            learner_id=1,
            item_id=1,
            kind="attempt",
            created_at=now,
        )
        assert model.created_at == now

    def test_interaction_model_id_positive(self):
        """Test that id must be positive integer."""
        now = datetime.now()
        model = InteractionModel(
            id=1,
            learner_id=1,
            item_id=1,
            kind="view",
            created_at=now,
        )
        assert model.id > 0


class TestInteractionLog:
    """Tests for InteractionLog database model."""

    def test_interaction_log_with_null_created_at(self):
        """Test InteractionLog allows null created_at."""
        log = InteractionLog(
            learner_id=1,
            item_id=1,
            kind="click",
            created_at=None,
        )
        assert log.created_at is None

    def test_interaction_log_default_kind(self):
        """Test InteractionLog with various kind values."""
        log = InteractionLog(
            learner_id=1,
            item_id=1,
            kind="purchase",
            created_at=None,
        )
        assert log.kind == "purchase"
