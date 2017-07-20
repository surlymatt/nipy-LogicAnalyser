import nidaqmx
import pprint
import time

import matplotlib.pyplot as plt
import numpy as np
from nidaqmx.constants import (LineGrouping)
pp = pprint.PrettyPrinter(indent=4)

numruns = 10000

with nidaqmx.Task() as task:

    task.di_channels.add_di_chan("Dev3/port0/line0:7",
                                 line_grouping = LineGrouping.CHAN_PER_LINE)

    t0 = time.time()
    data = task.read(number_of_samples_per_channel=numruns)
    t1 = time.time()

interval = t1-t0
speed = numruns/interval
print(round(interval,2),"seconds for",numruns,"reads.")
print(round(speed,1),"samples per second.")

traces = np.zeros((numruns,8),np.object)
for n in range(numruns):
    for m in range(8):
        traces[n][m] = m + 0.5* int(data[m][n])

# pp.pprint(data)
# pp.pprint(traces)
plt.title('Sledgehammer Logic Analyser - niDAQmx')
plt.plot(traces)
plt.grid(True)
plt.show()
