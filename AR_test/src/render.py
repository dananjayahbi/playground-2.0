import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

def draw_cube():
    """Draws a simple OpenGL cube."""
    gl.glBegin(gl.GL_QUADS)
    
    gl.glColor3f(1, 0, 0)  # Red
    gl.glVertex3f(-1, -1, -1)
    gl.glVertex3f(1, -1, -1)
    gl.glVertex3f(1, 1, -1)
    gl.glVertex3f(-1, 1, -1)

    gl.glColor3f(0, 1, 0)  # Green
    gl.glVertex3f(-1, -1, 1)
    gl.glVertex3f(1, -1, 1)
    gl.glVertex3f(1, 1, 1)
    gl.glVertex3f(-1, 1, 1)

    gl.glEnd()
