# API Documentation: Campaign Management

All secured endpoints require the following header:
- `x-api-key: <your-api-key>`

Base URL: `http://localhost:8000`

## Campaigns Endpoints

### Create Campaign
- **POST** `/campaigns/`
- **Headers:**
  - `Content-Type: application/json`
  - `x-api-key: <your-api-key>`
- **Body:**
  - `Name` (string, required)
  - `Description` (string, optional)
  - `StartDate` (string, required, format: YYYY-MM-DD)
  - `EndDate` (string, required, format: YYYY-MM-DD)
  - `DiscountType` (string, required)
  - `DiscountValue` (number, required)
  - `Status` (string, required; e.g., Draft, Live, Ended)
- **Response:**
  - JSON object of the created campaign

### List Campaigns
- **GET** `/campaigns/`
- **Headers:**
  - `x-api-key: <your-api-key>`
- **Response:**
  - Array of campaign objects

### Example Request: Create Campaign
```http
POST /campaigns/
Content-Type: application/json
x-api-key: <your-api-key>

{
  "Name": "Summer Sale",
  "Description": "Discounts on all summer items!",
  "StartDate": "2025-06-01",
  "EndDate": "2025-06-30",
  "DiscountType": "Percentage",
  "DiscountValue": 20,
  "Status": "Draft"
}
```

### Example Request: List Campaigns
```http
GET /campaigns/
x-api-key: <your-api-key>
```

---
Update this documentation as you add or modify endpoints.
