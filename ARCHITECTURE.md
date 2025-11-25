# Intelligence System - Architecture Documentation

## 🏗️ Architecture Overview

This project follows a **layered architecture** pattern with clear separation of concerns, built using **FastAPI** and **SQLModel ORM**.

```
┌─────────────────────┐
│  Terminal Client    │  ← Command-line Interface (client_main.py)
└──────────┬──────────┘
           │ HTTP Requests (JSON)
           ▼
┌─────────────────────┐
│   FastAPI Server    │  ← Web Application (app/)
│                     │
│  Routes → Services  │
│     ↓         ↓     │
│    DAL ← Models     │
└──────────┬──────────┘
           │ SQLModel ORM
           ▼
┌─────────────────────┐
│   MySQL Database    │  ← Data Persistence
└─────────────────────┘
```

---

## 📂 Project Structure

```
intelligence/
│
├── app/                              # 🎯 Main Application Package
│   ├── __init__.py
│   ├── main.py                      # FastAPI app instance & startup
│   ├── router.py                    # Main API router (combines all routes)
│   │
│   ├── routes/                      # 🌐 API Route Handlers
│   │   ├── __init__.py
│   │   ├── agents_routes.py         # Agent endpoints
│   │   ├── terrorists_routes.py     # Terrorist endpoints
│   │   ├── reports_routes.py        # Report endpoints
│   │   └── sql_routes.py            # SQL execution endpoints
│   │
│   ├── schemas/                     # 📋 Pydantic Schemas (DTOs)
│   │   ├── __init__.py
│   │   ├── agent_schemas.py         # Agent request/response models
│   │   ├── terrorist_schemas.py     # Terrorist request/response models
│   │   ├── report_schemas.py        # Report request/response models
│   │   └── common_schemas.py        # Shared schemas
│   │
│   ├── services/                    # 💼 Business Logic Layer
│   │   ├── __init__.py
│   │   ├── agent_service.py         # Agent business logic
│   │   ├── terrorist_service.py     # Terrorist business logic
│   │   └── report_service.py        # Report business logic
│   │
│   ├── dal/                         # 🗄️ Data Access Layer
│   │   ├── __init__.py
│   │   ├── agent_dal.py            # Agent database operations
│   │   ├── terrorist_dal.py        # Terrorist database operations
│   │   └── report_dal.py           # Report database operations
│   │
│   └── models/                      # 📊 Database Models (SQLModel)
│       ├── __init__.py
│       ├── agent.py                # Agent entity
│       ├── terrorist.py            # Terrorist entity
│       └── report.py               # Report entity
│
├── db/                              # 🔧 Database Configuration
│   └── database.py                 # Database engine & session management
│
├── client/                          # 🔌 HTTP Client
│   ├── __init__.py
│   └── http_client.py              # API client wrapper
│
├── utils/                           # 🛠️ Utilities
│   ├── __init__.py
│   └── auth.py                     # Authentication utilities
│
├── server.py                        # 🚀 FastAPI Server Entry Point
├── client_main.py                   # 💻 Terminal Client (HTTP-based)
├── config.py                        # ⚙️ Application Configuration
├── requirements.txt                 # 📦 Python Dependencies
├── README.md                        # 📖 Documentation
└── ARCHITECTURE.md                  # 📐 This file
```

---

## 🔄 Request Flow

### Example: Creating a Report

```
1. HTTP POST /reports
   ↓
2. app/routes/reports_routes.py (Route Handler)
   - Validates request using Pydantic schema
   - Calls service layer
   ↓
3. app/services/report_service.py (Business Logic)
   - Applies business rules
   - Calls DAL for data operations
   ↓
4. app/dal/report_dal.py (Data Access)
   - Executes database queries
   - Uses SQLModel ORM
   ↓
5. app/models/report.py (Database Model)
   - Defines table structure
   ↓
6. MySQL Database
   - Stores data
```

---

## 🎯 Layer Responsibilities

### 1. **Routes Layer** (`app/routes/`)
**Purpose**: HTTP endpoint definitions and request/response handling

**Responsibilities**:
- Define API endpoints with decorators (`@router.post`, `@router.get`, etc.)
- Validate incoming requests using Pydantic schemas
- Call appropriate service functions
- Handle HTTP-specific concerns (status codes, headers)
- Catch and format exceptions as HTTP responses

**File Naming**: `{resource}_routes.py`

**Example**:
```python
@router.post("/", response_model=ReportResponse, status_code=201)
async def create_report(report: ReportCreate):
    return create_report_service(report)
```

---

### 2. **Services Layer** (`app/services/`)
**Purpose**: Business logic and orchestration

**Responsibilities**:
- Implement core business rules
- Coordinate between routes and DAL
- Perform data validation and transformations
- Handle business-level exceptions
- Manage transactions when needed

**File Naming**: `{resource}_service.py`

**Example**:
```python
def create_report_service(report: ReportCreate) -> Report:
    # Business logic validation
    if not report.content:
        raise ValueError("Report content required")
    
    # Call DAL for persistence
    return create_report_dal(report)
```

