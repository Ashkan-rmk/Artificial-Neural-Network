from random import random

def read_train_file(file="OCR_train.txt"):
    training_data_list = []
    train_file = open(file, "r")
    for line in train_file:
        line = list(line.replace(" ", ""))
        line = [int(x) * 2 - 1 for x in line if x != "\n"]
        training_data_list.extend([line[:]])
    return training_data_list

def active_func(y_in):                    #activation function
    if y_in >= 0:
        return 1
    elif y_in < 0:
        return -1

def make_binary(n):
    pos = n.index(1) + 1
    res = list(format(pos, 'b').zfill(3))
    res = [int(x) for x in res]
    return res

def set_weight(num):
    weights = []
    for x in range(num):
        weights.extend([[random() for _ in range(64)]])  # initialize weights and biases
        # weights.extend([[0] * 64])
    return weights

cal_eroor = lambda error, total: (error / total) * 100


weights = set_weight(7)
"""3 CELLS"""
# weights = set_weight(3)

diff_weights = [0]*64                                     #contain errors of each training pair
epoch = 0                                           #counter of epochs
alpha = 1
epsilon = 1
training_data = read_train_file()


"""TRAINING PHASE OF NN"""
while max(diff_weights) < epsilon:                               #check stopping condition
    epoch += 1
    for j in training_data:
        x = j[:64]                 #set each input unit
        expected = j[-7:]

        """3 CELLS"""
        # expected = make_binary(expected)

        for weight, t in zip(weights, expected):    #each output unit
            result = 0                              # y_in in each training pair
            for w, s in zip(weight, x):
                result += w * s                     #calculate y_in(j)      j = 1, ..., 7

        for pos in range(63):
            temp = weight[pos]
            weight[pos] += alpha * (t - result) * x[pos]      #update weights(i, j)   i = 1, ..., 63
            diff_weights[pos] = weight[pos] - temp
        temp = weight[63]
        weight[63] += alpha * (t - result)              # update bias(j)
        diff_weights[63] = weight[63] - temp
for x in diff_weights:
    print(x)
print(str(epoch))

"""WEIGHTS AND BIASES SAVING PHASE OF NN"""
weight_file = open("Adeline_weights.txt‬‬", "w")
weight_file.write("Epochs: " + str(epoch) + "th" + "\n" + "\n")
for w in weights:
    weight_file.write(str(w) + "\n" + "\n")
weight_file.close()

print("\nThe Neural Network has been trained in " + str(epoch) + "th epochs.")
print("Weights and Biases saved in: ‫Adeline_weights.txt")


"""USE PHASE OF ADELINE NN"""
output = []
_error = 0
_total = 0
results = open("‫‪results_adeline.txt‬‬", "w")
if input("\nDo you want to use your Adeline NN? (y/n)") == 'y':
    test_file = read_train_file("OCR_test.txt")
    for elem in test_file:
        sample = elem[:64]
        target = elem[-7:]

        """3 CELLS"""
        # target = make_binary(target)

        output.clear()
        _total += 1
        for weight in weights:
            result = 0
            for w, s in zip(weight, sample):
                result += w * s
            output.append(active_func(result))
        if target != output:
            _error += 1
        print("Expected: " + str(target))
        results.write("Expected: " + str(target))
        print("Result:   " + str(output) + "\n------------\n")
        results.write("\nResult:   " + str(output) + "\n------------\n")

print("\n\nPercent of Error in NN: " + str(cal_eroor(_error, _total)))
print("\nNumber of Cells in NN: " + str(len(weights)))
results.write("\n\nPercent of Error in NN: " + str(cal_eroor(_error, _total)))
results.write("\nNumber of Cells in NN: " + str(len(weights)))
results.close()
