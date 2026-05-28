import matplotlib.pyplot as plt
import numpy as np

# Create a figure with 2 subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# ===== LEFT PLOT: Batch vs Individual Comparison =====
formats = ['CSV', 'HTML', 'JSON', 'XML']
batch_scores = [70, 70, 80, 65]
individual_scores = [80, 80, 80, 80]

x = np.arange(len(formats))
width = 0.35

bars1 = ax1.bar(x - width/2, batch_scores, width, label='Batch Mode',
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x + width/2, individual_scores, width, label='Individual Mode',
                color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}%', ha='center', va='bottom',
                 fontsize=12, fontweight='bold')

# Add improvement arrows
improvements = [10, 10, 0, 15]
colors_arrow = ['green', 'green', 'gray', 'darkgreen']
for i, (imp, color) in enumerate(zip(improvements, colors_arrow)):
    if imp > 0:
        ax1.annotate('', xy=(i + width/2, individual_scores[i] - 2),
                     xytext=(i - width/2, batch_scores[i] + 2),
                     arrowprops=dict(arrowstyle='->', lw=2.5, color=color, alpha=0.7))
        ax1.text(i, (batch_scores[i] + individual_scores[i])/2,
                 f'+{imp}%', ha='center', fontsize=11,
                 fontweight='bold', color=color,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax1.set_xlabel('Data Format', fontsize=13, fontweight='bold')
ax1.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
ax1.set_title('Batch vs Individual Mode\nPerformance Comparison', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(formats, fontsize=12, fontweight='bold')
ax1.set_ylim(0, 100)
ax1.legend(fontsize=11, loc='upper left', framealpha=0.9)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.axhline(y=80, color='red', linestyle='--', linewidth=2, alpha=0.4)

# ===== RIGHT PLOT: Difficulty Breakdown for Individual Mode =====
medium_scores = [100, 100, 100, 100]
hard_scores = [100, 71.4, 71.4, 71.4]
extremely_hard_scores = [42.9, 71.4, 71.4, 71.4]

width2 = 0.25
bars3 = ax2.bar(x - width2, medium_scores, width2, label='Medium (6Q)',
                color='#27ae60', alpha=0.8, edgecolor='black', linewidth=1.5)
bars4 = ax2.bar(x, hard_scores, width2, label='Hard (7Q)',
                color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
bars5 = ax2.bar(x + width2, extremely_hard_scores, width2, label='Extremely Hard (7Q)',
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars3, bars4, bars5]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.0f}%', ha='center', va='bottom',
                 fontsize=10, fontweight='bold')

ax2.set_xlabel('Data Format', fontsize=13, fontweight='bold')
ax2.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
ax2.set_title('Individual Mode Performance\nby Difficulty Level', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(formats, fontsize=12, fontweight='bold')
ax2.set_ylim(0, 110)
ax2.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add main title
fig.suptitle('Sprint 2: LLM Benchmark Results - Gemini 3.1 Pro Extended\nAll Formats Converge to 80% in Individual Mode',
             fontsize=17, fontweight='bold', y=0.98)

# Tight layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the figure
plt.savefig('/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 2/comprehensive_benchmark_analysis.png',
            dpi=300, bbox_inches='tight')
print("✅ Comprehensive graph saved: comprehensive_benchmark_analysis.png")

# Show the plot
plt.show()
