# StacksInk API 🚀

## Description

StacksInk is an blog API built using FastAPI and leveraging stacks/connect and stacks/transactions on the frontent. The platform supports a creating, updating, deleting, reading, blogs (integrated with @stacks/transactions), tipping management, and real-time recommendation engine using collaborative filtering.

## Features

- User Authentication
- Tipping Authors for a well written blog
- Profile Management System
- Collaborative Filtering for Blog Recommendations
- Payment Integration with @stacks/transactions

## Technology Stack

- **Backend**: FastAPI, Python
- **Database**: Postgresql, Redis, Pydantic, SqlModel
- **Containerization**: Docker, Docker Compose
- **Payment Integration**: @stacks/transactions
- **Recommendation System**: Collaborative Filtering

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10
- Paystack API credentials
- Postgres and Redis

[//]: # (### Installation Steps)

[//]: # ()
[//]: # (1. Clone the repository:)

[//]: # ()
[//]: # (   ```bash)

[//]: # (   git clone https://github.com/yourusername/redi-buy-api.git)

[//]: # (   cd redi-buy-api)

[//]: # (   ```)

[//]: # ()
[//]: # (2. Create a `.env` file in the root directory and add your Paystack API credentials:)

[//]: # ()
[//]: # (   ```bash)

[//]: # (    MONGODB_URL="mongodb://localhost:27017/my_local_db")

[//]: # (    PAYSTACK_SECRET_KEY="your_secret_key")

[//]: # (    REDIS_URL="redis://localhost:6379/0")

[//]: # (    ```)

[//]: # ()
[//]: # (3. Build and run the containers:)

[//]: # ()
[//]: # (    ```bash)

[//]: # (    docker-compose up --build)

[//]: # (    ```)

[//]: # ()
[//]: # (## API Documentation)

[//]: # ()
[//]: # (The API documentation can be accessed through the `/docs` or `/redoc` endpoints.)

[//]: # ()
[//]: # (- Swagger UI: `http://localhost:8000/docs`)

[//]: # (- ReDoc: `http://localhost:8000/redoc`)

[//]: # ()
[//]: # (## Usage)

[//]: # ()
[//]: # (### Create an Order)

[//]: # ()
[//]: # (```bash)

[//]: # (curl -X POST "http://localhost:8000/orders" -H "Content-Type: application/json" -d '{"user_id": "60c74b", "items": [...]}')

[//]: # (```)

[//]: # ()
[//]: # (## Contribution)

[//]: # ()
[//]: # (Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.)
