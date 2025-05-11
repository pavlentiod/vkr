import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/summary.csv")

# Время vs RMSE
plt.scatter(df["rmse"], df["disparity/ncc"])
plt.xlabel("RMSE")
plt.ylabel("Время disparity (sec)")
plt.title("Сравнение методов")
plt.grid(True)
plt.show()
