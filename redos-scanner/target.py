import re
import time


for n in range(100):
    start_time = time.time()
    re.match("(bb|b.)*a", "b" * n)
    print(n, time.time() - start_time)
