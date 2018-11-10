import numpy as np
import scipy.special
import random
import codecs, json

class neuralNetwork:

    #Initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        #set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.i = 1 # if i //200 == 0: slightly mutate the network

        #link weight matrices, wih and who(weight hidden output)
        #weights inside the arrays are w_i_j,  where link is from node i to node j in the next layer
        #w11 w21
        #w12 w22 etc
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0,5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0,5), (self.onodes, self.hnodes))

        #learning rate
        self.lr = learningrate



        self.sigmoid_function = lambda x: scipy.special.expit(x)


    #train the neural network
    def train(self, inputs_list, targets_list):
        #converts inputs into 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        #calculate the signals emerging from hidden layer
        hidden_outputs = self.sigmoid_function(hidden_inputs)

        #calculate signals into final output layer
        final_inputs = np.dot(self.who,hidden_outputs)
        #calculate the signals emerging from final output layer
        final_outputs = self.sigmoid_function(final_inputs)

        #error is the (target- actual)
        output_errors = targets - final_outputs
        #hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)

        #update the weights for the links between the hidden  and output layers
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        #update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

        pass

    #query the neural network
    def query(self, inputs_list):
        self.i += 1
        if self.i //200 == 0:
            self.mutate(0.03)
        #convert input  list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        #calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        #calculate the signals emerging from hidden layer
        hidden_outputs = self.sigmoid_function(hidden_inputs)

        #calculate signals into final output layer
        final_inputs = np.dot(self.who,hidden_outputs)
        #calculate the signals emerging from final output layer
        final_outputs = self.sigmoid_function(final_inputs)

        return final_outputs

    def saveNetwork(self,filename):
        print("Saving instance of neural network")
        networkInstance = [{"inodes": self.inodes,"hnodes": self.hnodes,"onodes":self.onodes,"lr":self.lr},{"wih":self.wih,"who":self.who}]

        np.save(filename,networkInstance)

    def loadNetwork(self,path):
        print("Loading instance of neural network")
        data = np.load(path)
        neuralNetworkInstance = neuralNetwork(data[0]["inodes"],data[0]["hnodes"],data[0]["onodes"],data[0]["lr"])
        neuralNetworkInstance.wih= data[1]["wih"]
        neuralNetworkInstance.who = data[1]["who"]
        return neuralNetworkInstance

    def mutate(self,rate):
        def mutate(value):
            if random.random() < rate:
                return value + random.gauss(0, 0.1)
            else:
                return value

        func = np.vectorize(mutate)
        self.wih = func(self.wih)
        self.who = func(self.who)
