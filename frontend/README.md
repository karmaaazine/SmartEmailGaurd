# 🎣 Catch a Phish! - React Frontend

A beautiful, responsive React application for email security and phishing detection with a beach theme.

## 🌊 Features

- **Beach-themed UI**: Beautiful ocean gradients and beach-inspired design
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Analysis**: Instant email scanning with AI-powered detection
- **Interactive Charts**: Data visualization with Recharts
- **Smooth Animations**: Framer Motion for delightful user experience
- **File Upload**: Support for .txt and .eml files
- **Sample Emails**: Built-in test emails for demonstration
- **Scan History**: View and analyze previous scans
- **Statistics Dashboard**: Comprehensive analytics and insights

## 🚀 Quick Start

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── index.html          # Main HTML file
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/         # React components
│   │   ├── Navigation.js   # Navigation bar
│   │   ├── Hero.js         # Hero section
│   │   ├── EmailScanner.js # Main scanner interface
│   │   ├── ResultDisplay.js # Scan results display
│   │   ├── ScanHistory.js  # History and analytics
│   │   ├── Statistics.js   # Statistics dashboard
│   │   └── About.js        # About page
│   ├── App.js              # Main app component
│   ├── App.css             # App-specific styles
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## 🎨 Design System

### Color Palette
- **Ocean Blue**: `#1e3a8a` - Primary brand color
- **Sand Beige**: `#fef3c7` - Background and cards
- **Coral Orange**: `#fb7185` - Accent and warnings
- **Seafoam Green**: `#34d399` - Success states
- **Sunset Yellow**: `#fbbf24` - Highlights and borders
- **Wave Blue**: `#0ea5e9` - Secondary actions

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Responsive**: Clamp functions for fluid typography

### Components
- **Beach Cards**: Rounded containers with gradient backgrounds
- **Wave Dividers**: Ocean-themed section separators
- **Metric Cards**: Statistics display with ocean styling
- **Result Boxes**: Color-coded analysis results
- **Animated Elements**: Floating fish and smooth transitions

## 🔧 Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (irreversible)

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: Below 768px
- **Small Mobile**: Below 480px

## 🌊 Beach Theme Elements

### Visual Elements
- **Ocean Gradient Background**: Deep blue to light blue gradient
- **Sand-colored Cards**: Warm beige backgrounds for content
- **Wave Dividers**: Curved ocean wave separators
- **Floating Fish**: Animated swimming fish across the screen
- **Beach Icons**: Ocean-themed emojis throughout the interface

### Terminology
- **"Cast Your Net"** instead of "Scan Email"
- **"Catch Report"** instead of "Analysis Result"
- **"Fishing Metrics"** instead of "Features"
- **"Beach Patrol"** instead of "Navigation"
- **"Catch Log"** instead of "Scan History"

## 📊 Data Visualization

### Charts Used
- **Pie Charts**: Classification distribution
- **Area Charts**: Activity over time
- **Bar Charts**: Confidence scores
- **Responsive**: All charts adapt to screen size

### Libraries
- **Recharts**: Main charting library
- **Framer Motion**: Smooth animations
- **React Icons**: Icon library

## 🔒 Security Features

- **API Key Authentication**: All requests include `x-api-key` header
- **Input Validation**: Client-side validation for all inputs
- **HTTPS Ready**: Configured for secure connections
- **No Data Storage**: Client-side only, no persistent storage

## 🎯 User Experience

### Loading States
- **Spinner Animations**: Ocean-themed loading indicators
- **Skeleton Screens**: Placeholder content while loading
- **Progress Indicators**: Step-by-step process feedback

### Error Handling
- **User-friendly Messages**: Clear error explanations
- **Graceful Degradation**: App continues working with partial failures
- **Retry Mechanisms**: Easy recovery from network issues

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and semantic HTML
- **Color Contrast**: WCAG compliant color combinations
- **Focus Management**: Clear focus indicators

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Netlify**: Drag and drop `build` folder
- **Vercel**: Connect GitHub repository
- **Firebase**: Use Firebase Hosting
- **AWS S3**: Upload to S3 bucket

### Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=your_api_key_here
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the "Catch a Phish!" email security application.

## 🏖️ Support

For support and questions:
- 🌊 Email: support@catchaphish.com
- 🏖️ Website: www.catchaphish.com
- 🎣 GitHub: github.com/catchaphish

---

**Built with ❤️ for email security and beach vibes! 🏖️🎣** 