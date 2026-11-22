import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def prepare(raw):
    if len(raw)>8*1024*1024: raise ValueError('Image exceeds 8 MB')
    try:
        im=Image.open(BytesIO(raw)); im.verify()
        im=Image.open(BytesIO(raw)).convert('RGB')
        if im.width<32 or im.height<32 or im.width*im.height>24_000_000: raise ValueError('Image dimensions unsupported')
        arr=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
        gray=cv2.cvtColor(arr,cv2.COLOR_BGR2GRAY)
        if float(cv2.Laplacian(gray,cv2.CV_64F).var())<8: raise ValueError('Image is too blurry; upload a clearer photo')
        return cv2.cvtColor(cv2.resize(arr,(224,224)),cv2.COLOR_BGR2RGB).astype('float32')
    except ValueError: raise
    except Exception: raise ValueError('Invalid or corrupted image')
