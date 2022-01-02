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
        if not result:
          result = current
        else:
          for res in result:
            for key in result[res]:
              result[res][key] = result[res][key] + current[res][key]
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

def map_y_axis(f, x_axis: list, y_axis: list):
  result = []
  for i, x in enumerate(x_axis):
    result.append(f(x, y_axis[i]))
  return result

def scatter_avg_plot(data: list, axes, title: str):
  axes.set(title=title)
  axes.set_xlabel("Number of urns")
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
  axes.set_xlabel("Number of urns")
  avg_mode = 'ro-' 
  avgs = avg_y_axis(data[1])
  mapped_avgs = list(map_y_axis(func, x_axis=data[0], y_axis=avgs))

  # Plot average data
  axes.plot(data[0], mapped_avgs, avg_mode, label=func_label, ms=4)
  return axes

def setup_plot(axes):
  axes.xaxis.set_major_locator(plt.MaxNLocator(12))
  axes.yaxis.set_major_locator(plt.MaxNLocator(8))
  axes.set_xlim(xmin=0, xmax=101000)
  axes.set_xticks([1000, 11000, 21000, 31000, 41000, 51000, 61000, 71000, 81000, 91000, 100000])
  axes.ticklabel_format(useOffset=False, style='plain')
  axes.legend()

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
    'bn': 'Bn - first non-empty urn picked (birthday paradox)',
    'un': 'Un - number of empty urns after inserting n balls',
    'ln': 'Ln - max number of balls after inserting n balls (maximum load)',
    'cn': 'Cn - minimum of insertions for every urn to have at least one ball inside (coupon collector\'s problem)',
    'dn': 'Dn - minimum of insertions for every urn to have at least two balls inside (coupon collector\'s brother',
    'dn_cn': 'Dn - Cn - number of insertions between Cn and Dn'
  }
  fig, ax = plt.subplots(6, 1, figsize=(10, 20))

  for i, key in enumerate(funcs_keys):
    scatter_avg_plot(funcs[key], ax[i], funcs_titles[key])
    setup_plot(ax[i])
  
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-all.png')
  
  # Bns
  fig, ax = plt.subplots(2, 1, figsize=(10, 6))
  mapped_avg_plot(data=funcs['bn'], axes=ax[0], title=funcs_titles['bn'], func=lambda x, y: y / x, func_label='Bn/x')
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['bn'], axes=ax[1], title=funcs_titles['bn'], func=lambda x, y: y / np.sqrt(x), func_label='Bn/sqrt(x)')
  ax[1].set_ylim(0.0, 10)
  # Big-O test
  # down = [(x, 1/np.sqrt(x)) for x in range(100, 100000, 100)]
  # upper = [(x, 500/np.sqrt(x)) for x in range(100, 100000, 100)]
  # print(test[0])
  # for i in test:
  #   ax[1].scatter(i[0], i[1], color='b', label='2/sqrt(x)', s=2)
  # ax[1].plot(*zip(*upper), color='g', label='500/sqrt(x)', ms=2)
  # ax[1].plot(*zip(*down), color='b', label='1/sqrt(x)', ms=2)

  setup_plot(ax[1])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-bns.png')

  # Uns
  fig, ax = plt.subplots(1, 1, figsize=(10, 3))
  mapped_avg_plot(data=funcs['un'], axes=ax, title=funcs_titles['un'], func=lambda x, y: y / x, func_label='Un/n')
  ax.set_ylim(0.0, 0.8)
  setup_plot(ax)
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-uns.png')

  # Lns
  fig, ax = plt.subplots(3, 1, figsize=(10, 9))
  mapped_avg_plot(data=funcs['ln'], axes=ax[0], title=funcs_titles['ln'], func=lambda x, y: y / np.log(x), func_label='Ln/ln(n)')
  ax[0].set_ylim(0.4, 1)  
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['ln'], axes=ax[1], title=funcs_titles['ln'], func=lambda x, y: y / (np.log(x) / np.log(np.log(x))), func_label='Ln/ln(n)/ln(ln(n))')  
  ax[1].set_ylim(1.2, 2.5)  
  setup_plot(ax[1])
  mapped_avg_plot(data=funcs['ln'], axes=ax[2], title=funcs_titles['ln'], func=lambda x,y : y / np.log(np.log(x)), func_label='Ln/ln(ln(n))')
  ax[2].set_ylim(2, 5)  
  setup_plot(ax[2])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-lns.png')

  # Cns
  fig, ax = plt.subplots(3, 1, figsize=(10, 9))
  mapped_avg_plot(data=funcs['cn'], axes=ax[0], title=funcs_titles['cn'], func=lambda x, y: y / x, func_label='Cn/n')
  ax[0].set_ylim(7, 16) 
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['cn'], axes=ax[1], title=funcs_titles['cn'], func=lambda x, y: y / (x * np.log(x)), func_label='Cn/nln(n)')  
  ax[1].set_ylim(0.5, 2)   
  setup_plot(ax[1])
  mapped_avg_plot(data=funcs['cn'], axes=ax[2], title=funcs_titles['cn'], func=lambda x,y : y / (x * x), func_label='Cn/n^2')
  setup_plot(ax[2])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-cns.png')

  # Dns
  fig, ax = plt.subplots(3, 1, figsize=(10, 9))
  mapped_avg_plot(data=funcs['dn'], axes=ax[0], title=funcs_titles['dn'], func=lambda x, y: y / x, func_label='Dn/n')
  ax[0].set_ylim(9, 17) 
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['dn'], axes=ax[1], title=funcs_titles['dn'], func=lambda x, y: y / (x * np.log(x)), func_label='Dn/nln(n)')  
  ax[1].set_ylim(1, 2)   
  setup_plot(ax[1])
  mapped_avg_plot(data=funcs['dn'], axes=ax[2], title=funcs_titles['dn'], func=lambda x,y : y / (x * x), func_label='Dn/n^2')
  setup_plot(ax[2])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-dns.png')

  # Dn-Cns
  fig, ax = plt.subplots(3, 1, figsize=(10, 9))
  mapped_avg_plot(data=funcs['dn_cn'], axes=ax[0], title=funcs_titles['dn_cn'], func=lambda x, y: y / x, func_label='(Dn-Cn)/n')
  ax[0].set_ylim(0.5, 6.5) 
  setup_plot(ax[0])
  mapped_avg_plot(data=funcs['dn_cn'], axes=ax[1], title=funcs_titles['dn_cn'], func=lambda x, y: y / (x * np.log(x)), func_label='(Dn-Cn)/nln(n)')  
  ax[1].set_ylim(0, 1) 
  setup_plot(ax[1])
  mapped_avg_plot(data=funcs['dn_cn'], axes=ax[2], title=funcs_titles['dn_cn'], func=lambda x,y : y / (x * np.log(np.log(x))), func_label='(Dn-Cn)/nln(ln(n))')
  ax[2].set_ylim(0, 2.5) 
  setup_plot(ax[2])
  fig.tight_layout()
  fig.show()
  fig.savefig(f'{save_dir}/task1-dn_cns.png')


  

