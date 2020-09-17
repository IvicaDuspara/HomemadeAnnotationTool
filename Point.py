import copy

class Point:
    def __init__(self, id_, c1, c2):
        self.id_ = id_
        self.c1 = c1
        self.c2 = c2

    def __str__(self):
        return "(" + str(self.id_) + "," + str(self.c1) + "," + str(self.c2) + ")"

    def __repr__(self):
        return str(self)


class Frame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.points_list = []

    def append_point(self, point):
        self.points_list.append(point)

    def set_points_list(self, points_list):
        self.points_list = points_list

    def get_point(self, index):
        return self.points_list[index]

    def get_number_of_points(self):
        return len(self.points_list)

    def __str__(self):
        my_str = "Frame " + str(self.id_) + "\n"
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
def read_points_from_file(path):
    if path is None or path == '':
        raise FileExistsError("File doesn't exist.")
    handle = open(path, 'r')
    Frame_List = []
    working_index = 0
    for line in handle:
        if "Frame" in line:
            working_index = int(line.split(" ")[1][0:-2])
            Frame_List.append(Frame(working_index))
        else:
            splits = line.split(" ")
            if len(splits) % 3 == 0:
                for i in range(0, len(splits), 3):
                    Frame_List[working_index].append_point(Point(int(splits[i]), int(splits[i+1]), int(splits[i+2])))
            else:
                continue
    handle.close()
    return Frame_List


def rough_interpolate(pif_list):
    last_working_index = 0
    for i in range(0, len(pif_list)):
        if pif_list[i].length() > 0:
            last_working_index = i
        else:
            pif_list[i].set_points(copy.deepcopy(pif_list[last_working_index].get_points()))
    return pif_list