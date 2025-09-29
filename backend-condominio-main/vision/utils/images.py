import base64, io, os
from PIL import Image
from django.conf import settings
from datetime import datetime

def decode_data_url(data_url: str) -> Image.Image:
    # admite "data:image/jpeg;base64,..." o directamente base64
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    img = Image.open(io.BytesIO(base64.b64decode(data_url))).convert("RGB")
    return img

def save_pil_image(img: Image.Image, subdir: str, prefix: str = "img") -> str:
    dt = datetime.now()
    rel_dir = os.path.join("vision", subdir, dt.strftime("%Y"), dt.strftime("%m"))
    abs_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
    os.makedirs(abs_dir, exist_ok=True)
    filename = f"{prefix}_{dt.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    abs_path = os.path.join(abs_dir, filename)
    img.save(abs_path, format="JPEG", quality=92)
    # devolver ruta relativa para servir por MEDIA_URL
    return os.path.join(rel_dir, filename).replace("\\", "/")
