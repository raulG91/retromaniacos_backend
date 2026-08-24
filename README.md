# Retromaniacos Backend 🎮🕹️

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.32-red.svg?style=flat-square)](https://sqlmodel.tiangolo.com/)
[![Database](https://img.shields.io/badge/MySQL-8.0-4479A1.svg?style=flat-square&logo=mysql)](https://www.mysql.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-yellow.svg?style=flat-square&logo=pytest)](https://docs.pytest.org/)

This is the backend API for **Retromaniacos**, a non-profit organization dedicated to preserving retro video game consoles, games, and hardware. The system is designed to streamline the management of members, physical retro-gaming inventory, event planning, and the association of materials and participants with specific events.

---

## 🚀 Features

- **Member Management (`Users`):** Secure registration, roles, and profile management for association members.
- **Material Catalog (`Material`):** Inventory tracking for retro consoles, games, accessories, and promotional items.
- **Event Planning (`Events`):** Scheduling and organizing gaming exhibitions, workshops, and retro meetings.
- **Event Logistics (`EventMaterial`):** Allocating hardware, consoles, and games to specific events with status tracking.
- **Participation (`EventParticipation`):** Coordinating member roles and participation in organized events.
- **Robust Security:** Secure authentication via JSON Web Tokens (JWT) and high-security password hashing with Argon2.

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **ORM / Database Layer:** SQLModel (backed by SQLAlchemy)
- **Database:** MySQL
- **Testing:** Pytest
- **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```text
retromaniacos_backend/
├── app/
│   ├── models/          # SQLModel database schemas & definitions
│   ├── routes/          # API endpoints organized by domain
│   ├── tests/           # Integration and unit tests using Pytest
│   ├── db.py            # Database engine and session configuration
│   ├── exceptions.py    # Custom exception handlers & API error definitions
│   ├── main.py          # Application entrypoint & FastAPI setup
│   └── util.py          # Auxiliary and utility functions
├── docker-compose.yml   # Multi-container orchestration (MySQL)
├── Dockerfile           # Backend deployment instructions
├── requirements.txt     # Python dependencies
└── diagram E-R.png      # Database Entity-Relationship layout
```

---

## ⚙️ Getting Started

### Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/retromaniacos_backend.git
cd retromaniacos_backend
```

### 2. Environment Setup

Create a `.env` file in the root directory and configure your environment variables:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/retromaniacos
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
```

### 3. Create Virtual Environment & Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv env
source env/bin/activate  # On Windows use: .\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Infrastructure (MySQL Database)

Spin up the MySQL container using Docker Compose:

```bash
docker compose up -d
```

### 5. Run the Application

Start the FastAPI local development server:

```bash
fastapi dev app/main.py
```

The API documentation will be available interactively at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Tests

A suite of pytest integration and unit tests is available. To run them, execute:

```bash
pytest
```

---

## 📐 Database Schema

The database utilizes relational entities to maintain data integrity. You can inspect the structural E-R details in the `diagram E-R.png` file located in the root of the project.

Key relations:
* **Users & Events** via `EventParticipation` (Many-to-Many)
* **Events & Materials** via `EventMaterial` (Many-to-Many)

---

## 🤝 Coding Conventions

- **Variable & Function Naming:** Use `camelCase` for variables and functions.
- **Error Handling:** Always leverage custom exceptions defined in `app/exceptions.py` to ensure uniform JSON error responses across the API.
