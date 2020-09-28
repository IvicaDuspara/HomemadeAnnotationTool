import Point
import GraphHolder
import cv2
import PySimpleGUI as psg
import ConfigParser
import copy


class GuiHolder:
    display_width = 800
    display_height = 600
    original_width = 800
    original_height = 600

    def __init__(self):
        self.__labels, self.__colors, self.__connected_points = [], [], []
        self.__cv_colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'blue': (255, 0, 0), 'green': (0, 255, 0),
                            'red': (0, 0, 255), 'yellow': (0, 255, 255), 'orange': (0, 128, 255)}

        # paths to files
        self.load_description_path = ""
        self.load_video_path = ""
        self.load_json_path = ""

        # different frames list
        self.original_frames = []
        self.resized_frames = []
        self.displayed_frames = []
        self.points_in_frames = []

        self.active_index = 0

        # other
        self.__cap = None
        self.__frame_rate = None
        self.window = None
        self.layout = []

        self.layout.append([psg.Text("Json file location:"),
                            psg.In(size=(30, 1), enable_events=True, key="-FILE_JSON-"),
                            psg.FileBrowse(),
                            psg.Text("Description file location:"),
                            psg.In(size=(30, 1), enable_events=True, key="-FILE_DESCRIPTION-"),
                            psg.FileBrowse(disabled=True),
                            psg.Text("Video file location:"),
                            psg.In(size=(30, 1), enable_events=True, key="-FILE_VIDEO-"),
                            psg.FileBrowse(disabled=True)
                            ])
        self.layout.append([psg.Button("Previous"), psg.Button("Play"), psg.Button("Next"),
                            psg.Button("Clear Selection", disabled=True, key="-CLEAR_SELECTION-"),
                            psg.Button("Save description", disabled=True, key="-SAVE_DESCRIPTION-"),
                            psg.Button("Save video", disabled=True, key="-SAVE_VIDEO-"),
                            psg.Button("Save as images", disabled=True, key="-SAVE_AS_IMAGES-"),
                            psg.Slider(default_value=0, range=(0, 0), disabled=True, enable_events=True,
                                       orientation='horizontal',
                                       size=(75, 25), key="-FRAME_SLIDER-")])
        self.layout.append([psg.HorizontalSeparator()])
        self.layout.append([psg.ProgressBar(max_value=0, orientation='horizontal', bar_color=('green', 'white'),
                                            visible=False, size=(100, 15))])
        self.layout.append([psg.Listbox(values=[], key="-LIST-", size=(50, 150),
                                        select_mode="LISTBOX_SELECT_MODE_SINGLE",
                                        enable_events=True, disabled=True),
                            psg.Graph((800, 600), (0, 600), (800, 0), enable_events=True, key="-GRAPH-",
                                      border_width=5, visible=True, drag_submits=True, background_color='white')])
        self.layout.append([psg.Button("Save description", disabled=True, key="-SAVE_DESCRIPTION-"),
                            psg.Button("Save video", disabled=True, key="-SAVE_VIDEO-")])

        # References/Names for GUI objects

        self.__description_button = self.layout[0][5]
        self.__video_button = self.layout[0][8]

        self.__clear_button = self.layout[1][3]
        self.__save_description = self.layout[1][4]
        self.__save_video = self.layout[1][5]
        self.__save_as_images = self.layout[1][6]
        self.__slider = self.layout[1][7]

        self.__progress_bar = self.layout[3][0]

        self.__listbox = self.layout[4][0]
        self.__graph = self.layout[4][1]

        self.__graph_holder = None

    def set_window(self, window):
        self.window = window

    # Methods which buttons call
    def load_json_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        self.__labels, self.__colors, self.__connected_points = ConfigParser.parse_json_file(path)
        self.load_json_path = path
        self.__description_button.update(disabled=False)
        self.__graph_holder = GraphHolder.GraphHolder(graph=self.__graph, colors=self.__colors,
                                                      connected_points=self.__connected_points)

    def load_description_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        self.points_in_frames = Point.read_points_from_file_2(path, self.__labels)
        self.points_in_frames = Point.rough_interpolate(self.points_in_frames)
        self.load_description_path = path
        self.__slider.update(value=self.active_index, range=(0, len(self.points_in_frames) - 1), disabled=False)
        self.update_listbox()
        self.__clear_button.update(disabled=False)
        self.__save_description.update(disabled=False)
        self.__video_button.update(disabled=False)

    def load_video_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        elif self.load_description_path == "":
            psg.popup_error('Video file error', 'Please load the file describing frames first')
            return
        self.load_video_path = path
        self.__cap = cv2.VideoCapture(path)
        self.__frame_rate = self.__cap.get(cv2.CAP_PROP_FPS)
        frame_counter = 0
        self.__progress_bar.update(frame_counter, max=int(len(self.points_in_frames)), visible=True)
        while self.__cap.isOpened():
            ret, frame = self.__cap.read()
            if ret:
                working_list = self.points_in_frames[frame_counter]
                height, width, channel = frame.shape
                self.original_width = width
                self.original_height = height
                imS = cv2.resize(frame, (GuiHolder.display_width, GuiHolder.display_height))
                for PIF in working_list.points_list:
                    PIF.set_scaled_coordinates(int(PIF.c1 * GuiHolder.display_width / width),
                                               int(PIF.c2 * GuiHolder.display_height / height))
                self.original_frames.append(frame)
                self.resized_frames.append(imS)
            else:
                break
            frame_counter += 1
            self.__progress_bar.update(frame_counter)
        self.__progress_bar.update(0, max=0, visible=False)
        self.__cap.release()
        self.__save_video.update(disabled=False)
        self.__save_as_images.update(disabled=False)
        self.displayed_frames = [None] * len(self.resized_frames)
        self.__listbox.update(disabled=False)
        self.update_listbox()
        self.update_displayed_frame()

    def save_description_file(self, filename):
        file = open(filename, 'w')
        for i in range(0, len(self.points_in_frames)):
            file.write("Frame " + str(i) + ":\n")
            temp_string = ""
            for j in range(0, self.points_in_frames[i].size()):
                working_point = self.points_in_frames[i].get_point(j)
                temp_string += str(working_point.id_) + " P(" + str(working_point.sc1) + "," + str(working_point.sc2) + ")"
                if j != self.points_in_frames[i].size() - 1:
                    temp_string += " "
                else:
                    temp_string += "\n"
            file.write(temp_string)
        file.close()

    def save_video_file(self, filename):
        self.__rescale_points()
        video_out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), self.__frame_rate,
                                    (self.original_width, self.original_height))
        self.__progress_bar.update(0, max=int(len(self.points_in_frames)), visible=True)
        for i in range(0, len(self.original_frames)):
            working_image = self.__draw_on_working_image(self.original_frames[i], self.points_in_frames[i])
            video_out.write(working_image)
            self.__progress_bar.update(i)
        video_out.release()
        self.__progress_bar.update(0, max=0, visible=False)

    def save_as_images(self):
        self.__rescale_points()
        self.__progress_bar.update(0, max=int(len(self.points_in_frames)), visible=True)
        for i in range(0, len(self.original_frames)):
            working_image = self.__draw_on_working_image(self.original_frames[i], self.points_in_frames[i])
            cv2.imwrite('./images/out' + str(i) + '.png', working_image)
            self.__progress_bar.update(i)
        self.__progress_bar.update(0, max=0, visible=True)

    def clear_selection(self):
        self.update_listbox()
        self.__graph_holder.clear_selection(self.points_in_frames[self.active_index])

    def next(self):
        if self.active_index == len(self.displayed_frames) - 1:
            self.active_index = 0
        else:
            self.active_index += 1
        self.update_listbox()
        self.update_displayed_frame()
        self.update_slider(self.active_index)
        self.__graph_holder.selected_index = None

    def previous(self):
        if self.active_index == 0:
            self.active_index = len(self.displayed_frames) - 1
        else:
            self.active_index -= 1
        self.update_listbox()
        self.update_displayed_frame()
        self.update_slider(self.active_index)
        self.__graph_holder.selected_index = None

    def play(self):
        pass

    def pause(self):
        pass

    def keyboard(self, key):
        if self.__graph_holder.selected_index is None:
            if key == 'up' or key == 'down':
                return
            elif key == 'left':
                self.previous()
            elif key == 'right':
                self.next()
        else:
            point_ = self.points_in_frames[self.active_index].get_point(self.__graph_holder.selected_index)
            new_sc1 = point_.sc1
            new_sc2 = point_.sc2
            if key == 'up':
                new_sc2 = new_sc2 - 1
                if new_sc2 < 0:
                    new_sc2 = 0
            elif key == 'down':
                new_sc2 = new_sc2 + 1
                if new_sc2 > self.display_height:
                    new_sc2 = self.display_height
            elif key == 'left':
                new_sc1 = new_sc1 - 1
                if new_sc1 < 0:
                    new_sc1 = 0
            elif key == 'right':
                new_sc1 = new_sc1 + 1
                if new_sc1 > self.display_width:
                    new_sc1 = self.display_width
            self.move_point((new_sc1, new_sc2))

    # Methods for updating gui
    def update_listbox(self):
        self.__listbox.update(values=self.points_in_frames[self.active_index].points_list)

    def update_slider(self, value):
        self.__slider.update(value=value)

    def slider_moved(self, value):
        self.active_index = value
        self.update_listbox()
        self.update_displayed_frame()

    def update_displayed_frame(self):
        if self.displayed_frames[self.active_index] is None:
            imgbytes = cv2.imencode(".png", self.resized_frames[self.active_index])[1].tobytes()
            self.displayed_frames[self.active_index] = imgbytes
        self.__graph_holder.draw_image(self.displayed_frames[self.active_index], self.points_in_frames[self.active_index])

    def listbox_item_selected(self, item):
        self.__graph_holder.select_point(item, self.points_in_frames[self.active_index])

    def move_point(self, coordinates):
        new_sc1 = int(coordinates[0])
        new_sc2 = int(coordinates[1])
        self.__graph_holder.move_point(self.points_in_frames[self.active_index], new_sc1, new_sc2)
        self.update_listbox()

    # Private methods
    def __rescale_points(self):
        for frame in self.points_in_frames:
            for i in range(0, frame.size()):
                working_point = frame.get_point(i)
                sc1 = working_point.sc1
                sc2 = working_point.sc2
                working_point.c1 = int(sc1 * self.original_width / self.display_width)
                working_point.c2 = int(sc2 * self.original_height / self.display_height)

    def __draw_on_working_image(self, original_image, working_frame):
        working_image = copy.deepcopy(original_image)
        for j in range(0, working_frame.size()):
            working_point = working_frame.get_point(j)
            working_image = cv2.circle(working_image, (working_point.c1, working_point.c2), 4,
                                       self.__cv_colors[self.__colors[j]], -1)
        for j in range(0, len(self.__connected_points)):
            splits = self.__connected_points[j].split(",")
            start_point = working_frame.get_point(int(splits[0]))
            end_point = working_frame.get_point(int(splits[1]))
            working_image = cv2.line(working_image, (start_point.c1, start_point.c2), (end_point.c1, end_point.c2),
                                     self.__cv_colors[splits[2]], 1)
        return working_image
