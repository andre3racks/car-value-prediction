import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# plot test and training performance over a given variable
def plot_2D(title, x_label, y_label, test, train, variable):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(variable, test, 'r')
    plt.plot(variable, train, 'g')
    plt.show()

# 3d plot
def plot_3D(title, x_label, y_label, z_label, xdata, ydata, zdata):
    fig = plt.figure()
    ax = Axes3D(fig) 
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
    plt.show()   