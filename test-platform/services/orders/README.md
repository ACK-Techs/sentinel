# orders

Order orchestration service. Calls `payments` and `inventory` in parallel, persists successful orders, caches reads, and emits Redis Streams events to `orders.events`.

