from sklearn.cluster import KMeans

def k_means_cluster(data, k, max_iter=300, alg='auto'):
    
    model = KMeans(n_clusters=k, max_iter=max_iter, algorithm=alg)
    model.fit(data['X_train'])

    # Opposite of the value of X on the K-means objective
    # what does this even mean??
    scores = {}
    scores['test'] = model.predict(data['X_test'])

    return scores
    