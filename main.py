import cv2
import PySimpleGUI as PSG
import Point
import GUI

c = GUI.GuiHolder()
window = PSG.Window("Demo", c.layout, size=(1200, 800)).Finalize()
window.maximize()
c.set_window(window)
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Bezveze" or event == PSG.WIN_CLOSED:
        break
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
        print("Aha, selkcija liste. Označen je:")
        print(values["-LIST-"])
        c.listbox_item_selected(values["-LIST-"][0])
window.close()