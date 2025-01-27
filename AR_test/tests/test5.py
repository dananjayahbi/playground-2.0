import cv2
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

# ✅ Initialize Pygame
pygame.init()

# ✅ Initialize Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ ERROR: Could not access the camera!")
    exit()

w, h = int(cap.get(3)), int(cap.get(4))

# ✅ Create OpenGL Window
pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL)
pygame.display.set_caption("AR Debugging - OpenGL & OpenCV")

# ✅ Camera Calibration
camera_matrix = np.array([[800, 0, w//2], [0, 800, h//2], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

# ✅ OpenGL Setup
glEnable(GL_DEPTH_TEST)  # Enable Depth Testing
glDepthFunc(GL_LEQUAL)  # 🔥 Fix depth issues
glEnable(GL_LIGHTING)  # 🔥 Enable lighting
glEnable(GL_LIGHT0)  # 🔥 Add a default light
glEnable(GL_COLOR_MATERIAL)  # 🔥 Allow objects to have colors
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, w / h, 0.1, 100.0)  # Ensure proper depth range
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# ✅ Function to Draw a Simple OpenGL Cube
def draw_debug_cube():
    """Draws a simple red OpenGL cube."""
    vertices = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # Front face
    ]

    faces = [
        (0, 1, 2, 3),  # Back face
        (4, 5, 6, 7),  # Front face
        (0, 1, 5, 4),  # Bottom face
        (2, 3, 7, 6),  # Top face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5)   # Right face
    ]

    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)  # 🔥 Ensure the cube is red and visible
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

# ✅ Load ArUco Dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

print("✅ Starting AR system...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ ERROR: Could not capture a frame from the camera!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # ✅ Estimate 3D Pose of ArUco Marker
        obj_points = np.array([[-1, 1, 0], [1, 1, 0], [1, -1, 0], [-1, -1, 0]], dtype=np.float32)
        _, rvec, tvec = cv2.solvePnP(obj_points, corners[0], camera_matrix, dist_coeffs)

        # ✅ Debugging: Log Cube Position
        print(f"🔹 Raw Cube Position: {tvec[:, 0]}")

        # ✅ Normalize Depth Values
        SCALE_FACTOR = 5.0  # 🔥 Adjust this value for perfect AR alignment
        tvec[:, 0] /= SCALE_FACTOR

        # ✅ Flip Z-Axis to Convert OpenCV to OpenGL
        tvec[:, 0][2] *= -1  # 🔥 Critical fix

        # ✅ Convert Pose to OpenGL Format
        rot_matrix, _ = cv2.Rodrigues(rvec)
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = rot_matrix
        transformation_matrix[:3, 3] = tvec[:, 0]
        transformation_matrix = transformation_matrix.T  # Transpose for OpenGL

        print(f"✅ Scaled Cube Position: {tvec[:, 0]}")  # 🔥 Debugging print

        # ✅ Convert OpenCV Frame to Pygame Surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.flip(frame, True, False)

        # ✅ Render Camera Background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        screen_texture = pygame.image.tostring(frame, "RGB", 1)
        glDrawPixels(w, h, GL_RGB, GL_UNSIGNED_BYTE, screen_texture)

        # ✅ Apply Marker Transformation
        glPushMatrix()
        glMultMatrixf(transformation_matrix.flatten())  # Align model with marker
        glScalef(10.0, 10.0, 10.0)  # 🔥 Scale up the cube to ensure visibility
        draw_debug_cube()
        glPopMatrix()

        # ✅ Update OpenGL display
        pygame.display.flip()

    # ✅ Handle Quit Event
    for event in pygame.event.get():
        if event.type == QUIT:
            print("✅ Closing AR system...")
            cap.release()
            pygame.quit()
            exit()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("✅ User pressed 'q'. Exiting...")
        break

# ✅ Cleanup
cap.release()
pygame.quit()
