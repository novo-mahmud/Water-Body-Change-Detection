import matplotlib.pyplot as plt
import pandas as pd

# Data from your analysis
years = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
area = [220.68, 191.76, 221.45, 262.39, 371.93, 167.01, 138.95, 89.58]

plt.figure(figsize=(10, 5))
plt.plot(years, area, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)

# Highlight the drop
plt.fill_between(years, area, color='lightblue', alpha=0.4)

plt.title('Water Surface Area Decline (1990-2025)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Area (Sq. Km)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(years, rotation=45)

# Save the graph
plt.tight_layout()
plt.savefig('Results/trend_graph.png', dpi=300)
print("Graph saved!")