const { contextBridge } = require("electron");
const CONFIG = require("./config");

contextBridge.exposeInMainWorld("api", {
  compressImage: async (formData, quality, maxSize, aspectRatio) => {
    const axios = require("axios");
    try {
      const response = await axios.post(`${CONFIG.API_BASE_URL}/upload-images/${quality}/${maxSize}/${aspectRatio}`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },
  
  getHistory: async (sortBy = 'date', order = 'desc') => {
    const axios = require("axios");
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/history?sort_by=${sortBy}&order=${order}`);
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },
  
  getStatistics: async () => {
    const axios = require("axios");
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/history/statistics`);
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },
  
  clearHistory: async () => {
    const axios = require("axios");
    try {
      const response = await axios.delete(`${CONFIG.API_BASE_URL}/history/clear`);
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  }
});
