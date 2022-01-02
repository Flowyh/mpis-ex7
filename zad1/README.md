## Run with:
```
python3 setup.py build_ext --inplace
python3 test.py
```
## Configuration:
In [test.py](test.py) you can change the variables of the simulation.
In my [implementation](sim_core.py) of task 1 I've defined current number of urns as 
$n * step$, where $step$ is the difference of number of urns between each nth iteration.
To change what iterations you want to calculate, you have to change either/both **n_beg** or/and **n_end**, which indicate the start and end index of the simulation loop.
To change the difference between number of urns between each nth iteration change **step** variable.
**K** is the amount of tests performed for every nth iteration.
**Count** is the amount of processess which will be run on your computer to execute this simulation (e.g: running 5 processes with k=10 will yield 5 different jsons of 10 tests for every n specified).

## Plot results with:
```
python3 plot.py [target_dir]
E.g: python3 plot.py results/31-12-2021_14\:35\:56/
```

## Example results and plots are in the results folder.
