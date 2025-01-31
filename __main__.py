from pogger import Pogger
import numpy as np
from matplotlib import pyplot as plt

pogger = Pogger(verbose=True)


@pogger.record(("arange", "string"), ("T", "bro"))
def test():
    test = np.arange(0, 10)
    plt.figure(label="lmao")
    plt.plot(-test)
    plt.draw()
    print("LMAOOOOO")
    return test, "hello"


pogger.set_context("hello")
test()
pogger.set_context("world")
test()
