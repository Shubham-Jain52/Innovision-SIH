# import cv2
# import os
# from ultralytics import YOLO
# from collections import defaultdict

# HOME = os.getcwd()
# VIDEO = f"{HOME}/kiit2.mp4"

# model = YOLO('yolo11n.pt')
# class_list = model.names

# cap = cv2.VideoCapture(VIDEO)
# line_y = 310


# class_counts = defaultdict(int)
# crossed_ids = set()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model.track(frame, persist=True , classes = [1,2,3,5,6,7])

#     if results[0].boxes.data is not None:
#         boxes = results[0].boxes.xyxy.cpu()

#         if results[0].boxes.id is not None:
#             track_ids = results[0].boxes.id.int().cpu().tolist()
#         else:
#             track_ids = [0] * len(boxes)

#         class_indices = results[0].boxes.cls.int().cpu().tolist()
#         confidence = results[0].boxes.conf.cpu()

#         for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidence):
#             x1, y1, x2, y2 = map(int, box)
#             cx = (x1 + x2) // 2
#             cy = (y1 + y2) // 2

#             class_name = class_list[class_idx]

#             cv2.line(frame, (280    , line_y), (700, line_y), (255, 255, 0), 3)
#             cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)


#             if cy > line_y and track_id not in crossed_ids:
#                 crossed_ids.add(track_id)
#                 class_counts[class_name] += 1

    
#     y_offset = 30
#     for class_name , count in class_counts.items():
#         cv2.putText(frame, f"{class_name}:{count}" , (50,y_offset),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8 , (0,255,0) , 2)
#         y_offset += 30

#     cv2.imshow('YOLO Tracking', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # print(class_name , count)

# cap.release()
# cv2.destroyAllWindows()

# output_file = "data.txt"
# with open(output_file, "w") as f:
#     for class_name, count in class_counts.items():
#         f.write(f"{class_name} - {count}\n")


import cv2
import os
import csv
from ultralytics import YOLO
from collections import defaultdict

HOME = os.getcwd()
VIDEO = f"{HOME}/kiit2.mp4" 

model = YOLO('yolov8n.pt')
class_list = model.names
cap = cv2.VideoCapture(VIDEO)

line_y = 310
class_counts = defaultdict(int)
crossed_ids = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, classes=[1, 2, 3, 5, 7])

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        class_indices = results[0].boxes.cls.int().cpu().tolist()

        for box, track_id, class_idx in zip(boxes, track_ids, class_indices):
            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            class_name = class_list[class_idx]

            cv2.line(frame, (280, line_y), (700, line_y), (255, 255, 0), 3)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            label = f"ID:{track_id} {class_name}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            if cy > line_y and track_id not in crossed_ids:
                crossed_ids.add(track_id)
                class_counts[class_name] += 1

    y_offset = 30
    for class_name, count in class_counts.items():
        count_text = f"{class_name}: {count}"
        cv2.putText(frame, count_text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        y_offset += 30

    cv2.imshow('YOLO Object Counting', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

output_file = "data.csv"
with open(output_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["class_name", "count"])
    for class_name, count in class_counts.items():
        csv_writer.writerow([class_name, count])

