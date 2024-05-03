import qrcode
from io import BytesIO
from PIL import Image
import base64

def qr_generator(date_request):
    
    input = date_request
    qr = qrcode.QRCode(version=1, box_size=15, border=2)
    qr.add_data(input)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    
    return img_base64


