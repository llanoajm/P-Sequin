from NSGA import *

nsga = NSGA(["AACTGT", "GGTA"])
result = nsga.run(4)
for s in result:
    print(s)

