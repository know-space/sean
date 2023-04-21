import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read in the CSV file
data = pd.read_csv(r"C:\Users\seanp\PycharmProjects\ScratchPad\space\sensor_observations.csv")

# Convert the azimuth and elevation to Cartesian coordinates
x = -data["Elevation"] * np.sin(np.radians(data["Azimuth"]))
y = -data["Elevation"] * np.cos(np.radians(data["Azimuth"]))
bins = 500

# Create a heatmap of the data
plt.hist2d(x, y, bins=bins, cmap=plt.cm.jet)

# Set the axis labels and title
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Sensor Observations")

# Add a colorbar to the plot
plt.colorbar()

# Save the plot to a file
plt.savefig(f"C:\\Users\\seanp\\PycharmProjects\\ScratchPad\\space\\sensor_heatmap_{bins}.png")

# Show the plot
plt.show()
