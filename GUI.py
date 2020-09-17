import Point
import cv2
import PySimpleGUI as psg

class GuiHolder:
    def __init__(self):
        # paths to files
        self.description_path = ""
        self.video_path = ""

        # different frames list
        self.original_frames = []
        self.resized_frames = []
        self.displayed_frames = []
        self.points_in_frames = []

        self.active_index = 0

        # other
        self.cap = None
        self.window = None
        self.layout = []

        self.layout.append([psg.Text("Description file location:"),
                            psg.In(size=(35, 1), enable_events=True, key="-FILE_DESCRIPTION-"),
                            psg.FileBrowse(),
                            psg.Text("Video file location:"),
                            psg.In(size=(35, 1), enable_events=True, key="-FILE_VIDEO-"),
                            psg.FileBrowse()])
        self.layout.append([psg.Button("Previous"), psg.Button("Play"), psg.Button("Next"),
                            psg.Slider(default_value=0, range=(0, 0), disabled=True, enable_events=True,
                                       orientation='horizontal',
                                       size=(75, 25), key="-FRAME_SLIDER-")])
        self.layout.append([psg.HorizontalSeparator()])
        self.layout.append([psg.ProgressBar(max_value=0, orientation='horizontal', bar_color=('green', 'white'),
                                            visible=False, size=(100, 15))])
        self.layout.append([psg.Listbox(values=[], key="-LIST-", size=(50, 150)),
                            psg.Image(filename="", key="-IMAGE-", size=(200, 200))])

        self.slider = self.layout[1][3]
        self.progress_bar = self.layout[3][0]
        self.listbox = self.layout[4][0]

    def set_window(self, window):
        self.window = window

    # Methods which buttons call
    def load_description_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        self.points_in_frames = Point.read_points_from_file(path)
        self.points_in_frames = Point.rough_interpolate(self.points_in_frames)
        self.description_path = path
        self.slider.update(value=self.active_index, range=(0, len(self.points_in_frames)), disabled=False)
        self.update_listbox()

    def load_video_file(self, path):
        if path is None:
            psg.popup_error('File error', 'Path can not be None')
            return
        elif path == '' or path.strip() == '':
            psg.popup_error('File error', 'Path can not be an empty string')
            return
        elif self.description_path == "":
            psg.popup_error('Video file error', 'Please load the file describing frames first')
            return
        self.video_path = path
        self.cap = cv2.VideoCapture(path)
        frame_counter = 0
        self.progress_bar.update(frame_counter, max=int(len(self.points_in_frames)), visible=True)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                working_list = self.points_in_frames[frame_counter]
                for PIF in working_list.points_list:
                    cv2.circle(frame, (int(PIF.c1), int(PIF.c2)), 3, (255, 0, 0))
                self.original_frames.append(frame)
                imS = cv2.resize(frame, (800, 600))
                self.resized_frames.append(imS)
            else:
                break
            frame_counter += 1
            self.progress_bar.update(frame_counter)
        self.progress_bar.update(0, max=0, visible=False)
        self.cap.release()
        self.displayed_frames = [None] * len(self.resized_frames)
        self.update_displayed_frame()

    def update_listbox(self):
        self.listbox.update(values=self.points_in_frames[self.active_index].points_list)

    def update_slider(self, value):
        self.slider.update(value=value)

    def slider_moved(self, value):
        self.active_index = value
        self.update_listbox()

    def update_displayed_frame(self):
        pass


    def next(self):
        if self.active_index == len(self.displayed_frames) - 1:
            self.active_index = 0
        else:
            self.active_index += 1
        self.update_listbox()
        self.update_displayed_frame()
        #self.slider.update(self.active_index)
        self.update_slider(self.active_index)

    def previous(self):
        if self.active_index == 0:
            self.active_index = len(self.displayed_frames) - 1
        else:
            self.active_index -= 1
        self.update_listbox()
        self.update_displayed_frame()
        self.update_slider(self.active_index)

    def play(self):
        pass

    def pause(self):
        pass