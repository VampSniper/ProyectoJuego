import moderngl as mgl
from pyrr import Vector3
import re

class ObjLoader:
    def __init__(self, game, filename):
        self.game = game
        self.vertices = [] # List to store vertices of the object
        self.normals = [] # List to store normals of the object
        self.indices = []  # List to store vertex indices for faces
        self.vertices_buffer = None # Buffer object for vertices
        self.normals_buffer = None # Buffer object for normals
        self.load_obj(filename)  # Load the OBJ file on initialization

    def load_obj(self, filename):
        """Loads vertices, normals, and indices from an OBJ file."""

        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('v '):  # Vertex line
                vertex = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line))) # Extract vertex coordinates
                self.vertices.append(vertex)
            elif line.startswith('vn '):# Normal line
                normal = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))  # Extract normal coordinates
                self.normals.append(normal)
            elif line.startswith('f '): # Face line
                face = re.findall(r'\d+', line)  # Extract vertex indices for a face
                self.indices.extend(map(int, face))
# Create buffers for vertices and normals

        self.vertices_buffer = self.game.ctx.buffer(data=bytes(self.vertices))
        self.normals_buffer = self.game.ctx.buffer(data=bytes(self.normals))

    def render(self):
        """Render the object using ModernGL."""
          # Create vertex array object (VAO) with shader program and buffer data
        vao = self.game.ctx.vertex_array(self.game.ctx.program(
            vertex_shader="""
            #version 330

            uniform mat4 projection;
            uniform mat4 view;
            in vec3 in_position;
            in vec3 in_normal;
            out vec3 frag_normal;

            void main() {
                gl_Position = projection * view * vec4(in_position, 1.0);
                frag_normal = in_normal;
            }
            """,
            fragment_shader="""
            #version 330

            in vec3 frag_normal;
            out vec4 frag_color;

            void main() {
                frag_color = vec4(1.0, 1.0, 1.0, 1.0);  // Color blanco, ajusta según necesites
            }
            """
        ), [
            (self.vertices_buffer, '3f', 'in_position'),
            (self.normals_buffer, '3f', 'in_normal')
        ])

        vao.render()

    def destroy(self):
        """Release resources used by the object."""
        self.vertices_buffer.release()
        self.normals_buffer.release()

class Cloud:
    def __init__(self, game, obj_file, position):
        self.game = game
        self.position = Vector3(position) # Position vector of the cloud
        self.obj_loader = ObjLoader(obj_file)  # OBJ loader instance for the cloud
        self.shader_program = self.game.ctx.program(
            vertex_shader="""
            #version 330

            uniform mat4 projection;
            uniform mat4 view;
            in vec3 in_position;
            in vec3 in_normal;
            out vec3 frag_normal;

            void main() {
                gl_Position = projection * view * vec4(in_position, 1.0);
                frag_normal = in_normal;
            }
            """,
            fragment_shader="""
            #version 330

            in vec3 frag_normal;
            out vec4 frag_color;

            void main() {
                frag_color = vec4(1.0, 1.0, 1.0, 1.0);  // Color blanco, ajusta según necesites
            }
            """
        )

    def render(self):
        """Render the cloud using the shader program and OBJ loader."""
        self.shader_program['projection'].write(self.game.camera.projection.astype('f4'))
        self.shader_program['view'].write(self.game.camera.view.astype('f4'))
        self.obj_loader.render() # Render the OBJ loaded by the cloud instance

    def destroy(self):
        """Release resources used by the cloud."""
        self.obj_loader.vao.release()  # Release VAO used by the OBJ loader
        self.shader_program.release() # Release shader program resources
