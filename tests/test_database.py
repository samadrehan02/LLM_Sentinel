from sentinel.infrastructure.database import (
    Base,
    create_engine,
    create_session_factory,
    create_tables,
    drop_tables,
)


def test_create_engine():
    engine = create_engine(
        "postgresql+asyncpg://test:test@localhost/testdb",
    )

    assert engine is not None

    engine.sync_engine.dispose()


def test_create_session_factory():
    engine = create_engine(
        "postgresql+asyncpg://test:test@localhost/testdb",
    )

    session_factory = create_session_factory(engine)

    assert session_factory is not None

    engine.sync_engine.dispose()


def test_base_contains_event_model():
    table_names = set(
        Base.metadata.tables.keys(),
    )

    assert "security_events" in table_names