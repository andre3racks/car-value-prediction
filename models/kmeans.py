from sklearn.cluster import KMeans

def k_means_cluster(data, k, max_iter=300, alg='auto'):
    
    model = KMeans(n_clusters=k, max_iter=max_iter, algorithm=alg)
    # fit model to X_train and predict the clusters for finding average price for clusters
    training_cluster_ass = model.fit_predict(data['X_train'])
    # predict X_test clusters for test performance
    testing_cluster_ass = model.predict(data['X_test'])

    # list of examples and their prices indexed by their assigned cluster
    list_prices_of_categories = list_examples_per_cluster(training_cluster_ass, data)

    # find average price of each cluster from list
    average_prices_of_categories = average_price_of_clusters(list_prices_of_categories)

    # find average percentage difference between cluster average prices and test/train labels
    train_err = find_err(average_prices_of_categories, training_cluster_ass, data['Y_train'])
    test_err = find_err(average_prices_of_categories, testing_cluster_ass, data['Y_test'])

    scores = {}

    scores['test'] = 1-test_err
    scores['train'] = 1-train_err

    return scores
    

def list_examples_per_cluster(training_cluster_ass, data):

    list_prices_of_categories = {}
    # append like examples to hashtable
    for i in range(len(training_cluster_ass)):
        # if no entry for this label add a list with this example
        if str(training_cluster_ass[i]) not in list_prices_of_categories.keys():
            list_prices_of_categories[str(training_cluster_ass[i])] = [data['Y_train'][i]]

        else:
            # otherwise append example
            list_prices_of_categories[str(training_cluster_ass[i])].append(data['Y_train'][i])

    return list_prices_of_categories


def average_price_of_clusters(average_prices_of_categories):

    for values in average_prices_of_categories.values():
        # last total to ensure no overflow whilst averaging
        prev_average = 0
        current_average = 0
        num_exs_so_far = 1

        # programmed to avoid overflow, a running average
        for value in values:
            value = abs(value)
            current_average = prev_average*(num_exs_so_far-1)/(num_exs_so_far) + value/(num_exs_so_far)
            assert current_average > 0, "Negative error in kmeans while finding average price for clusters"
            num_exs_so_far += 1
            prev_average = current_average

        # assign dictionary values to average price of cluster
        values = current_average

    return average_price_of_clusters


def find_err(average_price_of_clusters, cluster_assignments, labels):

    loss_sum = 0

    for i in range(len(cluster_assignments)):
        # for each cluster assignment, calculate difference between prediction and label
        cluster_price = average_price_of_clusters[str(cluster_assignments[i])]
        actual_price = labels[i]

        # find percentage off loss
        loss_sum += (cluster_price-actual_price) / actual_price


    return loss_sum/len(cluster_assignments)