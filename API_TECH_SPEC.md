# Skin Cancer Detection API - Technical Specification

**Version:** 1.0.0  
**Base URL:** `http://localhost:2500`  
**Protocol:** HTTP/HTTPS  
**Data Format:** JSON  
**Last Updated:** February 7, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Integration Guide](#integration-guide)
8. [Code Examples](#code-examples)

---

## Overview

The Skin Cancer Detection API provides AI-powered analysis of skin lesion images using deep learning models. The API accepts image uploads and returns detailed diagnostic information including cancer type classification, confidence scores, and medical recommendations.

### Key Features

- **AI-Powered Analysis:** Deep learning model trained on dermatological images
- **8 Classification Types:** Identifies 7 types of skin conditions + healthy skin
- **High Accuracy:** Confidence scores for each prediction
- **CORS Enabled:** Frontend integration from any origin
- **File Upload Support:** PNG, JPG, JPEG, GIF up to 10MB

### Tech Stack

- **Backend:** Flask (Python)
- **ML Framework:** TensorFlow/Keras
- **Image Processing:** Pillow, NumPy
- **CORS:** Flask-CORS

---

## Authentication

**Current Version:** No authentication required  
**Future Versions:** May implement API key authentication

All endpoints are currently open. For production deployment, consider implementing:
- API key authentication via headers
- OAuth 2.0 for user-specific data
- Rate limiting per IP address

---

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API server and ML model are operational.

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:2500
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-02-07T10:30:00.123456",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Model not loaded or service down

---

### 2. Analyze Image

**Endpoint:** `POST /api/analyze`

**Description:** Upload and analyze a skin lesion image.

**Content-Type:** `multipart/form-data`

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Image file (PNG, JPG, JPEG, GIF) max 10MB |

**Request Example:**
```http
POST /api/analyze HTTP/1.1
Host: localhost:2500
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="lesion.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary--
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "diagnosis_class": 6,
  "diagnosis": "Melanoma",
  "confidence": 0.92,
  "severity": "critical",
  "description": "Most dangerous form of skin cancer. Early detection is crucial.",
  "recommendation": "URGENT: Immediate consultation with dermatologist required.",
  "probabilities": {
    "Actinic keratoses and intraepithelial carcinomae": 0.01,
    "Basal Cell Carcinoma": 0.03,
    "Benign Keratosis": 0.00,
    "Dermatofibroma": 0.01,
    "Melanocytic nevus": 0.02,
    "Vascular Lesion": 0.01,
    "Melanoma": 0.92,
    "No Cancer Detected": 0.00
  },
  "image": {
    "filename": "20260207_103000_a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
    "original_filename": "lesion.jpg",
    "url": "/api/images/20260207_103000_a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
    "upload_time": "2026-02-07T10:30:00.123456"
  }
}
```

**Error Responses:**

**400 Bad Request** - Invalid request:
```json
{
  "success": false,
  "error": "No file provided. Please upload an image."
}
```

**400 Bad Request** - Invalid file type:
```json
{
  "success": false,
  "error": "Invalid file type. Allowed types: PNG, JPG, JPEG, GIF"
}
```

**413 Payload Too Large** - File too large:
```json
{
  "success": false,
  "error": "File too large. Maximum size is 10MB"
}
```

**503 Service Unavailable** - Model not loaded:
```json
{
  "success": false,
  "error": "Model not loaded. Please contact administrator."
}
```

**500 Internal Server Error** - Processing error:
```json
{
  "success": false,
  "error": "Image analysis failed: [error details]"
}
```

---

### 3. Get Image

**Endpoint:** `GET /api/images/{filename}`

**Description:** Retrieve a previously uploaded image.

**Request:**
```http
GET /api/images/20260207_103000_a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg HTTP/1.1
Host: localhost:2500
```

**Response:**
- **200 OK** - Returns the image file
- **404 Not Found** - Image not found

---

### 4. Get Classification Info

**Endpoint:** `GET /api/info`

**Description:** Get detailed information about all cancer classifications.

**Request:**
```http
GET /api/info HTTP/1.1
Host: localhost:2500
```

**Response (200 OK):**
```json
{
  "success": true,
  "classifications": [
    {
      "id": 0,
      "name": "Actinic keratoses and intraepithelial carcinomae",
      "severity": "moderate",
      "description": "Pre-cancerous skin condition that may develop into squamous cell carcinoma.",
      "recommendation": "Consult a dermatologist for evaluation and treatment."
    },
    {
      "id": 1,
      "name": "Basal Cell Carcinoma",
      "severity": "high",
      "description": "The most common form of skin cancer, grows slowly and rarely spreads.",
      "recommendation": "Immediate medical consultation required for proper treatment."
    },
    {
      "id": 2,
      "name": "Benign Keratosis",
      "severity": "low",
      "description": "Non-cancerous growth, usually harmless but should be monitored.",
      "recommendation": "Regular monitoring recommended. Consult dermatologist if changes occur."
    },
    {
      "id": 3,
      "name": "Dermatofibroma",
      "severity": "low",
      "description": "Benign fibrous nodule, generally harmless.",
      "recommendation": "Usually no treatment needed unless causing discomfort."
    },
    {
      "id": 4,
      "name": "Melanocytic nevus",
      "severity": "low",
      "description": "Common mole, typically benign but should be monitored.",
      "recommendation": "Monitor for changes using ABCDE method. Annual checkup recommended."
    },
    {
      "id": 5,
      "name": "Vascular Lesion",
      "severity": "low",
      "description": "Abnormality of blood vessels, usually benign.",
      "recommendation": "Consult dermatologist if rapidly changing or bleeding."
    },
    {
      "id": 6,
      "name": "Melanoma",
      "severity": "critical",
      "description": "Most dangerous form of skin cancer. Early detection is crucial.",
      "recommendation": "URGENT: Immediate consultation with dermatologist required."
    },
    {
      "id": 7,
      "name": "No Cancer Detected",
      "severity": "none",
      "description": "No signs of cancer detected in the analysis.",
      "recommendation": "Continue regular self-examinations and annual dermatologist visits."
    }
  ]
}
```

---

## Data Models

### Analysis Result Model

```typescript
interface AnalysisResult {
  success: boolean;
  diagnosis_class: number;         // 0-7
  diagnosis: string;                // Human-readable diagnosis
  confidence: number;               // 0.0 - 1.0
  severity: 'none' | 'low' | 'moderate' | 'high' | 'critical';
  description: string;              // Medical description
  recommendation: string;           // Medical recommendation
  probabilities: {
    [key: string]: number;         // All class probabilities
  };
  image: ImageInfo;
}

interface ImageInfo {
  filename: string;                // Unique server filename
  original_filename: string;       // Original upload filename
  url: string;                     // Relative URL to retrieve image
  upload_time: string;             // ISO 8601 timestamp
}
```

### Classification Model

```typescript
interface Classification {
  id: number;                      // 0-7
  name: string;                    // Classification name
  severity: 'none' | 'low' | 'moderate' | 'high' | 'critical';
  description: string;             // Medical description
  recommendation: string;          // Medical recommendation
}
```

### Error Model

```typescript
interface ErrorResponse {
  success: false;
  error: string;                   // Error message
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Endpoint or resource not found |
| 413 | Payload Too Large - File exceeds 10MB |
| 500 | Internal Server Error - Processing failed |
| 503 | Service Unavailable - Model not loaded |

### Error Response Format

All errors return a consistent JSON format:

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

---

## Rate Limiting

**Current Version:** No rate limiting implemented

**Recommended for Production:**
- Implement rate limiting: 100 requests per hour per IP
- Use Redis or similar for distributed rate limiting
- Return `429 Too Many Requests` when limit exceeded

---

## Integration Guide

### Frontend Integration Checklist

1. **CORS Configuration**
   - API already configured to accept requests from any origin
   - No additional configuration needed

2. **File Upload**
   - Use `FormData` for file uploads
   - Set `Content-Type: multipart/form-data`
   - Maximum file size: 10MB
   - Supported formats: PNG, JPG, JPEG, GIF

3. **Image Preview**
   - Use returned `image.url` to display uploaded image
   - Full URL: `${BASE_URL}${image.url}`

4. **Error Handling**
   - Check `success` field in response
   - Display `error` message to user if `success === false`

5. **Loading States**
   - Show spinner during upload/analysis
   - Average processing time: 1-3 seconds

6. **Result Display**
   - Show `diagnosis` prominently
   - Display `confidence` as percentage
   - Use `severity` for color coding:
     - `none`: Green
     - `low`: Blue
     - `moderate`: Yellow
     - `high`: Orange
     - `critical`: Red
   - Display `recommendation` with appropriate urgency

---

## Code Examples

### JavaScript (Fetch API)

```javascript
// Upload and analyze image
async function analyzeImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:2500/api/analyze', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      console.log('Diagnosis:', result.diagnosis);
      console.log('Confidence:', (result.confidence * 100).toFixed(2) + '%');
      console.log('Severity:', result.severity);
      console.log('Recommendation:', result.recommendation);
      
      // Display uploaded image
      const imageUrl = `http://localhost:2500${result.image.url}`;
      console.log('Image URL:', imageUrl);
    } else {
      console.error('Error:', result.error);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Usage with file input
document.getElementById('fileInput').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    analyzeImage(file);
  }
});
```

### React.js Example

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:2500';

function SkinAnalyzer() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/analyze`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      none: 'green',
      low: 'blue',
      moderate: 'yellow',
      high: 'orange',
      critical: 'red',
    };
    return colors[severity] || 'gray';
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !file}>
          {loading ? 'Analyzing...' : 'Analyze Image'}
        </button>
      </form>

      {error && (
        <div style={{ color: 'red' }}>
          Error: {error}
        </div>
      )}

      {result && (
        <div>
          <h2>Analysis Results</h2>
          
          {/* Display uploaded image */}
          <img
            src={`${API_BASE_URL}${result.image.url}`}
            alt="Uploaded lesion"
            style={{ maxWidth: '300px' }}
          />
          
          {/* Diagnosis */}
          <div style={{ color: getSeverityColor(result.severity) }}>
            <h3>{result.diagnosis}</h3>
            <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
            <p>Severity: {result.severity}</p>
          </div>
          
          {/* Description */}
          <p>{result.description}</p>
          
          {/* Recommendation */}
          <div style={{ 
            padding: '10px', 
            backgroundColor: '#f0f0f0',
            borderLeft: `4px solid ${getSeverityColor(result.severity)}`
          }}>
            <strong>Recommendation:</strong> {result.recommendation}
          </div>
          
          {/* Probabilities */}
          <details>
            <summary>All Probabilities</summary>
            <ul>
              {Object.entries(result.probabilities).map(([name, prob]) => (
                <li key={name}>
                  {name}: {(prob * 100).toFixed(2)}%
                </li>
              ))}
            </ul>
          </details>
        </div>
      )}
    </div>
  );
}

