# ⚡ FlashPulse Engine

> **High-Concurrency E-Commerce Flash Sale & Inventory Engine**

FlashPulse Engine is a **Django REST Framework backend** designed to explore how e-commerce systems can safely handle **high-concurrency flash-sale traffic**, prevent **inventory overselling**, and process order workflows asynchronously.

The project starts as a Django + DRF monolith and progressively evolves toward a production-oriented architecture using:

**Django → PostgreSQL → Redis → Celery → Docker → Nginx**

The primary engineering objective is **correctness under concurrency**, not simply building another CRUD API.

---

## 🚧 Project Status

**Current Phase:** Phase 1 — Core API & Authentication

| Component             | Current Status |
| --------------------- | -------------- |
| Django                | ✅ Implemented  |
| Django REST Framework | ✅ Implemented  |
| Custom User           | ✅ Implemented  |
| JWT Authentication    | ✅ Implemented  |
| Product CRUD          | ✅ Implemented  |
| Category CRUD         | ✅ Implemented  |
| Pagination            | ✅ Implemented  |
| SQLite                | ✅ Development  |
| PostgreSQL            | 🔜 Phase 2     |
| Transactions          | 🔜 Phase 2     |
| Row-Level Locking     | 🔜 Phase 2     |
| Idempotent Orders     | 🔜 Phase 2     |
| Redis                 | 🔜 Phase 3/4   |
| Celery                | 🔜 Phase 3     |
| Docker                | 🔜 Phase 5     |
| Nginx/Gunicorn        | 🔜 Phase 5     |
| Locust Load Testing   | 🔜 Phase 6     |

> **Important:** The current Phase 1 implementation is a development foundation. The high-concurrency inventory protection described below is part of the planned architecture and is not yet fully implemented.

---

# 🎯 Project Goal

Flash sales create a difficult backend problem:

> **What happens when thousands of users try to purchase the last few units of a product at almost the same time?**

A naive inventory implementation might perform:

```text
Read Stock
    ↓
Check Stock > 0
    ↓
Create Order
    ↓
Decrease Stock
```

Under concurrent requests, multiple transactions may read the same stock value before any of them updates it.

Example:

```text
Available Stock = 1

Request A ──► Read stock = 1 ──► Continue
Request B ──► Read stock = 1 ──► Continue
Request C ──► Read stock = 1 ──► Continue

                 ↓

          Multiple purchases

                 ↓

            OVERSOLD STOCK
```

FlashPulse Engine is being built to address this class of problem using **database transactions, row-level locking, Redis atomic operations, database constraints, idempotency, and asynchronous processing**.

---

# 🧠 Engineering Problems

The project focuses on several backend engineering challenges:

* High-concurrency purchase requests
* Race conditions
* Inventory overselling
* Transactional inventory reservation
* Duplicate checkout requests
* Idempotency
* Database contention
* Order expiration
* Background processing
* Redis caching
* Atomic inventory operations
* API throttling
* Production deployment
* Concurrency load testing

---

# 🏗️ Architecture

## Current Architecture

Phase 1 is intentionally simple.

```text
                    ┌───────────────────┐
                    │      Client       │
                    │ Web / Mobile / API│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Django + DRF   │
                    │     REST API      │
                    └─────────┬─────────┘
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
          ┌──────────────┐        ┌──────────────┐
          │    SQLite    │        │     JWT      │
          │  Development │        │ Authentication│
          └──────────────┘        └──────────────┘
```

The current system focuses on establishing a clean domain model, authentication system, catalog APIs, permissions, and API foundations before introducing distributed infrastructure.

---

# 🚀 Target Architecture

The final system will evolve toward:

```text
                         ┌──────────────────┐
                         │      Client      │
                         │ Web / Mobile /API│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Nginx       │
                         │  Reverse Proxy   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Django + DRF   │
                         │     REST API     │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │ PostgreSQL  │     │    Redis    │     │   Celery    │
       │ Transaction │     │ Cache/Atomic│     │   Workers   │
       │    State    │     │  Operations │     │             │
       └─────────────┘     └─────────────┘     └──────┬──────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ Celery Beat │
                                              │  Scheduler  │
                                              └─────────────┘
```

