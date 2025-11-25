# FastAPI Clean Architecture - Project Structure

## ✅ Refactoring Complete!

The codebase has been successfully refactored to follow **FastAPI Clean Architecture** conventions.

## 📂 New Directory Structure

```
intelligence/
│
├── app/                           # 🎯 Main FastAPI Application Package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app instance & configuration
│   │
│   ├── api/                      # 🌐 API Layer
│   │   ├── __init__.py
│   │   └── v1/                  # API Version 1
│   │       ├── __init__.py
│   │       ├── api.py          # Main API router (combines all endpoints)
│   │       └── endpoints/      # Route endpoints
│   │           ├── __init__.py
│   │           ├── agents.py              # Agent routes
│   │           ├── terrorists.py          # Terrorist routes
│   │           ├── reports.py             # Report routes
│   │           └── sql.py                 # SQL routes
│   │
│   ├── core/                     # ⚙️ Core Configuration
│   │   ├── __init__.py
│   │   ├── config.py           # Settings (Pydantic Settings)
│   │   └── database.py         # Database engine & dependencies
│   │
│   ├── schemas/                  # 📋 Request/Response DTOs
│   │   ├── __init__.py
│   │   ├── agent_schemas.py
│   │   ├── terrorist_schemas.py
│   │   ├── report_schemas.py
│   │   └── common_schemas.py
│   │
│   └── services/                 # 💼 Business Logic Layer
│       ├── __init__.py
│       ├── agent_service.py
│       ├── terrorist_service.py
│       └── report_service.py
│
├── dal/                          # 🗄️ Data Access Layer (kept as requested)
│   ├── __init__.py
│   ├── agent_dal.py
│   ├── terrorist_dal.py
│   └── report_dal.py
│
├── models/                       # 📊 Database Entities (SQLModel)
│   ├── __init__.py
│   ├── agent.py
│   ├── terrorist.py
│   └── report.py
│
├── client/                       # 🔌 HTTP Client Utilities
│   ├── __init__.py
│   └── http_client.py
│
├── utils/                        # 🛠️ Utility Functions
│   ├── __init__.py
│   └── auth.py
│
├── server.py                     # 🚀 Server Entry Point
├── client_main.py                # 💻 Terminal Client (HTTP-based)
├── main.py                       # 📜 Legacy Terminal Client (Direct DB)
├── requirements.txt              # 📦 Python Dependencies
├── README.md                     # 📖 Documentation
└── .gitignore                    # 🚫 Git Ignore File
```

## 🎯 Key Changes

### 1. **app/** - Main Application Package
   - All FastAPI code now lives under `app/`
   - Follows FastAPI project template conventions

### 2. **app/core/** - Configuration & Database
   - `config.py`: Centralized settings using Pydantic Settings
   - `database.py`: Database engine and dependency injection

### 3. **app/api/v1/** - Versioned API
   - API endpoints are now versioned (`/api/v1/`)
   - Easier to maintain multiple API versions
   - `api.py`: Main router that combines all endpoint routers

### 4. **app/api/v1/endpoints/** - Routes
   - Route files (`agents.py`, `reports.py`, etc.)
   - Handle HTTP requests/responses and error handling
   - Call services for business logic
   - No controllers - routes directly call services

### 5. **app/schemas/** - Request/Response Models
   - All Pydantic models for API validation
   - Separate from database models

### 6. **app/services/** - Business Logic
### 5. **app/schemas/** - Request/Response Models
   - All Pydantic models for API validation
   - Separate from database models

### 6. **app/services/** - Business Logic
   - Pure business logic functions
   - No HTTP concerns
   - Called directly by routes

### 7. **dal/** - Data Access Layer (Preserved)
   - Kept as a separate directory as requested
   - Direct database operations only

## 🔄 Request Flow

```
HTTP Request
    ↓
app/api/v1/endpoints/reports.py (Route - handles request/response & errors)
    ↓
app/services/report_service.py (Business Logic)
    ↓
dal/report_dal.py (Database Operations)
    ↓
models/report.py (Database Entity)
    ↓
MySQL Database
```

## 📡 API Changes

### Old Structure
- `/api/agents/login`
- `/api/reports/`

### New Structure
- `/api/v1/agents/login`
- `/api/v1/reports/`

## 🚀 Running the Application

### Start Server
```bash
python server.py
```

Server will run on: `http://localhost:8000`
- Docs: http://localhost:8000/docs
- API: http://localhost:8000/api/v1

### Start Client
```bash
python client_main.py
```

## 📦 Dependencies

Added to `requirements.txt`:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic-settings` - Configuration management
- `httpx` - HTTP client
- `python-multipart` - Form data support

## ✨ Benefits of This Architecture

1. **Scalability**: Easy to add new API versions
2. **Maintainability**: Clear separation of concerns
3. **Testability**: Each layer can be tested independently
4. **Documentation**: Auto-generated OpenAPI docs
5. **Type Safety**: Pydantic validation throughout
6. **Configuration**: Centralized settings management
7. **Dependency Injection**: Clean dependencies using FastAPI's DI system

## 🎓 FastAPI Best Practices Implemented

✅ **Versioned APIs** (`/api/v1/`)  
✅ **Structured Layout** (app/ directory)  
✅ **Settings Management** (Pydantic Settings)  
✅ **Dependency Injection** (get_engine)  
✅ **Lifespan Events** (Database initialization)  
✅ **Router Organization** (Separate routers per resource)  
✅ **Schema Validation** (Pydantic models)  
✅ **Error Handling** (HTTPException)  
✅ **CORS Configuration** (Middleware)  
✅ **API Documentation** (Auto-generated)  

## 📝 Migration Notes

### For Developers
- Update imports to use `app.*` instead of direct imports
- API URLs now include `/api/v1/` prefix
- Configuration is now in `app/core/config.py`
- Database connection in `app/core/database.py`

### For Clients
- Update API base URL from `/api/` to `/api/v1/`
- All endpoints remain functionally the same
- Error responses follow FastAPI standards

## 🔧 Configuration

Edit `app/core/config.py` to change:
- Database credentials
- Server host/port
- API version prefix
- CORS settings
- Application metadata

---

**Architecture Pattern**: FastAPI Clean Architecture  
**Status**: ✅ Production Ready  
**Last Updated**: November 25, 2025
