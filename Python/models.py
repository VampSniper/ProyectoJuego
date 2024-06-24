import numpy as np
import moderngl as mgl
from pyrr import Matrix44
from PIL import Image

class Cube:
    def __init__(self, app, position):
        self.app = app
        self.ctx = app.ctx
        self.position = position
        self.model = Matrix44.from_translation(position)
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()

        # Cargar la textura
        self.texture = self.load_texture('Python/pictures/cesped.png')  # Reemplaza con la ruta de tu textura

    def render(self):
        self.shader_program['model'].write(self.model.astype('f4'))

        # Activa la textura en la unidad 0
        self.texture.use(location=0)
        # Asigna la textura al shader
        self.shader_program['tex'].value = 0  # Asigna el índice de la unidad de textura al shader

        self.vao.render(mgl.TRIANGLES)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        self.texture.release()  # Libera la textura al destruir el cubo

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vertex_data(self):
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
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'Python/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'Python/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def load_texture(self, path):
        # Cargar la textura con Pillow y convertirla en formato adecuado para moderngl
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        image_data = np.array(image.convert('RGBA'))

        texture = self.ctx.texture(image.size, 4, image_data.tobytes())
        texture.build_mipmaps()
        texture.use()

        return texture
