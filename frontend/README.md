# CitiTrack Frontend

Progressive Web App (PWA) for CitiTrack platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with API URL
```

3. Run development server:
```bash
npm start
```

4. Build for production:
```bash
npm run build
```

## Features

- ✅ Offline-first architecture
- ✅ Service Workers for caching
- ✅ IndexedDB for local storage
- ✅ Responsive design
- ✅ Multilingual support
- ✅ Photo upload
- ✅ Geolocation

## Project Structure

```
src/
├── components/          # React components
├── services/            # API & offline services
├── hooks/               # Custom React hooks
├── utils/               # Utilities
└── App.jsx              # Main application
```