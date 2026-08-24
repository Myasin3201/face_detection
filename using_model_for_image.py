import os
from PIL import Image, ImageDraw
from ultralytics import YOLO


MODEL_PATH = "best.pt"

model = YOLO(MODEL_PATH)


def main(image_path: str, conf: float = 0.5):
    image = Image.open(image_path).convert("RGB")

    results = model.predict(source=image_path, conf=conf, save=False, verbose=False)
    boxes = results[0].boxes.xyxy

    draw = ImageDraw.Draw(image)
    face_count = 0
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box.tolist())
        draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=6)
        face_count += 1

    return face_count


if __name__ == "__main__":
    main(image_path = 'mor.png')
