import seaborn as sns
import numpy as np
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter

# Configure Matplotlib for scalable fonts
matplotlib.rcParams['pdf.fonttype'] = 42  # Use TrueType fonts

# What to plot?
vmsToPlot = ['Druid', 'SimpleDruid', 'DruidSTP', 'SimpleDruidSTP']
# vmsToPlot = ['FullBlocks', 'ConstantBlocks', 'CleanConstantBlocks']

# Sort benches
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
'Opal.*|AST.*',
'Microdown.*',
'Network.*|Zinc.*|Zodiac.*'
]



# Translations
benchNames = {
  "1+1": "Startup",
  'Opal': "Compiler",
  'ReverseComplement': 'ReverseComp'
}

def sanitizeBenchName(benchName):
  name = benchName.replace('bench', '').replace('SMark', '')
  name = name.split(".")[0]
  name = benchNames[name] if name in benchNames else name
  return name

# Translations
executorNames = {
  # 'Druid': 'Druid JIT',
  # 'Stack': 'Interpreter',
  'Stock': 'Manual',
  'Mirror': 'Mirror',
  'Simple': 'Simple',
  'Druid': 'D',
  'SimpleDruid': 'SD',
  'DruidSTP': 'DSTP',
  'SimpleDruidSTP': 'SDSTP',

  'FullBlocks': 'Full', 
  'ConstantBlocks': 'Const', 
  'CleanConstantBlocks': 'C&C'
}

font = { "fontsize": 8 }

## CHARTS ##

def next():
  global row
  global col
  col += 1
  if col == ncols:
    row +=1
    col = 0

def buildChart(plotter, data, column, benchName):
  plot = plotter(data[data['executor'].isin(vmsToPlot)], x='executor', y=column, ax=axs[row, col], hue="executor")
  title = sanitizeBenchName(benchName)

  plot.set(title=title, xlabel=None, ylabel=None)
  plot.title.set_size(10)
  plot.set_xticklabels(map(lambda x : executorNames[x.get_text()], plot.get_xticklabels()), rotation=30, fontdict=font)
  return plot


## PLOTS ##

def plotBoxes(data, column, benchName):
  boxplot = buildChart(getattr(sns, 'boxplot'), data, column, benchName)
  # plot.set_yticks([1,3,5,7])
  boxplot.set_yticklabels(boxplot.get_yticklabels(), fontdict=font)
  boxplot.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
  # boxplot.yaxis.set_major_locator(MaxNLocator(integer=True))
  return boxplot

def plotBars(data, column, benchName):
  barplot = buildChart(getattr(sns, 'barplot'), data, column, benchName)
  barplot.set(ylim=(data[column].min() - 10, None))
  barplot.set_yticklabels(barplot.get_yticklabels(), fontdict=font)
  return barplot


def boxplot_speedup_execution(df):
  for benchName, data in df.groupby('benchmark'):
    # Relative to Stack time
    stack = data[data['executor'] == 'Stack']['value'].mean()
    data['speedup'] = data['value'].rdiv(stack)
    plotBoxes(data, 'speedup', benchName)
    next()

def boxplot_speedup_compilation(df):
  for benchName, data in df.groupby('benchmark'):
    # Relative to Druid time 
    data['time'] = data['value'].div(1000) # Remove extras '000' by Rebench
    druid = data[data['executor'] == 'Druid']['time'].mean()
    data['speedup'] = data['time'].rdiv(druid)
    plotBoxes(data, 'speedup', benchName)
    next()

def barplot_size(df):
  for benchName, data in df.groupby('benchmark'):
    data['size'] = data['value'].div(1000).div(1000) # MB
    plotBars(data, 'size', benchName)
    next()


## INICIALIZATION ##

def sanitizeDF():
  global df
  interestVMs = vmsToPlot + ['Stack']
  df = df.loc[~df['benchmark'].str.contains("Network")]
  df = df.loc[~(df['criterion'] == 'MaxRSS')]
  df = df.loc[df['executor'].isin(interestVMs)]
  # df = df.loc[(df['benchmark'].str.contains("bench")) | (df['benchmark'].str.contains("SMark"))]

  # df.sort_values(by=['executor'], inplace=True)
  df = df.sort_values(
    by="executor",
    key=lambda col: col.map(lambda value: interestVMs.index(value))
  )
 
def initializeDF(path):
  global f, axs, row, col, df
  f, axs = plt.subplots(ncols=ncols, nrows=nrows, layout="compressed", figsize=(5, 7))
  row = 0
  col = 0
  df = pd.read_csv(path, sep='	', comment='#')
  sanitizeDF()
  return df


## SCRIPT ##

nrows = 6
ncols = 4

df = initializeDF('../data/new_posta/executionTime_simple.data')
boxplot_speedup_execution(df)
plt.savefig('chart-box.pdf', format='pdf')

df = initializeDF('../data/new_posta/compileSize_simple.data')
barplot_size(df)
plt.savefig('chart-bar.pdf', format='pdf')

# Show 
# plt.show()
