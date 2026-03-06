import asyncio
import shutil
import os
import zipfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from processor.image_processor import process_image

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD = "uploads"
OUTPUT = "outputs"

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)


def _process_images_sync(input_output_pairs: list[tuple[str, str]]) -> str:
    """Run blocking image processing in a thread."""
    processed = []
    for input_path, output_path in input_output_pairs:
        process_image(input_path, output_path)
        processed.append(output_path)
    zip_path = f"{OUTPUT}/result.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in processed:
            zipf.write(f, os.path.basename(f))
    return zip_path


@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    try:
        # Save uploads in async context, then process in thread
        pairs = []
        for file in files:
            input_path = f"{UPLOAD}/{file.filename}"
            output_path = f"{OUTPUT}/{file.filename}"
            with open(input_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            pairs.append((input_path, output_path))
        loop = asyncio.get_event_loop()
        zip_path = await loop.run_in_executor(None, _process_images_sync, pairs)
        if not os.path.isfile(zip_path):
            raise HTTPException(status_code=500, detail="Failed to create zip")
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="result.zip",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
