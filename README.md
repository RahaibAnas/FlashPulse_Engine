# High-Throughput Flash Sale & Inventory Engine

A high-concurrency flash sale and inventory management system designed to handle thousands of users attempting to purchase limited-stock products simultaneously.

The primary goal is to **prevent inventory overselling while maintaining high performance and low response times during extreme traffic spikes**.

## Core Idea

During a flash sale, thousands of users may try to purchase the same product at exactly the same time.

A traditional approach that reads and updates inventory directly in PostgreSQL can create:

* Race conditions
* Inventory overselling
* Database contention
* High database load
* Slow response times

This system uses **Redis as the high-speed inventory layer** and **PostgreSQL as the persistent source of truth**.

```text
Users
  |
  v
API
  |
  v
Redis
  |
  |-- Atomic Inventory Operations
  |-- Reservations
  |-- Virtual Queue
  |
  v
Background Processing
  |
  v
PostgreSQL
```

## Main Objectives

### 1. Prevent Overselling

Inventory must never become oversold even when thousands of users submit purchase requests concurrently.

Redis performs atomic inventory operations so that stock changes are processed safely.

### 2. Reduce Database Pressure

PostgreSQL should not receive every inventory request during the flash sale.

Instead, Redis handles the high-frequency operations and inventory state is periodically synchronized with PostgreSQL.

### 3. Handle High Concurrency

The system is designed around the assumption that a large number of users may request the same limited inventory simultaneously.

The reservation decision should therefore happen in the fastest possible layer.

### 4. Use Asynchronous Processing

Operations that do not need to happen during the immediate reservation request are processed in the background.

Examples include:

* Order generation
* Inventory synchronization
* Notifications
* Reservation expiration
* Queue management

### 5. Control Traffic With a Virtual Queue

When demand exceeds the available processing capacity, users can be placed into a virtual waiting queue.

Users receive a ticket and periodically check their position/status rather than maintaining a persistent connection.

## Flash Sale Workflow

### Before the Sale

Inventory for the upcoming sale is loaded into Redis before the sale begins.

```text
PostgreSQL
    |
    v
Redis
    |
    v
Ready for Flash Sale
```

This prevents thousands of users from simultaneously requesting inventory data from PostgreSQL when the sale starts.

### During the Sale

A user attempts to reserve an item.

```text
User
 |
 v
API
 |
 v
Redis Atomic Stock Operation
 |
 +-------------------+
 |                   |
Stock Available   Stock Exhausted
 |                   |
 v                   v
Reservation       Queue / Failure
```

If stock is available, the user receives a temporary reservation.

If stock is unavailable, the request can either fail immediately or enter the virtual queue.

### Reservation Period

A successful reservation remains valid for a limited period, such as **5 minutes**.

```text
Stock Reserved
      |
      v
5-Minute Checkout Window
      |
   +--+--+
   |     |
 Paid  Expired
   |     |
   v     v
Order  Return Stock
```

### Expired Reservations

If the user does not complete payment within the reservation window:

1. The reservation expires.
2. The reserved inventory is returned to the available pool.
3. The newly available inventory can be assigned to another waiting user.

## Main Components

### Django

Acts as the API and application layer responsible for handling users, authentication, requests, reservations, orders, and business logic.

### Redis

Acts as the high-speed operational layer for:

* Live inventory counters
* Atomic stock operations
* Reservations
* Virtual queue state
* Temporary flash-sale data

### Celery

Handles background processing such as:

* Order processing
* Inventory synchronization
* Expired reservation cleanup
* Queue processing

### PostgreSQL

Stores durable business data such as:

* Users
* Products
* Flash sales
* Orders
* Payments
* Persistent inventory state

## Core Architecture Principle

```text
Redis
  =
High-Speed Operational State

PostgreSQL
  =
Persistent Business State
```

The system separates the **high-frequency flash-sale operations** from the **durable database operations**, allowing the application to handle extreme concurrency while protecting the primary database from excessive traffic.
