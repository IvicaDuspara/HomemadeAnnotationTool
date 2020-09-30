# Homemade Annotation Tool (HAT)

## List of contents
 + [Introduction](#Introduction)
 + [Installing](#Installing)
   + [Installing dependencies](#Installing_dependencies)
   + [Installing HAT](#Installing_HAT)
 + [Description file](#Description)
 + [Labels file](#Labels)
 + [Usage](#Usage)
 + [TODO](#TODO)
 
 <a name="Introduction"></a>
 ### Introduction
 <b>H</b>omemade <b>A</b>nnotation <b>Tool</b> is a tool for changing annotations
 on a video. HAT is designed to be used for manual fixing of objects in frames of a video
 on which was annotated using some program.
 Example of this would be:
 
 You have a video of a human and you want to do human pose estimation. After running
 that video through some program you would have a video where key points(wrists, eyes,
 shoulders etc) in each frame are marked. If there is a frame in video which you would like to manually fix, you can do 
 it using HAT. Tehnicaly speaking, HAT can change any annotations or detected objects
 in video as long as they are marked with points.
 
 <a name="Installing"></a>
 ### Installing
 Before installing HAT you have to install dependencies. 
 
 <a name="Installing_dependencies"></a>
 #### Installing dependencies
 First, you need to install
 tkinter. On Debian/Ubuntu based distributions you can use apt-get
 ```bash
sudo apt-get install python3-tk
```
After that you can use pip to get necessary dependencies
```bash
$ pip3 install opencv-python
$ pip3 install pysimplegui 
```
<a name="Installing_HAT"></a>
#### Installing HAT
Once you have downloaded source code, navigate to the folder and simply
type
```bash
$ python3 main.py
``` 
<a name="Description"></a>
### Description file
As mentioned above, HAT requires three files to function. First of which
is a description file. This file describes position of every point in each frame
of a video. For example, if a video has 2 frames file should look like this:
```
Frame 0:
0 456 712 1 142 156
Frame 1:
0 456 743 1 168 190
```
For each frame in a video file should have line "Frame number_of_frame:"
In next line for each point in frame file has index of that point followed by x and y
coordinates. This is repeated for every frame. Full example available in result.txt

<a name="Labels_file"></a>
### Labels
Second file needed is a .json file which contains following:
 - labels object
 - colors object
 - lines object
 
Labels object describes what label is assigned at what point (via index) in 
each frame
Colors object describes which color will which point be

Lines object describes which points are connected and with what color should
line be drawn

See openvino_labels.json for a full example

<a name="Usage"></a>
### Usage
Run program. Load description file. Load video.
Selecting a point on listbox allows you to move it on display.  

<a name="TODO"></a>
This is a TODO list. These features are planned and will be coming
to HAT eventually.

High Priority:
 + Specify simpler json file which would only have labels. Colors
   would be defaulted while lines would not be drawn
 + Specify location of saved description file and saved video
 + Export annotated video (user chooses resolution)
 + Export series of images (user chooses resolution)
 + Cleaner error messages as pop-up windows

Normal Priority:
 + Allow user to flag specific frames with flags which describe state of annotated
   picture.
   + Completely annotated
   + Incomplete annotation
   + Needs manual fixing
 + Warning system for other annotators that they should check frames
   which were marked as incomplete or in need of fixing
 + Allow addition of points in each frames.
 + Allow creation of lines between points. 
 + Better progress loading / saving
 
Low Priority:
 + Allow drawing of polylines and polygons
 + Support for loading files with polylines and polygons
 + Embedding AI annotation
 + Skin styles
 
   