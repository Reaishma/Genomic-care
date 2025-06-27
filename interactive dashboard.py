import allel
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Simulate genotype data
np.random.seed(0)  # For reproducibility
genotypes = np.random.randint(0, 2, size=(10, 20, 2))

# Convert genotypes to allel format
genotypes_allel = allel.GenotypeArray(genotypes)

# Calculate allele frequencies
allele_freqs = genotypes_allel.count_alleles().to_frequencies()

# Create a figure with multiple subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=['Allele Frequencies', 'Allele Frequencies Heatmap', 'Mean Allele Frequencies', 'Allele Frequencies Dot Map'], specs=[[{"type": "bar"}, {"type": "heatmap"}], [{"type": "domain"}, {"type": "xy"}]])

# Bar plot
fig.add_trace(go.Bar(x=list(range(10)), y=allele_freqs[:, 0], name='Allele 0'), row=1, col=1)
fig.add_trace(go.Bar(x=list(range(10)), y=allele_freqs[:, 1], name='Allele 1'), row=1, col=1)

# Heatmap
import pandas as pd
df = pd.DataFrame(allele_freqs.T, columns=list(range(10)))
fig.add_trace(go.Heatmap(z=df.values, x=df.columns, y=['Allele 0', 'Allele 1'], colorscale='Blues'), row=1, col=2)

# Pie chart
fig.add_trace(go.Pie(labels=['Allele 0', 'Allele 1'], values=[np.mean(allele_freqs[:, 0]), np.mean(allele_freqs[:, 1])]), row=2, col=1)

# Scatter plot (dot map)
fig.add_trace(go.Scatter(x=list(range(10)), y=allele_freqs[:, 0], mode='markers', name='Allele 0'), row=2, col=2)
fig.add_trace(go.Scatter(x=list(range(10)), y=allele_freqs[:, 1], mode='markers', name='Allele 1'), row=2, col=2)

fig.update_layout(height=800, width=1000)
fig.show()
