import numpy as np
from json import dump
from tqdm import tqdm
from datetime import datetime
import os
from multiprocessing import Process, cpu_count

class Simulation:
  def __init__(self, n_beg: int, n_end: int, k: int, step: int, save_dir: str):
    self.n_beg = n_beg
    self.n_end = n_end
    self.k = k
    self.step = step
    self.urns = []
    self.cn_count = 0
    self.dn_count = 0
    self.flags = {
      'bn_flag': True,
      'dn_flag': True,
    } 
    self.tests_results = dict.fromkeys(['bn', 'un', 'ln', 'cn', 'dn', 'dn_cn'], -1)
    for i in self.tests_results:
        self.tests_results[i] = { (n * self.step):[-1] * self.k for n in range(self.n_beg, self.n_end + 1) }
    self.save_dir = save_dir
    self.gen = np.random.default_rng()
    self.batch = []

  def run_sim(self):
    for nth in tqdm(range(self.n_beg, self.n_end + 1), ncols=140, desc=f'Task 1 N=[{self.n_beg * self.step}, {self.n_end * self.step}] K={self.k} Step={self.step}'):
      n = nth * self.step
      self.batch = self.gen.integers(low=n, size=(n * self.k * 100))
      for kth in range(self.k):
        # Create empty urns
        self.urns = np.array([0 for i in range(n)])
        balls = 0
        while(self.flags['dn_flag']):
          # Pick an urn
          random_urn = self.batch[balls + n * kth * 100]
          # Bn
          if self.flags['bn_flag']:
            if self.urns[random_urn] != 0:
              if self.tests_results['bn'][n][kth] == -1:
                self.tests_results['bn'][n][kth] = balls
                self.flags['bn_flag'] = False
          # Dn        
          if self.dn_count == n:
            self.tests_results['dn'][n][kth] = balls
            self.flags['dn_flag'] = False
          # Cn
          if self.cn_count == n:
            if self.tests_results['cn'][n][kth] == -1:
              self.tests_results['cn'][n][kth] = balls
          # Ln/Un
          if balls == n:
            # Ln
            self.tests_results['ln'][n][kth] = np.max(self.urns).item()
            # Un
            zeros = len(self.urns) - np.count_nonzero(self.urns)
            self.tests_results['un'][n][kth] = zeros
          # Increment balls
          balls = balls + 1
          # Put ball into the urn
          self.urns[random_urn] = self.urns[random_urn] + 1
          if self.urns[random_urn] == 1:
            self.cn_count = self.cn_count + 1
          elif self.urns[random_urn] == 2:
            self.dn_count = self.dn_count + 1
      
        # Dn - Cn
        diff = balls - self.tests_results['cn'][n][kth]
        self.tests_results['dn_cn'][n][kth] = diff
        for flag in self.flags:
          self.flags[flag] = True
        self.urns = []
        self.cn_count = 0
        self.dn_count = 0
    now = datetime.now()
    if not os.path.exists(f'./results/{self.save_dir}'):
      os.makedirs(f'./results/{self.save_dir}')
    dump(self.tests_results, open(f'./results/{self.save_dir}/{self.n_beg}-{self.n_end}_{now}.json', 'w'))

def run(n_beg: int, n_end: int, step: int, k: int, count: int = cpu_count()):
  now = datetime.now()
  dt_str = now.strftime("%d-%m-%Y_%H:%M:%S")
  processess = []
  for i in range(count):
    sim = Simulation(n_beg=n_beg, n_end=n_end, step=step, k=k, save_dir=dt_str)
    p = Process(target=sim.run_sim)
    processess.append(p)
    p.start()