import matplotlib.pyplot as plt
import numpy as np

# Data
formats = ['CSV', 'HTML', 'JSON', 'XML']
batch_scores = [70, 70, 80, 65]
individual_scores = [80, 80, 80, 80]

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Set the width of bars and positions
x = np.arange(len(formats))
width = 0.35

# Create bars
bars1 = ax.bar(x - width/2, batch_scores, width, label='Batch Mode',
               color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, individual_scores, width, label='Individual Mode',
               color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

# Customization
ax.set_xlabel('Data Format', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
ax.set_title('LLM Benchmark: Batch vs Individual Mode Performance\nGemini 3.1 Pro Extended - 20 Questions',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(formats, fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
ax.legend(fontsize=12, loc='upper left', framealpha=0.9)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add horizontal line at 80% to show convergence
ax.axhline(y=80, color='red', linestyle='--', linewidth=2, alpha=0.5, label='80% Convergence Line')
ax.text(len(formats)-0.5, 82, '80% Convergence', fontsize=11, color='red',
        fontweight='bold', ha='right')

# Add improvement annotations
improvements = ['+10%', '+10%', '0%', '+15%']
for i, imp in enumerate(improvements):
    color = 'green' if '+' in imp and imp != '0%' else 'gray'
    ax.text(i, max(batch_scores[i], individual_scores[i]) + 3, imp,
            ha='center', fontsize=11, fontweight='bold', color=color)

# Tight layout
plt.tight_layout()

# Save the figure
plt.savefig('/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 2/benchmark_comparison_graph.png',
            dpi=300, bbox_inches='tight')
print("✅ Graph saved: benchmark_comparison_graph.png")

# Show the plot
plt.show()
