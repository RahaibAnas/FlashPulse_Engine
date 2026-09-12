# ⚡ High-Throughput E-Commerce Flash Sale & Inventory Engine

A production-oriented Django REST API designed to handle **high-concurrency flash sales**, prevent **inventory overselling**, and process checkout workflows asynchronously.

The project is being built incrementally, starting with a clean Django/DRF foundation and evolving toward a distributed architecture using **PostgreSQL, Redis, Celery, Docker, and Nginx**.

> **Project Status:** 🚧 In Development — Phase 1
> **Current Database:** SQLite
> **Target Database:** PostgreSQL

---

## 🎯 Project Goal

Traditional e-commerce APIs can struggle when thousands of users attempt to purchase a limited-stock product simultaneously.

This project focuses on solving the backend problems that appear during flash-sale traffic spikes:

* Concurrent inventory requests
* Race conditions
* Overselling
* Duplicate order requests
* Database contention
* Slow checkout operations
* Background processing
* Inventory reservation and expiration
* API rate limiting
* Caching and atomic counters
* Production deployment

The final architecture will combine **database-level concurrency control**, **Redis atomic operations**, and **asynchronous task processing**.

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         │ Web / Mobile/API │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Nginx       │
                         │ Reverse Proxy    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Django + DRF     │
                         │ REST API         │
                         └───────┬──────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
             PostgreSQL       Redis         Celery
             Primary DB      Cache/Lock     Workers
                  │              │              │
                  │              │              ▼
                  │              │        Background Jobs
                  │              │
                  └──────────────┴──────────────┐
                                                 │
                                                 ▼
                                          Order / Inventory
                                            Processing
```

### Current Phase

```text
Client
  │
  ▼
Django + DRF
  │
  ▼
SQLite
```

### Target Architecture

```text
Client
  │
  ▼
Nginx
  │
  ▼
Django + DRF
  │
  ├──────────────► PostgreSQL
  │
  ├──────────────► Redis
  │                    │
  │                    └──── Atomic inventory operations
  │
  └──────────────► Celery
                       │
                       └──── Background processing
```

---

# 🛠️ Tech Stack

| Technology            | Purpose                                 |
| --------------------- | --------------------------------------- |
| Python 3.11+          | Backend programming language            |
| Django 5.x            | Web framework                           |
| Django REST Framework | REST API                                |
| SimpleJWT             | JWT authentication                      |
| SQLite                | Development database                    |
| PostgreSQL            | Production relational database          |
| Redis                 | Caching and atomic inventory operations |
| Celery                | Background task processing              |
| Celery Beat           | Scheduled background tasks              |
| Docker                | Containerization                        |
| Docker Compose        | Multi-service orchestration             |
| Nginx                 | Reverse proxy                           |
| python-decouple       | Environment-based configuration         |

---

# 📦 Domain Architecture

The project is divided into separate Django applications based on business responsibilities.

```text
flash_sale_engine/
│
├── apps/
│   │
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── catalog/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── flash_sales/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── ...
│   │
│   └── orders/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

### Application Responsibilities

#### `users`

Responsible for:

* Custom user model
* UUID user IDs
* Email authentication
* User roles
* JWT authentication
* User profile API

#### `catalog`

Responsible for:

* Categories
* Products
* Base product information
* Base inventory

#### `flash_sales`

Responsible for:

* Flash-sale events
* Flash-sale pricing
* Allocated inventory
* Inventory reservations
* Sale time windows
* Sale status

#### `orders`

Responsible for:

* Order creation
* Order lifecycle
* Payment state
* Idempotency
* Order expiration
* Inventory reservation tracking

---

# 🗄️ Database Design

## User

```text
User
├── id              UUID PK
├── email           UNIQUE
├── first_name
├── last_name
├── role
├── is_active
├── created_at
└── updated_at
```

Roles:

```text
CUSTOMER
ADMIN
```

---

## Category

```text
Category
├── id              BigAutoField PK
├── name
└── slug            UNIQUE
```

---

## Product

```text
Product
├── id              UUID PK
├── category        FK → Category
├── name
├── slug            UNIQUE
├── description
├── base_price
├── base_stock
├── is_active
└── created_at
```

---

## Flash Sale

Planned model:

```text
FlashSaleItem
├── id
├── product
├── flash_price
├── allocated_stock
├── reserved_stock
├── start_time
├── end_time
└── status
```

