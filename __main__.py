from pogger import Pogger
import numpy as np
from matplotlib import pyplot as plt

pogger = Pogger(verbose=True)


@pogger.record(("arange", "string", "dictionary"), ("T", "bro", "string"))
def test():
    test = np.arange(0, 10)
    plt.figure(label="lmao")
    plt.plot(-test)
    plt.draw()
    print("LMAOOOOO")
    dictionary = {"hello": "world", "this is": "me"}
    return test, "hello", dictionary


pogger.set_context("hello")
test()
pogger.set_context("world")
test()
