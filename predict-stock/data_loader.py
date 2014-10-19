# We'll need the csv module to read the file
import csv
# We'll need numpy to manage arrays of data
import numpy as np

# We'll need the DenseDesignMatrix class to return the data
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix

def load_data(start, stop, file_name='stock_data.txt', norminize=True):
    """
    Loads the stock-data dataset from:

    The dataset contains n examples, including a floating point regression
    target.

    Parameters
    ----------
    start: int
    stop: int

    Returns
    -------

    dataset : DenseDesignMatrix
        A dataset include examples start (inclusive) through stop (exclusive).
        The start and stop parameters are useful for splitting the data into
        train, validation, and test data.
    """
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        X = []
        y = []
        header = True
        for row in reader:
            # Skip the first row containing the string names of each attribute
            """
            if header:
                header = False
                continue
            # Convert the row into numbers
            """
            row = [float(elem) for elem in row]
            X.append(row)

    #not divide 0
    min_sigma = 0.0001
    np_x = np.asarray(X);
    np_x = np_x[:,1:];#remove date column
    if norminize:
        mu = np_x.mean(axis=0)
        var = np_x.var(axis=0)
        print mu;
        print var;

        sigma = [ max(i, min_sigma) for i in var]
        np_x = np_x/sigma

    X = np_x[:, 0:-1]
    y = np_x[:,-1]
    y = y.reshape(y.shape[0], 1)

    X = X[start:stop, :]
    y = y[start:stop, :]

    return DenseDesignMatrix(X=X, y=y)

if __name__ == "__main__":
    print "test load_data"
    load_data(0, -1, "stock_data.txt");
