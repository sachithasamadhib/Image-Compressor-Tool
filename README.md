# 📦 Image Compressor Tool

An **Image Compression Tool** that uses **Huffman Coding (Binary Tree based lossless compression)** to reduce image sizes without losing quality.  
The project is built with a **Flask API backend** and a **React + Next.js frontend** for a modern, scalable, and interactive experience.  

---

## 🚀 Features  

- **Lossless Image Compression** using Huffman Coding.  
- **Batch Compression**: Compress multiple images at once.  
- **Compression History Tracker**: View details like file name, original size, compressed size, and date.  
- **Decompression Support**: Restore original image from compressed file.  
- **Cross-Platform Interfaces**:  
  - **Flask REST API** (backend)  
  - **React + Next.js frontend** (web interface)  
- **Performance Metrics**: Compression ratio, time taken, and storage saved.  

---

## 🛠️ Tech Stack  

### Backend  
- **Flask** (Python REST API)  
- **Pillow** – Image processing  
- **heapq** – Huffman Tree construction  
- **collections.Counter** – Frequency analysis  
- **collections.deque** – Queue for batch/history  
- **JSON / MongoDB** – History persistence  

### Frontend  
- **React** + **Next.js** – Interactive frontend  
- **TailwindCSS / CSS Modules** – Styling (customizable)  

### Algorithms Used  
- Huffman Coding (encoding/decoding)  
- Huffman Tree Construction (min-heap)  
- QuickSort (sorting images by size)  
- MergeSort (sorting history)  
- Queue operations (batch/history management)  

---

## 📂 Project Structure  

```
Image-Compressor-Tool/
│── backend/               # Flask API
│   ├── app.py             # Main Flask app
│   ├── compression/       # Huffman coding & utilities
│   ├── static/            # Stored images
│   └── requirements.txt   # Python dependencies
│
│── frontend/              # React + Next.js app
│   ├── pages/             # Next.js pages
│   ├── components/        # UI components
│   ├── styles/            # Styling
│   └── package.json       # Frontend dependencies
│
│── README.md
└── LICENSE
```

---

## ⚙️ Installation & Setup  

### 1. Clone Repository  
```bash
git clone https://github.com/sachithasamadhib/Image-Compressor-Tool.git
cd Image-Compressor-Tool
```

### 2. Environment Configuration
**🔒 Important: Set up environment variables for secure credential management**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your MongoDB credentials and configuration
# See ENV_SETUP.md for detailed configuration guide
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Validate Configuration (Optional)
```bash
python validate_env.py
```

### 5. Run Backend (Flask API)  
```bash
python Controller/AccessPoint.py
```
Flask server will start at: `http://localhost:5000`

### 3. Frontend (React + Next.js)  
```bash
cd frontend
npm install
npm run dev
```
Frontend will start at: `http://localhost:3000`

---

## 🔗 API Endpoints (Flask)  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/compress` | Upload and compress an image |
| `POST` | `/api/batch-compress` | Compress multiple images |
| `GET`  | `/api/history` | Get compression history |
| `POST` | `/api/decompress` | Decompress a compressed image |

---

## 📊 Example Workflow  

1. User uploads a **PNG/BMP image** via frontend.  
2. Flask API applies **Huffman Coding** and returns compressed file.  
3. Compression details (file name, original size, compressed size, ratio) saved in **history**.  
4. User can view/download compressed file or restore original.  

---

## � Security & Configuration

- All database credentials are stored in `.env` file
- `.env` is included in `.gitignore` for security
- Use `.env.example` as a template for your configuration
- See `ENV_SETUP.md` for detailed configuration guide

### Quick Security Setup:
```bash
cp .env.example .env
# Edit .env with your credentials
python validate_env.py  # Validate configuration
```

---

## �👥 Contributors
We are grateful to the following contributors for their valuable efforts in making this possible:

- [Viraj Wathsala Gunasinghe](https://github.com/virajwathsalag)
- [Sachitha Samadhi Bandara](https://github.com/sachithasamadhib)
- [Ravin Jayasanka](https://github.com/MrRaveen)
- [Sanuja Rasanajna](https://github.com/SanujaRasanajna2007)

---

## 📜 License  

This project is licensed under the MIT License – feel free to use, modify, and distribute.