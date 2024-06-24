import pygame as pg
import moderngl as mgl
import sys
from models import Cube
from camera import Camera

class Game:
    def __init__(self, win_size=(1000, 700)):
        #init pygames modules
        pg.init()
        #windows size
        self.WIN_SIZE = win_size
        #set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        #create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        #detect and use existing opengl context
        self.ctx = mgl.create_context()
        #create an object to help track time
        self.clock = pg.time.Clock()

        # Camera
        self.camera = Camera(
            position=(10.0, 10.0, 10.0),
            target=(0.0, 0.0, 0.0),
            up=(0.0, 1.0, 0.0),
            win_size=self.WIN_SIZE
        )

        # Multiplicate the cube
        self.cubes = []
        num_cubes_x = 10
        num_cubes_z = 8
        cube_spacing = 1

        for i in range(num_cubes_x):
            for j in range(num_cubes_z):
                x = i * cube_spacing
                z = j * cube_spacing
                self.cubes.append(Cube(self, position=(x, 0, z)))

        # Set projection and view matrix in each cube's shader
        for cube in self.cubes:
            cube.shader_program['projection'].write(self.camera.projection.astype('f4'))
            cube.shader_program['view'].write(self.camera.view.astype('f4'))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                for cube in self.cubes:
                    cube.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        #clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        #render each cube
        for cube in self.cubes:
            cube.shader_program['view'].write(self.camera.view.astype('f4'))
            cube.render()
        #swap buffers
        pg.display.flip()

    def run(self):
        while True:
            keys = pg.key.get_pressed()
            self.camera.update(self.clock.get_time() / 1000.0, keys)
            self.check_events()
            self.render()
            self.clock.tick(60)

if __name__ == '__main__':
    app = Game()
    app.run()
