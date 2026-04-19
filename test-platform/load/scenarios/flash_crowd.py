SCENARIO = {
    "host": "http://gateway:8080",
    "stages": [
        {"duration_s": 180, "users": 20, "spawn_rate": 2},
        {"duration_s": 300, "users": 100, "spawn_rate": 10},
        {"duration_s": 300, "users": 20, "spawn_rate": 4},
    ],
    "endpoints": {
        "POST /api/orders": 75,
        "GET /api/inventory/SKU-001": 15,
        "GET /api/orders/seed-order-001": 10,
    },
}
