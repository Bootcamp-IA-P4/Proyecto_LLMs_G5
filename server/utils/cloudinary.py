import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image_bytes(image_bytes, public_id=None):
    result = cloudinary.uploader.upload(
        image_bytes,
        resource_type="image",
        public_id=public_id,
        overwrite=True
    )
    return result.get("secure_url")