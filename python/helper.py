# import libs
import argparse
import os


def args():
    parser = argparse.ArgumentParser(
        description="DMX Interface", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--com_port", "-C",
                        help="COM Port to connect to", required=True)
    parser.add_argument("--device_id", "-D",
                        help="ID of capture device", required=True)
    parser.add_argument(
        "--groups", "-G", help="Groups to use for DMX parsing (e.g. \"1|4\" -> Two Groups with the channels [1] and [4], \"1|4,7|10\" -> Three Groups with the channels [1], [4 and 7] and [10])", default="1")
    parser.add_argument(
        "--width", "-W", help="Width of the captured video", default=1920)
    parser.add_argument(
        "--height", "-H", help="Height of the captured video", default=1080)
    parser.add_argument("--show_feeds", "-S", help="Show individual sliced feeds",
                        default=False, action="store_true")
    parser.add_argument("--show_video", "-V", help="Show Video feed",
                        default=False, action="store_true")
    return vars(parser.parse_args())


def groups(group_string):
    splitted_groups = group_string.split("|")
    groups = list(map(lambda splitted_group: splitted_group.split(
        ","), splitted_groups))
    return groups


def split_frames(frame, count):
    # get avg from length of first row of frames
    avg = len(frame[0]) / float(count)

    # create empty out frames
    out = []

    # create last index
    last = 0.0

    # split frames
    while last < len(frame[0]):
        out.append(frame[:, int(last):int(last + avg)])
        last += avg

    # return split frames
    return out


def command_builder(channel, value):
    return "{0}c{1}v".format(channel, value).encode()
