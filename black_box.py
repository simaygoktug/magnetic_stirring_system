import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Function to create a text box
def add_box(ax, text, xy, boxstyle="round,pad=0.3", text_size=10, box_width=0.4, box_height=0.1):
    ax.text(xy[0], xy[1], text, ha="center", va="center", size=text_size,
            bbox=dict(boxstyle=boxstyle, fc="lightgrey", ec="black"))

# Function to draw an arrow
def add_arrow(ax, start, end, text="", arrowprops=None):
    ax.annotate(text, xy=end, xytext=start, ha="center", va="center",
                arrowprops=arrowprops if arrowprops else dict(arrowstyle="->", lw=1.5))

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)

# Hide axes
ax.axis('off')

# Adding boxes with proper spacing around the center
add_box(ax, "User Input Parameters\n(RPM, Time, Temp, pH)", xy=(1, 5), box_width=0.6)
add_box(ax, "Electrical Power", xy=(1, 3.5), box_width=0.4)
add_box(ax, "Sensor Feedback\n(Temperature, pH)", xy=(1, 2), box_width=0.6)
add_box(ax, "Magnetic Stirrer System\n(Raspberry Pi)", xy=(5, 3), box_width=1.0, box_height=0.2, text_size=12)
add_box(ax, "Stirring Action\n(RS-550 DC Motors)", xy=(9, 5), box_width=0.5)
add_box(ax, "Controlled Temperature", xy=(9, 3.5), box_width=0.5)
add_box(ax, "Controlled pH", xy=(9, 2), box_width=0.5)

# Adding arrows with improved spacing to avoid overlap on the center box
add_arrow(ax, start=(2, 5), end=(4, 3.4), text="")  # User Input to System, slightly above
add_arrow(ax, start=(2, 3.5), end=(3.95, 3), text="")  # Electrical Power to System, middle
add_arrow(ax, start=(2, 2), end=(4, 2.6), text="")  # Sensor Feedback to System, slightly below

add_arrow(ax, start=(6, 3.4), end=(8, 5), text="")  # System to Stirring Action, slightly above
add_arrow(ax, start=(6.05, 3), end=(8, 3.5), text="")  # System to Controlled Temperature, middle
add_arrow(ax, start=(6, 2.6), end=(8, 2), text="")  # System to Controlled pH, slightly below

# Set title
plt.title("Black-Box Diagram: Magnetic Stirrer System", fontsize=14)

# Show diagram
plt.show()
