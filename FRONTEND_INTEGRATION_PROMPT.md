# Frontend Integration Prompt

## Project Overview

You are tasked with integrating the existing React/TypeScript frontend UI with a Flask backend API for a Skin Cancer Detection application. The frontend design is complete, and the backend API is fully functional. Your job is to connect them.

## Resources Available

### 1. UI Design Project
**Location:** `C:\Anjali\mysite\ui_design_project\skin-guardian`

This is a fully designed React + TypeScript + Vite application with:
- Beautiful dark theme UI with glassmorphism effects
- Animated backgrounds with particle effects
- Three main pages: Home (Index), SkinSense, and Learn
- All UI components are built using Radix UI and shadcn/ui
- Framer Motion animations throughout
- Tailwind CSS for styling

**Key Files:**
- `src/pages/Index.tsx` - Home page with hero section
- `src/pages/SkinSense.tsx` - Upload/analysis page (needs backend integration)
- `src/pages/Learn.tsx` - Educational content page
- `src/App.tsx` - Main app component with routing

### 2. Backend API Documentation
**Location:** `C:\Anjali\mysite\API_TECH_SPEC.md`

Complete technical specification with:
- All API endpoints
- Request/response formats
- Error handling
- TypeScript interfaces
- Code examples in JavaScript, React, and Python

**API Base URL:** `http://localhost:2500`

**Key Endpoints:**
- `GET /api/health` - Health check
- `POST /api/analyze` - Upload image and get diagnosis
- `GET /api/images/{filename}` - Retrieve uploaded images
- `GET /api/info` - Get cancer classification information

## Your Task

### Primary Objective
Modify the existing `SkinSense.tsx` page to integrate with the backend API. Currently, it has a mock implementation with `setAnalyzing(true)` and a 3-second timeout. You need to replace this with real API calls to the Flask backend.

### Specific Requirements

#### 1. File Upload Integration
- **Current State:** The UI has drag-drop file upload already built
- **What to Change:** Connect the file upload to `POST /api/analyze` endpoint
- **File:** `src/pages/SkinSense.tsx`
- **Function:** `handleAnalyze()` function needs to call the real API

#### 2. Display Results
The API returns this response structure:
```typescript
{
  success: true,
  diagnosis: "Melanoma",
  confidence: 0.92,
  severity: "critical",
  description: "Most dangerous form of skin cancer...",
  recommendation: "URGENT: Immediate consultation...",
  probabilities: { ... },
  image: {
    filename: "...",
    url: "/api/images/..."
  }
}
```

**Requirements:**
- Display the uploaded image using the returned `image.url`
- Show the `diagnosis` prominently
- Display `confidence` as a percentage
- Use `severity` for color coding:
  - `none`: Green
  - `low`: Blue  
  - `moderate`: Yellow
  - `high`: Orange
  - `critical`: Red
- Show the `description` and `recommendation`
- Optionally show all `probabilities` in an expandable section

#### 3. Error Handling
- Handle all error cases from the API (400, 413, 500, 503)
- Display user-friendly error messages
- Show validation errors before API call (file size, file type)

#### 4. Loading States
- Show a loading spinner during upload
- Show upload progress if possible
- Disable the analyze button while processing

#### 5. Configuration
Create an API configuration file:

**File to Create:** `src/config/api.ts`
```typescript
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:2500',
  ENDPOINTS: {
    HEALTH: '/api/health',
    ANALYZE: '/api/analyze',
    INFO: '/api/info',
    IMAGES: '/api/images'
  },
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']
};
```

#### 6. API Service Layer
Create a service file for API calls:

**File to Create:** `src/services/api.service.ts`

This should include:
- `healthCheck()` - Check API status
- `analyzeImage(file: File)` - Upload and analyze image
- `getClassificationInfo()` - Get all classifications
- `getImageUrl(filename: string)` - Build full image URL

Use `axios` or `fetch` for HTTP requests.

#### 7. State Management
Add proper state management in `SkinSense.tsx`:
- `analyzing: boolean` - Loading state
- `result: AnalysisResult | null` - API response
- `error: string | null` - Error messages
- `uploadProgress: number` - Upload progress (0-100)

#### 8. Environment Variables
Create `.env` file:
```
VITE_API_URL=http://localhost:2500
```

And `.env.production`:
```
VITE_API_URL=https://your-production-api.com
```

### Additional Enhancements (Optional but Recommended)

1. **Toast Notifications**
   - Success: "Analysis complete!"
   - Error: Show error message
   - Use the existing Sonner toaster from the UI

2. **Result History**
   - Store past analyses in localStorage
   - Allow users to view previous results

3. **Image Validation**
   - Check file size before upload
   - Check file type before upload
   - Show preview before analysis

4. **Retry Logic**
   - Implement retry on network failures
   - Show retry button on error

5. **Health Check**
   - Check API health on app mount
   - Show warning banner if API is down

## Implementation Steps

### Step 1: Install Dependencies
```bash
cd C:\Anjali\mysite\ui_design_project\skin-guardian
npm install axios
```

### Step 2: Create API Configuration
Create `src/config/api.ts` with the configuration above.

