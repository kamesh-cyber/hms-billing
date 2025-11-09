# API Endpoints Summary

## Billing Service Endpoints

### 1. **POST /v1/bills**
Create a new bill after a successful appointment.

**Request Body:**
```json
{
  "patient_id": 1,
  "appointment_id": "APT-101",
  "consultation_fee": 1000.0,
  "medication_fee": 500.0
}
```

**Response:** `201 Created`
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": "APT-101",
  "amount": 1575.0,
  "status": "PENDING",
  "created_at": "2025-11-09T10:30:00"
}
```

**Calculation:** `(consultation_fee + medication_fee) × 1.05 = (1000 + 500) × 1.05 = 1575.0`

---

### 2. **GET /v1/bills**
List bills with pagination and optional filters.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `page_size` (int, default: 10, max: 100): Items per page
- `patient_id` (int, optional): Filter by patient ID
- `appointment_id` (str, optional): Filter by appointment ID
- `status` (str, optional): Filter by status (`PENDING`, `PAID`, `CANCELLED`)

**Example:**
```bash
GET /v1/bills?page=1&page_size=10&patient_id=1&status=PENDING
```

**Response:** `200 OK`
```json
{
  "bills": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10
}
```

---

### 3. **GET /v1/bills/{bill_id}**
Get a specific bill by bill ID.

**Path Parameter:**
- `bill_id` (int): The bill ID

**Example:**
```bash
GET /v1/bills/1
```

**Response:** `200 OK`
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": "APT-101",
  "amount": 1575.0,
  "status": "PENDING",
  "created_at": "2025-11-09T10:30:00"
}
```

**Error Response:** `404 Not Found` if bill doesn't exist

---

### 4. **GET /v1/bills/bill** ✨ NEW
Get a bill by appointment ID using query parameter.

**Query Parameter:**
- `appointment_id` (str, required): The appointment ID

**Example:**
```bash
GET /v1/bills/bill?appointment_id=APT-101
```

**Response:** `200 OK`
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": "APT-101",
  "amount": 1575.0,
  "status": "PENDING",
  "created_at": "2025-11-09T10:30:00"
}
```

**Error Response:** `404 Not Found` if bill doesn't exist for the appointment

---

### 5. **PATCH /v1/bills/appointment/{appointment_id}/cancel**
Cancel a bill by marking it as CANCELLED (VOID) for a given appointment ID.

**Path Parameter:**
- `appointment_id` (str): The appointment ID

**Example:**
```bash
PATCH /v1/bills/appointment/APT-101/cancel
```

**Response:** `200 OK`
```json
{
  "bill_id": 1,
  "patient_id": 1,
  "appointment_id": "APT-101",
  "amount": 1575.0,
  "status": "CANCELLED",
  "created_at": "2025-11-09T10:30:00"
}
```

**Notes:**
- Idempotent: Returns the bill if already cancelled
- Error Response: `404 Not Found` if bill doesn't exist

---

## Health Endpoints (No Authentication Required)

### 6. **GET /health/live**
Liveness probe to check if the service is alive.

**Response:** `200 OK`
```json
{
  "status": "alive",
  "service": "billing_service"
}
```

---

### 7. **GET /health/ready**
Readiness probe to check if the service is ready to accept requests.

**Response:** `200 OK`
```json
{
  "status": "ready",
  "service": "billing_service",
  "database": "connected"
}
```

**Error Response:** `200 OK` (with error details)
```json
{
  "status": "not_ready",
  "service": "billing_service",
  "database": "disconnected",
  "error": "connection error details"
}
```

---

## Authentication

All billing endpoints (1-5) require HTTP Basic Authentication:

**Default Credentials:**
- Username: `admin` / Password: `admin123`
- Username: `billing_user` / Password: `billing123`

**Example:**
```bash
curl -u admin:admin123 http://localhost:3002/v1/bills
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Bill created successfully |
| 400 | Bad Request - Invalid input or duplicate bill |
| 401 | Unauthorized - Invalid credentials |
| 404 | Not Found - Bill not found |
| 500 | Internal Server Error - Server-side error |

---

## Complete cURL Examples

```bash
# Create a bill
curl -X POST http://localhost:3002/v1/bills \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 5,
    "appointment_id": "APT-200",
    "consultation_fee": 2000.0,
    "medication_fee": 800.0
  }'

# List all bills
curl -u admin:admin123 http://localhost:3002/v1/bills

# Get bill by ID
curl -u admin:admin123 http://localhost:3002/v1/bills/1

# Get bill by appointment ID (NEW)
curl -u admin:admin123 "http://localhost:3002/v1/bills/bill?appointment_id=APT-101"

# Cancel a bill
curl -X PATCH http://localhost:3002/v1/bills/appointment/APT-101/cancel \
  -u admin:admin123

# Health checks (no auth required)
curl http://localhost:3002/health/live
curl http://localhost:3002/health/ready
```

