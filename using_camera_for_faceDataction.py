import cv2
from ultralytics import YOLO

# Load the trained model
model = YOLO('best.pt')

# Start the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the YOLO model to the frame
    results = model.predict(source=frame, conf=0.5, save=False)

    # Draw only the boxes (without labels)
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0]  # Box coordinates
        frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Draw the box

    # Display the output on the screen
    cv2.imshow("YOLO Face Detection", frame)

    # Wait for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()