Possible statuses:

```text
SCHEDULED
ACTIVE
ENDED
SOLD_OUT
```

> **Design note:** if a product can participate in multiple flash-sale events, `product` should normally be a `ForeignKey`, not a `OneToOneField`. A `OneToOneField` would allow each product to have only one flash-sale record for its entire lifetime.

---

## Order

Planned model:

```text
Order
├── id
├── user
├── flash_sale_item
├── total_amount
├── status
├── idempotency_key
└── expires_at
```

Order states:

```text
PENDING_PAYMENT
PAID
CANCELLED
EXPIRED
```

---

# 🔐 Authentication

The API uses **JWT authentication** through SimpleJWT.

Authentication flow:

```text
Register
   │
   ▼
Login with email/password
   │
   ▼
Access + Refresh tokens
   │
   ├── Access Token → API requests
   │
   └── Refresh Token → New Access Token
```

Protected requests use:

```http
Authorization: Bearer <access_token>
```

---

# 📡 API Endpoints

## Authentication

| Method | Endpoint                    | Description           | Authentication |
| ------ | --------------------------- | --------------------- | -------------- |
| POST   | `/api/users/register/`      | Register a new user   | No             |
| POST   | `/api/users/login/`         | Login a user          | No             |
| POST   | `/api/users/logout/`        | logout a user         | Yes            |
| POST   | `/api/users/token/`         | Obtain JWT tokens     | No             |
| POST   | `/api/users/token/refresh/` | Refresh access token  | No             |
| GET    | `/api/users/profile/`       | Retrieve current user | Yes            |

---

# 📝 API Examples

## Register

### Request

```http
POST /api/v1/users/register/
Content-Type: application/json
```

```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "first_name": "Rahaib",
    "last_name": "Anas"
}
```

### Response

```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "user@example.com",
    "first_name": "Rahaib",
    "last_name": "Anas",
    "role": "CUSTOMER"
}
```

---

## Login

### Request

```http
POST /api/v1/users/token/
Content-Type: application/json
```

```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}
```

### Response

```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

## Current User

### Request

```http
GET /api/v1/users/me/
Authorization: Bearer <access_token>
```

### Response

```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "user@example.com",
    "first_name": "Rahaib",
    "last_name": "Anas",
    "role": "CUSTOMER"
}
```

---


# 🧪 Testing

Testing will be expanded throughout the project.

Planned coverage includes:

* User registration
* Authentication
* Permissions
* Product APIs
* Flash-sale APIs
* Order creation
* Inventory allocation
* Idempotency
* Concurrent purchase requests
* Order expiration
* Celery tasks
* Redis operations

The final system will specifically test concurrency scenarios where multiple requests attempt to purchase the last available units.

---

# 📈 Development Roadmap

## Phase 1 — Core API & Domain Setup

**Status: ✅ In Progress / Development**

* [x] Custom User model
* [x] UUID user IDs
* [x] Email-based authentication
* [x] User roles
* [x] JWT authentication
* [x] User registration
* [x] Current-user endpoint
* [x] Category model
* [x] Product model
* [x] Development environment

---

## Phase 2 — PostgreSQL & Transactional Inventory

**Status: ⏳ Planned**

Move from SQLite to PostgreSQL.

### Goals

* [ ] PostgreSQL configuration
* [ ] Environment-based database configuration
* [ ] FlashSaleItem model
* [ ] Order model
* [ ] Database constraints
* [ ] Transactions with `transaction.atomic()`
* [ ] Row-level locking
* [ ] `select_for_update()`
* [ ] Inventory reservation
* [ ] Order state transitions
* [ ] Idempotent order creation

### Core concurrency concept

```python
with transaction.atomic():
    item = (
        FlashSaleItem.objects
        .select_for_update()
        .get(id=flash_sale_item_id)
    )

    # Validate inventory
    # Reserve stock
    # Create order
```

The goal is to make inventory allocation safe when multiple transactions compete for the same stock.

---

# Phase 3 — Celery & Redis

**Status: ⏳ Planned**

Introduce asynchronous processing.

### Celery

Background jobs will handle operations such as:

```text
Order
  │
  ├── Payment simulation
  ├── Receipt generation
  └── Notification processing