### Step 3: Create API Service
Create `src/services/api.service.ts` with all API functions.

### Step 4: Create TypeScript Interfaces
Create `src/types/api.types.ts`:
```typescript
export interface AnalysisResult {
  success: boolean;
  diagnosis: string;
  diagnosis_class: number;
  confidence: number;
  severity: 'none' | 'low' | 'moderate' | 'high' | 'critical';
  description: string;
  recommendation: string;
  probabilities: Record<string, number>;
  image: {
    filename: string;
    original_filename: string;
    url: string;
    upload_time: string;
  };
}

export interface ErrorResponse {
  success: false;
  error: string;
}

export interface Classification {
  id: number;
  name: string;
  severity: string;
  description: string;
  recommendation: string;
}
```

### Step 5: Update SkinSense.tsx
Modify the `handleAnalyze` function to call the real API and display results.

### Step 6: Test Integration
1. Start the backend: `python api.py` (from C:\Anjali\mysite)
2. Start the frontend: `npm run dev`
3. Test file upload and analysis
4. Verify error handling
5. Check all edge cases

### Step 7: Add Environment Setup
Create `.env` and `.env.production` files.

## Code Examples

### Example API Service Implementation

```typescript
// src/services/api.service.ts
import axios from 'axios';
import { API_CONFIG } from '@/config/api';
import type { AnalysisResult, Classification } from '@/types/api.types';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 30000,
});

export const apiService = {
  async healthCheck() {
    const response = await api.get(API_CONFIG.ENDPOINTS.HEALTH);
    return response.data;
  },

  async analyzeImage(file: File, onProgress?: (progress: number) => void) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<AnalysisResult>(
      API_CONFIG.ENDPOINTS.ANALYZE,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(progress);
          }
        },
      }
    );

    return response.data;
  },

  async getClassificationInfo() {
    const response = await api.get<{ success: boolean; classifications: Classification[] }>(
      API_CONFIG.ENDPOINTS.INFO
    );
    return response.data;
  },

  getImageUrl(filename: string) {
    return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.IMAGES}/${filename}`;
  },
};
```

### Example SkinSense.tsx Integration

```typescript
// In SkinSense.tsx - Update handleAnalyze function
const handleAnalyze = async () => {
  if (!file) return;

  setAnalyzing(true);
  setError(null);
  setResult(null);

  try {
    const result = await apiService.analyzeImage(file, setUploadProgress);
    
    if (result.success) {
      setResult(result);
      toast.success('Analysis complete!');
    } else {
      setError(result.error);
      toast.error(result.error);
    }
  } catch (err: any) {
    const errorMessage = err.response?.data?.error || 'Analysis failed. Please try again.';
    setError(errorMessage);
    toast.error(errorMessage);
  } finally {
    setAnalyzing(false);
  }
};
```

## Testing Checklist

- [ ] Backend API is running on `http://localhost:2500`
- [ ] Health check endpoint works
- [ ] File upload accepts valid image files
- [ ] File upload rejects invalid files (wrong type, too large)
- [ ] Analysis returns results correctly
- [ ] Results are displayed with proper formatting
- [ ] Severity colors are applied correctly
- [ ] Uploaded image is displayed
- [ ] Error messages are user-friendly
- [ ] Loading states work correctly
- [ ] Upload progress is shown (if implemented)
- [ ] Toast notifications appear (if implemented)
- [ ] Mobile responsive design is maintained

## Important Notes

1. **CORS:** Backend is already configured to accept requests from any origin
2. **No Authentication:** Current API has no auth; add if needed for production
3. **File Storage:** Backend stores files in `C:\Anjali\mysite\static\uploads`
4. **Model:** Backend uses TensorFlow model for predictions (already configured)
5. **Design:** Keep all existing animations and UI design intact
6. **TypeScript:** Ensure all code is properly typed

## Deliverables

1. Modified `SkinSense.tsx` with API integration
2. New `src/config/api.ts` file
3. New `src/services/api.service.ts` file
4. New `src/types/api.types.ts` file
5. `.env` file for local development
6. Updated `package.json` if new dependencies added
7. Brief testing report confirming all features work

## Questions to Consider

- Should we add retry logic for failed requests?
- Should we cache previous analysis results?
- Should we add a "Try Another Image" button after results?
- Should we display all probability scores or just top 3?
- Should we add a health check indicator in the UI?

## Success Criteria

✅ User can upload an image via drag-drop or file picker  
✅ Upload shows loading state with optional progress  
✅ Analysis returns results from backend API  
✅ Results display diagnosis, confidence, severity, description, and recommendation  
✅ Uploaded image is displayed in results  
✅ Errors are handled gracefully with user-friendly messages  
✅ All existing UI design and animations remain intact  
✅ Code is clean, typed, and follows React best practices  

---

**Reference Documents:**
- Full API documentation: `C:\Anjali\mysite\API_TECH_SPEC.md`
- Backend code: `C:\Anjali\mysite\api.py`
- UI design project: `C:\Anjali\mysite\ui_design_project\skin-guardian`

**Contact Backend Developer:** If you encounter API issues or need clarification on any endpoint behavior.
