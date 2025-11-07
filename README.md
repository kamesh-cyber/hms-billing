# HMS Billing Service

A FastAPI-based billing service for the Hospital Management System (HMS) with MySQL database integration.

## Features

- **FastAPI & Uvicorn**: High-performance async web framework
- **Authentication**: HTTP Basic Authentication with username/password
- **Docker Compose**: Containerized deployment with MySQL database
- **Database Seeding**: Automatic initialization with sample data
- **Comprehensive Logging**: Request/response logging with latency tracking
- **Pagination & Filtering**: Efficient bill retrieval with multiple filter options

## Requirements

- Docker & Docker Compose
- Python 3.11+ (for local development)



## Database Schema

### Bills Table
```sql
CREATE TABLE bills (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    appointment_id INT NOT NULL,
    amount FLOAT NOT NULL,
    status ENUM('PENDING', 'PAID', 'CANCELLED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);
```

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   cd /Users/kchand995@apac.comcast.com/hms-billing
   ```

2. **Build and start services**
   ```bash
   docker-compose up --build
   ```

3. **Access the service**
   - API: http://localhost:3002
   - API Docs: http://localhost:3002/docs
   - Database: localhost:3307

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 3002 --reload
   ```

## API Endpoints

### Authentication
All endpoints require HTTP Basic Authentication.

**Default Credentials:**
- Username: `admin` / Password: `admin123`
- Username: `billing_user` / Password: `billing123`

### Endpoints

#### 1. Create Bill
**POST** `/v1/bills`

Creates a new bill after a successful appointment. Automatically calculates the total amount including 5% tax.

**Request Body:**
```json
{
  "patient_id": 1,
  "appointment_id": 101,
  "consultation_fee": 1000.0,
  "medication_fee": 500.0
}
```

**Response:**
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": 101,
  "amount": 1575.0,
  "status": "PENDING",
  "created_at": "2025-11-07T10:30:00Z"
}
```

**Calculation:** `(consultation_fee + medication_fee) × 1.05 = (1000 + 500) × 1.05 = 1575.0`

#### 2. List Bills
**GET** `/v1/bills`

Retrieves a paginated list of bills with optional filters.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `page_size` (int, default: 10): Items per page (max: 100)
- `patient_id` (int, optional): Filter by patient ID
- `appointment_id` (int, optional): Filter by appointment ID
- `status` (string, optional): Filter by status (`PENDING`, `PAID`, `CANCELLED`)

**Example:**
```bash
GET /v1/bills?page=1&page_size=10&patient_id=1&status=PENDING
```

**Response:**
```json
{
  "bills": [
    {
      "bill_id": 1,
      "patient_id": 1,
      "appointment_id": 101,
      "amount": 1575.0,
      "status": "PENDING",
      "created_at": "2025-11-07T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

#### 3. Get Bill by ID
**GET** `/v1/bills/{bill_id}`

Retrieves a specific bill by its ID.

**Response:**
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": 101,
  "amount": 1575.0,
  "status": "PENDING",
  "created_at": "2025-11-07T10:30:00Z"
}
```

#### 4. Health Check
**GET** `/`

Check service status.

**Response:**
```json
{
  "service": "Billing Service",
  "status": "running",
  "version": "1.0.0"
}
```

## Testing with cURL

### Create a Bill
```bash
curl -X POST http://localhost:3002/v1/bills \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 5,
    "appointment_id": 106,
    "consultation_fee": 2000.0,
    "medication_fee": 800.0
  }'
```

### List All Bills
```bash
curl -X GET http://localhost:3002/v1/bills \
  -u admin:admin123
```

### List Bills with Filters
```bash
curl -X GET "http://localhost:3002/v1/bills?page=1&page_size=5&patient_id=1&status=PENDING" \
  -u admin:admin123
```

### Get Bill by ID
```bash
curl -X GET http://localhost:3002/v1/bills/1 \
  -u admin:admin123
```

## Seed Data

The application automatically seeds the database on startup with:

### Users
- `admin` / `admin123`
- `billing_user` / `billing123`

### Sample Bills
- 5 sample bills with varying patient IDs, amounts, and statuses

## Logging

The service implements comprehensive logging:

- **Request/Response Logging**: All API requests are logged with method, path, and status code
- **Latency Tracking**: Each request includes timing information
- **Custom Headers**: Response includes `X-Process-Time` header
- **Log Format**: `timestamp - logger_name - level - message`

**Example Log Output:**
```
2025-11-07 10:30:15 - app.main - INFO - Request started: POST /v1/bills
2025-11-07 10:30:15 - app.main - INFO - Creating bill for patient_id=1, appointment_id=101
2025-11-07 10:30:15 - app.main - INFO - Bill created successfully: bill_id=1, amount=1575.0, time_taken=0.0234s
2025-11-07 10:30:15 - app.middleware - INFO - Request completed: POST /v1/bills | Status: 201 | Latency: 0.0245s
```

## Docker Services

### billing_database
- **Image**: MySQL 8.0
- **Port**: 3308 (host) → 3306 (container)
- **Credentials**: root / rootpassword
- **Database**: billing_db
- **Health Check**: Ensures database is ready before starting the billing service

### billing_service
- **Port**: 3002
- **Dependencies**: billing_database
- **Auto-restart**: Yes
- **Logs**: Available via `docker-compose logs billing_service`

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Billing service only
docker-compose logs -f billing_service

# Database only
docker-compose logs -f billing_database
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Services
```bash
docker-compose up --build
```

### Access MySQL Database
```bash
docker exec -it billing_database mysql -uroot -prootpassword billing_db
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:rootpassword@billing_database:3306/billing_db` |
| `SECRET_KEY` | JWT secret key | (generated) |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

## API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:3002/docs
- **ReDoc**: http://localhost:3002/redoc

## Error Handling

The service provides clear error messages:

- **400 Bad Request**: Invalid input or duplicate bill
- **401 Unauthorized**: Invalid credentials
- **404 Not Found**: Bill not found
- **500 Internal Server Error**: Server-side errors

## Security

- Passwords are hashed using bcrypt
- HTTP Basic Authentication for all endpoints
- SQL injection protection via SQLAlchemy ORM
- Environment variables for sensitive configuration
