
class Camera:
    def __init__(self, w, h):
        self.dx = 0
        self.dy = 0
        self.w = w
        self.h = h

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.h // 2)