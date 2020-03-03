Hey guys, it's probably best for usability purposes to make sure we are building models similarily to each other.
Check out models/kmeans.py for an example.

Some assumptions I made that I think should be present in all models:

   1. take in an object called 'data' in the arguments
   1a. data is a dictionary
   1b. data['X_train'] = X training data, data['Y_train'] = Y training labels, data['X_test'] = .... , data['Y_test'] = ..
        
   2. for simple performance tests, return a dictionary called 'scores'
   2a. where scores contains all the relevant scores for the test being ran
   2b. ie. scores['test'] is testing performance, scores['train'] is training performance, etc....
        
        
