// API Configuration
// Switch between local and production environments

const config = {
    // For local development
    local: {
        API_URL: 'http://localhost:5000/api'
    },
    
    // For production (update with your deployed backend URL)
    production: {
        API_URL: 'https://eia-backend.vercel.app/api'  // Replace with your actual backend URL
    }
};

// Auto-detect environment
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1' ||
                window.location.protocol === 'file:';

// Export the appropriate configuration
const API_URL = isLocal ? config.local.API_URL : config.production.API_URL;

console.log('EIA Platform Configuration:', {
    environment: isLocal ? 'local' : 'production',
    apiUrl: API_URL
});