import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Define positions for the blocks with increased spacing and better alignment
positions = {
    "User Interface": (0.05, 0.75),
    "Raspberry Pi": (0.2, 0.55),
    "Motor Drivers": (0.48, 0.55),
    "RS-550 Motors": (0.76, 0.55),
    "Sensors": (0.2, 0.3),
    "Power Supply": (0.05, 0.1),
    "Summation": (0.25, 0.435)  # Position of the summation point (Σ)
}

# Define block labels
blocks = {
    "User Interface": "User Interface\n(Touchscreen)\n(RPM, Time, Temp, pH)",
    "Raspberry Pi": "Raspberry Pi\n(Control Unit)",
    "Motor Drivers": "BTS7960 Motor Drivers",
    "RS-550 Motors": "RS-550 Motors",
    "Sensors": "Sensors\n(DHT22, pH Sensors)",
    "Power Supply": "Power Supply"
}

# Draw blocks with better padding
for label, (x, y) in positions.items():
    if label != "Summation":  # Don't draw a rectangle for the summation point
        width, height = 0.2, 0.1
        ax.add_patch(patches.FancyBboxPatch(
            (x, y), width, height, boxstyle="round,pad=0.03",
            edgecolor="black", facecolor="lightgrey"
        ))
        ax.text(x + width / 2, y + height / 2, blocks[label],
                ha="center", va="center", fontsize=10)

# Function to draw straight arrows with manual segments
def draw_straight_arrow(start, via, end):
    # Draw arrow from start to via, and then from via to end
    arrow1 = FancyArrowPatch(
        start, via, arrowstyle='-', mutation_scale=15, lw=1.5, color='black'
    )
    arrow2 = FancyArrowPatch(
        via, end, arrowstyle='->', mutation_scale=15, lw=1.5, color='black'
    )
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)

# Draw the summation point (Σ symbol)
summation_x, summation_y = positions["Summation"]
ax.add_patch(Circle((summation_x + 0.1, summation_y + 0.05), 0.025, color="black", fill=False))

# Define the manual arrows as segments with control points
arrows_segments = [
    ((0.15, 0.75), (0.15, 0.65), (0.2, 0.65)),  # User Interface -> Raspberry Pi
    ((0.35, 0.55), (0.45, 0.55), (0.5, 0.55)),  # Raspberry Pi -> Motor Drivers
    ((0.65, 0.55), (0.65, 0.55), (0.7, 0.55)),  # Motor Drivers -> RS-550 Motors
    ((0.2, 0.1), (0.25, 0.2), (0.2, 0.55)),  # Power Supply -> Raspberry Pi
    ((0.2, 0.1), (0.35, 0.4), (0.5, 0.55)),  # Power Supply -> Motor Drivers
    ((0.2, 0.1), (0.55, 0.4), (0.7, 0.55)),  # Power Supply -> RS-550 Motors
    ((0.2, 0.3), (0.25, 0.4), (0.25, 0.485)),  # Sensors -> Summation
    ((0.7, 0.55), (0.65, 0.45), (0.25, 0.485))  # RS-550 Motors -> Summation
]

# Draw each segmented arrow
for start, via, end in arrows_segments:
    draw_straight_arrow(start, via, end)

# Function to adjust the feedback loop from summation to Raspberry Pi
def feedback_to_raspberry_pi():
    summation_pos = (summation_x + 0.1, summation_y + 0.05)
    raspberry_pos = (positions["Raspberry Pi"][0] + 0.1, positions["Raspberry Pi"][1] + 0.1)
    
    feedback_arrow = FancyArrowPatch(
        summation_pos, raspberry_pos, arrowstyle='->', mutation_scale=15, lw=1.5, color='black'
    )
    ax.add_patch(feedback_arrow)

# Draw the feedback loop to Raspberry Pi
feedback_to_raspberry_pi()

# Title and display
ax.set_title("Block Diagram: Magnetic Stirrer System with Feedback", fontsize=14)
ax.axis('off')
plt.show()
