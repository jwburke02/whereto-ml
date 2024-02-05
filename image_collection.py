from flask import Flask, request
from utils import sign_url
import requests
import config
import math
import os

app = Flask(__name__)

def generate_base_heading(dy, dx):
    base_heading = math.atan2(dy, dx) * 180 / math.pi
    if base_heading < 0:
        base_heading = 360 + base_heading
    return base_heading

@app.route("/gather_image_data")
def gather_image_data():
    '''
        This endpoint requires there to be passed a street name.

        This endpoint requires the initial and final coordinates of a street segment to be passed.
    '''

    xi = float(request.args.get('xi'))
    xf = float(request.args.get('xf'))
    yi = float(request.args.get('yi'))
    yf = float(request.args.get('yf'))
    idx_base = int(request.args.get('idx'))

    API_KEY = config.map_api_key
    BASE_URL = "https://maps.googleapis.com/maps/api/streetview"

    d = math.sqrt((xf - xi) ** 2 + (yf - yi) ** 2)
    steps = int(d * 8000)
    dx = (xf - xi) / steps
    dy = (yf - yi) / steps
    base_heading = generate_base_heading(dy, dx)
    headings = [base_heading]
    for _ in range(7):
        base_heading = (base_heading + 45) % 360
        headings.append(base_heading)

    size = "?size=640x640"
    pitch = "&pitch=0"
    fov = "&fov=80"
    api = "&key=" + API_KEY
    idx = 0

    for count in range(steps + 1):
        x = xi + count * dx
        y = yi + count * dy
        location = "&location=" + str(x) + "," + str(y)
        for heading in headings:
            query = sign_url(BASE_URL + size + location + pitch + fov + "&heading=" + str(heading) + api)
            img = requests.get(query).content
            pics_directory = "./Data Collection"
            if not os.path.exists(pics_directory):
                os.makedirs(pics_directory)
            file_path = os.path.join(pics_directory, f"image{idx + idx_base}.jpg")
            idx += 1
            with open(file_path, 'wb') as handler:
                handler.write(img)
                
    return "Images downloaded."

if __name__ == '__main__':
    app.run(debug=True)