### Responsibility of Each Layer

| Component    | Responsibility                           |
| ------------ | ---------------------------------------- |
| Django + DRF | API and business logic                   |
| PostgreSQL   | Durable transactional state              |
| Redis        | Caching and high-speed atomic operations |
| Celery       | Background processing                    |
| Celery Beat  | Scheduled jobs                           |
| Nginx        | Reverse proxy                            |
| Gunicorn     | Production WSGI server                   |
| Docker       | Containerization                         |
| Locust       | Concurrency/load testing                 |

---

# 🛠️ Tech Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Backend programming            |
| Django                | Web framework                  |
| Django REST Framework | REST API                       |
| SimpleJWT             | JWT authentication             |
| SQLite                | Phase 1 development database   |
| PostgreSQL            | Production relational database |
| Redis                 | Cache and atomic operations    |
| Celery                | Asynchronous task processing   |
| Celery Beat           | Scheduled tasks                |
| Docker                | Containerization               |
| Docker Compose        | Multi-container orchestration  |
| Nginx                 | Reverse proxy                  |
| Gunicorn              | Production application server  |
| Locust                | Load and concurrency testing   |
| python-decouple       | Environment configuration      |

---

# 📦 Domain Architecture

The project is divided into Django applications based on business responsibility.

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

---

# 🧩 Django Applications

## `users`

Responsible for:

* Custom user model
* UUID user IDs
* Email-based authentication
* User roles
* JWT authentication
* User registration
* User profile

### Roles

```text
CUSTOMER
ADMIN
```

---

## `catalog`

Responsible for:

* Categories
* Products
* Product CRUD
* Category CRUD
* Product/category relationships
* Pagination
* Base product information
* Base inventory

---

## `flash_sales`

Planned responsibility:

* Flash-sale events
* Sale pricing
* Allocated inventory
* Inventory reservations
* Sale start/end times
* Sale status
* Inventory locking

---

## `orders`

Planned responsibility:

* Order creation
* Order lifecycle
* Payment state
* Idempotency
* Reservation tracking
* Order expiration

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

## Flash Sale Item

**Planned model**

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

Possible states:

```text
SCHEDULED
ACTIVE
ENDED
SOLD_OUT
```

A product can participate in multiple flash-sale events, so the relationship is designed around a `ForeignKey` rather than a one-to-one relationship.

---

## Order

**Planned model**

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

Possible states:

```text
PENDING_PAYMENT
PAID
CANCELLED
EXPIRED
COMPLETED
```

---

# 🔐 Authentication

FlashPulse Engine uses **JWT authentication with SimpleJWT**.

```text
              Register
                  │
                  ▼
          Email + Password
                  │
                  ▼
                Login
                  │
          ┌───────┴───────┐
          ▼               ▼
     Access Token    Refresh Token
          │               │
          ▼               ▼
     API Requests    New Access Token
```

Authenticated requests use:

```http
Authorization: Bearer <access_token>
```

---

# 📡 API

## Authentication

| Method | Endpoint                    | Description          | Auth |
| ------ | --------------------------- | -------------------- | ---- |
| POST   | `/api/users/register/`      | Register user        | No   |
| POST   | `/api/users/login/`         | Login user           | No   |
| POST   | `/api/users/logout/`        | Logout user          | Yes  |
| POST   | `/api/users/token/`         | Obtain JWT tokens    | No   |
| POST   | `/api/users/token/refresh/` | Refresh access token | No   |
| GET    | `/api/users/profile/`       | Get current user     | Yes  |

---

# 📦 Catalog API

## Products

### List Products

```http
GET /api/catalog/products/
```

### Create Product

```http
POST /api/catalog/products/
```

### Retrieve Product

```http
GET /api/catalog/products/<product_id>/
```

### Update Product

```http
PUT /api/catalog/products/<product_id>/
```

### Partial Update

```http
PATCH /api/catalog/products/<product_id>/
```

### Delete Product

```http
DELETE /api/catalog/products/<product_id>/
```

---

## Categories

### List Categories

```http
GET /api/catalog/categories/
```

### Create Category

