import cv2
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *  # Import OpenGL constants
from OpenGL.GLU import gluPerspective, gluLookAt

# Initialize Pygame (for OpenGL rendering inside OpenCV)
pygame.init()

# Load ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Initialize camera
cap = cv2.VideoCapture(0)
w, h = int(cap.get(3)), int(cap.get(4))

# Create Pygame OpenGL window (same size as OpenCV frame)
pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Augmented Reality")

def draw_cube():
    """Draw a simple 3D cube."""
    glBegin(GL_QUADS)

    glColor3f(1, 0, 0)  # Red
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    glColor3f(0, 1, 0)  # Green
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    glEnd()

# OpenGL Projection Settings
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, w / h, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

while True:
    # Read camera frame
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Convert OpenCV frame to Pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)  # Rotate to match OpenGL coordinate system
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.flip(frame, True, False)

        # Draw the camera frame as a background in OpenGL
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        screen_texture = pygame.image.tostring(frame, "RGB", 1)
        glDrawPixels(w, h, GL_RGB, GL_UNSIGNED_BYTE, screen_texture)

        # Set OpenGL camera position
        glPushMatrix()
        glTranslatef(0, 0, -5)  # Move cube in front of the camera
        draw_cube()
        glPopMatrix()

        # Update OpenGL display
        pygame.display.flip()

    # Handle quit event
    for event in pygame.event.get():
        if event.type == QUIT:
            cap.release()
            pygame.quit()
            exit()

    # Remove the extra OpenCV window
    # cv2.imshow("AR Camera", frame)  <- Comment this line out

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
pygame.quit()
