import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

#X = [[1,2,3,2.5],[2.0, 5.0, -1.0, 2.0], [-1.5, 2.7, 3.3, -0.8]]

def create_data(points, classes):
    X = np.zeros((points*classes, 2))
    y = np.zeros(points* classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(points * class_number, points * (class_number + 1))
        r = np.linspace(0.0, 1, points)
        t = np.linspace(class_number * 4, (class_number + 1) * 4, points) + np.random.randn(points)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X,y

def plot_data(X, y):
    plt.scatter(X[:,0], X[:,1], c=y, cmap='brg')
    plt.show()

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class ReLU_Activation:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class Softmax_Activation:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss

class Loss_CategoricalCrossEntropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

        if len(y_true.shape)==1:
            correct_confidences = y_pred_clipped[range(samples), y_true]

        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)

        negative_log_likelihoods = np.log(correct_confidences)
        return negative_log_likelihoods

X, y = create_data(100, 3)

dense1 = Layer_Dense(2,3)
activation1 = ReLU_Activation()

dense2 = Layer_Dense(3,3)
activation2 = Softmax_Activation()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

print(activation2.output[:5])

loss_function = Loss_CategoricalCrossEntropy()
loss = loss_function.calculate(activation2.output, y)

print("Loss:  ", loss)