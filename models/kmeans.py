from sklearn.cluster import KMeans
import clean_sample_data
import sys
sys.path.append('../')
from data.data_loader import get_splits
from utils.plot import plot_2D

def k_means_cluster(data, k, max_iter=300, alg='auto'):
    
    model = KMeans(n_clusters=k, max_iter=max_iter, algorithm=alg)
    # fit model to X_train and predict the clusters for finding average price for clusters
    print("fitting k means")
    training_cluster_ass = model.fit_predict(data['X_train'])
    # predict X_test clusters for test performance
    print("predicting test data for k means")
    testing_cluster_ass = model.predict(data['X_test'])

    # list of examples and their prices indexed by their assigned cluster
    print("summing examples")
    list_prices_of_categories = list_examples_per_cluster(training_cluster_ass, data)
    assert len(list_prices_of_categories) == k, "list prices contains too many lists"
    # find average price of each cluster from list
    print("finding averages")
    average_prices_of_categories = average_price_of_clusters(list_prices_of_categories)
    # print(average_prices_of_categories)
    assert len(average_prices_of_categories) == k, "average prices contains too many values"
    # find average percentage difference between cluster average prices and test/train labels
    print("calculating error")
    train_err = find_err(average_prices_of_categories, training_cluster_ass, data['Y_train'])
    test_err = find_err(average_prices_of_categories, testing_cluster_ass, data['Y_test'])

    scores = {}

    scores['test'] = test_err
    scores['train'] = train_err

    return scores
    

def list_examples_per_cluster(training_cluster_ass, data):

    list_prices_of_categories = {}
    # append like examples to hashtable
    for i in range(len(training_cluster_ass)):
        # if no entry for this label add a list with this example
        if str(training_cluster_ass[i]) not in list_prices_of_categories.keys():
            # list_prices_of_categories[str(training_cluster_ass[i])] = [data['Y_train'][i]]
            # iloc change for pandas
            list_prices_of_categories[str(training_cluster_ass[i])] = [data['Y_train'].iloc[i]]

        else:
            # otherwise append example
            # list_prices_of_categories[str(training_cluster_ass[i])].append(data['Y_train'][i])
            # iloc change for pandas
            list_prices_of_categories[str(training_cluster_ass[i])].append(data['Y_train'].iloc[i])
            

    return list_prices_of_categories


def average_price_of_clusters(average_prices_of_categories):

    for keys, values in average_prices_of_categories.items():
        prev_average = 0
        current_average = 0
        num_exs_so_far = 1

        for value in values:
            current_average = prev_average*(num_exs_so_far-1)/(num_exs_so_far) + value/(num_exs_so_far)
            assert current_average > 0, "Negative error in kmeans while finding average price for clusters"
            num_exs_so_far += 1
            prev_average = current_average

        average_prices_of_categories[keys] = current_average

    return average_prices_of_categories


def find_err(average_prices_of_categories, cluster_assignments, labels):

    prev_avg = 0
    current_average = 0
    num_exs_so_far = 1

    for i in range(len(cluster_assignments)):
        # for each cluster assignment, calculate difference between prediction and label
        cluster_price = average_prices_of_categories[str(cluster_assignments[i])]
        # actual_price = labels[i]
        # iloc change for pandas
        actual_price = labels.iloc[i]

        # print("actual: {}; estimation: {}".format(actual_price, cluster_price))

        # find percentage off loss
        difference = abs(cluster_price-actual_price)

        current_average = prev_avg*(num_exs_so_far-1)/(num_exs_so_far) + difference/num_exs_so_far
        prev_avg = current_average
        num_exs_so_far += 1

    # print("loss sum: {}".format(loss_sum))
    return current_average


def progress_report(data):
    ks = []
    test_errs = []
    train_errs = []

    for k in range(10, 610, 50):
        scores = k_means_cluster(data, k, max_iter=300)
        ks.append(k)
        test_errs.append(scores['test'])
        train_errs.append(scores['train'])
    
    plot_2D("kmeans performance varying K", "K", "Error in dollars", test_errs, train_errs, ks)



# debug purposes
if __name__ == "__main__":
    data = get_splits("../data/vehicles_cleaner.csv", 0.2)
    if data is not None:
        # print(data['X_train'])
        # print(k_means_cluster(data, 500, max_iter=300))
        progress_report(data)
    pass