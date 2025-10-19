// Configuration for frontend API calls
// This file contains the API base URL configuration
const CONFIG = {
    API_BASE_URL: process.env.API_BASE_URL || 'http://127.0.0.1:5000',
    MAX_FILE_SIZE_MB: parseInt(process.env.MAX_FILE_SIZE_MB) || 50,
};

module.exports = CONFIG;