SCENARIO = {
    "host": "http://gateway:8080",
    "stages": [
        {"duration_s": 1800, "users": 50, "spawn_rate": 5},
    ],
    "endpoints": {
        "POST /api/orders": 70,
        "GET /api/inventory/SKU-001": 20,
        "GET /api/orders/seed-order-001": 10,
    },
}
