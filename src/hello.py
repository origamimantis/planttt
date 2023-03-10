import serial
import time
import matplotlib.pyplot as plt
import csv
import math
from collections import deque

UPDATE_INTERVAL=50
MAXLEN = math.ceil(10*1000 / UPDATE_INTERVAL)

class LivePlotter:
    def __init__(self):
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title("BOO")
        self.ax.set_xlabel("time (s)")
        self.ax.set_ylabel("voltage (V)")

        self.ax.set_xlim(0,100)
        self.ax.set_ylim(-5,5)
        self.ax.grid(True)

        self.graph = self.ax.plot([], [], 'b-')[0]

        self.frames_per_update = math.ceil(10*1000 / UPDATE_INTERVAL)

    def update(self, data, times):
        # limit to at most last 10 seconds
        self.ax.set_xlim(times[0],times[-1])
        self.ax.set_xticks(range(math.ceil(times[0]), math.ceil(times[-1])))
        self.ax.set_xticks(range(math.ceil(times[0]), math.ceil(times[-1])))

        self.graph.set_ydata(data)
        self.graph.set_xdata(times)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main(arduino, csv_writer):

    print("Start")
    data = deque(maxlen=MAXLEN)
    times = deque(maxlen=MAXLEN)

    plotter = LivePlotter()

    # let leftover buffer data fill up before clearing
    time.sleep(0.5)
    arduino.reset_input_buffer()

    num_loops = 0

    # based on past runs, this will run for 10 loops (1 second) before getting input
    while True:
        l = arduino.readline()
        if l:
            l = l.decode().strip()
            reading, t= l.split()
            reading = float(reading)/1024*5
            t = float(t)/1000

            data.append(reading)
            times.append(t)
            csv_writer.writerow([reading, t])

            print(reading)
            if num_loops > 0 and num_loops % 4 == 0:
                plotter.update(data, times)
            num_loops += 1


with serial.Serial(port = "/dev/ttyACM0", baudrate = 9600, timeout = 0.1) as arduino:
    with open("data.csv", "w") as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(["time", "reading"])
        main(arduino, csv_writer)
