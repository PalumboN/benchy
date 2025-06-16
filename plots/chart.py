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
# vmsToPlot = ['Druid', 'SimpleDruid', 'DruidSTP', 'SimpleDruidSTP']
vmsToPlot = ['FullBlocks', 'CleanBlocks', 'CleanConstantBlocks']
vmsToPlot = ['CleanConstantBlocks']
# baseline = 'Stack'
baseline = 'FullBlocks'

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
  'CleanBlocks': 'Clean', 
  'CleanConstantBlocks': 'C&C',

  'FullBlockClosure': 'Full', 
  'CleanBlockClosure': 'Clean', 
  'ConstantBlockClosure': 'Const',
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
    if row == nrows:
      row -=1

def buildChart(plotter, data, column, benchName, **kwargs):
  if not 'hue' in kwargs.keys(): kwargs['hue'] = 'executor'
  plot = plotter(data[data['executor'].isin(vmsToPlot)], x='unit', y=column, ax=axs[row, col], **kwargs)
  title = sanitizeBenchName(benchName)

  plot.set(title=title, xlabel=None, ylabel=None)
  plot.title.set_size(10)
  plot.set_xticklabels(map(lambda x : executorNames[x.get_text()], plot.get_xticklabels()), rotation=30, fontdict=font)
  return plot


## PLOTS ##

def plotBoxes(data, column, benchName):
  boxplot = buildChart(getattr(sns, 'boxplot'), data, column, benchName, showfliers=False)
  # plot.set_yticks([1,3,5,7])
  boxplot.set_yticklabels(boxplot.get_yticklabels(), fontdict=font)
  boxplot.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
  # boxplot.yaxis.set_major_locator(MaxNLocator(integer=True))
  return boxplot

def plotBars(data, column, benchName):
  barplot = buildChart(getattr(sns, 'barplot'), data, column, benchName, hue="unit", legend=False)
  # barplot.set(ylim=(data[column].min() - 10, None))
  barplot.set(ylim=(None, data[column].max() + 10 ))
  barplot.set_yticklabels(barplot.get_yticklabels(), fontdict=font)
  for container in barplot.containers:
    barplot.bar_label(container, fontsize=5)
  return barplot


def boxplot_speedup_execution(df):
  log('boxplot_speedup_execution')
  for benchName, data in df.groupby('benchmark'):
    # Relative to baseline time
    base = data[data['executor'] == baseline]['value'].mean()
    data['speedup'] = data['value'].rdiv(base)
    plotBoxes(data, 'speedup', benchName)
    logLines(benchName, data, 'speedup')
    next()

def boxplot_speedup_compilation(df):
  log('boxplot_speedup_compilation')
  for benchName, data in df.groupby('benchmark'):
    # Relative to Druid time 
    data['time'] = data['value'].div(1000) # Remove extras '000' by Rebench
    druid = data[data['executor'] == 'Druid']['time'].mean()
    data['speedup'] = data['time'].rdiv(druid)
    plotBoxes(data, 'speedup', benchName)
    next()

def barplot_size(df):
  log('barplot_size')
  for benchName, data in df.groupby('benchmark'):
    data['size'] = data['value'].div(1000).div(1000) # MB
    plotBars(data, 'size', benchName)
    next()

def barplot_hits(df):
  log('barplot_hits')
  for benchName, data in df.groupby('benchmark'):
    data['hits'] = data['value'].div(1000) # KHits
    plotBars(data, 'hits', benchName)
    logLines(benchName, data, 'hits')
    next()


## LOGS ##
logs = []
def log(text): logs.append(text)
def logLines(benchName, df, column): 
  for executor, values in df.loc[(df['executor'] == 'CleanConstantBlocks')].groupby('unit'):
    log(' '.join([benchName, executor, str(values[column].mean())]))
def flushLogs(file):
  global logs
  with open(file, 'w') as f:
    for text in logs: f.write(text + '\n')
  logs = []

def save(name):
  plt.savefig('chart-' + name + '.pdf', format='pdf')
  flushLogs('chart-' + name + '.log')


## INICIALIZATION ##
closures = ['FullBlockClosure', 'CleanBlockClosure', 'ConstantBlockClosure']

def sanitizeDF(**kwargs):
  global df
  interestVMs = vmsToPlot + [baseline]
  df = df.loc[~df['benchmark'].str.contains("Network")]
  df = df.loc[(df['criterion'] == 'total')]
  df = df.loc[df['executor'].isin(interestVMs)]
  # df = df.loc[(df['benchmark'].str.contains("bench")) | (df['benchmark'].str.contains("SMark"))]

  if not 'by' in kwargs.keys(): kwargs['by'] = ['executor']
  df = df.sort_values(
    key=lambda col: col.map(lambda value: (interestVMs+closures).index(value)),
    **kwargs
  )
 
def initializeDF(path, **kwargs):
  global f, axs, row, col, df
  f, axs = plt.subplots(ncols=ncols, nrows=nrows, layout="compressed", figsize=(5, 7))
  row = 0
  col = 0
  df = pd.read_csv(path, sep='	', comment='#')
  sanitizeDF(**kwargs)
  return df


## SCRIPT ##

nrows = 7
ncols = 3

df = initializeDF('../data/executionHits_blockClosures.data', by='unit')
barplot_hits(df)
save('blockHits')

# df = initializeDF('../data/executionTime_Blocks.data')
# boxplot_speedup_execution(df)
# save('speedUp')

# Show 
# plt.show()
