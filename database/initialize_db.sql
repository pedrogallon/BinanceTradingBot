CREATE TABLE price_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL,
    symbol TEXT,
    price REAL,
    delta REAL
)
