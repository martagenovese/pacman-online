import threading

class My2DSyncArray:
    def __init__(self, rows):
        self.array = [Point() for _ in range(rows)]
        self.lock = threading.Lock()

    def set_x(self, row, value):
        with self.lock:
            self.array[row].x = value

    def set_y(self, row, value):
        with self.lock:
            self.array[row].y = value

    def get_x(self, row):
        with self.lock:
            return self.array[row].x

    def get_y(self, row):
        with self.lock:
            return self.array[row].y

    def __str__(self):
        with self.lock:
            return "\n".join([f"[{point}]" for point in self.array])

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"