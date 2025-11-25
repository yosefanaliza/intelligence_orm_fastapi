# Intelligence Reporting System

A comprehensive intelligence reporting system with clean architecture, featuring a 3-tier architecture: Terminal Client → HTTP API Server → Database.

## 🏗️ Architecture

The system follows **FastAPI Clean Architecture** conventions with clear separation of concerns:

```
┌─────────────────────┐
│  Terminal Client    │  ← User Interface (client_main.py)
└──────────┬──────────┘
           │ HTTP Requests (JSON)
           ▼
┌─────────────────────┐
│   HTTP API Server   │  ← FastAPI Application
│      (app/)         │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    ▼             ▼          ▼          ▼
┌────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐
│ Routes │→ │Services │→ │   DAL   │→ │Database│
└────────┘  └─────────┘  └─────────┘  └────────┘
                                         (MySQL)
```

### Layer Responsibilities

1. **Routes** (`app/api/v1/endpoints/`)
   - Define API endpoints
   - Handle HTTP request routing
   - Validate request parameters
   - Call controller functions

2. **Controllers** (`app/api/v1/endpoints/*_controller.py`)
   - HTTP request/response handling
   - Input validation
   - Call appropriate service functions
   - Format responses
   - Handle HTTP errors

3. **Services** (`app/services/`)
   - Business logic
   - Validation
   - Coordinate between controllers and DAL
   - Transaction management

4. **DAL - Data Access Layer** (`dal/`)
   - Direct database operations
   - CRUD operations
   - Query execution
   - No business logic

5. **Models** (`models/`)
   - Database entities (SQLModel)
   - Define table structure
   - Relationships between entities

6. **Schemas** (`app/schemas/`)
   - Request/Response DTOs (Pydantic)
   - API data validation
   - Serialization/Deserialization

7. **Core** (`app/core/`)
   - Configuration management
   - Database connection
   - Application settings

8. **Client** (`client/`)
   - HTTP client utilities
   - API communication
   - Error handling

## 📁 Project Structure

```
intelligence/
├── app/                        # Main FastAPI Application
│   ├── api/                   # API Layer
│   │   └── v1/               # API Version 1
│   │       ├── endpoints/    # Route Endpoints
│   │       │   ├── agents.py              # Agent routes
│   │       │   ├── terrorists.py          # Terrorist routes
│   │       │   ├── reports.py             # Report routes
│   │       │   ├── sql.py                 # SQL routes
│   │       │   ├── agent_controller.py     # Agent controllers
│   │       │   ├── terrorist_controller.py # Terrorist controllers
│   │       │   ├── report_controller.py    # Report controllers
│   │       │   └── sql_controller.py       # SQL controllers
│   │       └── api.py        # API v1 Router
│   ├── core/                 # Core Configuration
│   │   ├── config.py        # Settings & Configuration
│   │   └── database.py      # Database Engine & Connection
│   ├── schemas/             # Pydantic Models (DTOs)
│   │   ├── agent_schemas.py
│   │   ├── terrorist_schemas.py
│   │   ├── report_schemas.py
│   │   └── common_schemas.py
│   ├── services/            # Business Logic Layer
│   │   ├── agent_service.py
│   │   ├── terrorist_service.py
│   │   └── report_service.py
│   └── main.py             # FastAPI App Instance
├── client/                  # HTTP Client Utilities
│   ├── __init__.py
│   └── http_client.py      # APIClient for HTTP requests
├── dal/                     # Data Access Layer
│   ├── __init__.py
│   ├── agent_dal.py
│   ├── terrorist_dal.py
│   └── report_dal.py
├── models/                  # Database Entities (SQLModel)
│   ├── __init__.py
│   ├── agent.py
│   ├── terrorist.py
│   └── report.py
├── utils/                   # Utilities
│   ├── __init__.py
│   └── auth.py
├── server.py               # Server Entry Point
├── client_main.py          # Terminal Client (HTTP-based)
├── main.py                 # Old Terminal Client (Direct DB - Legacy)
├── requirements.txt        # Python Dependencies
└── README.md              # This file
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database**
   
   Edit `app/core/config.py` with your MySQL credentials:
   ```python
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "your_password"
   MYSQL_HOST = "localhost"
   MYSQL_PORT = "3306"
   MYSQL_DATABASE = "intelligence"
   ```

3. **Create MySQL database**
   ```sql
   CREATE DATABASE intelligence;
   ```

## 🎯 Usage

### Starting the System

The system requires **two processes** running simultaneously:

#### 1. Start the API Server

```bash
python server.py
```

The server will start on `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API v1**: http://localhost:8000/api/v1

#### 2. Start the Terminal Client

In a **separate terminal**:

```bash
python client_main.py
```

### Client Operations

The terminal client provides the following operations:

