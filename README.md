
# Image Green Background Tool

Features

- AI background removal
- Remove image borders
- Replace background with bright green
- Resize to 96x74
- Batch image processing
- Download ZIP

## Run with Docker

docker-compose up

Open:

http://localhost:5173

## 目錄結構

```text
image-green-bg-tool/
├─ backend/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ main.py
│  ├─ processor/
│  │  └─ image_processor.py
│  ├─ uploads/   (執行時產生)
│  └─ outputs/   (執行時產生)
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ vite.config.js
│  ├─ public/
│  └─ src/
│     ├─ main.jsx
│     └─ App.jsx
├─ docker-compose.yml
├─ .gitignore
└─ README.md
```
