import event_set
from physics_data import WIN_WIDTH

class Camera:
    def __init__(self, win_width, win_height):
        # 월드 좌표계에서 카메라의 중심 위치
        self.world_x = 0
        self.world_y = 0

        self.screen_width = win_width
        self.screen_height = win_height

        # 뷰 좌표계에서 카메라의 중심 위치
        self.view_x = win_width // 2
        self.view_y = win_height // 2

        # cam_lock시 뷰 좌표계 오프셋 값
        self.offset_x = 0
        self.offset_y = 0

        self.zoom = win_width / 1920 * 1.4
        self.lock = False
        self.lock_target = None

    def cam_lock(self, target, offset_x=0, offset_y=0):
        self.lock = True
        self.lock_target = target
        self.offset_x = offset_x
        self.offset_y = offset_y

    def cam_unlock(self):
        self.lock = False
        self.lock_target = None
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        if self.lock and self.lock_target is not None:
            self.world_x = self.lock_target.x
            self.world_y = self.lock_target.y

    def world_to_view(self, world_x, world_y):
        view_x = (world_x - self.world_x) * self.zoom + self.view_x + self.offset_x
        view_y = (world_y - self.world_y) * self.zoom + self.view_y + self.offset_y
        return view_x, view_y

    def value_to_view(self, value):
        return value * self.zoom

    def coord_x_to_view(self, value):
        return (value - self.world_x) * self.zoom + self.view_x

    def coord_y_to_view(self, value):
        return (value - self.world_y) * self.zoom + self.view_y

    def get_draw_size(self, width, height):
        return round(width * self.zoom) + 1, round(height * self.zoom) + 1

    def handle_event(self, event):
        if event_set.equals_pressed(('INPUT', event)):
            self.zoom += 0.05
        elif event_set.minus_pressed(('INPUT', event)):
            self.zoom -= 0.05
            if self.zoom < 0.2:
                self.zoom = 0.2

    def camera_enter_mine(self):
        self.zoom = 2.0
        self.offset_x = 0
        self.offset_y = 0

    def camera_exit_mine(self):
        self.zoom = self.screen_width / 1920 * 1.4
        self.offset_x = WIN_WIDTH // 3