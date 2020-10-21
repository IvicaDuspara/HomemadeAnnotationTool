import Point
import GraphHolder
import cv2
import PySimpleGUI as psg
import ConfigParser
import copy


def check_maximum_index(list_of_frames):
    maximum = 0
    for i in range(0, len(list_of_frames)):
        size = list_of_frames[i].size()
        maximum = max(maximum, size)
    return maximum


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

        self.all_frames = []
        self.__completed_frames = []
        self.__to_fix_frames = []
        self.__undecided_frames = []
        self.displayed_frames = []

        self.__points_in_all_frames = []
        self.__points_in_completed_frames = []
        self.__points_in_to_fix_frames = []
        self.__points_in_undecided_frames = []
        self.displayed_points = []

        self.active_index = 0
        self.__all_index = 0
        self.__to_fix_index = 0
        self.__completed_index = 0
        self.__frame_counter = 0
        self.__undecided_index = 0


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
        self.layout.append([psg.Button("Jump", disabled=True, key="-JUMP-"), psg.In(size=(15, 1), enable_events=True,
                                                                                    key="-JMP_DESTINATION-"),
                            psg.Button("Save satisfactory images", disabled=True, key="-SAVE_SATISFACTORY-")])
        self.layout.append([psg.HorizontalSeparator()])
        self.layout.append([psg.ProgressBar(max_value=0, orientation='horizontal', bar_color=('green', 'white'),
                                            visible=False, size=(100, 15))])
        self.__column_layout = [[psg.Radio("Satisfactory", group_id=1, default=False, enable_events=True,
                                           key='-Radio_S-', disabled=True)],
                                [psg.Radio("Needs fixing", group_id=1, default=False, enable_events=True,
                                           key="-Radio_F-", disabled=True)],
                                [psg.Radio("Undecided", group_id=1, default=False, enable_events=True,
                                           key="-Radio_U-", disabled=True)],
                                [psg.Combo(values=('All', 'Satisfactory', 'Needs fixing', 'Undecided'),
                                           default_value='All', enable_events=True, key='-COMBO-', disabled=True),
                                 psg.Text(text="Current value:", size=(35, 1))]]
        self.layout.append([psg.Listbox(values=[], key="-LIST-", size=(35, 35),
                                        select_mode="LISTBOX_SELECT_MODE_SINGLE",
                                        enable_events=True, disabled=True),
                            psg.Graph((800, 600), (0, 600), (800, 0), enable_events=True, key="-GRAPH-",
                                      border_width=5, visible=True, drag_submits=True, background_color='white')])
        self.layout.append([psg.Column(layout=self.__column_layout, visible=True, key='-COLUMN-',
                                       vertical_alignment='top', element_justification='center')])
        # References/Names for GUI objects

        self.__description_button = self.layout[0][5]
        self.__video_button = self.layout[0][8]

        self.__clear_button = self.layout[1][3]
        self.__save_description = self.layout[1][4]
        self.__save_video = self.layout[1][5]
        self.__save_as_images = self.layout[1][6]
        self.__slider = self.layout[1][7]

        self.__progress_bar = self.layout[4][0]

        self.__listbox = self.layout[5][0]
        self.__graph = self.layout[5][1]
        self.__column = self.layout[6][0]
        self.__radio_buttons = [self.__column_layout[0][0], self.__column_layout[1][0], self.__column_layout[2][0]]
        self.__combo = self.__column_layout[3][0]
        self.__text = self.__column_layout[3][1]

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
        d_color = False
        if len(self.__colors) == 0:
            d_color = True
        self.load_json_path = path
        self.__description_button.update(disabled=False)
        self.__graph_holder = GraphHolder.GraphHolder(graph=self.__graph, colors=self.__colors,
                                                      connected_points=self.__connected_points, defaulted_color=d_color)

    def load_description_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        self.__points_in_all_frames = Point.read_points_from_file_2(path, self.__labels)
        self.__points_in_all_frames = Point.rough_interpolate(self.__points_in_all_frames)
        self.displayed_points = self.__points_in_all_frames
        self.active_index = self.__all_index
        max_frame = check_maximum_index(self.__points_in_all_frames)
        if self.__graph_holder.defaulted_color:
            colors = ['blue'] * max_frame
            self.__graph_holder.colors = colors
        self.load_description_path = path
        self.__slider.update(value=self.active_index, range=(0, len(self.__points_in_all_frames) - 1), disabled=False)
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
        self.__cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.__frame_rate = self.__cap.get(cv2.CAP_PROP_FPS)
        self.__save_video.update(disabled=False)
        self.__save_as_images.update(disabled=False)
        self.__radio_buttons[0].update(disabled=False)
        self.__radio_buttons[1].update(disabled=False)
        self.__radio_buttons[2].update(disabled=False)
        self.__combo.update(disabled=False)
        self.layout[2][0].update(disabled=False)
        self.layout[2][2].update(disabled=False)
        self.all_frames = [None] * len(self.__points_in_all_frames)
        self.displayed_frames = self.all_frames
        self.__listbox.update(disabled=False)
        self.update_listbox()
        self.update_displayed_frame()

    def save_description_file(self, filename):
        self.__rescale_points()
        file = open(filename, 'w')
        for i in range(0, len(self.__points_in_all_frames)):
            file.write("Frame " + str(i) + ":\n")
            temp_string = ""
            for j in range(0, self.__points_in_all_frames[i].size()):
                working_point = self.__points_in_all_frames[i].get_point(j)
                temp_string += str(working_point.id_) + " P(" + str(working_point.x) + "," + str(working_point.y) + ")"
                if j != self.__points_in_all_frames[i].size() - 1:
                    temp_string += " "
                else:
                    temp_string += "\n"
            file.write(temp_string)
        file.close()

    def save_video_file(self, filename):
        self.__rescale_points()
        video_out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), self.__frame_rate,
                                    (self.original_width, self.original_height))
        self.__progress_bar.update(0, max=int(len(self.__points_in_all_frames)), visible=True)
        for i in range(0, len(self.__points_in_all_frames)):
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = self.__cap.read()
            if ret:
                working_image = self.__draw_on_working_image(frame, self.__points_in_all_frames[i])
                video_out.write(working_image)
                self.__progress_bar.update(i)
            else:
                psg.popup_error('Save error', 'A frame in a video is missing.\nThis frame will be skipped')
        video_out.release()
        self.__progress_bar.update(0, max=0, visible=False)

    def save_as_images(self):
        self.__rescale_points()
        self.__progress_bar.update(0, max=int(len(self.__points_in_all_frames)), visible=True)
        for i in range(0, len(self.__points_in_all_frames)):
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = self.__cap.read()
            if ret:
                working_image = self.__draw_on_working_image(frame, self.__points_in_all_frames[i])
                cv2.imwrite('./images/out' + str(i) + '.png', working_image)
                self.__progress_bar.update(i)
            else:
                psg.popup_error('Save error', 'A frame in a video is missing.\nThis frame will be skipped')
        self.__progress_bar.update(0, max=0, visible=False)

    def save_satisfactory_images(self):
        self.__rescale_points()
        self.__progress_bar.update(0, max=int(len(self.__points_in_completed_frames)), visible=True)
        for i in range(0, len(self.__points_in_completed_frames)):
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, self.__points_in_completed_frames[i].frame_id)
            ret, frame = self.__cap.read()
            if ret:
                working_image = self.__draw_on_working_image(frame, self.__points_in_completed_frames[i])
                cv2.imwrite('./images/out' + str(i) + '.png', working_image)
                self.__progress_bar.update(i)
            else:
                psg.popup_error('Save error', 'A frame in a video is missing.\nThis frame will be skipped')
        self.__progress_bar.update(0, max=0, visible=False)


    def clear_selection(self):
        self.update_listbox()
        self.__graph_holder.clear_selection(self.__points_in_all_frames[self.active_index])

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
            point_ = self.__points_in_all_frames[self.active_index].get_point(self.__graph_holder.selected_index)
            new_scx = point_.scx
            new_scy = point_.scy
            if key == 'up':
                new_scy = new_scy - 1
                if new_scy < 0:
                    new_scy = 0
            elif key == 'down':
                new_scy = new_scy + 1
                if new_scy > self.display_height:
                    new_scy = self.display_height
            elif key == 'left':
                new_scx = new_scx - 1
                if new_scx < 0:
                    new_scx = 0
            elif key == 'right':
                new_scx = new_scx + 1
                if new_scx > self.display_width:
                    new_scx = self.display_width
            self.move_point((new_scx, new_scy))

    def jump(self):
        value = self.layout[2][1].get()
        try:
            value = int(value)
            self.update_slider(value)
            self.slider_moved(value)
        except:
            return

    # Methods for updating gui
    def update_listbox(self):
        if len(self.displayed_points) == 0:
            self.__listbox.update(values=[])
        else:
            self.__listbox.update(values=self.displayed_points[self.active_index].points_list)

    def update_slider(self, value):
        self.__slider.update(value=value)

    def slider_moved(self, value):
        self.active_index = value
        self.update_listbox()
        self.update_displayed_frame()

    def update_displayed_frame(self):
        if len(self.displayed_frames) == 0:
            self.__graph.update(visible=False)
        else:
            self.__graph.update(visible=True)
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, self.active_index)
            if self.all_frames[self.active_index] is None:
                ret, frame = self.__cap.read()
                if ret:
                    working_list = self.__points_in_all_frames[self.active_index]
                    height, width, channel = frame.shape
                    self.original_width = width
                    self.original_height = height
                    imS = cv2.resize(frame, (GuiHolder.display_width, GuiHolder.display_height))
                    for PIF in working_list.points_list:
                        PIF.set_scaled_coordinates(int(PIF.x * GuiHolder.display_width / width),
                                                   int(PIF.y * GuiHolder.display_height / height))
                    img_bytes = cv2.imencode(".png", imS)[1].tobytes()
                    working_list.was_displayed = True
                    self.all_frames[self.active_index] = img_bytes
                else:
                    psg.popup_error('Read error', 'Couldn\'t read frame no: ' + str(self.active_index))
            self.__graph_holder.draw_image(self.displayed_frames[self.active_index], self.displayed_points[self.active_index])
            status = self.displayed_points[self.active_index].status
            self.__update_text(status)
            if status == 4:
                self.__radio_buttons[0].update(value=False)
                self.__radio_buttons[1].update(value=False)
                self.__radio_buttons[2].update(value=False)
            else:
                self.__radio_buttons[self.displayed_points[self.active_index].status - 1].update(value=True)

    def listbox_item_selected(self, item):
        self.__graph_holder.select_point(item, self.__points_in_all_frames[self.active_index])

    def move_point(self, coordinates):
        new_scx = int(coordinates[0])
        new_scy = int(coordinates[1])
        self.__graph_holder.move_point(self.__points_in_all_frames[self.active_index], new_scx, new_scy)
        self.update_listbox()

    def set_status(self, number):
        old_status = self.__points_in_all_frames[self.active_index].status
        id_ = self.__points_in_all_frames[self.active_index].frame_id
        self.__remove_specific(id_, old_status)
        self.__points_in_all_frames[self.active_index].status = number
        self.__radio_buttons[number - 1].update(value=True)
        self.__id_insert(id_, number)
        self.__update_text(number)

    def change_display(self, value):
        if value == 'All':
            self.displayed_frames = self.all_frames
            self.displayed_points = self.__points_in_all_frames
            self.active_index = self.__all_index
        elif value == 'Need fixing':
            self.displayed_frames = self.__to_fix_frames
            self.displayed_points = self.__points_in_to_fix_frames
            self.active_index = self.__to_fix_index
        elif value == 'Undecided':
            self.displayed_frames = self.__undecided_frames
            self.displayed_points = self.__points_in_undecided_frames
            self.active_index = self.__to_fix_index
        elif value == 'Completed':
            self.displayed_frames = self.__completed_frames
            self.displayed_points = self.__points_in_completed_frames
            self.active_index = self.__completed_index
        self.__slider.update(value=self.active_index, range=(0, len(self.displayed_frames) - 1))
        self.update_listbox()
        self.update_displayed_frame()

    def close(self):
        if self.__cap is not None:
            self.__cap.release()

    # Private methods
    def __rescale_points(self):
        for frame in self.__points_in_all_frames:
            if frame.was_displayed:
                for i in range(0, frame.size()):
                    working_point = frame.get_point(i)
                    scx = working_point.scx
                    scy = working_point.scy
                    working_point.x = int(scx * self.original_width / self.display_width)
                    working_point.y = int(scy * self.original_height / self.display_height)

    def __draw_on_working_image(self, original_image, working_frame):
        working_image = copy.deepcopy(original_image)
        for j in range(0, working_frame.size()):
            working_point = working_frame.get_point(j)
            working_image = cv2.circle(working_image, (working_point.x, working_point.y), 4,
                                       self.__cv_colors[self.__colors[j]], -1)
        for j in range(0, len(self.__connected_points)):
            splits = self.__connected_points[j].split(",")
            start_point = working_frame.get_point(int(splits[0]))
            end_point = working_frame.get_point(int(splits[1]))
            working_image = cv2.line(working_image, (start_point.x, start_point.y), (end_point.x, end_point.y),
                                     self.__cv_colors[splits[2]], 1)
        return working_image

    def __remove_specific(self, id_, old_status):
        if old_status == 4:
            return
        working_display_list = None
        working_points_list = None
        if old_status == 1:
            working_display_list = self.__completed_frames
            working_points_list = self.__points_in_completed_frames
        elif old_status == 2:
            working_display_list = self.__to_fix_frames
            working_points_list = self.__points_in_to_fix_frames
        elif old_status == 3:
            working_display_list = self.__undecided_frames
            working_points_list = self.__points_in_undecided_frames
        for i in range(0, len(working_points_list)):
            if working_points_list[i].frame_id == id_:
                working_display_list.pop(i)
                working_points_list.pop(i)
                break

    def __id_insert(self, id_, new_status):
        working_display_list = None
        working_points_list = None
        if new_status == 1:
            working_display_list = self.__completed_frames
            working_points_list = self.__points_in_completed_frames
        elif new_status == 2:
            working_display_list = self.__to_fix_frames
            working_points_list = self.__points_in_to_fix_frames
        elif new_status == 3:
            working_display_list = self.__undecided_frames
            working_points_list = self.__points_in_undecided_frames
        insertion_flag = 0
        for i in range(0, len(working_points_list)):
            if working_points_list[i].frame_id > id_:
                working_points_list.insert(i, self.__points_in_all_frames[id_])
                working_display_list.insert(i, self.all_frames[id_])
                insertion_flag = 1
                break
        if insertion_flag == 0:
            working_points_list.append(self.__points_in_all_frames[id_])
            working_display_list.append(self.all_frames[id_])

    def __update_text(self, number):
        if number == 1:
            self.__text.update(value='Current value: Satisfactory')
        elif number == 2:
            self.__text.update(value='Current value: Needs fixing')
        elif number == 3:
            self.__text.update(value='Current value: Undecided')
        else:
            self.__text.update(value='Current value: ')
