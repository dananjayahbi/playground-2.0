import cv2
from src.camera import get_camera
from src.aruco_detector import detect_markers
from src.render import draw_cube

# Initialize Camera
cap = get_camera()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect ArUco marker
    corners, ids = detect_markers(frame)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Call OpenGL function to render 3D object
        draw_cube()  # You can replace this with a custom 3D model rendering

    cv2.imshow("AR Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
