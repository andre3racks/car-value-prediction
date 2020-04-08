import clean_sample_data
import sys
sys.path.append('../')
from data.data_loader import get_splits
from utils.plot import plot_2D
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from collections import Counter
import random

def plot_accuracies(number_trees, mse_test, mse_train, mae_test, mae_train):
    plt.title("Accuracies for the test and training sets")
    plt.plot(number_trees, mse_test, color='r', label='MSE Test')
    plt.plot(number_trees, mse_train, color='g', label='MSE Train')
    plt.plot(number_trees, mae_test, color='b', label='MAE Test')
    plt.plot(number_trees, mae_train, color='y', label='MAE Train')
    plt.legend()
    plt.savefig("mechanicalAccuracies.png")
    plt.clf()

def plot_MAE(number_trees, mse_test, mse_train, mae_test, mae_train):
    plt.title("Mean Absolute Error (MAE)")
    plt.plot(number_trees, mse_test, color='r', label='MSE Test')
    plt.plot(number_trees, mse_train, color='g', label='MSE Train')
    plt.plot(number_trees, mae_test, color='b', label='MAE Test')
    plt.plot(number_trees, mae_train, color='y', label='MAE Train')
    plt.legend()
    plt.savefig("mechanicalError.png")
    plt.clf()

def plot_values(pred, test):
    pred = [x * 4198286601 for x in pred]
    test = [x * 4198286601 for x in test]
    test = list(filter(lambda a: a > 10, test))
    plt.title("Predicted and actual values for the test dataset")
    plt.xlabel("Predicted price")
    plt.ylabel("Actual price")
    plt.yscale('log')
    plt.xscale('log')
    plt.scatter(test, pred, color='r', s=.4)
    plt.scatter(test, test, color='g', s=.1)
    plt.savefig("fullPrices.png")
    plt.clf()

def calc_accuracy(pred, test):
    acc_count = 0
    unacc_count = 0
    for index in range(len(pred)):
        accuracy = abs(pred[index] - test[index]) / test[index]
        if accuracy < .1:
            acc_count = acc_count + 1
        else:
            unacc_count = unacc_count + 1
    percent = acc_count/len(pred)
    return accuracy

def random_forest(X_train, X_test, y_train, y_test, criteria, num_trees):
    accuracies = []
    accuracies.append([])
    accuracies.append([])
    train_accuracies = []
    train_accuracies.append([])
    train_accuracies.append([])
    errors = []
    errors.append([])
    errors.append([])
    train_errors = []
    train_errors.append([])
    train_errors.append([])

    num_trees = [1, 2, 5, 7, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000, 25000, 50000, 75000, 100000]
    depth = 122
    samples_split, samples_leaf = 87, 87
    impurity_split = .08

    for num_tree in num_trees:
        forest = RandomForestRegressor(n_estimators=num_tree, criterion='mse', max_depth=depth, min_samples_split=samples_split, min_samples_leaf=samples_leaf, min_impurity_decrease=impurity_split)
        forest.fit(X_train, y_train)
        y_pred = forest.predict(X_test)
        y_pred_train = forest.predict(X_train)
        train_accuracies[0].append(calc_accuracy(y_pred_train.tolist(), y_train.tolist()))
        accuracies[0].append(calc_accuracy(y_pred.tolist(), y_test.tolist()))
        train_errors[0].append(metrics.mean_absolute_error(y_train, y_pred_train))
        errors[0].append(metrics.mean_absolute_error(y_test, y_pred))

        mae_forest = RandomForestRegressor(n_estimators=num_tree, criterion='mae',  max_depth=depth, min_samples_split=samples_split, min_samples_leaf=samples_leaf, min_impurity_decrease=impurity_split)
        forest.fit(X_train, y_train)
        y_pred = forest.predict(X_test)
        y_pred_train = forest.predict(X_train)
        train_accuracies[0].append(calc_accuracy(y_pred_train.tolist(), y_train.tolist()))
        accuracies[0].append(calc_accuracy(y_pred.tolist(), y_test.tolist()))
        train_errors[0].append(metrics.mean_absolute_error(y_train, y_pred_train))
        errors[0].append(metrics.mean_absolute_error(y_test, y_pred))

    plot_values(y_pred.tolist(), y_test.tolist())
    plot_accuracies(num_trees, test_accuracies[0], train_accuracies[0], test_accuracies[1], train_accuracies[1])
    plot_MAE(num_trees, errors[0], train_errors[0], errors[1], train_errors[1])
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

    random_forest(X_train, X_test, Y_train, Y_test, 'entropy', 10000)
    pass