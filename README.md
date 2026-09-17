# ⚡ High-Throughput E-Commerce Flash Sale & Inventory Engine

A production-oriented Django REST API designed to handle **high-concurrency flash sales**, prevent **inventory overselling**, and process checkout workflows asynchronously.

The project is being built incrementally, starting with a clean Django/DRF foundation and evolving toward a distributed architecture using **PostgreSQL, Redis, Celery, Docker, and Nginx**.

> **Project Status:** 🚧 In Development — Phase 1
> **Current Database:** SQLite
> **Target Database:** PostgreSQL

---

## 🎯 Project Goal

Traditional e-commerce APIs can struggle when thousands of users attempt to purchase a limited-stock product simultaneously.

This project focuses on solving backend problems that appear during flash-sale traffic spikes:

* Concurrent inventory requests
* Race conditions
* Inventory overselling
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

# 🏗️ Architecture

## Current Architecture

The current implementation is a Django + DRF monolith using SQLite during development.

```text
                         ┌──────────────────┐
                         │      Client      │
                         │ Web / Mobile/API │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Django + DRF   │
                         │     REST API     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
              SQLite Database            JWT Authentication
```

## Target Architecture

The final system will evolve into a multi-service backend:

```text
                         ┌──────────────────┐
                         │      Client      │
                         │ Web / Mobile/API │
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

## Application Responsibilities

### `users`

Responsible for:

* Custom user model
* UUID user IDs
* Email authentication
* User roles
* JWT authentication
* User profile API

### `catalog`

Responsible for:

* Categories
* Products
* Product CRUD operations
* Category CRUD operations
* Product/category relationships
* Pagination
* Base product information
* Base inventory

### `flash_sales`

Responsible for:

* Flash-sale events
* Flash-sale pricing
* Allocated inventory
* Inventory reservations
* Sale time windows
* Sale status

### `orders`

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

> **Design note:** If a product can participate in multiple flash-sale events, `product` should normally be a `ForeignKey` rather than a `OneToOneField`.

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

The API is versioned by application/domain rather than placing all endpoints under one resource.

## Authentication API

| Method | Endpoint                    | Description           | Auth |
| ------ | --------------------------- | --------------------- | ---- |
| POST   | `/api/users/register/`      | Register a new user   | No   |
| POST   | `/api/users/login/`         | Login a user          | No   |
| POST   | `/api/users/logout/`        | Logout a user         | Yes  |
| POST   | `/api/users/token/`         | Obtain JWT tokens     | No   |
| POST   | `/api/users/token/refresh/` | Refresh access token  | No   |
| GET    | `/api/users/profile/`       | Retrieve current user | Yes  |

---

# 📦 Catalog API

The Catalog API currently supports **Product CRUD**, **Category CRUD**, and **pagination**.

## Products

### Product List / Create

```http
GET /api/catalog/products/
POST /api/catalog/products/
```

| Method | Description                     | Authentication               |
| ------ | ------------------------------- | ---------------------------- |
| GET    | Retrieve paginated product list | Depends on API configuration |
| POST   | Create a product                | Depends on API configuration |

Example:

```text
http://127.0.0.1:8000/api/catalog/products/
```

---

### Product Detail

```http
GET /api/catalog/products/<product_id>
PUT /api/catalog/products/<product_id>
PATCH /api/catalog/products/<product_id>
DELETE /api/catalog/products/<product_id>
```

Example:

```text
http://127.0.0.1:8000/api/catalog/products/0a90b9ff-7abd-4aac-8a30-ec0cbdc97397
```

Supported operations:

| Method | Operation                   |
| ------ | --------------------------- |
| GET    | Retrieve a single product   |
| PUT    | Completely update a product |
| PATCH  | Partially update a product  |
| DELETE | Delete a product            |

---

# 🗂️ Categories

### Category List / Create

```http
GET /api/catalog/catagories/
POST /api/catalog/catagories/
```

Example:

```text
http://127.0.0.1:8000/api/catalog/Categories/
```

Supported operations:

| Method | Operation              |
| ------ | ---------------------- |
| GET    | Retrieve category list |
| POST   | Create a category      |

---

### Category Detail

```http
GET /api/catalog/Categories/<category_id>
PUT /api/catalog/Categories/<category_id>
PATCH /api/catalog/Categories/<category_id>
DELETE /api/catalog/Categories/<category_id>
```

Example:

```text
http://127.0.0.1:8000/api/catalog/Categories/0a90b9ff-7abd-4aac-8a30-ec0cbdc97397
```

Supported operations:

| Method | Operation                    |
| ------ | ---------------------------- |
| GET    | Retrieve a single category   |
| PUT    | Completely update a category |
| PATCH  | Partially update a category  |
| DELETE | Delete a category            |



---

# 📄 Pagination

The Product API supports paginated responses.

Instead of returning every product in a single response, the API divides the results into pages.

Example:

```http
GET /api/catalog/products/?page=1
```

Example:

```http
GET /api/catalog/products/?page=2
```

A typical paginated response has the following structure:

```json
{
    "count": 50,
    "next": "http://127.0.0.1:8000/api/catalog/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": "0a90b9ff-7abd-4aac-8a30-ec0cbdc97397",
            "catagory": "footwear",
            "name": "Classic Running Sneakers",
            "slug": "classic-running-sneakers",
            "description": "Lightweight mesh athletic sneakers with cushioned foam soles for daily wear.",
            "base_price": "75.00",
            "base_stock": 120,
            "is_active": true,
            "created_at": "2026-09-15T12:18:28.902037Z",
            "updated_at": "2026-09-15T12:18:28.902096Z"
        }
    ]
}
```

Pagination is important for the project because a production e-commerce system may eventually contain thousands or millions of catalog records.

---

# 📝 API Examples

## Register User

### Request

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

# 🔑 Login

### Request

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

### Response

```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

