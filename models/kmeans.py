from sklearn.cluster import KMeans
import clean_sample_data
import sys
sys.path.append('../')
from data.data_loader import get_splits
from utils.plot import plot_2D
import numpy as np
from sklearn.model_selection import KFold
from sklearn.utils import shuffle

def k_means_cluster(data, k, max_iter=300, alg='auto', weighted_average=False):
    
    model = KMeans(n_clusters=k, max_iter=max_iter, algorithm=alg)
    # fit model to X_train and predict the clusters for finding average price for clusters
    print("fitting k means")
    training_cluster_ass = model.fit_predict(data['X_train'])
    # predict X_test clusters for test performance
    print("predicting test data for k means")
    testing_cluster_ass = model.predict(data['X_test'])
    cluster_locations = model.cluster_centers_

    train_err = 0
    test_err = 0
    acceptance_rate = 0

    if weighted_average:
        print("listing weighted examples")
        w_list_prices_of_categories = list_weighted_examples_per_cluster(training_cluster_ass, data, cluster_locations)
        assert len(w_list_prices_of_categories) == k, "list prices contains too many lists"

        print("finding weighted averages")
        w_avg_prices_of_categories = weighted_avg_price_of_clusters(w_list_prices_of_categories)
        assert len(w_avg_prices_of_categories) == k, "average prices contains too many values"

        print("calculating weighted error")
        train_err, null = find_err(w_avg_prices_of_categories, training_cluster_ass, data['Y_train'])
        test_err, acceptance_rate = find_err(w_avg_prices_of_categories, testing_cluster_ass, data['Y_test'])

    else:
        # list of examples and their prices indexed by their assigned cluster
        print("listing examples")
        list_prices_of_categories = list_examples_per_cluster(training_cluster_ass, data)
        assert len(list_prices_of_categories) == k, "list prices contains too many lists"

        # find average price of each cluster from list
        print("finding averages")
        average_prices_of_categories = average_price_of_clusters(list_prices_of_categories)
        # print(average_prices_of_categories)
        assert len(average_prices_of_categories) == k, "average prices contains too many values"

        # find average percentage difference between cluster average prices and test/train labels
        train_err, null = find_err(average_prices_of_categories, training_cluster_ass, data['Y_train'])
        test_err, acceptance_rate = find_err(average_prices_of_categories, testing_cluster_ass, data['Y_test'])
    

    scores = {}

    scores['test'] = test_err
    scores['train'] = train_err
    print(scores)

    return scores, model.inertia_, acceptance_rate


def list_examples_per_cluster(training_cluster_ass, data):

    list_prices_of_categories = {}
    # append like examples to hashtable
    for i in range(len(training_cluster_ass)):
        # if no entry for this label add a list with this example
        if str(training_cluster_ass[i]) not in list_prices_of_categories.keys():
            list_prices_of_categories[str(training_cluster_ass[i])] = [data['Y_train'].iloc[i]]

        else:
            # otherwise append example
            list_prices_of_categories[str(training_cluster_ass[i])].append(data['Y_train'].iloc[i])
            

    return list_prices_of_categories

def list_weighted_examples_per_cluster(cluster_ass, data, cluster_centers):
    # append prices and corresponding weights as tuple
    list_prices_of_categories = {}
    for i in range(len(cluster_ass)):
        # calculate weight (1/euclidian distance squared)
        example_loc = data['X_train'].iloc[i]
        example_loc = np.asarray(example_loc).astype(np.float)
        centroid_loc = cluster_centers[cluster_ass[i]]

        # print("example_loc: {}, centroid_loc: {}".format(example_loc, centroid_loc))

        dist = np.linalg.norm(centroid_loc-example_loc)
        weight = 0

        if dist == 0:
            # idk what to do here ...
            weight = 100000
        else:
            weight = 1/dist
        

        price = np.asarray(data['Y_train'].iloc[i]).astype(np.float)
    
        price_and_weight = {}
        price_and_weight['price'] = price
        price_and_weight['weight'] = weight

        # if no entry for this label add a list with this example
        if str(cluster_ass[i]) not in list_prices_of_categories.keys():
            list_prices_of_categories[str(cluster_ass[i])] = [price_and_weight]

        else:
            # otherwise append example
            list_prices_of_categories[str(cluster_ass[i])].append(price_and_weight)

    return list_prices_of_categories



