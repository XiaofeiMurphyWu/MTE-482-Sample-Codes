import numpy as np
import matplotlib.pyplot as plt

base = np.loadtxt("base3.txt", comments="#", delimiter=",", encoding='UTF-8', unpack=False)
data = np.loadtxt("hand3.txt", comments="#", delimiter=",", encoding='UTF-8', unpack=False)

fdata = data - base

# data_file = np.genfromtxt("plot1.csv", delimiter=',', encoding='UTF-8')
sz = np.shape(fdata)
nrows = sz[0]
ncols = sz[1]
pixel_plot = plt.figure()
# pixel_plot.add_axes([0.1, 0.1, 0.5, 0.5])
plt.title("pixel_plot")
pixel_plot = plt.imshow(
  fdata, cmap='Blues', interpolation='nearest')
plt.colorbar(pixel_plot)
# plt.plot(pixel_plot)
plt.show()