# 👤 Current User

### Request

```http
GET /api/users/profile/
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

# 🛍️ Product API Example

### Create Product

```http
POST /api/catalog/products/
Content-Type: application/json
```

Example:

```json
{
    "name": "Mechanical Keyboard",
    "description": "RGB mechanical keyboard",
    "base_price": "79.99",
    "base_stock": 100,
    "category": 1
}
```

### Get Products

```http
GET /api/catalog/products/
```

### Get Single Product

```http
GET /api/catalog/products/<product_id>
```

### Update Product

```http
PUT /api/catalog/products/<product_id>
```

### Partial Update

```http
PATCH /api/catalog/products/<product_id>
```

### Delete Product

```http
DELETE /api/catalog/products/<product_id>
```

---

# 🗂️ Category API Example

### Create Category

```http
POST /api/catalog/categories/
Content-Type: application/json
```

Example:

```json
{
    "name": "Electronics",
}
```

### Get Categories

```http
GET /api/catalog/categories/
```

### Get Single Category

```http
GET /api/catalog/categories/<category_id>
```

### Update Category

```http
PUT /api/catalog/categories/<category_id>
```

### Partial Update

```http
PATCH /api/catalog/categories/<category_id>
```

### Delete Category

```http
DELETE /api/catalog/categories/<category_id>
```

---

# 🚀 Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/flash_sale_engine.git

cd flash_sale_engine
```

---

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

---

## 3. Install Dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt python-decouple
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1
```

For future phases:

```env
DATABASE_URL=

REDIS_URL=redis://localhost:6379/0

CELERY_BROKER_URL=redis://localhost:6379/0

CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Never commit your real `.env` file to Git.

---

## 5. Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## 6. Create Admin User

```bash
python manage.py createsuperuser
```

---

## 7. Start Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 🧪 Testing

Testing will be expanded throughout the project.

Planned coverage includes:

* [ ] User registration
* [ ] Authentication
* [ ] Permissions
* [ ] Product CRUD
* [ ] Category CRUD
* [ ] Pagination
* [ ] Flash-sale APIs
* [ ] Order creation
* [ ] Inventory allocation
* [ ] Idempotency
* [ ] Concurrent purchase requests
* [ ] Order expiration
* [ ] Celery tasks
* [ ] Redis operations

The final system will specifically test concurrency scenarios where multiple requests attempt to purchase the last available units.

---

# 📈 Development Roadmap

## Phase 1 — Core API & Domain Setup

**Status: 🟢 Active Development**

### Completed

