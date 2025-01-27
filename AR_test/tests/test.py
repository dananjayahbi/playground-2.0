import cv2
import numpy as np

# Load ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Marker ID (change for different patterns)
marker_id = 12  # You can use 0, 1, 2... up to 49 in DICT_4X4_50
marker_size = 200  # Marker size in pixels

# Create an empty image for the marker
marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)

# Generate correct ArUco marker
cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size, marker_image, 1)

# Save and display
cv2.imwrite("aruco_marker_corrected.png", marker_image)
cv2.imshow("ArUco Marker", marker_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
