import moderngl as mgl
from pyrr import Vector3
import re

class ObjLoader:
    def __init__(self, game, filename):
        self.game = game
        self.vertices = []
        self.normals = []
        self.indices = []
        self.vertices_buffer = None
        self.normals_buffer = None
        self.load_obj(filename)

    def load_obj(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('v '):
                vertex = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                self.vertices.append(vertex)
            elif line.startswith('vn '):
                normal = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", line)))
                self.normals.append(normal)
            elif line.startswith('f '):
                face = re.findall(r'\d+', line)
                self.indices.extend(map(int, face))

        self.vertices_buffer = self.game.ctx.buffer(data=bytes(self.vertices))
        self.normals_buffer = self.game.ctx.buffer(data=bytes(self.normals))

    def render(self):
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
        self.vertices_buffer.release()
        self.normals_buffer.release()

class Cloud:
    def __init__(self, game, obj_file, position):
        self.game = game
        self.position = Vector3(position)
        self.obj_loader = ObjLoader(obj_file)
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
        self.shader_program['projection'].write(self.game.camera.projection.astype('f4'))
        self.shader_program['view'].write(self.game.camera.view.astype('f4'))
        self.obj_loader.render()

    def destroy(self):
        self.obj_loader.vao.release()
        self.shader_program.release()
