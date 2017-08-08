import os
import sys
import json
import shutil
import pickle
import logging
import data_helper
import numpy as np
import pandas as pd
import tensorflow as tf
from text_cnn_rnn import TextCNNRNN

logging.getLogger().setLevel(logging.INFO)

model_dir = "trained_results_1502115011"

def load_trained_params(trained_dir):
	params = json.loads(open(trained_dir + 'trained_parameters.json').read())
	words_index = json.loads(open(trained_dir + 'words_index.json').read())
	labels = json.loads(open(trained_dir + 'labels.json').read())

	with open(trained_dir + 'embeddings.pickle', 'rb') as input_file:
		fetched_embedding = pickle.load(input_file)
	embedding_mat = np.array(fetched_embedding, dtype = np.float32)
	return params, words_index, labels, embedding_mat


def map_word_to_index(examples, words_index):
	x_ = []
	for example in examples:
		temp = []
		for word in example:
			if word in words_index:
				temp.append(words_index[word])
			else:
				temp.append(0)
		x_.append(temp)
	return x_

def predict_unseen_data(text):
	trained_dir = model_dir
	if not trained_dir.endswith('/'):
		trained_dir += '/'

	params, words_index, labels, embedding_mat = load_trained_params(trained_dir)

	x_ = [data_helper.clean_str(text).split(' ')]
	x_ = data_helper.pad_sentences(x_, forced_sequence_length=params['sequence_length'])
	x_ = map_word_to_index(x_, words_index)
	x_test = np.asarray(x_)
	with tf.Graph().as_default():
		session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
		sess = tf.Session(config=session_conf)
		with sess.as_default():
			cnn_rnn = TextCNNRNN(
				embedding_mat = embedding_mat,
				non_static = params['non_static'],
				hidden_unit = params['hidden_unit'],
				sequence_length = len(x_test[0]),
				max_pool_size = params['max_pool_size'],
				filter_sizes = map(int, params['filter_sizes'].split(",")),
				num_filters = params['num_filters'],
				num_classes = len(labels),
				embedding_size = params['embedding_dim'],
				l2_reg_lambda = params['l2_reg_lambda'])
			
			def real_len(batches):
				return [np.ceil(np.argmin(batch + [0]) * 1.0 / params['max_pool_size']) for batch in batches]

			def predict_step(x_batch):
				feed_dict = {
					cnn_rnn.input_x: x_batch,
					cnn_rnn.dropout_keep_prob: 1.0,
					cnn_rnn.batch_size: len(x_batch),
					cnn_rnn.pad: np.zeros([len(x_batch), 1, params['embedding_dim'], 1]),
					cnn_rnn.real_len: real_len(x_batch),
				}
				predictions = sess.run([cnn_rnn.predictions], feed_dict)
				return predictions

			checkpoint_file = trained_dir + 'best_model.ckpt'
			saver = tf.train.Saver(tf.global_variables())
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file[:-5]))
			saver.restore(sess, checkpoint_file)
			logging.critical('{} has been loaded'.format(checkpoint_file))

			batches = data_helper.batch_iter(list(x_), params['batch_size'], 1, shuffle=False)
			predictions = ""
			for x_batch in batches:
				batch_predictions = predict_step(x_batch)[0][0]
				predictions = batch_predictions
			return labels[predictions]


if __name__ == '__main__':
	print(predict_unseen_data("india"))
