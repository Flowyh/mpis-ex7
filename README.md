# Implementations of task 1, 2 and 3 from [here](https://cs.pwr.edu.pl/gotfryd/dyd/mps2021_22/ex/pbb_ex7_v2.pdf)

Author: Maciej Bazela Index: 261743

Each task was implemented in Python 3. 
I've used Cython to speed up execution time for each task.  
Therefore if you want to run this code and don't have cython installed, run a simple pip install:
```
pip3 install Cython
```

### Some questions I think you may ask me, and I don't want to answer them several times:
* ***Why do you use np.random.Generator instead of random.random()?***
It's simply faster, especially when you have to generate arrays of random integers.  
Both np.random and random.random use [Mersenne Twister sequence](https://en.wikipedia.org/wiki/Mersenne_Twister), so therefore this number generator is good enough for me.

* ***Why is your whole simulation logic in a single function?!***
Apparently, Python function calls are really expensive, and I mean **really** expensive. 
When I've first implemented task 1, I've written everything like it really should be: clean and neatly separated into different class methods, but apparently it made my simulation run **~25% slower**.
I was disgusted at first, but it really is a difference.
Then I've decided to use Cython to speed it up even more, so I don't know anymore if I had to put everything into one method or not ¯\\\_(ツ)_/¯.

* ***Why are the results in some tasks separated into different files?***
It was faster for me to run ~5 threads with given k, than run everything in one.

* ***Why did you put so much effort into speeding everything up?***
I don't know, I want my code to run fast.


### And as a humble reminder: 
Python is really slow, so I had to use some pretty weird hacks to lower the calculation time. 
I think it's the last time I've tried to use it to calculate such simulations, I guess.

![a humble reminder](https://cdn.discordapp.com/attachments/386257623952916480/926463212881346630/g7g5hf7dxm741.png)