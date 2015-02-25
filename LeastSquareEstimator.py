import numpy
import math
import scipy.optimize as optimization

# objective function for lsq
def func(params, xdata, ydata):
    return (ydata - numpy.dot(xdata, params))

x = []
y = []

# load data from training set for least square model
training_data = open('training.data', 'r')
for line in training_data:

    data = line.strip().split()

    # ground truth data
    y.append(float(data[0]))

    # model matrix
    d = []
    for i in range(1, 13):
        if len(data[i]) == 0:
            # continue
            d.append(0.0)
        else:
            d.append(float(data[i]))
    x.append(d)
training_data.close()

# perform least square error calculation to form the model
xdata = numpy.array(x)
ydata = numpy.array(y)
x0 = numpy.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
coefficients = optimization.leastsq(func, x0, args=(xdata, ydata))[0]

# print the coefficients of the generated model
print coefficients

# evaluate the model based on the testing set
for sample_data in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 327]:
    testing_data = open('testing.data', 'r')
    squared_err_sum = 0
    sum = 0
    for line in testing_data:

        data = line.strip().split()

        ground_truth_star = float(data[0])
        computed_star = 0

        for i in range(1, 13):
            computed_star += float(data[i]) * coefficients[i-1]

        sum += 1
        squared_err_sum += math.pow(computed_star - ground_truth_star, 2)
        if sum == sample_data:
            break
    testing_data.close()

    # print the mean squarred error of the generated model
    mean_squared_err = squared_err_sum / sum
    print 'sample-data[' + str(sample_data) + '] mean_squared_err: ' + str(mean_squared_err)
