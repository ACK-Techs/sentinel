SCENARIO = {
    "host": "http://gateway:8080",
    "stages": [
        {"duration_s": 1800, "users": 10, "spawn_rate": 1},
        {"duration_s": 1800, "users": 30, "spawn_rate": 2},
        {"duration_s": 1800, "users": 60, "spawn_rate": 3},
        {"duration_s": 1800, "users": 80, "spawn_rate": 4},
    ],
    "endpoints": {
        "POST /api/orders": 60,
        "GET /api/inventory/SKU-001": 30,
        "GET /api/orders/seed-order-001": 10,
    },
}