1. **Agent Login** - Authenticate or register new agent
2. **Execute Free SQL** - Run custom SQL queries
3. **Create Intelligence Report** - Add new intelligence report
4. **Delete Intelligence Report** - Remove a report
5. **Search Reports by Keywords** - Find reports containing specific words
6. **Search Reports by Terrorist** - View reports about a specific terrorist
7. **Search Dangerous Terrorists** - Find terrorists with >5 reports
8. **Search Super Dangerous Terrorists** - Find terrorists with >10 reports containing weapon keywords

### Example Workflow

```
1. Start server: python server.py
2. Start client: python client_main.py
3. Login or create account (option 1)
4. Create terrorist record (option 3 → option 2)
5. Create intelligence report (option 3)
6. Search reports (options 5-8)
```

## 📡 API Endpoints

### Base URL
`http://localhost:8000/api/v1`

### Agent Endpoints

- `POST /agents/register` - Register new agent
- `POST /agents/login` - Login agent

### Terrorist Endpoints

- `POST /terrorists/` - Create new terrorist
- `GET /terrorists/{id}` - Get terrorist by ID

### Report Endpoints

- `POST /reports/` - Create new report
- `DELETE /reports/{id}` - Delete report
- `GET /reports/search/text?keyword={keyword}` - Search by text
- `GET /reports/search/terrorist/{id}` - Search by terrorist
- `GET /reports/dangerous` - Get dangerous terrorists
- `GET /reports/super-dangerous` - Get super dangerous terrorists

### SQL Endpoints

- `POST /sql/execute` - Execute raw SQL query

## 🔄 Data Flow

### Creating a Report (Example)

```
1. User Input (Terminal Client)
   ↓
2. client_main.py calls api_client.create_report()
   ↓
3. HTTP POST request to /api/v1/reports/
   ↓
4. app/api/v1/endpoints/reports.py receives request
   ↓
5. report_controller.create_report_controller() validates and processes
   ↓
6. report_service.create_report() handles business logic
   ↓
7. report_dal.create_report() executes database operation
   ↓
8. Database stores the report
   ↓
9. Response flows back through all layers
   ↓
10. Client displays success message
```

## 🗄️ Database Schema

### Tables

- **agent** - Intelligence agents
  - id (PK)
  - name
  - username (unique)
  - password
  - created_at

- **terrorist** - Tracked individuals
  - id (PK)
  - name
  - affiliation
  - location
  - created_at

- **report** - Intelligence reports
  - id (PK)
  - content
  - agent_id (FK → agent)
  - terrorist_id (FK → terrorist)
  - created_at

## 🛠️ Development

### Adding New Endpoints

1. Define schema in `app/schemas/`
2. Create service function in `app/services/`
3. Create controller function in `app/api/v1/endpoints/*_controller.py`
4. Add route in `app/api/v1/endpoints/*.py`
5. Update client in `client/http_client.py`
6. Add menu option in `client_main.py`

### Configuration

All configuration is managed through `app/core/config.py` using Pydantic Settings.

## 📋 FastAPI Clean Architecture Best Practices

This project follows FastAPI best practices:

✅ **Versioned API** (`/api/v1/`)  
✅ **Dependency Injection** (Database engine)  
✅ **Pydantic Models** for validation  
✅ **Modular Structure** (Clear separation of concerns)  
✅ **Configuration Management** (Pydantic Settings)  
✅ **Lifespan Events** (Startup/Shutdown)  
✅ **API Documentation** (Auto-generated OpenAPI)  
✅ **CORS Middleware** (Cross-origin requests)  
✅ **Error Handling** (HTTP status codes)  

## 📝 Assignment Requirements Met

This implementation fulfills all assignment requirements:

✅ **3-Tier Architecture**: Client → HTTP Server → Database  
✅ **Clean Architecture**: Routes → Controllers → Services → DAL  
✅ **Agent Login**: POST /api/v1/agents/login  
✅ **Agent Registration**: POST /api/v1/agents/register  
✅ **Create Terrorist**: POST /api/v1/terrorists/  
✅ **Create Report**: POST /api/v1/reports/  
✅ **Delete Report**: DELETE /api/v1/reports/{id}  
✅ **Search by Text**: GET /api/v1/reports/search/text  
✅ **Search by Terrorist**: GET /api/v1/reports/search/terrorist/{id}  
✅ **Dangerous Terrorists**: GET /api/v1/reports/dangerous (>5 reports)  
✅ **Super Dangerous Terrorists**: GET /api/v1/reports/super-dangerous  
✅ **Raw SQL Execution**: POST /api/v1/sql/execute  
✅ **Error Handling**: HTTP status codes and error messages  
✅ **Client Changes**: Uses HTTP requests instead of direct DB access  

### Weapon Keywords Detection

Super dangerous terrorists are identified by having:
- More than 10 reports
- At least one report containing these Hebrew keywords:
  - פיגוע (attack)
  - סכין (knife)
  - רובה (rifle)
  - אקדח (pistol)
  - פצצה (bomb)

---

**Architecture**: FastAPI Clean Architecture  
**Last Updated**: November 25, 2025
