# libs
import cv2 as opencv
import serial as serial

# scripts
import calculations
import config

# config
CONFIG = config.load()

# previous averages storage
previousAverages = [None] * 512

# create DMX controller
controller = serial.Serial(CONFIG["COMPORT"], 115200)

# create and config video capture
capture = opencv.VideoCapture(CONFIG["CAPTUREDEVICE"])
capture.set(opencv.CAP_PROP_FRAME_HEIGHT, calculations.scaleInputVideo(
    CONFIG["INPUTHEIGHT"], CONFIG["SCALEINPUT"]))
capture.set(opencv.CAP_PROP_FRAME_WIDTH, calculations.scaleInputVideo(
    CONFIG["INPUTWIDTH"], CONFIG["SCALEINPUT"]))

# check if capture works
if capture.isOpened():
    status = capture.read()
else:
    status = False

# infinite loop when capture works
while status:
    # capture frame
    status, frame = capture.read()

    # display full frame when config is set
    if CONFIG["SHOWINPUT"]:
        opencv.imshow("Frame: Full-Input", frame)

    # split frame into their sections
    frameSections = calculations.splitIntoSections(
        frame, CONFIG["ROWS"], CONFIG["COLS"])

    # 2d loop over all frames
    for frameSectionRow in range(0, len(frameSections)):
        for frameSectionCol in range(0, len(frameSections[frameSectionRow])):
            # calculate DMX Channel
            dmxChannel = calculations.dmxChannel(len(frameSections), len(
                frameSections[frameSectionRow]), frameSectionRow, frameSectionCol)

            # calculate RGB Average
            rgbAverage = calculations.rgbAverage(
                frameSections[frameSectionRow][frameSectionCol])

            # display sections config is set
            if CONFIG["SHOWSECTIONS"]:
                opencv.imshow("Frame: " + str(frameSectionRow) + "/" + str(
                    frameSectionCol) + " DMX: " + str(dmxChannel), frameSections[frameSectionRow][frameSectionCol])

            # send RGB Averages to controller
            for dmxAdder in range(0, 3):
                # calculate channel and value
                channel = dmxChannel + dmxAdder
                value = int(rgbAverage[dmxAdder])

                # update values if values changed
                if previousAverages[channel] != value:
                    controller.write("{0}c{1}v".format(
                        channel, value).encode())
                    previousAverages[channel] = value

    # exit on ESC
    if opencv.waitKey(20) == 27:
        break

# release video capture device
capture.release()
