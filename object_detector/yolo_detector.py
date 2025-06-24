from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

while True:
    res,frame = cap.read()
    if not res:
        break

    results = model(frame)
    annotated = results[0].plot()

    cv2.imshow("SpideySense View", annotated)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()