```

### Celery Beat

Scheduled tasks will handle:

* Expired orders
* Unreleased reservations
* Flash-sale status updates
* Periodic cleanup jobs

---

# Phase 4 — Redis & High-Speed Inventory Protection

**Status: ⏳ Planned**

Redis will be introduced for operations that should not require PostgreSQL for every request.

Planned functionality:

* [ ] Redis caching
* [ ] Atomic inventory counters
* [ ] `DECR` / atomic decrement operations
* [ ] Cache invalidation
* [ ] Inventory protection
* [ ] DRF throttling
* [ ] Request rate limiting
* [ ] Hot-product optimization

Conceptually:

```text
Incoming Purchase Request
          │
          ▼
     Redis Counter
          │
     ┌────┴────┐
     │         │
   Stock > 0  Stock <= 0
     │         │
     ▼         ▼
 Continue    Reject
     │
     ▼
 PostgreSQL
```

Redis will act as a **fast protection layer**, while PostgreSQL remains responsible for durable transactional state.

---

# Phase 5 — Docker & Production Architecture

**Status: ⏳ Planned**

The application will eventually run as multiple services:

```text
┌─────────────────────────────────────────────┐
│              Docker Compose                 │
│                                             │
│  ┌──────────┐                               │
│  │  Nginx   │                               │
│  └────┬─────┘                               │
│       │                                      │
│  ┌────▼─────┐       ┌──────────────┐        │
│  │  Django  │──────►│ PostgreSQL   │        │
│  └────┬─────┘       └──────────────┘        │
│       │                                      │
│       ├──────────────► Redis                 │
│       │                                      │
│       ▼                                      │
│  ┌────────────┐                              │
│  │   Celery   │                              │
│  │   Worker   │                              │
│  └─────┬──────┘                              │
│        │                                     │
│        ▼                                     │
│  ┌────────────┐                              │
│  │ Celery Beat│                              │
│  └────────────┘                              │
│                                             │
└─────────────────────────────────────────────┘
```

Planned production concerns:

* [ ] Dockerfile
* [ ] Docker Compose
* [ ] PostgreSQL container
* [ ] Redis container
* [ ] Celery worker
* [ ] Celery Beat
* [ ] Nginx
* [ ] Gunicorn
* [ ] HTTPS/TLS
* [ ] Static/media storage
* [ ] Production secrets
* [ ] Health checks
* [ ] Logging
* [ ] Monitoring

---

# 🔥 Concurrency & Overselling Problem

The central engineering problem is:

> What happens when 10,000 users attempt to purchase 100 available items at nearly the same time?

A naive implementation can produce:

```text
Request A → stock = 1
Request B → stock = 1
Request C → stock = 1

A → purchase
B → purchase
C → purchase

Result:
Stock becomes negative or more units are sold than actually exist.
```

The project progressively introduces stronger mechanisms to solve this.

### Layer 1 — Database Transactions

```text
transaction.atomic()
```

Provides transactional consistency.

### Layer 2 — Row-Level Locking

```text
select_for_update()
```

Prevents competing database transactions from modifying the same inventory row simultaneously.

### Layer 3 — Redis Atomic Operations

```text
DECR
```

Allows extremely fast atomic inventory checks before expensive database operations.

### Layer 4 — Idempotency

```text
Idempotency-Key
```

Prevents accidental duplicate order creation when clients retry requests.

---

# 🔑 Idempotency

A client may accidentally send the same purchase request multiple times:

```text
Client
  │
  ├── Request 1 ──► API
  │
  └── Request 2 ──► API
```

Without idempotency:

```text
1 request
   ↓
2 orders
```

With an idempotency key:

```text
Request
   │
   ▼
Idempotency Key
   │
   ├── New → Process order
   │
   └── Existing → Return previous result
```

Example:

```http
POST /api/v1/orders/

Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

---

# 🔄 Order Lifecycle

```text
                ┌──────────────────┐
                │     PENDING      │
                │     PAYMENT      │
                └────────┬─────────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
             PAID             EXPIRED
                │
                │
                ▼
             COMPLETED
```

Cancellation can occur before payment completion:

```text
PENDING_PAYMENT
       │
       ▼
   CANCELLED
```

The exact state machine and allowed transitions will be enforced at the application level.

---

# 🧩 Engineering Concepts Demonstrated

This project is intended to demonstrate practical backend engineering rather than simply CRUD development.

### Django

* Custom User Models
* Models and relationships
* Managers
* Admin customization
* Environment configuration
* Transactions
* Database constraints

### Django REST Framework

