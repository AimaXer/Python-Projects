import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json 
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler
# only displays the most important warnings

# Analitics functions for calculating effectivness of every strategy
class strategiesFunctions():

    @staticmethod
    def dataSplitting(data):
        df = data.sort_values('Date')
        high_prices = df.loc[:,'AskHigh'].to_numpy()
        low_prices = df.loc[:,'AskLow'].to_numpy()
        mid_prices = (high_prices+low_prices)/2.0
        train_data = mid_prices[:30000] 
        test_data = mid_prices[30000:]

        return train_data, test_data

    @staticmethod
    def dataVisualization(df):
        plt.figure(figsize = (18,9))
        plt.plot(range(df.shape[0]),(df['AskLow']+df['AskHigh'])/2.0)
        plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
        plt.xlabel('Date',fontsize=18)
        plt.ylabel('Mid Price',fontsize=18)
        plt.show()

    @staticmethod
    def normalizeData(data, train_data, test_data):
        scaler = MinMaxScaler()
        train_data = train_data.reshape(-1,1)
        test_data = test_data.reshape(-1,1)

        smoothing_window_size = 2500
        for di in range(0,10000,smoothing_window_size):
            scaler.fit(train_data[di:di+smoothing_window_size,:])
            train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])


        scaler.fit(train_data[di+smoothing_window_size:,:])
        train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])

        return train_data, test_data, scaler

    @staticmethod
    def scallerData(train_data, test_data):
        EMA = 0.0
        gamma = 0.1
        for ti in range(30000):
          EMA = gamma*train_data[ti] + (1-gamma)*EMA
          train_data[ti] = EMA

        # Used for visualization and test purposes
        all_mid_data = np.concatenate([train_data,test_data],axis=0)
        return all_mid_data, train_data, test_data

    @staticmethod
    def main(data):

        manager = strategiesFunctions()

        #manager.dataVisualization(data)
        
        train_data, test_data = manager.dataSplitting(data)
        train_data, test_data, scaler = manager.normalizeData(data, train_data, test_data)

        train_data = train_data.reshape(-1)
        test_data = scaler.transform(test_data).reshape(-1)

        all_mid_data, train_data, test_data = manager.scallerData(train_data, test_data)

        
        D = 1 # Dimensionality of the data. Since your data is 1-D this would be 1
        num_unrollings = 50 # Number of time steps you look into the future.
        batch_size = 500 # Number of samples in a batch
        num_nodes = [200,200,150] # Number of hidden nodes in each layer of the deep LSTM stack we're using
        n_layers = len(num_nodes) # number of layers
        dropout = 0.2 # dropout amount

        #tf.reset_default_graph() # This is important in case you run this multiple times

        
        # Input data.
        train_inputs, train_outputs = [],[]

        # You unroll the input over time defining placeholders for each time step
        for ui in range(num_unrollings):
            train_inputs.append(tf.Variable(tf.zeros(shape=[batch_size,D]),name='train_inputs_%d'%ui))
            train_outputs.append(tf.Variable(tf.zeros(shape=[batch_size,1]),name='train_outputs_%d'%ui))

        
        lstm_cells = [
            tf.keras.layers.LSTMCell(units=num_nodes[li],
                                    kernel_initializer= tf.keras.initializers.GlorotUniform()
                                   )
         for li in range(n_layers)]

        drop_lstm_cells = [tf.compat.v1.nn.rnn_cell.DropoutWrapper(
            lstm, input_keep_prob=1.0,output_keep_prob=1.0-dropout, state_keep_prob=1.0-dropout
        ) for lstm in lstm_cells]
        drop_multi_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(drop_lstm_cells)
        multi_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(lstm_cells)
        

        w = tf.compat.v1.get_variable('w',shape=[num_nodes[-1], 1], initializer=tf.keras.initializers.glorot_normal())
        b = tf.compat.v1.get_variable('b',initializer=tf.keras.backend.random_uniform([1],-0.1,0.1))

        
        lstm_cells = [
            tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=num_nodes[li],
                                    state_is_tuple=True,
                                    initializer= tf.keras.initializers.glorot_normal()
                                   )
         for li in range(n_layers)]

        drop_lstm_cells = [tf.compat.v1.nn.rnn_cell.DropoutWrapper(
            lstm, input_keep_prob=1.0,output_keep_prob=1.0-dropout, state_keep_prob=1.0-dropout
        ) for lstm in lstm_cells]
        drop_multi_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(drop_lstm_cells)
        multi_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(lstm_cells)

        w = tf.compat.v1.get_variable('w',shape=[num_nodes[-1], 1], initializer=tf.keras.initializers.glorot_normal())
        b = tf.compat.v1.get_variable('b',initializer=tf.keras.backend.random_uniform([1],-0.1,0.1))

        # loss of all the unrolled steps at the same time
        # Therefore, take the mean error or each batch and get the sum of that over all the unrolled steps

        print('Defining training Loss')
        loss = 0.0
        with tf.control_dependencies([tf.assign(c[li], state[li][0]) for li in range(n_layers)]+
                                     [tf.assign(h[li], state[li][1]) for li in range(n_layers)]):
          for ui in range(num_unrollings):
            loss += tf.reduce_mean(0.5*(split_outputs[ui]-train_outputs[ui])**2)

        print('Learning rate decay operations')
        global_step = tf.Variable(0, trainable=False)
        inc_gstep = tf.assign(global_step,global_step + 1)
        tf_learning_rate = tf.placeholder(shape=None,dtype=tf.float32)
        tf_min_learning_rate = tf.placeholder(shape=None,dtype=tf.float32)

        learning_rate = tf.maximum(
            tf.train.exponential_decay(tf_learning_rate, global_step, decay_steps=1, decay_rate=0.5, staircase=True),
            tf_min_learning_rate)

        # Optimizer.
        print('TF Optimization operations')
        optimizer = tf.train.AdamOptimizer(learning_rate)
        gradients, v = zip(*optimizer.compute_gradients(loss))
        gradients, _ = tf.clip_by_global_norm(gradients, 5.0)
        optimizer = optimizer.apply_gradients(
            zip(gradients, v))

        print('\tAll done')

        
        print('Defining prediction related TF functions')

        sample_inputs = tf.placeholder(tf.float32, shape=[1,D])

        # Maintaining LSTM state for prediction stage
        sample_c, sample_h, initial_sample_state = [],[],[]
        for li in range(n_layers):
          sample_c.append(tf.Variable(tf.zeros([1, num_nodes[li]]), trainable=False))
          sample_h.append(tf.Variable(tf.zeros([1, num_nodes[li]]), trainable=False))
          initial_sample_state.append(tf.contrib.rnn.LSTMStateTuple(sample_c[li],sample_h[li]))

        reset_sample_states = tf.group(*[tf.assign(sample_c[li],tf.zeros([1, num_nodes[li]])) for li in range(n_layers)],
                                       *[tf.assign(sample_h[li],tf.zeros([1, num_nodes[li]])) for li in range(n_layers)])

        sample_outputs, sample_state = tf.nn.dynamic_rnn(multi_cell, tf.expand_dims(sample_inputs,0),
                                           initial_state=tuple(initial_sample_state),
                                           time_major = True,
                                           dtype=tf.float32)

        with tf.control_dependencies([tf.assign(sample_c[li],sample_state[li][0]) for li in range(n_layers)]+
                                      [tf.assign(sample_h[li],sample_state[li][1]) for li in range(n_layers)]):  
          sample_prediction = tf.nn.xw_plus_b(tf.reshape(sample_outputs,[1,-1]), w, b)

        print('\tAll done')