import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

from logs.logger import logger

app = FastAPI()
UPLOAD_FOLDER = "saved_photos/photos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class WhatsAppPhoto(BaseModel):
    """Model for WhatsApp photo message with URL and sender info."""

    image_url: str
    from_: str  # use 'from_' because 'from' is a reserved word


@app.post("/webhook")
async def webhook(photo: WhatsAppPhoto):
    """Save incoming WhatsApp photo and respond with confirmation."""
    try:
        safe_timestamp = (
            datetime.now().isoformat().replace(":", "-").replace(".", "-")
        )
        filename = f"{safe_timestamp}_{photo.from_}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(b"FAKE_IMAGE_DATA")  # simulate image saving
        # TODO: change it to real data saving logic

        logger.info(f"Saved photo from {photo.from_} as {filename}")

        return {"message": "Фото збережено, дякуємо!"}
    except Exception as e:
        logger.error(f"Failed to save photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to save photo")


def run_whatsapp_bot():
    """Start the WhatsApp webhook FastAPI server with uvicorn."""
    logger.info("Starting WhatsApp webhook server on http://0.0.0.0:8000")
    uvicorn.run(
        "bot_whatsapp.whatsapp_handler:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
