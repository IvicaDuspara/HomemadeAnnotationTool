class GraphHolder:
    def __init__(self, graph):
        self.graph = graph
        self.image_id = None
        self.drawn_points = []
        self.selected_index = None

        self.colors = ['white', 'white', 'white',
                       'white', 'white', 'red',
                       'blue', 'red', 'blue',
                       'red', 'blue', 'yellow',
                       'green', 'yellow', 'green',
                       'yellow', 'green']

    def draw_image(self, image, frame):
        if self.image_id is not None:
            self.graph.DeleteFigure(self.image_id)
            for i in range(0, len(self.drawn_points)):
                self.graph.DeleteFigure(self.drawn_points[i])
        self.image_id = self.graph.DrawImage(data=image, location=(0, 0))
        for i in range(0, frame.size()):
            point_ = frame.get_point(i)
            self.drawn_points.append(self.graph.DrawCircle((point_.sc1, point_.sc2), radius=4,
                                                           fill_color=self.colors[i]))

    def set_image_id(self, image_id):
        self.image_id = image_id

    def select_point(self, item, frame):
        sc1 = item.sc1
        sc2 = item.sc2
        if self.selected_index is None:
            self.selected_index = item.id_
            if item.id_ not in (0, len(self.drawn_points)):
                print("OOF")
            self.graph.DeleteFigure(self.drawn_points[self.selected_index])
            self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                           fill_color=self.colors[self.selected_index],
                                                                           line_color="lime", line_width=2)
        else:
            # First three lines remove highlight from currently selected point.
            self.graph.DeleteFigure(self.drawn_points[self.selected_index])
            point_ = frame.get_point(self.selected_index)
            self.drawn_points[self.selected_index] = self.graph.DrawCircle((point_.sc1, point_.sc2), radius=4,
                                                                           fill_color=self.colors[self.selected_index])
            self.selected_index = item.id_
            self.graph.DeleteFigure(self.drawn_points[self.selected_index])
            self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                           fill_color=self.colors[self.selected_index],
                                                                           line_color="lime", line_width=2)

    def clear_selection(self, frame):
        if self.selected_index is None:
            return
        sc1 = frame.get_point(self.selected_index).sc1
        sc2 = frame.get_point(self.selected_index).sc2
        self.graph.DeleteFigure(self.drawn_points[self.selected_index])
        self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                       fill_color=self.colors[self.selected_index])
        self.selected_index = None

