class Camera:
    def __init__(self, win_width, win_height):
        # 월드 좌표계에서 카메라의 중심 위치
        self.world_x = 0
        self.world_y = 0

        self.screen_width = win_width
        self.screen_height = win_height

        # 뷰 좌표계에서 카메라의 중심 위치(= 윈도우의 중심 위치)
        self.view_x = win_width // 2
        self.view_y = win_height // 2

        self.zoom = win_width / 1920 * 2
        self.lock = False
        self.lock_target = None

    def cam_lock(self, target):
        self.lock = True
        self.lock_target = target

    def cam_unlock(self):
        self.lock = False
        self.lock_target = None

    def update(self):
        if self.lock and self.lock_target is not None:
            self.world_x = self.lock_target.x
            self.world_y = self.lock_target.y

    def world_to_view(self, world_x, world_y):
        view_x = (world_x - self.world_x) * self.zoom + self.view_x
        view_y = (world_y - self.world_y) * self.zoom + self.view_y
        return view_x, view_y

    def coord_x_to_view(self, value):
        return (value - self.world_x) * self.zoom + self.view_x

    def coord_y_to_view(self, value):
        return (value - self.world_y) * self.zoom + self.view_y

    def get_draw_size(self, width, height):
        return round(width * self.zoom) + 1, round(height * self.zoom) + 1

    def handle_event(self, event):
        pass