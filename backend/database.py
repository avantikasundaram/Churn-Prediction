import os
import datetime
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def get_db():
    """Return a live MongoDB database connection, or raise with a helpful message."""
    global _client, _db
    if _db is not None:
        return _db

    uri = os.getenv("MONGO_URI", "").strip()
    db_name = os.getenv("MONGO_DB_NAME", "").strip()

    if not uri:
        raise RuntimeError(
            "MONGO_URI is missing. Add your MongoDB Atlas URI in backend/.env."
        )
    if not (uri.startswith("mongodb://") or uri.startswith("mongodb+srv://")):
        raise RuntimeError(
            "Invalid MONGO_URI. It must start with mongodb:// or mongodb+srv://"
        )

    try:
        _client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=300000,
            maxPoolSize=80,
            retryWrites=True,
        )
        _client.admin.command("ping")
    except Exception as exc:
        _client = None
        raise RuntimeError(
            f"MongoDB connection failed: {exc}\n"
            "Checklist:\n"
            "  1. Atlas Network Access → whitelist your IP or add 0.0.0.0/0 for dev.\n"
            "  2. Verify username/password in MONGO_URI.\n"
            "  3. Free-tier cluster may be paused — resume it in the Atlas console."
        ) from exc

    if db_name:
        _db = _client[db_name]
    else:
        _db = _client.get_default_database()

    _init_indexes(_db)
    print(f"[DB] ✅ Connected to MongoDB Atlas database: {_db.name}")
    return _db


def _init_indexes(db):
    indexes = [
        (db.users, [("email", ASCENDING)], {"unique": True, "name": "email_unique_idx"}),
        (db.customers, [("customer_id", ASCENDING)], {"name": "customer_id_idx"}),
        (db.customers, [("risk", ASCENDING)], {"name": "customer_risk_idx"}),
        (db.predictions, [("customer_id", ASCENDING)], {"name": "prediction_customer_idx"}),
        (db.predictions, [("created_at", ASCENDING)], {"name": "prediction_created_idx"}),
        (db.datasets, [("created_at", ASCENDING)], {"name": "dataset_created_idx"}),
        (db.settings, [("key", ASCENDING)], {"unique": True, "name": "settings_key_unique_idx"}),
    ]
    for collection, keys, options in indexes:
        try:
            collection.create_index(keys, background=True, **options)
        except Exception as exc:
            print(f"[DB] Index warning for {collection.name}: {exc}")


def require_db():
    db = get_db()
    if db is None:
        raise RuntimeError("MongoDB connection unavailable")
    return db
