# libs
import cv2 as opencv
import numpy as numpy


# scale the input video dimensions by a factor
def scaleInputVideo(value, factor=1):
    return int(value * factor)


# split a frame into its sections defined by rows and cols
def splitIntoSections(frame, rows, cols):
    frameSections = [[0 for col in range(cols)] for row in range(rows)]
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    for row in range(0, rows):
        for col in range(0, cols):
            frameSections[row][col] = frame[
                int(row * frameHeight / rows): int(
                    row * frameHeight / rows + frameHeight / rows
                ),
                int(col * frameWidth / cols): int(
                    col * frameWidth / cols + frameWidth / cols
                ),
            ]
    return frameSections


# calculate the average rgb value of a frame
def rgbAverage(section):
    section = opencv.cvtColor(section, opencv.COLOR_BGR2RGB)
    return numpy.average(section, axis=(0, 1))


# calculate dmx channel
def dmxChannel(rows, cols, cRow, cCol):
    # convert 0 based index to 1 based
    cRow += 1
    cCol += 1

    # calculate DMX channel
    return (cols * (cRow - 1) + cCol) * 4 - 3
