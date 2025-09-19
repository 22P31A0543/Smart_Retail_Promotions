# API Documentation

All secured endpoints require the following header:

- `x-api-key: mysecretapikey`

## Products Endpoints

### Create Product
- **POST** `/products/`
- **Body:**
  - `SKU` (string, required)
  - `ProductName` (string, required)
  - `Price` (number, required)
  - `ImageURL` (string, optional)
- **Response:** Product object
- **Headers:** None required

### List Products
- **GET** `/products/`
- **Response:** List of Product objects
- **Headers:** None required

## Campaigns Endpoints (Secured)

### Create Campaign
- **POST** `/campaigns/`
- **Headers:** `x-api-key: mysecretapikey`
- **Body:**
  - `Name` (string, required)
  - `Description` (string, optional)
  - `StartDate` (date, optional)
  - `EndDate` (date, optional)
  - `DiscountType` (string, optional)
  - `DiscountValue` (number, optional)
  - `Status` (string, optional)
- **Response:** Campaign object

### List Campaigns
- **GET** `/campaigns/`
- **Headers:** `x-api-key: mysecretapikey`
- **Response:** List of Campaign objects

### Get Campaign by ID
- **GET** `/campaigns/{campaign_id}`
- **Headers:** `x-api-key: mysecretapikey`
- **Response:** Campaign object

### Update Campaign
- **PUT** `/campaigns/{campaign_id}`
- **Headers:** `x-api-key: mysecretapikey`
- **Body:** Same as Create Campaign
- **Response:** Updated Campaign object

### Delete Campaign
- **DELETE** `/campaigns/{campaign_id}`
- **Headers:** `x-api-key: mysecretapikey`
- **Response:** `{ "detail": "Campaign deleted" }`

### Publish Campaign
- **POST** `/publishCampaign/{campaign_id}`
- **Headers:** `x-api-key: mysecretapikey`
- **Response:** `{ "detail": "Campaign published", "public_url": "https://mockcampaigns.com/campaign/{campaign_id}" }`

### Get Campaign QR Code
- **GET** `/campaigns/{campaign_id}/qrcode`
- **Headers:** `x-api-key: mysecretapikey`
- **Response:** PNG image (QR code for the campaign public URL)

## General
- All endpoints return JSON except for the QR code endpoint, which returns an image.
- CORS is enabled for all origins, allowing frontend integration from any domain.

---
Update this documentation as you add or modify endpoints.
