import sys
from time import time, sleep
from src.Simulator import Simulator


def simulate():
  if len(sys.argv) != 2:
    print(f"Must specify step amount: python {sys.argv[0]} <steps>")
    exit()
  if not sys.argv[1].isnumeric():
    print(f"Steps must be integers: python {sys.argv[0]} <steps>")
    exit()

  steps = int(sys.argv[1])
  sim = Simulator()
  for step in range(steps):
    start_time = time()
    sim.step()
    duration = time() - start_time
    # se ejecutará 1 paso por segundo como maximo
    if duration < 1:
      sleep(1 - duration)
    print(f"Iteration: {step}", flush=True)

if __name__ == '__main__':
  simulate()