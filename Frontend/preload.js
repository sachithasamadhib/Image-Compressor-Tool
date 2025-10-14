const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("api", {
  compressImage: async (formData) => {
    const axios = require("axios");
    try {
      const response = await axios.post("http://127.0.0.1:5000/compress", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  }
});
