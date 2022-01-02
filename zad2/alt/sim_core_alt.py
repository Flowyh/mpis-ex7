import numpy as np
from json import dump
from tqdm import tqdm
from datetime import datetime
import os
from multiprocessing import Process, cpu_count

class Simulation:
  def __init__(self, n_beg: int, n_end: int, k: int, d: int, step: int, save_dir: str):
    self.n_beg = n_beg
    self.n_end = n_end
    self.k = k
    self.d = d
    self.step = step
    self.urns = []
    self.tests_results = dict.fromkeys(['ln'], -1)
    self.gen = np.random.default_rng()
    for i in self.tests_results:
        self.tests_results[i] = { (n * self.step):[-1] * self.k for n in range(self.n_beg, self.n_end + 1) }
    self.save_dir = save_dir
    self.batch = []

  def run_sim(self):
    for nth in tqdm(range(self.n_beg, self.n_end + 1), ncols=140, desc=f'Task 1 N=[{self.n_beg * self.step}, {self.n_end * self.step}] K={self.k} Step={self.step} D={self.d}'):
      n = nth * self.step
      self.batch = self.gen.integers(low=n, size=(n * self.k * self.d))
      curr_beg = 0
      for kth in range(self.k):
        # New number generator
        # Create empty urns
        self.urns = np.array([0 for i in range(n)])
        balls = 0
        while(balls != n):
          # Pick an urn
          random_urns = self.batch[curr_beg:curr_beg + self.d]
          # Increment balls
          balls = balls + 1
          # Increment curr_beg
          curr_beg = curr_beg + self.d
          # Temp array of randomly picked indexes
          temp = [self.urns[index] for index in random_urns]
          # Find minimum urns in randomly picked urns
          if self.d == 1: 
            random_min = random_urns[0]
          if self.d == 2:
            random_min = random_urns[0] if temp[0] < temp[1] else random_urns[1]
          if self.d == 3:
            temp_1 = 0 if temp[0] < temp[1] else 1
            random_min = random_urns[temp_1] if self.urns[random_urns[temp_1]] < temp[2] else random_urns[2]
          # print(random_urns, temp, random_min)
          # Put ball into the random minimal urn
          self.urns[random_min] = self.urns[random_min] + 1
        # Ln
        self.tests_results['ln'][n][kth] = np.max(self.urns).item()
        self.urns = []
    now = datetime.now()
    if not os.path.exists(f'./results/{self.save_dir}'):
      os.makedirs(f'./results/{self.save_dir}')
    dump(self.tests_results, open(f'./results/{self.save_dir}/d{self.d}-{self.n_beg}-{self.n_end}_{now}.json', 'w'))

def run(n_beg: int, n_end: int, step: int, k: int, d: int, count: int = cpu_count()):
  now = datetime.now()
  dt_str = now.strftime("%d-%m-%Y_%H:%M:%S")
  processess = []
  for i in range(count):
    sim = Simulation(n_beg=n_beg, n_end=n_end, step=step, k=k, d=d, save_dir=dt_str)
    p = Process(target=sim.run_sim)
    processess.append(p)
    p.start()