```http
POST /api/catalog/categories/
```

### Retrieve Category

```http
GET /api/catalog/categories/<category_id>/
```

### Update Category

```http
PUT /api/catalog/categories/<category_id>/
```

### Partial Update

```http
PATCH /api/catalog/categories/<category_id>/
```

### Delete Category

```http
DELETE /api/catalog/categories/<category_id>/
```

---

# 📄 Pagination

The Product API supports pagination.

Example:

```http
GET /api/catalog/products/?page=1
```

Example response:

```json
{
    "count": 50,
    "next": "http://127.0.0.1:8000/api/catalog/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": "0a90b9ff-7abd-4aac-8a30-ec0cbdc97397",
            "category": "footwear",
            "name": "Classic Running Sneakers",
            "slug": "classic-running-sneakers",
            "description": "Lightweight athletic sneakers.",
            "base_price": "75.00",
            "base_stock": 120,
            "is_active": true
        }
    ]
}
```

Pagination becomes important as the catalog grows to thousands or millions of records.

---

# 🔑 API Examples

## Register

```http
POST /api/users/register/
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

Example response:

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

```http
POST /api/users/token/
Content-Type: application/json
```

```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}
```

Response:

```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

## Get Current User

```http
GET /api/users/profile/
Authorization: Bearer <access_token>
```

Response:

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

# ⚡ Flash Sale Concurrency Strategy

The central engineering challenge is preventing overselling when many users compete for limited inventory.

The planned architecture uses multiple layers.

## Layer 1 — Database Transactions

Django's:

```python
transaction.atomic()
```

will ensure that inventory reservation and order creation occur within a transactional boundary.

---

## Layer 2 — Row-Level Locking

PostgreSQL will use:

```python
select_for_update()
```

to lock the relevant inventory row while the transaction is executing.

Conceptually:

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

This is intended to prevent concurrent transactions from modifying the same inventory record incorrectly.

---

## Layer 3 — Database Constraints

The database will enforce business invariants where appropriate.

For example:

```text
reserved_stock >= 0
allocated_stock >= 0
```

Database constraints provide a final layer of protection against invalid states.

---

## Layer 4 — Redis Atomic Operations

Redis will eventually provide a high-speed inventory gate using atomic operations such as:

```text
DECR
```

Conceptually:

```text
Incoming Request
       │
       ▼
 Redis Inventory Counter
       │
   ┌───┴────┐
   │        │
Stock > 0  Stock <= 0
   │        │
   ▼        ▼
Continue   Reject
   │
   ▼
PostgreSQL Transaction
```

Redis will act as a **fast traffic-control layer**, while PostgreSQL remains the source of durable transactional state.

---

## Layer 5 — Idempotency

A client may retry a checkout request because of a timeout or network failure.

Without idempotency:

```text
1 logical purchase
       │
       ├── Request 1
       ├── Request 2
       └── Request 3
              │
              ▼
       Multiple orders
```

With an idempotency key:

```text
Request
   │
   ▼
Idempotency-Key
   │
   ├── New ──────► Process
   │
   └── Existing ─► Return previous result
```

Example:

```http
POST /api/orders/
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

---

# 🔄 Order Lifecycle

The planned order lifecycle is:

```text
             ┌───────────────────┐
             │ PENDING_PAYMENT   │
             └─────────┬─────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
            PAID             EXPIRED
              │
              ▼
          COMPLETED
```

Cancellation may occur before payment completion:

```text
PENDING_PAYMENT
       │
       ▼
   CANCELLED
```

The final implementation will enforce valid state transitions at the application level.

---

# ⚙️ Asynchronous Processing

Celery will be introduced to move non-critical work outside the main HTTP request.

Planned background tasks include:

* Order expiration
* Inventory reservation release
* Notification processing
* Receipt generation
* Payment simulation
* Flash-sale status updates
* Periodic cleanup

Example:

```text
             Order Created
                  │
                  ▼
             Django API
                  │
                  ▼
             Celery Queue
                  │
          ┌───────┴────────┐
          ▼                ▼
       Worker          Celery Beat
          │                │
          ▼                ▼
 Background Jobs     Scheduled Jobs
