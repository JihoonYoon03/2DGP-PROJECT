class Camera:
    def __init__(self, x_width, y_height):
        self.world_x = 0
        self.world_y = 0
        self.view_x = x_width // 2
        self.view_y = y_height // 2
        self.zoom = x_width / 1920
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

    def handle_event(self, event):
        pass