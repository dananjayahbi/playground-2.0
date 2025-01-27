import cv2

def get_camera(index=0):
    """Initializes and returns a video capture object."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise Exception("Could not open webcam!")
    return cap
