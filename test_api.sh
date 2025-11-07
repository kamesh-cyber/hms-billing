#!/bin/bash

# HMS Billing Service API Test Script

BASE_URL="http://localhost:3002"
USERNAME="admin"
PASSWORD="admin123"

echo "=========================================="
echo "HMS Billing Service API Tests"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check Endpoint"
echo "   GET /"
curl -s $BASE_URL/ | python3 -m json.tool
echo ""
echo ""

# Test 2: List All Bills
echo "2. Testing List All Bills"
echo "   GET /v1/bills"
curl -s -u $USERNAME:$PASSWORD $BASE_URL/v1/bills | python3 -m json.tool
echo ""
echo ""

# Test 3: Get Bill by ID
echo "3. Testing Get Bill by ID"
echo "   GET /v1/bills/1"
curl -s -u $USERNAME:$PASSWORD $BASE_URL/v1/bills/1 | python3 -m json.tool
echo ""
echo ""

# Test 4: Create New Bill
echo "4. Testing Create New Bill"
echo "   POST /v1/bills"
echo "   Body: patient_id=10, appointment_id=200, consultation_fee=1500, medication_fee=500"
curl -s -X POST $BASE_URL/v1/bills \
  -u $USERNAME:$PASSWORD \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 10,
    "appointment_id": 200,
    "consultation_fee": 1500.0,
    "medication_fee": 500.0
  }' | python3 -m json.tool
echo ""
echo "   Expected amount: (1500 + 500) * 1.05 = 2100.0"
echo ""
echo ""

# Test 5: Pagination
echo "5. Testing Pagination"
echo "   GET /v1/bills?page=1&page_size=3"
curl -s -u $USERNAME:$PASSWORD "$BASE_URL/v1/bills?page=1&page_size=3" | python3 -m json.tool
echo ""
echo ""

# Test 6: Filter by Patient ID
echo "6. Testing Filter by Patient ID"
echo "   GET /v1/bills?patient_id=1"
curl -s -u $USERNAME:$PASSWORD "$BASE_URL/v1/bills?patient_id=1" | python3 -m json.tool
echo ""
echo ""

# Test 7: Filter by Status
echo "7. Testing Filter by Status"
echo "   GET /v1/bills?status=PENDING"
curl -s -u $USERNAME:$PASSWORD "$BASE_URL/v1/bills?status=PENDING" | python3 -m json.tool
echo ""
echo ""

# Test 8: Combined Filters
echo "8. Testing Combined Filters"
echo "   GET /v1/bills?patient_id=1&status=PENDING"
curl -s -u $USERNAME:$PASSWORD "$BASE_URL/v1/bills?patient_id=1&status=PENDING" | python3 -m json.tool
echo ""
echo ""

# Test 9: Invalid Authentication
echo "9. Testing Invalid Authentication"
echo "   GET /v1/bills (with wrong password)"
curl -s -u admin:wrongpassword $BASE_URL/v1/bills
echo ""
echo ""

# Test 10: Non-existent Bill
echo "10. Testing Non-existent Bill"
echo "    GET /v1/bills/9999"
curl -s -u $USERNAME:$PASSWORD $BASE_URL/v1/bills/9999 | python3 -m json.tool
echo ""
echo ""

# Test 11: Duplicate Bill Creation
echo "11. Testing Duplicate Bill Creation"
echo "    POST /v1/bills (with duplicate appointment_id)"
curl -s -X POST $BASE_URL/v1/bills \
  -u $USERNAME:$PASSWORD \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "appointment_id": 101,
    "consultation_fee": 1000.0,
    "medication_fee": 0.0
  }' | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "Tests Completed!"
echo "=========================================="

