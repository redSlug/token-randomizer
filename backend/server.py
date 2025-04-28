from processor import process_image
from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={
    r"*": {
        "origins": ["localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["POST", "GET"],
        "allow_headers": ["Content-Type"]
    }
})
CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})


@app.route("/")
def home():
    return "Hello, World"


@app.route("/randomize", methods=["POST"])
def randomize_image():
    if "image" not in request.files:
        return "No image uploaded", 400
    image_file = request.files["image"]
    image = Image.open(image_file.stream)

    os.makedirs("/tmp/input/", exist_ok=True)
    filename = "uploaded_image.png"
    save_path = os.path.join("/tmp/input/", filename)
    image.save(save_path)
    result = process_image(save_path)

    updated_image = Image.open(result)
    img_io = io.BytesIO()
    updated_image.save(img_io, format="PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
