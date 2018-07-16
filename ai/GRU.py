import tensorflow as tf


class GRUNetwork:
    
    def __init__(self, data, n_hidden_layers, n_layers, epoch=10):
        self.data = data 
        self.n_hidden_layers = n_hiddens_layers
        self.n_layers = n_layers
        self.bias = tf.random_normal([1, 1])
        self.weight = tf.random_normal([1, 1])
        self.epoch = epoch
    
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
    
    def loss_function(self):
        pass
    
    def optimize(self):
        pass
    
    def run_network(self):
        rows = data['X_train'].shape[0]
        for epoch in range(self.epoch):
            for row in rows:
                word = data['X_train']['word'][row] 
                if word == 999999:
                    self.network.zero_state(batch_size, dtype=tf.float32)
                else:
                    pred = self.run_GRU(
                        data['X_train']['word'][row],
                        data['X_test']['word'][row],
                    )


        
        