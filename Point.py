import copy
import Constants


class Point:
    def __init__(self, id_, x, y, label):
        self.id_ = id_
        self.x = x
        self.y = y
        self.scx = x
        self.scy = y
        self.label = label

    def __str__(self):
        return str(self.label) + " " + "(" + str(self.id_) + "," + str(self.scx) + "," + str(self.scy) + ")"

    def __repr__(self):
        return str(self)

    def set_scaled_coordinates(self, scx, scy):
        self.scx = scx
        self.scy = scy

    def get_my_label(self):
        return self.label


class Frame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.points_list = []
        self.status = Constants.flag_nothing
        self.was_displayed = False

    def append_point(self, point):
        self.points_list.append(point)

    def set_points_list(self, points_list):
        self.points_list = points_list

    def set_status(self, status):
        self.status = status

    def get_point(self, index):
        return self.points_list[index]

    def size(self):
        return len(self.points_list)

    def __str__(self):
        my_str = "Frame " + str(self.frame_id) + "\n"
        for i in range(0, len(self.points_list)):
            my_str += str(self.points_list[i])
            if i != len(self.points_list) - 1:
                my_str += " "
            else:
                my_str += "\n"
        return my_str

    def __repr__(self):
        return str(self)


# Functions for creating points / list of points
def read_points_from_file(path, labels):
    if path is None or path == '':
        raise FileExistsError("File doesn't exist.")
    handle = open(path, 'r')
    frame_list = []
    working_index = 0
    for line in handle:
        if "Frame" in line:
            working_index = int(line.split(" ")[1][0:-2])
            frame_list.append(Frame(working_index))
        else:
            splits = line.split(" ")
            if len(splits) % 3 == 0:
                for i in range(0, len(splits), 3):
                    frame_list[working_index].append_point(Point(int(splits[i]), int(splits[i+1]),
                                                                 int(splits[i+2]), labels[i//3]))
            else:
                continue
    handle.close()
    return frame_list


def rough_interpolate(frame_list):
    last_working_index = 0
    for i in range(0, len(frame_list)):
        if frame_list[i].size() > 0:
            last_working_index = i
        else:
            frame_list[i].set_points_list(copy.deepcopy(frame_list[last_working_index].points_list))
    return frame_list


def read_points_from_file_2(path, labels):
    handle = open(path, 'r')
    frame_list = []
    working_index = 0
    for line in handle:
        if "Frame" in line:
            working_index = int(line.split(" ")[1][0:-2])
            frame_list.append(Frame(working_index))
        else:
            splits = line.strip().split(" ")
            if len(splits) == 1:
                continue
            else:
                for i in range(0, len(splits), 2):
                    shape_index = int(splits[i])
                    type_of_shape = splits[i+1][0]
                    parameters = splits[i+1].strip()[2:-1].split(",")
                    if type_of_shape == 'P':
                        frame_list[working_index].append_point(Point(shape_index, int(parameters[0]),
                                                                     int(parameters[1]), labels[i // 2]))
                    elif type_of_shape == 'R':
                        raise ValueError("Currently not supported")
                    elif type_of_shape == 'C':
                        raise ValueError("Currently not supported")
                    else:
                        raise ValueError("UNK")
    handle.close()
    return frame_list

