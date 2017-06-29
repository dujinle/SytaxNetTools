from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections,os,codecs
import tensorflow as tf


def _read_words(filename):
	with codecs.open(filename,'r','utf-8') as f:
		keys = list();
		values = list();
		while True:
			line = f.readline();
			if not line: break;
			line = line.strip('\n').strip('\r');
			if len(line) == 0 or line[0] == '#': continue;
			split = line.split('\t');
			keys.extend(split[0].split(' '));
			values.extend(split[1].split(' '));
		return (keys,values);

def _build_vocab(filename):
	keys,values = _read_words(filename);
	data = keys + values;
	counter = collections.Counter(data)
	count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

	words, _ = list(zip(*count_pairs))
	word_to_id = dict(zip(words, range(len(words))))
	return word_to_id,words


def _file_to_word_ids(filename, word_to_id):
	keys,values = _read_words(filename)
	kids = [word_to_id[word] for word in keys if word in word_to_id];
	vids = [word_to_id[word] for word in values if word in word_to_id];
#	print(' '.join(values))
#	print(' '.join([str(wid) for wid in vids]))
	return kids,vids;

def djl_raw_data(data_path=None):
	train_path = os.path.join(data_path, "djl.train.txt")
	test_path = os.path.join(data_path, "djl.test.txt")

	word_to_id,vocab = _build_vocab(train_path)
	train_data,target_data = _file_to_word_ids(train_path, word_to_id)
	test_data,target_test = _file_to_word_ids(test_path, word_to_id)
	return train_data, target_data, test_data, target_test,vocab

def djl_producer(raw_data,targets, batch_size, num_steps, name=None):
	with tf.name_scope(name, "DJLProducer", [raw_data, batch_size, num_steps]):
#		print('djl producer------------------------------------')
#		print(' '.join([str(wid) for wid in raw_data]))
#		print(' '.join([str(wid) for wid in targets]))
		raw_data = tf.convert_to_tensor(raw_data, name="raw_data", dtype=tf.int32)
		tar_data = tf.convert_to_tensor(targets, name="tar_data", dtype=tf.int32)
		data_len = tf.size(raw_data)
		batch_len = data_len // batch_size
		data = tf.reshape(raw_data[0 : batch_size * batch_len],[batch_size, batch_len])
		tars = tf.reshape(tar_data[0 : batch_size * batch_len],[batch_size, batch_len])

		epoch_size = (batch_len - 1) // num_steps
		assertion = tf.assert_positive(epoch_size,message="epoch_size == 0, decrease batch_size or num_steps")
		with tf.control_dependencies([assertion]):
			epoch_size = tf.identity(epoch_size, name="epoch_size")

		i = tf.train.range_input_producer(epoch_size, shuffle=False).dequeue()
		x = tf.strided_slice(data, [0, i * num_steps],[batch_size, (i + 1) * num_steps])
		x.set_shape([batch_size, num_steps])
		y = tf.strided_slice(tars, [0, i * num_steps],[batch_size, (i + 1) * num_steps])
		y.set_shape([batch_size, num_steps])
		return x,y
