class GraphHolder:
    def __init__(self, graph, colors, connected_points):
        self.graph = graph
        self.image_id = None
        self.drawn_points = []
        self.drawn_lines = []
        self.lines_dictionary = {}
        self.selected_index = None
        self.selected_text = None
        self.colors = colors
        self.connected_points = connected_points

    def draw_image(self, image, frame):
        if self.image_id is not None:
            self.graph.DeleteFigure(self.image_id)
            for i in range(0, len(self.drawn_points)):
                self.graph.DeleteFigure(self.drawn_points[i])
            for i in range(0, len(self.drawn_lines)):
                self.graph.DeleteFigure(self.drawn_lines[i])
        self.image_id = self.graph.DrawImage(data=image, location=(0, 0))
        self.drawn_points = []
        self.drawn_lines = []
        self.lines_dictionary = {}

        for i in range(0, frame.size()):
            point_ = frame.get_point(i)
            self.drawn_points.append(self.graph.DrawCircle((point_.sc1, point_.sc2), radius=4,
                                                           fill_color=self.colors[i]))
        counter = 0
        for item in self.connected_points:
            splits = item.split(",")
            start_point = frame.get_point(int(splits[0]))
            end_point = frame.get_point(int(splits[1]))
            self.drawn_lines.append(self.graph.DrawLine(point_from=(start_point.sc1, start_point.sc2),
                                                        point_to=(end_point.sc1, end_point.sc2),
                                                        color=splits[2]))
            if int(splits[0]) not in self.lines_dictionary:
                connected = [(int(splits[1]), counter)]
                self.lines_dictionary[int(splits[0])] = connected
            else:
                self.lines_dictionary[int(splits[0])].append((int(splits[1]), counter))
            counter += 1

    def print_it(self):
        print(self.lines_dictionary)

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
            self.selected_text = self.graph.DrawText(item.get_my_label(), location=(sc1 - 10, sc2 - 10))

        else:
            # First three lines remove highlight from currently selected point.
            self.graph.DeleteFigure(self.drawn_points[self.selected_index])
            self.graph.DeleteFigure(self.selected_text)
            point_ = frame.get_point(self.selected_index)
            self.drawn_points[self.selected_index] = self.graph.DrawCircle((point_.sc1, point_.sc2), radius=4,
                                                                           fill_color=self.colors[self.selected_index])
            self.selected_index = item.id_
            self.graph.DeleteFigure(self.drawn_points[self.selected_index])
            self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                           fill_color=self.colors[self.selected_index],
                                                                           line_color="lime", line_width=2)

            self.selected_text = self.graph.DrawText(item.get_my_label(), location=(sc1 - 10, sc2 - 10))

    def clear_selection(self, frame):
        if self.selected_index is None:
            return
        sc1 = frame.get_point(self.selected_index).sc1
        sc2 = frame.get_point(self.selected_index).sc2
        self.graph.DeleteFigure(self.drawn_points[self.selected_index])
        self.graph.DeleteFigure(self.selected_text)
        self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                       fill_color=self.colors[self.selected_index])
        self.selected_index = None
        self.selected_text = None

    def move_point(self, frame, new_sc1, new_sc2):
        # delete old point
        pass
        # delete lines