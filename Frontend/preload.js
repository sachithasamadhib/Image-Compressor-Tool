const { contextBridge, ipcRenderer } = require("electron");
const CONFIG = require("./config");

console.log("Preload script loaded");
console.log("CONFIG:", CONFIG);

contextBridge.exposeInMainWorld("api", {
  compressImage: async (formData, quality, maxSize, aspectRatio, compressionMethod = 'jpeg') => {
    const axios = require("axios");
    try {
      const response = await axios.post(`${CONFIG.API_BASE_URL}/upload-images/${quality}/${maxSize}/${aspectRatio}/${compressionMethod}`, formData, {
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
  },
  
  getCompressionMethods: async () => {
    const axios = require("axios");
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/compression-methods`);
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },
  
  compressImageHuffman: async (formData) => {
    const axios = require("axios");
    try {
      const response = await axios.post(`${CONFIG.API_BASE_URL}/compress-huffman`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },
  
  testConnection: async () => {
    const axios = require("axios");
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/test-connection`);
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  },

  // Dialog API for folder selection
  showOpenDialog: async (options) => {
    try {
      const result = await ipcRenderer.invoke('dialog:openDirectory', options);
      return result;
    } catch (error) {
      return { error: error.message };
    }
  }
});

// Expose electronAPI for direct access
contextBridge.exposeInMainWorld("electronAPI", {
  showOpenDialog: async (options) => {
    try {
      const result = await ipcRenderer.invoke('dialog:openDirectory', options);
      return result;
    } catch (error) {
      return { error: error.message };
    }
  }
});
