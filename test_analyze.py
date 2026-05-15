import requests
from PIL import Image
import io
import os

# Create a small test image
img_path = os.path.join(os.path.dirname(__file__), 'test_img.jpg')
Image.new('RGB', (64, 64), (200, 100, 50)).save(img_path, 'JPEG')

files = {'image': open(img_path, 'rb')}

data = {
    'lang': 'te',
    'soil_moisture': '50',
    'temperature': '25',
    'ph_level': '6.5',
    'npk_n': '40',
    'npk_p': '20',
    'npk_k': '30',
    'ec': '1.0',
    'co2': '400',
    'region': 'telangana',
    'weather': 'normal'
}

try:
    resp = requests.post('http://127.0.0.1:5000/analyze', files=files, data=data, timeout=30)
    print('Status:', resp.status_code)
    print('Response JSON/text:')
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
except Exception as e:
    print('Request failed:', str(e))
finally:
    try:
        files['image'].close()
    except Exception:
        pass