* Serializers
* APIViews
* Generic Views
* ViewSets
* Routers
* Authentication
* Permissions
* Throttling
* Pagination
* Filtering
* Error handling

### PostgreSQL

* Relational modeling
* Indexes
* Constraints
* Transactions
* Row-level locking
* Query optimization
* Concurrent transactions

### Redis

* Caching
* Atomic counters
* Fast inventory checks
* Cache invalidation

### Celery

* Background jobs
* Task retries
* Scheduled jobs
* Celery Beat
* Async order processing

### DevOps

* Docker
* Docker Compose
* Nginx
* Gunicorn
* Environment variables
* Secrets
* Health checks
* Production deployment

---

# 📊 Target System Behavior

The final system aims to support the following flow:

```text
                 Flash Sale Starts
                       │
                       ▼
                User sends request
                       │
                       ▼
                DRF Authentication
                       │
                       ▼
                 Rate Limiting
                       │
                       ▼
                 Redis Inventory
                       │
                ┌──────┴──────┐
                │             │
             Available      Sold Out
                │             │
                ▼             ▼
        Create/Reserve      Reject
                │
                ▼
        PostgreSQL Transaction
                │
                ▼
          Create Order
                │
                ▼
          Celery Processing
                │
        ┌───────┴────────┐
        ▼                ▼
     Payment          Expiration
        │                │
        ▼                ▼
      PAID            EXPIRED
```

---

# ⚠️ Current Limitations

The current Phase 1 implementation is **not designed for real flash-sale traffic**.

Currently:

* SQLite is used for development
* Redis is not yet integrated
* Celery is not yet integrated
* PostgreSQL locking is not yet implemented
* Inventory concurrency protection is not yet implemented
* Docker deployment is not yet implemented
* Production monitoring is not yet implemented

Therefore, the current version should be considered a **development foundation**, not a production-ready flash-sale system.

---

# 🔮 Future Improvements

Potential future additions include:

* Distributed locks
* Advanced inventory reservation
* Payment gateway integration
* WebSocket-based order updates
* Event-driven architecture
* Kafka/RabbitMQ evaluation
* Prometheus metrics
* Structured logging
* Distributed tracing
* Load testing
* Locust-based traffic simulation
* Database query optimization
* Horizontal API scaling
* Read replicas
* Circuit breakers
* Graceful task retries

---

# 🧪 Load Testing Goal

A major goal of the project is to eventually simulate flash-sale traffic rather than only testing normal CRUD requests.

Example scenario:

```text
Available Stock: 100

Concurrent Requests: 10,000

Expected Result:

Successful purchases ≤ 100
Overselling = 0
Duplicate orders = 0
Invalid inventory state = 0
```

This will provide a measurable demonstration of the concurrency controls implemented throughout the project.

---

# 🔐 Security

Security considerations include:

* JWT authentication
* Password hashing through Django's authentication system
* Role-based permissions
* API throttling
* Environment-based secrets
* Input validation
* Database constraints
* Idempotency protection
* Production HTTPS
* Secure cookie/header configuration where applicable

Never commit `.env` files or production secrets to Git.

---

# 📁 Environment Variables

Example:

```env
DEBUG=True

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=

REDIS_URL=redis://localhost:6379/0

CELERY_BROKER_URL=redis://localhost:6379/0

CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Production values should be supplied through the deployment environment or a dedicated secrets mechanism.

---

# 🤝 Development

Clone the project:

```bash
git clone https://github.com/your-username/flash_sale_engine.git
cd flash_sale_engine
```

Create a branch:

```bash
git checkout -b feature/inventory-locking
```

Run migrations:

```bash
python manage.py migrate
```

Run tests:

```bash
python manage.py test
```

Start development server:

```bash
python manage.py runserver
```

---

# 📜 License

This project is currently being developed as a backend engineering portfolio and learning project.

Add an appropriate open-source license before distributing the project publicly.

---

# 👨‍💻 Project Focus

The primary objective of this project is to demonstrate how a Django REST API can evolve from a simple monolithic application into a system capable of handling:

```text
High Traffic
     ↓
Concurrency
     ↓
Transactions
     ↓
Inventory Protection
     ↓
Caching
     ↓
Asynchronous Processing
     ↓
Containerized Deployment
     ↓
Production Architecture
```

The project prioritizes **correctness under concurrency** over simply adding more infrastructure.
