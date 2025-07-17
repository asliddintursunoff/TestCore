import io
from PIL import Image
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile

def qr_code_pic(link) -> InMemoryUploadedFile:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Save image to BytesIO
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)


    qr_image_file = InMemoryUploadedFile(
        file=img_io,
        field_name=None,
        name='qr_code.png',
        content_type='image/png',
        size=img_io.getbuffer().nbytes,
        charset=None
    )

    return qr_image_file
