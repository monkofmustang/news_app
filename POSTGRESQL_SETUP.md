# PostgreSQL Database Setup Guide

This guide explains how to set up and use the PostgreSQL database for the News App.

## Prerequisites

1. **PostgreSQL Installation**: Make sure PostgreSQL is installed on your system
2. **Python Dependencies**: Install the required Python packages

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create PostgreSQL Database

```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create database and user
CREATE DATABASE news_app;
CREATE USER news_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE news_app TO news_user;
\q
```

### 3. Configure Environment Variables

Copy `env_template.txt` to `.env` and update the database URL:

```bash
cp env_template.txt .env
```

Edit `.env` and update the `DATABASE_URL`:

```env
DATABASE_URL=postgresql://news_user:your_password@localhost:5432/news_app
```

### 4. Initialize Database

```bash
# Create tables
python -c "from db.db_connection import create_tables; create_tables()"

# Or use Alembic for migrations
alembic init alembic  # Only needed once
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Database Schema

### Subscribers Table

- `id`: Primary key (auto-increment)
- `name`: Subscriber name (optional)
- `mobNumber`: Mobile number (unique, required)
- `state`: State/location (optional)

## API Endpoints

### Subscribers

- `GET /subscribers/` - Get all subscribers
- `POST /subscribers/` - Create a new subscriber
- `GET /subscribers/{id}` - Get a specific subscriber
- `DELETE /subscribers/{id}` - Delete a subscriber

## Example Usage

### Create a Subscriber

```bash
curl -X POST "http://localhost:8000/subscribers/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "mobNumber": 1234567890, "state": "California"}'
```

### Get All Subscribers

```bash
curl "http://localhost:8000/subscribers/"
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure PostgreSQL is running and the connection string is correct
2. **Permission Error**: Ensure the database user has proper privileges
3. **Port Conflict**: Default PostgreSQL port is 5432, make sure it's not blocked

### Useful Commands

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Connect to database
psql -h localhost -U news_user -d news_app

# List tables
\dt

# Check table structure
\d subscribers
```

## Migration from MongoDB

The application has been migrated from MongoDB to PostgreSQL. Key changes:

- Replaced `motor` (async MongoDB driver) with `psycopg2-binary` and `sqlalchemy`
- Updated models to use SQLAlchemy ORM
- Added Alembic for database migrations
- Updated API endpoints to use PostgreSQL

## Development

### Adding New Models

1. Create the model in the `models/` directory
2. Import it in `alembic/env.py`
3. Generate and run migrations

### Running Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
