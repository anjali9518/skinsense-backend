# Quick Start Guide - Backend API

## Installation

1. **Install Flask-CORS:**
```bash
pip install flask-cors
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

**Option 1: Use the new API file**
```bash
python api.py
```

**Option 2: Keep using app.py (if you want)**
The old `app.py` still works for the full website with templates.

## Test the API

### 1. Health Check
```bash
curl http://localhost:2500/api/health
```

### 2. Analyze Image
```bash
curl -X POST http://localhost:2500/api/analyze -F "file=@path/to/your/image.jpg"
```

### 3. Get Classification Info
```bash
curl http://localhost:2500/api/info
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check if API is running |
| POST | `/api/analyze` | Upload image for analysis |
| GET | `/api/images/{filename}` | Get uploaded image |
| GET | `/api/info` | Get all classification info |

## What Changed?

### Old (app.py) - Full Website
- Returns HTML templates
- Has frontend UI built-in
- Routes: `/`, `/home`, `/try_now`, `/learn`

### New (api.py) - Backend API Only
- Returns JSON responses
- No frontend (frontend connects via HTTP)
- Routes: `/api/health`, `/api/analyze`, `/api/images/*`, `/api/info`
- CORS enabled for any origin
- Better error handling

## Frontend Integration

Your frontend developer needs:
1. **API_TECH_SPEC.md** - Complete technical documentation
2. **Base URL:** `http://localhost:2500` (update for production)
3. **CORS:** Already configured, no extra setup needed

## Example Frontend Request

```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:2500/api/analyze', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.diagnosis); // "Melanoma", "No Cancer Detected", etc.
```

## Important Files

- **api.py** - New backend API (use this for frontend integration)
- **app.py** - Old full-stack app (use this for the complete website)
- **API_TECH_SPEC.md** - Complete API documentation for your frontend developer
- **requirements.txt** - Updated with Flask-CORS

## Next Steps

1. Start the API: `python api.py`
2. Send **API_TECH_SPEC.md** to your frontend developer
3. Test endpoints with curl or Postman
4. Update BASE_URL when deploying to production
