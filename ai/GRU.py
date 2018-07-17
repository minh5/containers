import tensorflow as tf


class GRUNetwork:
    
    def __init__(self,
        data,
        n_hidden_layers, 
        n_layers, 
        epoch=10, 
        learning_rate=0.01
    ):
        self.data = data 
        self.n_hidden_layers = n_hiddens_layers
        self.n_layers = n_layers
        self.bias = tf.random_normal([1, 1])
        self.weight = tf.random_normal([1, 1])
        self.epoch = epoch
        self.learning_rate = learning_rate
    
    def run_GRU(self, word, pos):
        self.network = tf.contrib.rnn_cell.GRUNetwork(
            self.n_hiddens_layers,
            word
        )
        prediction = tf.nn.softmax(
            tf.matmul(self.network, self.weight) + self.bias
        )
        prediction = tf.reshape(
            prediction,
            [-1, 1, 5]
        )
        return prediction

    def calculate_cost(self, prediction, target):
        cross_entropy = -tf.reduce_sum(
            target * tf.log(prediction),
             [1, 2]
        )
        return tf.reduce_mean(cross_entropy)
    
    def optimize(self, cost):
        optim = tf.train.RMSPropOptimizer(self.learning_rate)
        return optim.minimize(cost)
    
    def _run(self, word, target):
        if word == 999999:
            self.network.zero_state(batch_size, dtype=tf.float32)
        else:
            pred = self.run_GRU(
                word,
                target,
            )
            return pred

    def train_network(self):
        for epoch in self.epoch:
            for i in range(self.data['X_train'].shape[0]):
                prediction = self._run(
                    self.data['X_train']['word'][i],
                    self.data['X_train']['new_pos'][i]
                )
                if prediction:
                    self.cost = self.calculate_cost(
                        prediction,
                        self.data['X_train']['new_pos'][i]
                    )
                    self.optimize(self.cost)

        
        
        