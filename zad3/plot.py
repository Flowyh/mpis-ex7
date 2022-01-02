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
        result = current
  return result

def make_axes(res: dict, func_key: str):
  x_axis = []
  y_axis = []
  for n in res[func_key]:
    x_axis.append(n)
    y_axis.append(res[func_key][n])
  return [x_axis, y_axis]

def avg_y_axis(y_axis: list):
  return np.average(y_axis, axis=1)

def map_y_axis(f, x_axis: list, y_axis: list):
  result = []
  for i, x in enumerate(x_axis):
    result.append(f(int(x), int(y_axis[i])))
  return result

def tuple_all(data: list):
  tupled = []
  for x in data[0]:
    for y in data[1]:
      for val in [y]:
        tupled.append()

  return zip(*tupled)

def scatter_avg_plot(data: list, axes, title: str):
  axes.set(title=title)
  axes.set_xlabel('Size of array')
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

def mapped_avg_plot(data: list, axes, title: str, func, func_label: str):
  axes.set(title=title)
  axes.set_xlabel('Size of array')
  avg_mode = 'ro-' 
  avgs = avg_y_axis(data[1])
  mapped_avgs = list(map_y_axis(func, x_axis=data[0], y_axis=avgs))

  # Plot average data
  axes.plot(data[0], mapped_avgs, avg_mode, label=func_label, ms=4)
  axes.legend()
  return axes

def setup_plot(axes):
  axes.xaxis.set_major_locator(plt.MaxNLocator(20))
  axes.yaxis.set_major_locator(plt.MaxNLocator(10))
  axes.set_xlim(xmin=0)
  #axes.set_xticks([1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 100])
  axes.ticklabel_format(axis='y', useOffset=False, style='plain')

if __name__ == '__main__':
  if len(argv) != 3:
    print("Usage python plot.py [target_dir] [k]")
    exit(1)
  target_dir = argv[1]
  k = argv[2]
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
    'cmp': f'Cmp k={k} - Number of comparisons',
    's': f'S k={k} - Number of swaps',
    'time': f'Time elapsed k={k}'
  }

  fig, ax = plt.subplots(3, 1, figsize=(10, 9))

  for i, key in enumerate(funcs):
    if key == 'time':
      continue
    scatter_avg_plot(data=funcs[key], axes=ax[i], title=funcs_titles[key])
    ax[i].set_ylim(ymin=1)
    setup_plot(ax[i])

  scatter_avg_plot(data=funcs['time'], axes=ax[2], title=funcs_titles['time'])
  ax[2].xaxis.set_major_locator(plt.MaxNLocator(20))
  ax[2].yaxis.set_major_locator(plt.MaxNLocator(10))
  ax[2].set_xlim(xmin=0)
  ax[2].set_ylabel('Time in seconds (floating point)')
  ax[2].ticklabel_format(axis='y', useOffset=False, style='plain')
  
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task3-all.png')
  
  # Cmps
  fig, ax = plt.subplots(2, 1, figsize=(10, 6))
  mapped_avg_plot(data=funcs['cmp'], axes=ax[0], title=funcs_titles['cmp'], func=lambda x, y: y / x, func_label='Cmp/x')
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['cmp'], axes=ax[1], title=funcs_titles['cmp'], func=lambda x, y: y / (x * x), func_label='Cmp/x^2')
  ax[1].set_ylim(0, 0.8) 
  setup_plot(ax[1])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task3-cmp.png')

  # S
  fig, ax = plt.subplots(2, 1, figsize=(10, 6))
  mapped_avg_plot(data=funcs['s'], axes=ax[0], title=funcs_titles['s'], func=lambda x, y: y / x, func_label='S/x')
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['s'], axes=ax[1], title=funcs_titles['s'], func=lambda x, y: y / (x * x), func_label='S/x^2')
  ax[1].set_ylim(0, 0.8)   
  setup_plot(ax[1])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task3-s.png')


  

