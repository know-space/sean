import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('measurements.csv')

# Convert the 'Ob Time' column to datetime objects
df['Ob Time'] = pd.to_datetime(df['Ob Time'])

# Convert the datetime objects to seconds since Unix epoch time
df['Ob Time'] = df['Ob Time'].apply(lambda x: x.timestamp())

# Create a colormap based on the time values. viridis plasma inferno magma cividis cool coolwarm hot
# spring summer autumn winter gray
cmap = plt.get_cmap('cool')
norm = colors.Normalize(vmin=df['Ob Time'].min(), vmax=df['Ob Time'].max())

# Set up the plot
fig, ax = plt.subplots(facecolor='white')
sc = ax.scatter(df['Right Ascension'], df['Declination'], c=df['Ob Time'], cmap=cmap, norm=norm,
                marker='o', s=20, edgecolor='none', alpha=0.6)
ax.set_xlabel('Right Ascension')
ax.set_ylabel('Declination')

# Set the background color of the plot area
ax.set_facecolor('black')

# Add grid lines
ax.grid(True, color='grey', linestyle='-')

# Colorbar
cbar = plt.colorbar(sc)
cbar.set_label('Ob Time')

# Add a time text box for animated measurements
time_text = ax.text(0.05, .95, '', transform=ax.transAxes, color='white', fontsize=10)

# Create a new axis for the progress bar
progress_ax = plt.axes([0.1, .009, 0.7, 0.02])  # [left, bottom, width, height]
progress_ax.set_xticks([])  # Remove x-axis ticks
progress_ax.set_yticks([])  # Remove y-axis ticks

# Create the progress bar rectangle
progress_rect = plt.Rectangle((0, 0), 0, 1, facecolor='purple')
progress_ax.add_patch(progress_rect)

# Animation update function
def update(frame):
    current_time = unique_times[frame]
    current_df = df[df['Ob Time'] == current_time]
    sc_live = ax.scatter(current_df['Right Ascension'], current_df['Declination'], c='yellow', marker='.', s=250,
                         edgecolor='black', alpha=1)

    # Get the object ID for the current frame
    obj_id = current_df['Object Id'].iloc[0]

    # Set the title to the object ID
    ax.set_title(f'Object {obj_id} Animation')

    # Update the time text
    time_text.set_text(f'Ob Time: {pd.to_datetime(current_time, unit="s")}')

    # Update the progress bar
    progress_rect.set_width((frame + 1) / len(unique_times))

    return sc, sc_live, time_text, progress_rect

# Get the unique time values and sort them
unique_times = np.sort(df['Ob Time'].unique())

# Create the animation
ani = FuncAnimation(fig, update, frames=len(unique_times), interval=2, blit=True)

# Save the animation as a GIF
# ani.save('colored_ra_dec.gif', writer='imagemagick', fps=10, dpi=80)

# Show the plot
plt.show()
