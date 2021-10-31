#!/usr/bin/env python3
import sys
import os
from time import sleep
from collections import Counter, deque
from functools import cache
from threading import Thread
from rectangle import Rectangle

# Keep a count of each area a rectangle might have
rect_areas = Counter()
# A deque is a thread-safe data structure
rect_list = deque()
area_list = deque()


@cache
def create_rectangle(bottom, left, top, right):
    "Creating a rectangle is expensive, reuse an existing one if available"
    return Rectangle(bottom, left, top, right)


def read_rectangles():
    for line in sys.stdin:
        cmd, data = line.split(maxsplit=1)
        if cmd == "CREATE":
            bottom, left, top, right = [float(n) for n in data.split()]
            rect = create_rectangle(bottom, left, top, right)
            rect_list.append(rect)
        elif cmd == "MOVE":
            # Add moved version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_list[-1]
            new_rect = rect.move(vertical, horizontal)
            rect_list.append(new_rect)
        elif cmd == "RESIZE":
            # Add resized version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_list[-1]
            new_rect = rect.resize(vertical, horizontal)
            rect_list.append(new_rect)


def rect_to_area():
    while rect_list:
        rect = rect_list.pop()
        area = rect.area()
        area_list.append(area)


def area_to_counter():
    while area_list:
        rect_areas[area_list.pop()] += 1


if __name__ == '__main__':
    read_rectangles()
    for _ in range(os.cpu_count()):
        Thread(target=rect_to_area).start()

    # Wait for the threads to empty rect_list
    while rect_list:
        sleep(0.1)
    area_to_counter()

    print("Number of rectangles computed:", sum(rect_areas.values()))
    print("Most common rectangle areas:")
    for area, count in rect_areas.most_common(20):
        print("  Area %s\t%d rectangles" % (area, count))