```

---

# 🧪 Testing Strategy

Testing will evolve with each phase.

### Current / Planned Coverage

```text
[ ] User registration
[ ] Authentication
[ ] JWT validation
[ ] Permissions
[ ] Product CRUD
[ ] Category CRUD
[ ] Pagination
[ ] Flash-sale creation
[ ] Inventory reservation
[ ] Order creation
[ ] Idempotency
[ ] Order expiration
[ ] Redis operations
[ ] Celery tasks
[ ] Transaction behavior
[ ] Concurrent purchases
[ ] Database constraints
```

The most important tests will focus on **concurrent requests competing for limited inventory**.

---

# 🔥 Concurrency Load-Test Scenario

The final load-testing scenario will simulate:

```text
Available Inventory:       100 units
Concurrent Requests:       10,000

Expected Invariants:

Successful Purchases:      ≤ 100
Oversold Items:             0
Duplicate Orders:           0
Negative Inventory:         0
Invalid Inventory State:    0
```

Locust will eventually be used to generate concurrent traffic and measure how the backend behaves under load.

---

# 🐘 Development Roadmap

## Phase 1 — Core API & Domain Setup

**Status: 🟢 In Progress**

* [x] Custom User model
* [x] UUID user IDs
* [x] Email authentication
* [x] User roles
* [x] JWT authentication
* [x] User registration
* [x] User profile API
* [x] Category model
* [x] Product model
* [x] Product CRUD
* [x] Category CRUD
* [x] Pagination
* [x] Environment configuration

### Remaining

* [ ] Improve API documentation
* [ ] Expand automated tests
* [ ] Advanced filtering
* [ ] Search
* [ ] Ordering
* [ ] Prepare PostgreSQL migration

---

# Phase 2 — PostgreSQL & Transactional Inventory

**Status: ⏳ Planned**

* [ ] PostgreSQL configuration
* [ ] Database environment configuration
* [ ] FlashSale model
* [ ] FlashSaleItem model
* [ ] Order model
* [ ] Database constraints
* [ ] `transaction.atomic()`
* [ ] `select_for_update()`
* [ ] Inventory reservation
* [ ] Order state transitions
* [ ] Idempotent order creation
* [ ] Transaction/concurrency tests

**Primary goal:** establish a correct transactional inventory model before introducing Redis.

---

# Phase 3 — Celery & Background Processing

**Status: ⏳ Planned**

* [ ] Celery configuration
* [ ] Redis broker
* [ ] Celery worker
* [ ] Celery Beat
* [ ] Order expiration
* [ ] Reservation release
* [ ] Notification tasks
* [ ] Task retries
* [ ] Scheduled cleanup

---

# Phase 4 — Redis & High-Speed Protection

**Status: ⏳ Planned**

* [ ] Redis caching
* [ ] Atomic inventory counters
* [ ] Inventory `DECR`
* [ ] Cache invalidation
* [ ] Hot-product optimization
* [ ] DRF throttling
* [ ] Request rate limiting
* [ ] Redis integration tests

---

# Phase 5 — Docker & Production Architecture

**Status: ⏳ Planned**

```text
Docker Compose
│
├── Nginx
├── Django / Gunicorn
├── PostgreSQL
├── Redis
├── Celery Worker
└── Celery Beat
```

Planned production concerns:

* [ ] Dockerfile
* [ ] Docker Compose
* [ ] PostgreSQL container
* [ ] Redis container
* [ ] Celery worker
* [ ] Celery Beat
* [ ] Gunicorn
* [ ] Nginx
* [ ] HTTPS/TLS
* [ ] Static/media handling
* [ ] Production secrets
* [ ] Health checks
* [ ] Logging
* [ ] Monitoring

---

# Phase 6 — Concurrency & Load Testing

**Status: ⏳ Planned**

The final phase will stress-test the inventory system.

Example:

```text
10,000 concurrent purchase attempts
              │
              ▼
       Limited inventory
              │
              ▼
       Concurrency controls
              │
              ▼
        PostgreSQL + Redis
              │
              ▼
      Measure system invariants
