from sentinel.infrastructure.database import (
    Base,
    create_engine,
    create_session_factory,
)


def test_create_engine() -> None:
    engine = create_engine(
        "postgresql+asyncpg://test:test@localhost/testdb",
    )

    assert engine is not None

    engine.sync_engine.dispose()


def test_create_session_factory() -> None:
    engine = create_engine(
        "postgresql+asyncpg://test:test@localhost/testdb",
    )

    session_factory = create_session_factory(engine)

    assert session_factory is not None

    engine.sync_engine.dispose()


def test_base_contains_event_model() -> None:
    table_names = set(Base.metadata.tables.keys())

    assert "security_events" in table_names


def test_base_contains_evaluation_model() -> None:
    table_names = set(Base.metadata.tables.keys())

    assert "evaluations" in table_names