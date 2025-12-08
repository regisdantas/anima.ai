import io
import qrcode
import random


def generate_qr_code(pix_code):
    qr = qrcode.QRCode()
    qr.add_data(pix_code)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return img_buffer


def get_random(items: list) -> any:
    return random.choice(items) if items else None