```

The primary success criteria are:

```text
Overselling       = 0
Negative Stock    = 0
Duplicate Orders  = 0
```

---

# 🔐 Security

Security considerations include:

* JWT authentication
* Password hashing through Django authentication
* Role-based permissions
* API throttling
* Input validation
* Database constraints
* Idempotency protection
* Environment-based secrets
* HTTPS in production
* Secure cookie/header configuration where applicable

Never commit real environment secrets to Git.

---

# ⚙️ Environment Configuration

Create a `.env` file:

```env
DEBUG=True

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=

REDIS_URL=redis://localhost:6379/0

CELERY_BROKER_URL=redis://localhost:6379/0

CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Production secrets should be supplied through the deployment environment or an appropriate secrets-management system.

---

# 🚀 Quick Start

## 1. Clone

```bash
git clone https://github.com/your-username/flashpulse-engine.git

cd flashpulse-engine
```

## 2. Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install django \
    djangorestframework \
    djangorestframework-simplejwt \
    python-decouple
```

## 4. Configure Environment

Create `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create Admin User

```bash
python manage.py createsuperuser
```

## 7. Run Server

```bash
python manage.py runserver
```

API:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 📈 Project Evolution

FlashPulse Engine is intentionally developed in stages:

```text
                    Phase 1
                       │
                       ▼
                  CRUD + JWT
                       │
                       ▼
                 PostgreSQL
                       │
                       ▼
                 Transactions
                       │
                       ▼
              Row-Level Locking
                       │
                       ▼
              Inventory Control
                       │
                       ▼
                    Redis
                       │
                       ▼
                   Celery
                       │
                       ▼
                    Docker
                       │
                       ▼
             Production Architecture
                       │
                       ▼
              Concurrency Testing
```

Each phase introduces a specific backend engineering concept rather than adding infrastructure without a clear purpose.

---

# 🧠 Engineering Concepts Demonstrated

### Django

* Custom User Models
* Custom managers
* Model relationships
* Django Admin
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
* Pagination
* Filtering
* Throttling
* Error handling

### PostgreSQL

* Relational modeling
* Constraints
* Indexes
* Transactions
* Row-level locking
* Concurrent transactions
* Query optimization

### Redis

* Caching
* Atomic counters
* Inventory protection
* Cache invalidation

### Celery

* Background jobs
* Task retries
* Scheduled tasks
* Celery Beat
* Asynchronous workflows

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

# 🔮 Future Improvements

Potential future extensions include:

* Distributed locking
* Advanced inventory reservation
* Payment gateway integration
* WebSocket order updates
* Event-driven architecture
* Kafka/RabbitMQ evaluation
* Prometheus metrics
* Structured logging
* Distributed tracing
* Database query optimization
* Horizontal API scaling
* Read replicas
* Circuit breakers
* Graceful task retries

---

# ⚠️ Current Limitations

The current Phase 1 system is **not a production flash-sale system**.

Currently:

* SQLite is used for development
* PostgreSQL concurrency controls are not implemented
* Redis is not integrated
* Celery is not integrated
* Inventory reservation is not implemented
* Idempotent checkout is not implemented
* Docker deployment is not implemented
* Load testing is not implemented
* Production monitoring is not implemented

The current release should therefore be viewed as the **foundation for the final high-concurrency system**.

---

# 🎯 Final Objective

The ultimate objective of FlashPulse Engine is to demonstrate how a backend can evolve from a conventional REST API into a system designed around **correctness, concurrency, transactional integrity, and asynchronous processing**.

The project is not simply about adding Django, PostgreSQL, Redis, and Celery.

It is about understanding **why each component is introduced and what engineering problem it solves**.

```text
CRUD
  ↓
Authentication
  ↓
Domain Modeling
  ↓
PostgreSQL
  ↓
Transactions
  ↓
Concurrency Control
  ↓
Inventory Reservation
  ↓
Idempotency
  ↓
Redis
  ↓
Celery
  ↓
Docker
  ↓
Load Testing
  ↓
Production Architecture
```

> **Core principle:** Build for correctness first, then optimize for scale.

---

## 📜 License

This project is currently being developed as a backend engineering portfolio and learning project.

An appropriate open-source license can be added before public distribution.
