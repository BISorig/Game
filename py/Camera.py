
class Camera:
    def __init__(self, w):
        self.dx = 0
        self.dy = 0
        self.w = w
        self.h = 2000

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.w // 2)