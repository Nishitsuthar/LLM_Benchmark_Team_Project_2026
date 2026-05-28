import matplotlib.pyplot as plt
import numpy as np

# Data for Individual Mode by Difficulty
formats = ['CSV', 'HTML', 'JSON', 'XML']
medium_scores = [100, 100, 100, 100]
hard_scores = [100, 71.4, 71.4, 71.4]
extremely_hard_scores = [42.9, 71.4, 71.4, 71.4]

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Set the width of bars and positions
x = np.arange(len(formats))
width = 0.25

# Create bars
bars1 = ax.bar(x - width, medium_scores, width, label='Medium (6 questions)',
               color='#27ae60', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x, hard_scores, width, label='Hard (7 questions)',
               color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
bars3 = ax.bar(x + width, extremely_hard_scores, width, label='Extremely Hard (7 questions)',
               color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Customization
ax.set_xlabel('Data Format', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
ax.set_title('Individual Mode Performance by Difficulty Level\nGemini 3.1 Pro Extended - All Formats Converge to 80% Overall',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(formats, fontsize=13, fontweight='bold')
ax.set_ylim(0, 110)
ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add annotation for CSV's perfect Hard score
ax.annotate('Perfect Score!\nCSV: 100% on Hard',
            xy=(0, 100), xytext=(0.5, 105),
            fontsize=10, fontweight='bold', color='darkgreen',
            ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

# Tight layout
plt.tight_layout()

# Save the figure
plt.savefig('/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 2/difficulty_breakdown_graph.png',
            dpi=300, bbox_inches='tight')
print("✅ Graph saved: difficulty_breakdown_graph.png")

# Show the plot
plt.show()