* [x] Custom User model
* [x] UUID user IDs
* [x] Email-based authentication
* [x] User roles
* [x] JWT authentication
* [x] User registration
* [x] User profile endpoint
* [x] Category model
* [x] Product model
* [x] Product CRUD API
* [x] Category CRUD API
* [x] Product pagination
* [x] Environment-based configuration
* [x] Development environment

### Remaining

* [ ] Improve API documentation
* [ ] Expand automated tests
* [ ] Add advanced catalog filtering/search
* [ ] Prepare database migration

---

# 🐘 Phase 2 — PostgreSQL & Transactional Inventory

**Status: ⏳ Planned**

Move from SQLite to PostgreSQL.

### Goals

* [ ] PostgreSQL configuration
* [ ] Environment-based database configuration
* [ ] FlashSale model
* [ ] FlashSaleItem model
* [ ] Order model
* [ ] Database constraints
* [ ] `transaction.atomic()`
* [ ] Row-level locking
* [ ] `select_for_update()`
* [ ] Inventory reservation
* [ ] Order state transitions
* [ ] Idempotent order creation

### Core Concurrency Concept

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

The objective is to make inventory allocation safe when multiple transactions compete for the same inventory.

---

# ⚙️ Phase 3 — Celery & Redis

**Status: ⏳ Planned**

Introduce asynchronous processing.

## Celery

Background jobs will handle:

```text
Order
  │
  ├── Payment simulation
  ├── Receipt generation
  └── Notification processing
```

## Celery Beat

Scheduled tasks will handle:

* Expired orders
* Unreleased reservations
* Flash-sale status updates
* Periodic cleanup jobs

---

# ⚡ Phase 4 — Redis & High-Speed Inventory Protection

**Status: ⏳ Planned**

Redis will be introduced for high-speed operations.

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

# 🐳 Phase 5 — Docker & Production Architecture

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
More units can be sold than actually exist.
```

The project progressively introduces stronger mechanisms to solve this.

## Layer 1 — Database Transactions

```text
transaction.atomic()
```

Provides transactional consistency.

## Layer 2 — Row-Level Locking

```text
select_for_update()
```

Allows PostgreSQL transactions to coordinate access to the same inventory row.

## Layer 3 — Redis Atomic Operations

```text
DECR
```

Provides fast atomic counter operations for the high-traffic path.

## Layer 4 — Idempotency

```text
Idempotency-Key
```

Prevents duplicate order processing when clients retry requests.

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
1 logical purchase
       ↓
Potentially multiple orders
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
POST /api/orders/

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

## Django

* Custom User Models
* Model relationships
* Custom managers
* Django Admin
* Environment configuration
* Transactions
* Database constraints

## Django REST Framework

* Serializers
* APIViews
* Generic Views
* ViewSets
* Routers
* Authentication
* Permissions
* Pagination
* Throttling
* Filtering
* Error handling

## PostgreSQL

* Relational modeling
* Indexes
* Constraints
* Transactions
* Row-level locking
* Query optimization
* Concurrent transactions

## Redis

* Caching
* Atomic counters
* Fast inventory checks
* Cache invalidation

## Celery

* Background jobs
* Task retries
* Scheduled jobs
* Celery Beat
* Async order processing

## DevOps

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

The current version should therefore be considered a **development foundation**, not a production-ready flash-sale system.

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
* Locust-based load testing
* Database query optimization
* Horizontal API scaling
* Read replicas
* Circuit breakers
* Graceful task retries

---

# 🧪 Load Testing Goal

A major goal of the project is to simulate flash-sale traffic rather than only testing normal CRUD requests.

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

Create a feature branch:

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

Start the development server:

```bash
python manage.py runserver
```

---

# 📜 License

This project is currently being developed as a backend engineering portfolio and learning project.

Add an appropriate open-source license before distributing the project publicly.

---

# 👨‍💻 Project Focus

The primary objective of this project is to demonstrate how a Django REST API can evolve from a simple CRUD backend into a system designed for high-concurrency workloads.

```text
CRUD API
   ↓
Authentication
   ↓
Pagination
   ↓
PostgreSQL
   ↓
Transactions
   ↓
Concurrency Control
   ↓
Inventory Protection
   ↓
Redis
   ↓
Asynchronous Processing
   ↓
Celery
   ↓
Docker
   ↓
Production Architecture
```

The project prioritizes **correctness under concurrency** over simply adding more infrastructure.
