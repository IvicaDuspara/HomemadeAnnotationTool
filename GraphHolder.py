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
            self.__delete_selected_point()
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
        self.__delete_selected_point()
        self.drawn_points[self.selected_index] = self.graph.DrawCircle((sc1, sc2), radius=4,
                                                                       fill_color=self.colors[self.selected_index])
        self.selected_index = None
        self.selected_text = None

    def move_point(self, frame, new_sc1, new_sc2):
        # delete old point
        if self.selected_index is None:
            return
        # Delete selected point
        self.__delete_selected_point()
        # Delete old lines which start with this point:
        if self.selected_index in self.lines_dictionary:
            for item in self.lines_dictionary[self.selected_index]:
                index_in_drawn_lines = item[1]
                self.graph.DeleteFigure(self.drawn_lines[index_in_drawn_lines])
        # Delete old lines which end with this point:
        for key, value in self.lines_dictionary.items():
            for pair in value:
                if pair[0] == self.selected_index:
                    self.graph.DeleteFigure(self.drawn_lines[pair[1]])

        # Move selected point
        frame.get_point(self.selected_index).set_scaled_coordinates(new_sc1, new_sc2)
        # Draw selected point again
        self.drawn_points[self.selected_index] = self.graph.DrawCircle((new_sc1, new_sc2), radius=4,
                                                                       fill_color=self.colors[self.selected_index],
                                                                       line_color="lime", line_width=2)
        self.selected_text = self.graph.DrawText(frame.get_point(self.selected_index).get_my_label(),
                                                 location=(new_sc1 - 10, new_sc2 - 10))
        # Draw lines which start with moved point again
        if self.selected_index in self.lines_dictionary:
            for item in self.lines_dictionary[self.selected_index]:
                start_point = frame.get_point(self.selected_index)
                end_point = frame.get_point(item[0])
                index_in_drawn_lines = item[1]
                color = self.connected_points[index_in_drawn_lines].split(",")[2]
                self.drawn_lines[index_in_drawn_lines] = self.graph.DrawLine(point_from=(start_point.sc1,
                                                                                         start_point.sc2),
                                                                             point_to=(end_point.sc1, end_point.sc2),
                                                                             color=color)
        for key, value in self.lines_dictionary.items():
            for pair in value:
                if pair[0] == self.selected_index:
                    start_point = frame.get_point(key)
                    end_point = frame.get_point(self.selected_index)
                    index_in_drawn_lines = pair[1]
                    color = self.connected_points[index_in_drawn_lines].split(",")[2]
                    self.drawn_lines[index_in_drawn_lines] = self.graph.DrawLine(point_from=(start_point.sc1,
                                                                                             start_point.sc2),
                                                                                 point_to=(end_point.sc1,
                                                                                           end_point.sc2),
                                                                                 color=color)

    # Private methods
    def __delete_selected_point(self):
        self.graph.DeleteFigure(self.drawn_points[self.selected_index])
        self.graph.DeleteFigure(self.selected_text)