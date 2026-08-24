
import os
import uuid
from flask import Flask, request, jsonify, render_template, url_for
from PIL import Image, ImageDraw
from ultralytics import YOLO

# ---------------------------------------------------------
# ۱) تنظیمات اولیه
# ---------------------------------------------------------
backend_of_faceDetection = Flask(__name__)


UPLOAD_FOLDER = os.path.join("static", "uploads")
RESULT_FOLDER = os.path.join("static", "results")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


MODEL_PATH = "best.pt"

model = YOLO(MODEL_PATH)


def detect_face(image_path: str, save_path: str, conf: float = 0.5):

    image = Image.open(image_path).convert("RGB")

    results = model.predict(source=image_path, conf=conf, save=False, verbose=False)
    boxes = results[0].boxes.xyxy

    draw = ImageDraw.Draw(image)
    face_count = 0
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box.tolist())
        draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=6)
        face_count += 1

    image.save(save_path)
    return face_count


# ---------------------------------------------------------
# ۳) مسیر (route) صفحه اصلی
# ---------------------------------------------------------
@backend_of_faceDetection.route("/")
def index():
    # این خط فایل templates/index.html را به مرورگر نمایش می‌دهد
    return render_template("index.html")


# ---------------------------------------------------------
# ۴) مسیر (route) دریافت عکس و پردازش آن
# ---------------------------------------------------------
@backend_of_faceDetection.route("/detect", methods=["POST"])
def detect():
    # آیا اصلاً فایلی در درخواست وجود دارد؟
    if "image" not in request.files:
        return jsonify({"error": "هیچ فایلی ارسال نشده است"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "نام فایل خالی است"}), 400

    # برای جلوگیری از تداخل نام فایل‌های مختلف کاربران، یک نام یکتا می‌سازیم
    unique_id = uuid.uuid4().hex
    upload_filename = f"{unique_id}_{file.filename}"
    upload_path = os.path.join(UPLOAD_FOLDER, upload_filename)
    file.save(upload_path)

    result_filename = f"result_{unique_id}.jpg"
    result_path = os.path.join(RESULT_FOLDER, result_filename)

    try:
        face_count = detect_face(upload_path, result_path)
    except Exception as e:
        return jsonify({"error": f"خطا در پردازش تصویر: {str(e)}"}), 500

    # آدرس قابل‌دسترس از طریق مرورگر برای عکس نتیجه
    result_url = url_for("static", filename=f"results/{result_filename}")

    return jsonify({
        "result_image_url": result_url,
        "face_count": face_count
    })

if __name__ == "__main__":
    # debug=True یعنی هر تغییری در کد بدهید سرور خودش ری‌استارت می‌شود (فقط برای توسعه، نه محیط نهایی)
    backend_of_faceDetection.run(debug=True, host="127.0.0.1", port=5000)
