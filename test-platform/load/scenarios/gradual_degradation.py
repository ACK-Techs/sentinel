SCENARIO = {
    "host": "http://gateway:8080",
    "stages": [
        {"duration_s": 600, "users": 40, "spawn_rate": 3},
        {"duration_s": 600, "users": 40, "spawn_rate": 1},
    ],
    "endpoints": {
        "POST /api/orders": 65,
        "GET /api/inventory/SKU-001": 25,
        "GET /api/orders/seed-order-001": 10,
    },
}
