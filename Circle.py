class Circle:

    def __init__(self, id_, x, y, radius, label):
        self.id_ = id_
        self.x = x
        self.y = y
        self.scx = x
        self.scy = y
        self.radius = radius
        self.label = label

    def __str__(self):
        return str(self.label) + " " + "(" + str(self.id_) + "," + str(self.x) + "," + str(self.y) + "," \
                                                                                    + str(self.radius) + ")"

    def __repr__(self):
        return str(self)

    def set_scaled_coordinates(self, x, y):
        self.scx = x
        self.scy = y

    def get_my_label(self):
        return self.label
