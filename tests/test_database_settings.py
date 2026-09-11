from sentinel.infrastructure.settings import DatabaseSettings


def test_database_settings_has_default_url():
    settings = DatabaseSettings()

    assert settings.database_url.startswith(
        "postgresql+asyncpg://"
    )


def test_database_settings_reads_environment_variable(
    monkeypatch,
):
    monkeypatch.setenv(
        "SENTINEL_DATABASE_URL",
        "postgresql+asyncpg://test:test@localhost/testdb",
    )

    settings = DatabaseSettings()

    assert settings.database_url == (
        "postgresql+asyncpg://test:test@localhost/testdb"
    )