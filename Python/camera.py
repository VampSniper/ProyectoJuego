import pygame as pg
from pyrr import Matrix44, Vector3, Quaternion

class Camera:
    def __init__(self, position, target, up, win_size):
        self.position = Vector3(position)
        self.target = Vector3(target)
        self.up = Vector3(up)
        self.forward = (self.target - self.position).normalized
        self.right = self.forward.cross(self.up).normalized
        self.win_size = win_size

        self.view = Matrix44.look_at(
            eye=self.position,
            target=self.target,
            up=self.up
        )
        self.projection = Matrix44.perspective_projection(
            45.0, self.win_size[0] / self.win_size[1], 0.1, 100.0
        )

        self.move_speed = 0.01
        self.turn_speed = 0.01

        self.mouse_sensitivity = 0.01
        self.last_x, self.last_y = pg.mouse.get_pos()
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def update(self, dt, keys):
        if keys[pg.K_w]:
            self.position += self.forward * self.move_speed
        if keys[pg.K_s]:
            self.position -= self.forward * self.move_speed
        if keys[pg.K_a]:
            self.position -= self.right * self.move_speed
        if keys[pg.K_d]:
            self.position += self.right * self.move_speed
        if keys[pg.K_SPACE]:
            self.position += self.up * self.move_speed
        if keys[pg.K_LSHIFT]:
            self.position += self.down * self.move_speed

        x, y = pg.mouse.get_pos()
        dx = (x - self.last_x) * self.mouse_sensitivity
        dy = (y - self.last_y) * self.mouse_sensitivity
        self.last_x, self.last_y = x, y

        self.yaw(dx)
        self.pitch(dy)

        self.update_view_matrix()

    def yaw(self, angle):
        rotation = Quaternion.from_y_rotation(angle)
        self.forward = Vector3(rotation * self.forward)
        self.right = self.forward.cross(self.up).normalized

    def pitch(self, angle):
        rotation = Quaternion.from_axis_rotation(self.right, angle)
        self.forward = Vector3(rotation * self.forward)
        self.up = self.right.cross(self.forward).normalized

    def update_view_matrix(self):
        self.target = self.position + self.forward
        self.view = Matrix44.look_at(
            eye=self.position,
            target=self.target,
            up=self.up
        )
