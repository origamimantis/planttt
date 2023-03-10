import serial
import time
import matplotlib.pyplot as plt
import csv
import math

UPDATE_INTERVAL=50

class LivePlotter:
    def __init__(self):
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(0,100)
        self.ax.set_ylim(0,2000)
        self.graph = self.ax.plot([], [], 'b-')[0]

        self.frames_per_update = math.ceil(10*1000 / UPDATE_INTERVAL)

    def update(self, data, times):
        # limit to at most last 10 seconds
        if len(data) > self.frames_per_update:
            data = data[-self.frames_per_update:]
            times = times[-self.frames_per_update:]

        self.ax.set_xlim(times[0],times[-1])
        self.graph.set_ydata(data)
        self.graph.set_xdata(times)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main(arduino, csv_writer):

    print("Start")
    data = []
    times = []

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
            reading = float(reading)
            t = float(t)/1000

            data.append(reading)
            times.append(t)
            csv_writer.writerow([reading, t])

            if num_loops > 0 and num_loops % 4 == 0:
                plotter.update(data, times)
            num_loops += 1


with serial.Serial(port = "/dev/ttyACM0", baudrate = 9600, timeout = 0.1) as arduino:
    with open("data.csv", "w") as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(["time", "reading"])
        main(arduino, csv_writer)
