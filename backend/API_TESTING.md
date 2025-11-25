# API Testing Guide

This document provides examples for testing the Flask API endpoints using curl and Postman.

## Base URL

```
http://localhost:5000
```

## Health Check

### GET /api/health

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## A1 Cutting Process Feedback

### POST /api/a1/submit

Submit A1 cutting process feedback form with files.

**Using curl:**

```bash
curl -X POST http://localhost:5000/api/a1/submit \
  -F "date_time=2024-01-15 10:30:00" \
  -F "lot_number=12345" \
  -F "item_type=TypeA" \
  -F "gsx_machine_no=GSX001" \
  -F "mc_machine_no=MC001" \
  -F "cut_operator_payroll=OP001" \
  -F "ng_block_lot=5" \
  -F "ng_chip_qty_lot=10" \
  -F "block_number=B001" \
  -F "confirm_date=2024-01-15" \
  -F "reason=After Repair" \
  -F "reason=After Shut Down" \
  -F "defects=w shift" \
  -F "defects=L shift" \
  -F "judgement_block_a=Good" \
  -F "judgement_block_b=NG" \
  -F "judgement_block_c=Good" \
  -F "judgement_block_d=NG" \
  -F "shifting_amount_a=10" \
  -F "shifting_amount_b=20" \
  -F "shifting_amount_c=15" \
  -F "shifting_amount_d=25" \
  -F "shifting_direction_a=W shift front" \
  -F "shifting_direction_b=L shift right" \
  -F "shifting_direction_c=good" \
  -F "shifting_direction_d=W shift back" \
  -F "quality_case=open" \
  -F "process_selection=Cutting Feedback" \
  -F "grid=[[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false]]" \
  -F "photos=@/path/to/photo1.jpg" \
  -F "photos=@/path/to/photo2.jpg"
```

**Using JSON data field (alternative):**

```bash
curl -X POST http://localhost:5000/api/a1/submit \
  -F "data={\"date_time\":\"2024-01-15 10:30:00\",\"lot_number\":\"12345\",\"item_type\":\"TypeA\",\"gsx_machine_no\":\"GSX001\",\"mc_machine_no\":\"MC001\",\"cut_operator_payroll\":\"OP001\",\"ng_block_lot\":\"5\",\"ng_chip_qty_lot\":\"10\",\"block_number\":\"B001\",\"confirm_date\":\"2024-01-15\",\"reason\":[\"After Repair\"],\"defects\":[\"w shift\"],\"judgement_block_a\":\"Good\",\"judgement_block_b\":\"NG\",\"judgement_block_c\":\"Good\",\"judgement_block_d\":\"NG\",\"shifting_amount_a\":\"10\",\"shifting_amount_b\":\"20\",\"shifting_amount_c\":\"15\",\"shifting_amount_d\":\"25\",\"shifting_direction_a\":[\"W shift front\"],\"shifting_direction_b\":[\"L shift right\"],\"shifting_direction_c\":[\"good\"],\"shifting_direction_d\":[\"W shift back\"],\"quality_case\":\"open\",\"process_selection\":[\"Cutting Feedback\"],\"grid\":[[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false],[false,false,false,false,false,false]]}" \
  -F "photos=@/path/to/photo1.jpg"
```

### GET /api/a1/history

Retrieve A1 feedback history.

```bash
curl http://localhost:5000/api/a1/history
```

### GET /api/a1/history/download

Download A1 history as Excel file.

```bash
curl http://localhost:5000/api/a1/history/download -o history_A1.xlsx
```

## GHM Cutting Process Feedback

### POST /api/ghm/submit

Submit GHM cutting process feedback form.

```bash
curl -X POST http://localhost:5000/api/ghm/submit \
  -F "date_time=2024-01-15 10:30:00" \
  -F "lot_number=12345" \
  -F "item_type=TypeB" \
  -F "mln_machine_no=MLN001" \
  -F "mc_machine_no=MC001" \
  -F "cut_operator_payroll=OP001" \
  -F "ng_block_lot=5" \
  -F "ng_chip_qty_lot=10" \
  -F "block_number=B001" \
  -F "confirm_date=2024-01-15" \
  -F "reason=After Repair" \
  -F "defects=w shift" \
  -F "judgement=Good" \
  -F "shifting_amount=10" \
  -F "shifting_direction=W shift front" \
  -F "quality_case=open" \
  -F "process_selection=Cutting Feedback" \
  -F "grid=[[false,false,false],[false,false,false],[false,false,false]]" \
  -F "photos=@/path/to/photo1.jpg"
```

### GET /api/ghm/history

```bash
curl http://localhost:5000/api/ghm/history
```

### GET /api/ghm/history/download

```bash
curl http://localhost:5000/api/ghm/history/download -o history_GHM.xlsx
```

## KEM Cutting Process Feedback

### POST /api/kem/submit

Submit KEM cutting process feedback form.

```bash
curl -X POST http://localhost:5000/api/kem/submit \
  -F "date_time=2024-01-15 10:30:00" \
  -F "lot_number=12345" \
  -F "item_type=TypeC" \
  -F "erst_machine_no=ERST001" \
  -F "mc_machine_no=MC001" \
  -F "cut_operator_payroll=OP001" \
  -F "ng_block_lot=5" \
  -F "ng_chip_qty_lot=10" \
  -F "block_number=B001" \
  -F "confirm_date=2024-01-15" \
  -F "reason=After Repair" \
  -F "defects=w shift" \
  -F "judgement=Good" \
  -F "shifting_amount=10" \
  -F "shifting_direction=W shift front" \
  -F "quality_case=open" \
  -F "process_selection=Cutting Feedback" \
  -F "grid=[[false,false,false],[false,false,false],[false,false,false]]" \
  -F "photos=@/path/to/photo1.jpg"
```

### GET /api/kem/history

```bash
curl http://localhost:5000/api/kem/history
```

### GET /api/kem/history/download

```bash
curl http://localhost:5000/api/kem/history/download -o history_KEM.xlsx
```

## Postman Collection

### Setup

1. Create a new Postman collection
2. Set base URL variable: `{{base_url}}` = `http://localhost:5000`

### A1 Submit Request

- **Method:** POST
- **URL:** `{{base_url}}/api/a1/submit`
- **Body Type:** form-data
- **Fields:**
  - Add all form fields as key-value pairs
  - Add `photos` as file type (can add multiple)
  - For arrays (reason, defects, etc.), add multiple entries with same key
  - For grid, add as text field with JSON string

### Common Headers

No special headers required for most endpoints. CORS is handled automatically.

## Error Responses

All endpoints return JSON error responses in this format:

```json
{
  "error": "Error type",
  "message": "Error message",
  "details": {}  // Optional, for validation errors
}
```

### Common Error Codes

- `400`: Bad Request (validation errors)
- `404`: Not Found
- `500`: Internal Server Error

## Notes

1. Grid data must be a valid JSON string representing a 2D boolean array
2. A1 grid must be 6x6
3. GHM and KEM grids must be 3x3
4. All file uploads must be images (jpg, jpeg, png)
5. Maximum file size is 10MB by default (configurable)
6. All required fields must be provided



