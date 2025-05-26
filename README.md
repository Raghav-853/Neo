Overview

This project is a backend API. The focus is on demonstrating strong software engineering practices, thoughtful architectural decisions, and robust handling of edge cases and scalability. The implementation leverages modern Python frameworks and tools to deliver a maintainable and extensible codebase.

Tech Stack & Major Dependencies

- FastAPI: High-performance web framework for building APIs with Python 3.7+
- Uvicorn: ASGI server for running FastAPI applications
- SQLAlchemy: SQL toolkit and ORM for database interactions
- Alembic: Database migrations
- python-dotenv: Loads environment variables from `.env` files
- psycopg2-binary: PostgreSQL database adapter
- Pydantic: Data validation and settings management
- pydantic-settings: For managing application settings

> Justification: These libraries are industry standards for building robust, scalable, and maintainable Python web applications. FastAPI provides automatic OpenAPI/Swagger documentation, while SQLAlchemy and Alembic ensure reliable database management.

Project Structure

```
Neo/
  app/
    api/        # API route handlers
    core/       # Core logic and configuration
    db/         # Database session and base
    models/     # ORM models
    schemas/    # Pydantic schemas
  alembic/      # Database migrations
  requirements.txt
  README.md
  .env
```

Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Neo
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   - Copy `.env.example` to `.env` and update values as needed.

5. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.api.main:app --reload
   ```

API Documentation

- **Swagger UI**: Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

Architectural Decisions

- **Modular Structure**: Separation of concerns between API, core logic, models, and schemas for maintainability.
- **Environment-based Configuration**: Using `python-dotenv` and `pydantic-settings` for flexible configuration.
- **Database Migrations**: Managed via Alembic for versioned schema changes.
- **Validation**: Pydantic ensures strict data validation at the API boundary.

Changelog Diff Feature

- The changelog diff feature is implemented to track and display changes between different versions of entities. This is a key part of the task and is designed for clarity and extensibility. (See code for details.)

Database Migrations

- Migration scripts are located in `alembic/versions/`.
- To create a new migration:
  ```bash
  alembic revision --autogenerate -m "Migration message"
  alembic upgrade head
  ```

Testing

- Use the built-in Swagger UI for manual API testing.
- Automated tests can be added under a `tests/` directory (not included by default).
