from pogger import Pogger
import numpy as np

pogger = Pogger()
test = np.arange(0, 10)
pogger.write_array("arange", test, "T")
