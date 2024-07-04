import numpy as np
import moderngl as mgl # Import moderngl for OpenGL context handling
from pyrr import Matrix44 # Import Matrix44 from pyrr for matrix operations
from PIL import Image # Import Image from PIL for image loading


class Cube:
    def __init__(self, app, position):
        self.app = app # Store the application reference
        self.ctx = app.ctx # Store the moderngl context from the application
        self.position = position # Store the position of the cube
        self.model = Matrix44.from_translation(position) # Create a translation matrix for the cube's position
        self.vbo = self.get_vbo()  # Initialize vertex buffer object (VBO) for vertex data
        self.shader_program = self.get_shader_program('default') # Load shader program for rendering
        self.vao = self.get_vao() # Initialize vertex array object (VAO) for vertex data and shader program

        # Load texture for the cube
        self.texture = self.load_texture('Python/pictures/cesped.png')  

    def render(self):
        self.shader_program['model'].write(self.model.astype('f4')) # Update model matrix uniform in shader

         # Activate texture unit 0 and bind the loaded texture
        self.texture.use(location=0)
        # Assign texture unit index 0 to the 'tex' uniform in the shader
        self.shader_program['tex'].value = 0  
# Render the cube using the configured VAO and shader program
        self.vao.render(mgl.TRIANGLES)

    def destroy(self):
         # Release resources: VBO, shader program, VAO, and texture
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.texture.release()  # Libera la textura al destruir el cubo

    def get_vao(self):
         # Create a vertex array object (VAO) with the configured shader program and VBO
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vertex_data(self):
         # Define vertex data for each face of the cube
        vertex_data = [
            # Front face
            -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  0.5,
            -0.5, -0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  0.5,  0.5,
            # Back face
            -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5, -0.5, -0.5,
            # Left face
            -0.5, -0.5, -0.5, -0.5, -0.5,  0.5, -0.5,  0.5,  0.5,
            -0.5, -0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5, -0.5,
            # Right face
             0.5, -0.5, -0.5,  0.5,  0.5,  0.5,  0.5, -0.5,  0.5,
             0.5, -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,  0.5,  0.5,
            # Top face
            -0.5,  0.5, -0.5, -0.5,  0.5,  0.5,  0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,  0.5,  0.5,  0.5,  0.5,  0.5, -0.5,
            # Bottom face
            -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,  0.5, -0.5,  0.5,
            -0.5, -0.5, -0.5,  0.5, -0.5,  0.5, -0.5, -0.5,  0.5,
        ]
        vertex_data = np.array(vertex_data, dtype='f4')  # Convert vertex data to numpy array
        return vertex_data

    def get_vbo(self):
        # Create a vertex buffer object (VBO) with the vertex data
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        # Load vertex and fragment shader source code from files and create a shader program
        with open(f'Python/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'Python/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def load_texture(self, path):
     # Load texture using Pillow, convert it to RGBA format, and create a moderngl texture object
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        image_data = np.array(image.convert('RGBA'))

        texture = self.ctx.texture(image.size, 4, image_data.tobytes())
        texture.build_mipmaps() # Generate mipmaps for the texture
        texture.use() # Bind the texture for use

        return texture
