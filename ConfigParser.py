import json as json


def parse_labels_file(path):
    if path is None:
        raise ValueError("Path to json labels file can not be none.\n")
    elif path.strip() == "":
        raise ValueError("Path to json labels not be an empty string.\n")
    labels = []
    colors = []
    lines = []
    with open(path) as json_file:
        json_data = json.load(json_file)
        i = 0
        for item in json_data["labels"]:
            labels.append(item[str(i)])
            i += 1
        i = 0
        for item in json_data["colors"]:
            colors.append(item[str(i)])
            i += 1
        i = 0
        for item in json_data["lines"]:
            lines.append(item[str(i)])
            i += 1
    return labels, colors, lines


def parse_json_file(path):
    if path is None:
        raise ValueError("Path to json labels file can not be none.\n")
    elif path.strip() == "":
        raise ValueError("Path to json labels can not be an empty string.\n")
    labels = []
    colors = []
    lines = []
    with open(path) as json_file:
        json_data = json.load(json_file)
        i = 0
        if "labels" not in json_data:
            raise ValueError("json file must have labels key. See instructions/example for more info.")
        for item in json_data["labels"]:
            labels.append(item[str(i)])
            i += 1
        i = 0
        if "colors" in json_data:
            for item in json_data["colors"]:
                colors.append(item[str(i)])
                i += 1
        i = 0
        if "lines" in json_data:
            for item in json_data["lines"]:
                lines.append(item[str(i)])
                i += 1
    return labels, colors, lines
