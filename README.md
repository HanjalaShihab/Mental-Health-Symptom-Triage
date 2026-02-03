# Mental Health Symptom Triage

A comprehensive web-based mental health symptom assessment and triage application designed to help evaluate mental health symptoms and provide personalized care recommendations.

## Overview

This application provides:
- **Patient Assessment**: 10-question comprehensive mental health assessment
- **Risk Scoring**: Advanced scoring system to determine risk levels
- **Triage Classification**: Categorization into Low, Mild, Moderate, Severe, or Critical risk levels
- **Personalized Recommendations**: Evidence-based care recommendations based on assessment results
- **Emergency Resources**: Crisis hotline information and emergency protocols for critical cases

## Project Structure

```
Mental Health Symptom Triage/
├── server/                           # Node.js/Express backend
│   ├── index.js                     # Main server file
│   ├── routes/
│   │   ├── assessmentRoutes.js      # Assessment API endpoints
│   │   └── triageRoutes.js          # Triage processing endpoints
│   └── services/
│       ├── assessmentService.js     # Assessment question management
│       └── triageService.js         # Triage logic and scoring
├── client/                           # React frontend
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   ├── App.css                  # Global styles
│   │   ├── main.jsx                 # React entry point
│   │   ├── index.css                # Base styles
│   │   └── components/
│   │       ├── HomePage.jsx         # Landing page
│   │       ├── AssessmentForm.jsx   # Assessment form component
│   │       └── TriageResults.jsx    # Results display component
│   ├── index.html                   # HTML template
│   ├── package.json                 # Client dependencies
│   └── vite.config.js               # Vite configuration
├── package.json                      # Server dependencies
└── README.md                         # This file
```

## Features

### Assessment Module
- 10 comprehensive mental health questions covering:
  - Mood and depression
  - Anxiety and panic
  - Sleep patterns
  - Cognitive function
  - Social withdrawal
  - Physical symptoms
  - Risk factors
  - Daily functioning

### Triage Engine
- **Scoring System**: 0-30 point scale based on symptom severity
- **Risk Levels**:
  - **CRITICAL**: Immediate emergency intervention needed
  - **SEVERE**: Professional intervention required within 24-48 hours
  - **MODERATE**: Professional evaluation within 1-2 weeks
  - **MILD**: Self-care with preventive support
  - **LOW**: Maintenance of healthy lifestyle

### Personalized Recommendations
- Category-specific guidance based on assessment responses
- Evidence-based treatment recommendations
- Resource matching based on risk level
- Next-step action plans

## Technology Stack

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **CORS** - Cross-origin resource sharing
- **UUID** - Unique identifier generation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Setup

1. **Install server dependencies:**
   ```bash
   npm install
   ```

2. **Install client dependencies:**
   ```bash
   cd client
   npm install
   cd ..
   ```

Or install both at once:
   ```bash
   npm run install-all
   ```

## Running the Project

### Development Mode

**Option 1: Run server and client separately**

Terminal 1 - Start the backend server:
```bash
npm run dev
```
Server runs on http://localhost:5000

Terminal 2 - Start the frontend development server:
```bash
npm run client
```
Client runs on http://localhost:3000

**Option 2: Run both concurrently**
```bash
npm run dev:full
```

### Production Build

Build the frontend:
```bash
npm run build
```

## API Endpoints

### Assessment Endpoints
- `GET /api/assessment/questions` - Get all assessment questions
- `GET /api/assessment/categories` - Get question categories
- `GET /api/assessment/questions/category/:category` - Get questions by category
- `GET /api/assessment/question/:id` - Get specific question

### Triage Endpoints
- `POST /api/triage/submit` - Submit assessment and get triage results
- `GET /api/triage/report/:reportId` - Retrieve stored assessment report
- `GET /api/triage/resources/emergency` - Get emergency crisis resources
- `GET /api/triage/resources/:riskLevel` - Get resources based on risk level

## Usage

1. **Start the application** using one of the methods above
2. **Open your browser** to http://localhost:3000
3. **Click "Start Assessment"** on the home page
4. **Enter patient information** (name and age)
5. **Answer all 10 assessment questions** honestly
6. **Submit the assessment** to receive:
   - Risk level classification
   - Detailed scoring breakdown
   - Category-specific recommendations
   - Personalized next steps
   - Emergency resources if needed

## Assessment Scoring

### Scoring Scale
- Each question is scored 0-3 based on severity
- **0** = No or minimal symptoms
- **1** = Mild symptoms
- **2** = Moderate symptoms
- **3** = Severe symptoms

### Risk Level Calculation
- **Low**: 0-25% of maximum possible score
- **Mild**: 25-50%
- **Moderate**: 50-70%
- **Severe**: 70% and above (excluding critical)
- **Critical**: If any risk-related question scores 2 or higher

## Crisis Support

If you or someone you know is in crisis:

| Resource | Contact | Available |
|----------|---------|-----------|
| National Suicide Prevention Lifeline | 988 | 24/7 |
| Crisis Text Line | Text HOME to 741741 | 24/7 |
| SAMHSA National Helpline | 1-800-662-4357 | 24/7 |
| Emergency Services | 911 | 24/7 |

## Important Disclaimer

**This assessment tool is NOT a substitute for professional mental health evaluation.** It provides preliminary screening and symptom assessment only. Always consult with a qualified mental health professional for:
- Accurate diagnosis
- Personalized treatment planning
- Medication management
- Crisis intervention

The results generated by this tool are for informational purposes and should be reviewed with a mental health provider.

## Data Privacy

- This application stores assessment reports in-memory during the session
- For production use, implement proper database and security measures
- Patient data should be encrypted and stored securely
- Comply with HIPAA and relevant healthcare privacy regulations

## Development

### Project Setup with Vite

The client uses Vite for fast development and optimized builds:
- Hot module replacement (HMR) for instant code updates
- Optimized production builds
- Modern ES module support

### Code Organization

- **Services**: Business logic (assessment and triage)
- **Routes**: API endpoint handlers
- **Components**: React UI components
- **Styling**: Component and global CSS files

## Future Enhancements

- Database integration for persistent storage
- User authentication and authorization
- HIPAA-compliant data handling
- Mobile app version
- Advanced analytics and reporting
- Integration with electronic health records (EHR)
- Multi-language support
- Accessibility improvements
- Teletherapy integration

## Contributing

This is a demonstration project for mental health triage. For improvements or modifications:
1. Review the code structure
2. Test thoroughly before deploying
3. Ensure compliance with healthcare regulations
4. Validate changes with healthcare professionals

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please review the code documentation or consult with mental health professionals when deploying this tool in clinical settings.

---

**Important**: This tool is designed to assist in initial mental health screening. It should never replace professional psychiatric or psychological evaluation and care.
