import sys
import matplotlib.pyplot as plt

args = sys.argv[1:]
print(f"Hello from python: {args}")

fig, ax = plt.subplots()

ax.plot([1, 2, 3], [1, 2, 3])

ax.set(title=f"{args}")
plt.show()

sys.stdout.flush()