import clean_sample_data
import sys
sys.path.append('../')
from data.data_loader import get_splits
from utils.plot import plot_2D
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import cross_val_score

def random_forest(X_train, X_test, y_train, y_test, criteria, num_trees):
    accuracies = []
    train_accuracies = []

    forest = RandomForestRegressor(criterion="mse", n_estimators=num_trees)
    forest.fit(X_train, y_train)
    y_pred = forest.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    '''
    y_pred = forest.predict(X_test)
    y_train_pred = forest.predict(X_train)
    accuracies.append(metrics.score(y_test, y_pred))
    train_accuracies.append(metrics.score(y_train, y_train_pred))


    plt.title("Test and training accuracies")
    plt.xlabel("Number of nodes split with " + "entropy index")
    plt.ylabel("Test accuracy (red) and train (green)")
    plt.plot(accuracies, 'r')
    plt.plot(train_accuracies, 'g')
    plt.savefig('RFAccuracies.png')
    '''

    return

# debug purposes
if __name__ == "__main__":
    data = get_splits("../data/encoded_data/full_encoded.csv", 0.2)
    X_train = data['X_train']
    X_test = data['X_test']
    Y_train = data['Y_train']
    Y_test = data['Y_test']
    if data is not None:
        print("Success")
    #print(X_train[0:20])

    random_forest(X_train[0:20], X_test[0:20], Y_train[0:20], Y_test[0:20], 'entropy', 10000)
    pass