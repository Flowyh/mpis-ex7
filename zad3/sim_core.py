import numpy as np
from json import dump
from tqdm import tqdm
from datetime import datetime
import os
from multiprocessing import Process, cpu_count
from time import time

class Simulation:
  def __init__(self, n_beg: int, n_end: int, k: int, step: int, save_dir: str):
    self.n_beg = n_beg
    self.n_end = n_end
    self.k = k
    self.step = step
    self.tests_results = dict.fromkeys(['cmp', 's', 'time'], -1)
    for i in self.tests_results:
        self.tests_results[i] = { (n * self.step):[-1] * self.k for n in range(self.n_beg, self.n_end + 1) }
    self.save_dir = save_dir
    self.gen = np.random.default_rng()
    self.batch = []

  def run_sim(self):
    for nth in tqdm(range(self.n_beg, self.n_end + 1), ncols=140, desc=f'Task 1 N=[{self.n_beg * self.step}, {self.n_end * self.step}] K={self.k} Step={self.step}'):
      n = nth * self.step
      self.batch = [self.gen.permutation(n) for i in range(self.k)]
      for kth in range(self.k):
        current_array = self.batch[kth]
        compare = 0
        swaps = 0
        start_time = time()
        for j in range(1, n):
          key = current_array[j]
          i = j - 1
          while i > 0 and current_array[i] > key:
            compare = compare + 1
            current_array[i + 1] = current_array[i]
            swaps = swaps + 1
            i = i - 1
          current_array[i + 1] = key
          swaps = swaps + 1
        end_time = time()
        self.tests_results['time'][n][kth] = end_time - start_time
        self.tests_results['cmp'][n][kth] = compare
        self.tests_results['s'][n][kth] = swaps

    now = datetime.now()
    if not os.path.exists(f'./results/{self.save_dir}'):
      os.makedirs(f'./results/{self.save_dir}')
    dump(self.tests_results, open(f'./results/{self.save_dir}/k{self.k}_{self.n_beg}-{self.n_end}_{now}.json', 'w'))

def run(n_beg: int, n_end: int, step: int, k: int, count: int = cpu_count()):
  now = datetime.now()
  dt_str = now.strftime("%d-%m-%Y_%H:%M:%S")
  processess = []
  for i in range(count):
    sim = Simulation(n_beg=n_beg, n_end=n_end, step=step, k=k, save_dir=dt_str)
    p = Process(target=sim.run_sim)
    processess.append(p)
    p.start()