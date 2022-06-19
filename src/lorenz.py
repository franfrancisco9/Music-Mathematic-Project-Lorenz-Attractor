import numpy as np
import matplotlib.pyplot as plt
from creating_lorenz import Lorenz

newfig = plt.figure()
xpoints, zpoints, initial = Lorenz(start = 0, end= 30, step_count = 30000, initial = np.array([1.0,1.0,1.0]))
plt.plot(xpoints, zpoints, label= "(x,y,z) = (1, 1, 1)")
xpoints, zpoints, initial = Lorenz(start = 0, end= 30, step_count = 30000, initial = np.array([0.995,1.0,1.0]))
plt.plot(xpoints, zpoints, 'r', label = "(x,y,z) = (0.95, 1, 1)")
plt.title("Sobreposição de dois modelos de Lorenz")
plt.grid()
#plt.show()
plt.savefig("../images/sobreposicao_de_dois_modelos_de_lorenz.png")