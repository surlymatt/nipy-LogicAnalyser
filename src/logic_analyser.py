import nidaqmx
import pprint
import time

import matplotlib.pyplot as plt
import numpy as np
from nidaqmx.constants import (LineGrouping)
pp = pprint.PrettyPrinter(indent=4)

numSamples = 10000
daqDevice = "Dev3/port0/line0:7"

with nidaqmx.Task() as task:

    task.di_channels.add_di_chan(daqDevice,
                                 line_grouping = LineGrouping.CHAN_PER_LINE)

    t0 = time.time()
    data = task.read(number_of_samples_per_channel=numSamples)
    t1 = time.time()

interval = t1-t0
speed = numSamples / interval
print(round(interval,2),"seconds for", numSamples, "reads.")
print(round(speed,1),"samples per second.")

# Convert the list of lists a numpy array and add offsets to each channel
# TODO: find a numpy way of doing this.  Maybe zip?
traces = np.zeros((numSamples, 8), np.object)
for n in range(numSamples):
    for m in range(8):
        traces[n][m] = m + 0.7* int(data[m][n])

plt.title('Poor Mans Logic Analyser - niDAQmx')
plt.xlabel('Sample number')
plt.ylabel('Pin state')
plt.plot(traces)
plt.grid(True)
plt.savefig("plot.png")
plt.show()
