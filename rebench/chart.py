
import seaborn as sns
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter


# Read data
df = pd.read_csv('../data/compileSize_Simple_2024-10-17.data', sep='	', comment='#')
# Filter data
# df = df.loc[(df['benchmark'].str.contains("bench")) | (df['benchmark'].str.contains("SMark"))]
# df = df.loc[~(df['benchmark'].str.contains("Kernel") | df['benchmark'].str.contains("File"))]
df = df.loc[~(df['criterion'] == 'MaxRSS')]

# Sort values
sorted_benches = [
'benchBinaryTrees',
'benchChameleons',
'benchChameneosRedux',
'SMarkDeltaBlue',
'benchFasta',
'benchKNucleotide',
'benchMandelbrot',
'benchMeteor',
'benchNBody',
'benchPiDigits',
'benchRegexDNA',
'benchReverseComplement',
'SMarkRichards',
'1+1',
'SMarkSlopstone',
'benchSpectralNorm',
'benchThreadRing',
'Kernel.*',
'File.*',
'Opal.* AST.*',
'Microdown.*',
'Network.* Zinc.* Zodiac.*'
]

(df
  # .sort_values(
  #   by="benchmark",
  #   key=lambda col: col.map(lambda value: sorted_benches.index(value))
  # )
  .sort_values(by=['executor'], inplace=True)
)

# Chart layout
nrows = 6
f, axs = plt.subplots(ncols=4, nrows=nrows, layout="compressed", figsize=(5, 7))
row = 0
col = 0

titles = {
  "1+1": "Startup",
  'Opal.* AST.*': "Compiler",
  'Microdown.*': "Microdown",
  'Network.* Zinc.* Zodiac.*': "Network",
  'ReverseComplement': 'ReverseComp'
}

executors = {
  # 'Druid': 'Druid JIT',
  # 'Stack': 'Interpreter',
  'Druid': 'Druid',
  'Stock': 'Manual',
  'Mirror': 'Mirror',
  'Simple': 'Simple',
  'SimpleDruid': 'SimpleDruid',

  'FullBlocks': 'Full', 
  'ConstantBlocks': 'Const', 
  'CleanConstantBlocks': 'C&C'
}

# Plot each chart
for benchName, y in df.groupby('benchmark'):
  # Relative
  full = y[y['executor'] == 'Druid']['value'].mean()
  y['speedup'] = y['value'].div(full)

  # y['time'] = y['value'].div(1000)
  # druid = y[y['executor'] == 'Druid']['time'].mean()
  # y['speedup'] = y['time'].rdiv(druid)

  # What to plot?
  # vmsToPlot = ['FullBlocks', 'ConstantBlocks', 'CleanConstantBlocks']
  vmsToPlot = ['Druid', 'SimpleDruid']

  # Get a good name  
  name = benchName.replace('bench', '').replace('SMark', '')
  name = titles[name] if name in titles else name

  # Plot sub-chart
  boxplot = sns.boxplot(y[y['executor'].isin(vmsToPlot)], x='executor', y='speedup', ax=axs[row, col], hue="executor")
  boxplot.set(title=name, xlabel=None, ylabel=None)
  boxplot.title.set_size(10)
  boxplot.set_xticklabels(map(lambda x : executors[x.get_text()], boxplot.get_xticklabels()), rotation=30, fontdict={"fontsize": 8})
  boxplot.set_yticklabels(boxplot.get_yticklabels(), fontdict={"fontsize": 8})
  boxplot.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
  # boxplot.yaxis.set_major_locator(MaxNLocator(integer=True))
  # boxplot.set_yticks([1,3,5,7])

  # Iterate
  col += 1
  if col == 4:
    row +=1
    col = 0

# Show
# plt.show()
plt.savefig('chart.pdf')