import PySimpleGUI as PSG
import GUI
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--description', help='Path to description file')
parser.add_argument('-j', '--json', help='Path to .json file')
args = parser.parse_args()

c = GUI.GuiHolder()
window = PSG.Window("Demo", c.layout, size=(1330, 900), return_keyboard_events=True).Finalize()
window.maximize()
c.set_window(window)
if args.json is not None:
    c.load_json_file(args.json)
if args.description is not None:
    c.load_description_file(args.description)


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == PSG.WIN_CLOSED:
        break
    elif event == "-FILE_JSON-":
        c.load_json_file(values["-FILE_JSON-"])
    elif event == "-FILE_DESCRIPTION-":
        c.load_description_file(values["-FILE_DESCRIPTION-"])
    elif event == "-FILE_VIDEO-":
        c.load_video_file(values["-FILE_VIDEO-"])
    elif event == "Previous":
        c.previous()
    elif event == "Next":
        c.next()
    elif event == "Play":
        c.play()
    elif event == "Pause":
        c.pause()
    elif event == "-FRAME_SLIDER-":
        c.slider_moved(int(values["-FRAME_SLIDER-"]))
    elif event == "-LIST-":
        c.listbox_item_selected(values["-LIST-"][0])
    elif event == "-CLEAR_SELECTION-":
        c.clear_selection()
    elif event == "-GRAPH-":
        c.move_point(values["-GRAPH-"])
    elif event == "-SAVE_DESCRIPTION-":
        c.save_description_file("./saved.txt")
    elif event == "-SAVE_VIDEO-":
        c.save_video_file("./out.mp4")
    elif event == "-SAVE_AS_IMAGES-":
        c.save_as_images()
    elif event == 'Up:111':
        c.keyboard('up')
    elif event == 'Down:116':
        c.keyboard('down')
    elif event == 'Left:113':
        c.keyboard('left')
    elif event == 'Right:114':
        c.keyboard('right')
window.close()