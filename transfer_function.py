import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Define positions for the blocks
positions = {
    "Setpoint": (0.05, 0.7),
    "PID Controller": (0.2, 0.55),
    "Motor Transfer Function": (0.5, 0.55),
    "Feedback Loop": (0.8, 0.55),
    "Summation": (0.15, 0.7)  # Position of the summation point (Σ)
}

# Define block labels
blocks = {
    "Setpoint": "Setpoint (Desired RPM)",
    "PID Controller": "PID Controller\n(Kp, Ki, Kd)",
    "Motor Transfer Function": "RS-550 Motor Transfer Function",
    "Feedback Loop": "Feedback Loop\n(Current Motor Speed)"
}

# Draw blocks
for label, (x, y) in positions.items():
    if label != "Summation":  # Don't draw a rectangle for the summation point
        width, height = 0.25, 0.1
        ax.add_patch(patches.FancyBboxPatch(
            (x, y), width, height, boxstyle="round,pad=0.03",
            edgecolor="black", facecolor="lightgrey"
        ))
        ax.text(x + width / 2, y + height / 2, blocks[label],
                ha="center", va="center", fontsize=10)

# Function to draw arrows with better angles and segmentation
def draw_segmented_arrow(start, middle, end):
    arrow_1 = FancyArrowPatch(start, middle, arrowstyle='-|>', mutation_scale=15, lw=1.5, color='black')
    arrow_2 = FancyArrowPatch(middle, end, arrowstyle='-|>', mutation_scale=15, lw=1.5, color='black')
    ax.add_patch(arrow_1)
    ax.add_patch(arrow_2)

# Draw the summation point (Σ symbol)
summation_x, summation_y = positions["Summation"]
ax.add_patch(Circle((summation_x + 0.1, summation_y + 0.05), 0.025, color="black", fill=False))
ax.text(summation_x + 0.1, summation_y + 0.08, "+", ha="center", va="center", fontsize=14)

# Draw arrows with segmentation for better adjustment
draw_segmented_arrow((positions["Setpoint"][0] + 0.2, positions["Setpoint"][1] + 0.05),
                     (positions["Summation"][0] + 0.1, positions["Summation"][1] + 0.05),
                     (positions["PID Controller"][0] + 0.1, positions["PID Controller"][1] + 0.1))

# Arrows connecting PID controller to motor and feedback loop
draw_segmented_arrow((positions["PID Controller"][0] + 0.25, positions["PID Controller"][1] + 0.05),
                     (positions["Motor Transfer Function"][0], positions["Motor Transfer Function"][1] + 0.05),
                     (positions["Motor Transfer Function"][0] + 0.25, positions["Motor Transfer Function"][1] + 0.05))

# Feedback loop connection
draw_segmented_arrow((positions["Motor Transfer Function"][0] + 0.25, positions["Motor Transfer Function"][1] + 0.05),
                     (positions["Feedback Loop"][0], positions["Feedback Loop"][1] + 0.05),
                     (positions["Feedback Loop"][0] + 0.25, positions["Feedback Loop"][1] + 0.05))

# Arrow returning from feedback loop to the summation point
draw_segmented_arrow((positions["Feedback Loop"][0] + 0.1, positions["Feedback Loop"][1] + 0.05),
                     (positions["Summation"][0] + 0.1, positions["Summation"][1] + 0.05),
                     (positions["Summation"][0] + 0.1, positions["Summation"][1]))

# Title and display
ax.set_title("Block Diagram: RS-550 Motor with PID Control System", fontsize=14)
ax.axis('off')
plt.show()
