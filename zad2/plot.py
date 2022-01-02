from types import FunctionType
import matplotlib.pyplot as plt
import os
from json import loads
import numpy as np
from sys import argv

def wrap_jsons(target: str):
  result = {}
  for filename in os.listdir(target):
    path = os.path.join(target, filename)
    if os.path.isfile(path):
      with open(path, "r") as file:
        current = loads(file.read())
        d = filename[0:2]
        result[d] = current['ln']
  return result

def make_axes(res: dict, func_key: str):
  x_axis = []
  y_axis = []
  for n in res[func_key]:
    x_axis.append(int(n))
    y_axis.append(res[func_key][n])
  return [x_axis, y_axis]

def avg_y_axis(y_axis: list):
  return np.average(y_axis, axis=1)

def scatter_avg_plot(data: list, axes, title: str):
  axes.set(title=title)
  axes.set_xlabel("Number of urns")
  #axes.set_yscale('log')
  #axes.set_xscale('log')
  avg_mode = 'ro'

  # Scatter all data
  scatter_x = []
  for i, x in enumerate(data[0]):
    for j in range(len(data[1][i])):
      scatter_x.append(x)
  axes.scatter(scatter_x, data[1], c='gold', label='All data', s=3)

  # Plot average data
  axes.plot(data[0], avg_y_axis(data[1]), avg_mode, label='Data average', ms=4)
  axes.legend()
  return axes

def setup_plot(axes):
  #print("placeholder")
  axes.xaxis.set_major_locator(plt.MaxNLocator(12))
  axes.set_xlim(xmin=0, xmax=1010000)
  axes.ticklabel_format(axis='y', useOffset=False, style='plain')

if __name__ == '__main__':
  if len(argv) != 2:
    print("Usage python plot.py [target_dir]")
    exit(1)
  target_dir = argv[1]
  wrapped_results = wrap_jsons(target=target_dir)
  funcs_keys = wrapped_results.keys()
  funcs = {}
  for key in funcs_keys:
    funcs[key] = make_axes(wrapped_results, key)

  if not os.path.exists(f'{target_dir}/plots'):
      os.makedirs(f'{target_dir}/plots')

  save_dir = f'{target_dir}/plots'

  # Plotting:

  # First 6 plots:
  funcs_titles = {
    'ln': 'Ln - max number of balls after inserting n balls (maximum load)',
  }

  fig, ax = plt.subplots(3, 1, figsize=(10, 9))

  for i, key in enumerate(['d1', 'd2', 'd3']):
    scatter_avg_plot(funcs[key], ax[i], f'Ln (d={key[1]}) - max number of balls after inserting n balls (maximum load)')
    setup_plot(ax[i])
  
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task2.png')

  # # Lns
  # fig, ax = plt.subplots(3, 1, figsize=(10, 9))
  # mapped_avg_plot(data=funcs['ln'], axes=ax[0], title=funcs_titles['ln'], func=lambda x, y: y / np.log(x), func_label='Ln/ln(n)')
  # setup_plot(ax[0])
  # mapped_avg_plot(data=funcs['ln'], axes=ax[1], title=funcs_titles['ln'], func=lambda x, y: y / (np.log(x) / np.log(np.log(x))), func_label='Ln/ln(n)/ln(ln(n))')  
  # setup_plot(ax[1])
  # mapped_avg_plot(data=funcs['ln'], axes=ax[2], title=funcs_titles['ln'], func=lambda x,y : y / np.sqrt(x), func_label='Ln/sqrt(n)')
  # setup_plot(ax[2])
  # fig.tight_layout()
  # fig.show()
  # fig.savefig(f'{save_dir}/task1-lns.png')


  

