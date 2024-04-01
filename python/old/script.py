# imports
import cv2
import numpy
import serial
import helper

# parse config
config = helper.args()

# create video feed
live = cv2.VideoCapture(int(config["device_id"]))
live.set(cv2.CAP_PROP_FRAME_WIDTH, int(config["width"]))
live.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config["height"]))

# setup serial controller
controller = serial.Serial(config["com_port"], 115200)

# parse group string
groups = helper.groups(config["groups"])

# prev averages
prev_averages = []

# insert empty prev values
for i in groups:
    prev_averages.append([0, 0, 0])

while (True):
    # read video frame
    _, frame = live.read()
    
    # show live feed
    if config["show_video"]:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN) 
        cv2.imshow("window", frame)
        cv2.waitKey(1)

    # split frames into groups
    frames = helper.split_frames(frame, len(groups))

    for frame_idx in range(len(frames)):
        # build average for frame slice
        slice_average = numpy.average(numpy.average(
            frames[frame_idx], axis=0), axis=0)[::-1]

        # show feed when flag is set
        if config["show_feeds"]:
            # show feed image
            cv2.imshow(
                "{0}/{1}".format(frame_idx + 1, len(groups)), frames[frame_idx])
            cv2.waitKey(1)

        # loop over rgb
        for color_idx in range(len(slice_average)):
            # check if color of frame slice has changed
            if round(prev_averages[frame_idx][color_idx]) != round(slice_average[color_idx]):
                # set color
                color = round(slice_average[color_idx])

                # update prev values
                prev_averages[frame_idx][color_idx] = round(
                    slice_average[color_idx])

                # loop over all channels
                for dmx_channel in groups[frame_idx]:
                    # build command
                    command = helper.command_builder(
                        int(dmx_channel) + color_idx, color)

                    # send command to controller
                    controller.write(command)