def weighted_avg_price_of_clusters(list_prices_of_categories):
    
    for keys, values in list_prices_of_categories.items():

        sum_of_weights = 0
        weighted_sum = 0
        prev_sum = 0

        for value in values:
            weight = value['weight']
            price = value['price']
            prev_sum = weighted_sum
            sum_of_weights += weight
            weighted_sum += price*weight
            assert prev_sum <= weighted_sum, "overflow error in weighted_avg_price_of_clusters"

        list_prices_of_categories[keys] = weighted_sum/sum_of_weights

    return list_prices_of_categories


def average_price_of_clusters(list_prices_of_categories):

    for keys, values in list_prices_of_categories.items():
        prev_average = 0
        current_average = 0
        num_exs_so_far = 1

        for value in values:
            val = value
            current_average = prev_average*(num_exs_so_far-1)/(num_exs_so_far) + val/(num_exs_so_far)
            assert current_average >= 0, "Negative error in kmeans while finding average price for clusters"
            num_exs_so_far += 1
            prev_average = current_average

        list_prices_of_categories[keys] = current_average

    return list_prices_of_categories


def find_err(average_prices_of_categories, cluster_assignments, labels):

    prev_avg = 0
    current_average = 0
    num_exs_so_far = 1
    num_accepted = 0

    for i in range(len(cluster_assignments)):
        # for each cluster assignment, calculate difference between prediction and label
        cluster_price = average_prices_of_categories[str(cluster_assignments[i])]
        # actual_price = labels[i]
        # iloc change for pandas
        actual_price = labels.iloc[i]

        # print("actual: {}; estimation: {}".format(actual_price, cluster_price))

        # find percentage off loss
        difference = abs(cluster_price-actual_price) / cluster_price

        if difference <= 0.1:
            num_accepted += 1

        current_average = prev_avg*(num_exs_so_far-1)/(num_exs_so_far) + difference/num_exs_so_far
        prev_avg = current_average
        num_exs_so_far += 1

    # print("loss sum: {}".format(loss_sum))
    return current_average, num_accepted/(num_exs_so_far-1)


def k_fold_analysis(data, k_init, k_final, jump):

    num_splits = int((k_final - k_init - 1) / jump)
    print("num splits: {}".format(num_splits))
    kf = KFold(n_splits= num_splits, shuffle=True)
    
    ks = []
    test_errs = []
    train_errs = []
    costs = []
    k = k_init
    acceptance_rates = []

    # aggregate all examples for KFold val
    
    
    X = data['X_train'].append(data['X_test'])
    y = data['Y_train'].append(data['Y_test'])
    

    for z, (train, test) in enumerate(kf.split(X,y)):

        # X,y = shuffle(X,y)
        X_train, X_test = X.iloc[train], X.iloc[test]
        y_train, y_test = y.iloc[train], y.iloc[test]

        # X_train = X_train[:10000]
        # y_train = y_train[:10000]

        # X_test = X_test[:2000]
        # y_test = y_test[:2000]

        print("len of X_train: {}".format(len(X_train)))

        print("len of X_test: {}".format(len(X_test)))

        # create fold dict for passing to Kmeans
        fold = {}
        fold['X_train'], fold['X_test'], fold['Y_train'], fold['Y_test'] = X_train, X_test, y_train, y_test
        scores, cost, acceptance_rate = k_means_cluster(fold, k, max_iter=300, weighted_average=True)
        
        # skip bad results for better graphing
        if scores['test'] > 1.5:
            continue
        # track for plotting
        
        ks.append(k)
        test_errs.append(scores['test'])
        train_errs.append(scores['train'])   
        costs.append(cost) 
        acceptance_rates.append(acceptance_rate)   
        # increment k
        k += jump 
    
    plot_2D("average error varying K", "K", "Average Error Percentage", test_errs, train_errs, ks)
    plot_2D("Model Costs", "K", "Cost", costs, None, ks)
    plot_2D("Model Acceptance Rates", "K", "Acceptance Rate", acceptance_rates, None, ks)



# debug purposes
if __name__ == "__main__":
    data = get_splits("../data/encoded_data/full_encoded.csv", 0.2)
    if data is not None:
        # print(data['X_train'])
        # print(k_means_cluster(data, 500, max_iter=300))
        k_fold_analysis(data, 5, 16, 2)
    pass