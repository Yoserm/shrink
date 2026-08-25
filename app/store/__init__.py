from .base import Store


def get_store(settings) -> Store:
    match settings.store:
        case "sqlite":
            from .sqlite import SqliteStore
            return SqliteStore(settings)

        case "postgres":
            from .postgres import PostgresStore
            return PostgresStore(settings)

        case "table":
            from .table import TableStore
            return TableStore(settings)

        case other:
            raise ValueError(f"unknown SHRINK_STORE: {other!r}")