export default SkinAnalyzer;
```

### Python (Requests)

```python
import requests

API_BASE_URL = 'http://localhost:2500'

def analyze_image(image_path):
    """Upload and analyze an image"""
    url = f'{API_BASE_URL}/api/analyze'
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        
        if result['success']:
            print(f"Diagnosis: {result['diagnosis']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Severity: {result['severity']}")
            print(f"Recommendation: {result['recommendation']}")
            print(f"Image URL: {API_BASE_URL}{result['image']['url']}")
            return result
        else:
            print(f"Error: {result['error']}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

# Usage
result = analyze_image('path/to/lesion.jpg')
```

### cURL

```bash
# Analyze image
curl -X POST http://localhost:2500/api/analyze \
  -F "file=@lesion.jpg"

# Health check
curl http://localhost:2500/api/health

# Get classification info
curl http://localhost:2500/api/info
```

---

## Best Practices

### 1. File Validation (Frontend)

```javascript
function validateFile(file) {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
  
  if (file.size > maxSize) {
    return 'File size exceeds 10MB';
  }
  
  if (!allowedTypes.includes(file.type)) {
    return 'Invalid file type. Please upload PNG, JPG, JPEG, or GIF';
  }
  
  return null; // Valid
}
```

### 2. Image Preview Before Upload

```javascript
function previewImage(file, imgElement) {
  const reader = new FileReader();
  reader.onload = (e) => {
    imgElement.src = e.target.result;
  };
  reader.readAsDataURL(file);
}
```

### 3. Progress Indication

```javascript
async function analyzeWithProgress(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post('http://localhost:2500/api/analyze', formData, {
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      onProgress(percentCompleted);
    }
  });
}
```

### 4. Retry Logic

```javascript
async function analyzeWithRetry(file, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await analyzeImage(file);
      return response;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

---

## Deployment Considerations

### Environment Variables

```bash
# .env file
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MODEL_PATH=/path/to/model.h5
UPLOAD_DIR=/path/to/uploads
MAX_FILE_SIZE=10485760
PORT=2500
```

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use production WSGI server (gunicorn, uWSGI)
- [ ] Implement API key authentication
- [ ] Add rate limiting
- [ ] Set up HTTPS/SSL
- [ ] Configure proper CORS origins (remove `*`)
- [ ] Set up file cleanup job (delete old uploads)
- [ ] Implement request logging
- [ ] Set up monitoring and alerts
- [ ] Use cloud storage for uploaded images (S3, Azure Blob)

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://127.0.0.1:2500;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## Support

For technical support or questions:
- **API Issues:** Check `/api/health` endpoint
- **Model Issues:** Verify model file exists at configured path
- **Integration Help:** Refer to code examples above

---

## Changelog

### Version 1.0.0 (2026-02-07)
- Initial API release
- Image upload and analysis
- 8 classification types
- CORS enabled
- Health check endpoint
- Classification info endpoint

---

## License

[Your License Information]

---

**Document End**