---

### 3. **DAL Layer** (`app/dal/`)
**Purpose**: Database operations using SQLModel ORM

**Responsibilities**:
- Execute database queries (SELECT, INSERT, UPDATE, DELETE)
- Use SQLModel ORM for type-safe database access
- Return database models or results
- Handle database-level exceptions
- Manage database sessions

**File Naming**: `{resource}_dal.py`

**Example**:
```python
def create_report_dal(report: ReportCreate) -> Report:
    with Session(engine) as session:
        db_report = Report.model_validate(report)
        session.add(db_report)
        session.commit()
        session.refresh(db_report)
        return db_report
```

---

### 4. **Models Layer** (`app/models/`)
**Purpose**: Database table definitions

**Responsibilities**:
- Define database schema using SQLModel
- Specify table columns, types, and constraints
- Define relationships between tables
- Serve as ORM entities

**File Naming**: `{resource}.py`

**Example**:
```python
class Report(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    terrorist_id: int = Field(foreign_key="terrorist.id")
```

---

### 5. **Schemas Layer** (`app/schemas/`)
**Purpose**: API data validation and serialization

**Responsibilities**:
- Define request/response models using Pydantic
- Validate incoming data
- Serialize outgoing data
- Separate API contracts from database models

**File Naming**: `{resource}_schemas.py`

**Example**:
```python
class ReportCreate(BaseModel):
    content: str
    terrorist_id: int

class ReportResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
```

---

## 🌐 API Structure

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Agents
- `POST /agents/login` - Agent authentication
- `POST /agents/` - Create new agent

#### Terrorists
- `POST /terrorists/` - Add terrorist
- `GET /terrorists/{id}` - Get terrorist details

#### Reports
- `POST /reports/` - Create report
- `DELETE /reports/{id}` - Delete report
- `GET /reports/search/text` - Search reports by content
- `GET /reports/search/terrorist/{id}` - Get reports for terrorist
- `GET /reports/dangerous` - Get dangerous terrorists
- `GET /reports/super-dangerous` - Get super dangerous terrorists

#### SQL
- `POST /sql/execute` - Execute raw SQL queries

---

## 🗄️ Database Schema

### Tables

**agents**
- `id`: INT (PK, Auto-increment)
- `nickname`: VARCHAR (Unique)
- `password`: VARCHAR (Hashed)

**terrorists**
- `id`: INT (PK, Auto-increment)
- `name`: VARCHAR
- `location`: VARCHAR
- `threat_level`: INT

**reports**
- `id`: INT (PK, Auto-increment)
- `content`: TEXT
- `terrorist_id`: INT (FK → terrorists.id)
- `agent_id`: INT (FK → agents.id)
- `created_at`: TIMESTAMP

---

## 🚀 Running the Application

### 1. Start the Server
```bash
python server.py
```

Server runs at: `http://localhost:8000`
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### 2. Start the Client
```bash
python client_main.py
```

### 3. Database Setup
Ensure MySQL is running and database is configured in `config.py`:
```python
DATABASE_URL = "mysql+pymysql://user:password@localhost/intelligence_db"
```

---

## 📦 Key Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLModel**: SQL database ORM with Pydantic integration
- **Uvicorn**: ASGI server for FastAPI
- **PyMySQL**: MySQL database driver
- **Pydantic**: Data validation and settings management
- **httpx**: HTTP client for terminal client

---

## ✨ Architecture Benefits

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Layers can be tested independently
3. **Maintainability**: Clear structure makes code easy to navigate
4. **Scalability**: Easy to add new features or modify existing ones
5. **Type Safety**: Pydantic and SQLModel provide runtime validation
6. **Documentation**: Auto-generated OpenAPI/Swagger docs
7. **Flexibility**: Business logic separated from HTTP and database concerns

---

## 🎓 Design Patterns Used

- **Layered Architecture**: Clear separation between routes, services, and data access
- **Repository Pattern**: DAL abstracts database operations
- **DTO Pattern**: Schemas separate API models from database models
- **Dependency Injection**: FastAPI's DI system for database sessions
- **ORM Pattern**: SQLModel for object-relational mapping

---

## 📝 Development Guidelines

### Adding a New Feature

1. **Define Model** (`app/models/`) - Database schema
2. **Create Schemas** (`app/schemas/`) - API request/response models
3. **Implement DAL** (`app/dal/`) - Database operations
4. **Write Service** (`app/services/`) - Business logic
5. **Add Routes** (`app/routes/`) - HTTP endpoints
6. **Register Router** (`app/router.py`) - Include in main router

### File Naming Conventions

- Routes: `{resource}_routes.py`
- Services: `{resource}_service.py`
- DAL: `{resource}_dal.py`
- Models: `{resource}.py`
- Schemas: `{resource}_schemas.py`

---

**Architecture Pattern**: Layered Architecture with FastAPI  
**ORM**: SQLModel  
**Database**: MySQL  
**Status**: ✅ Production Ready  
**Last Updated**: November 25, 2025
