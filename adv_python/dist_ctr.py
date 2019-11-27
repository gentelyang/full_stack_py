#!/usr/bin/env python
# coding=utf-8

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import time
import sys
import os
import glob
import json
from datetime import date, timedelta

import paddlecloud.upload_utils as upload_utils
import tensorflow as tf
import logging

#################### CMD Arguments ####################
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer("num_threads", 16, "Embedding size")
tf.app.flags.DEFINE_integer("embedding_size", 10, "Embedding size")
tf.app.flags.DEFINE_integer("num_epochs", 10, "Number of epochs")
tf.app.flags.DEFINE_integer("batch_size", 1000, "batch size")
tf.app.flags.DEFINE_float("learning_rate", 0.0001, "learning rate")
tf.app.flags.DEFINE_integer("dict_size", 1000001, "dict size of sparse feature")
tf.app.flags.DEFINE_integer("dense_nums", 13, "dense feature num")
tf.app.flags.DEFINE_integer("slot_nums", 26, "sparse feature num")

tf.app.flags.DEFINE_string("train_data_dir", 'train_data', "train data dir")
tf.app.flags.DEFINE_string("test_data_dir", 'test_data', "test data dir")
tf.app.flags.DEFINE_string("model_dir", 'output', "model check point dir")
tf.app.flags.DEFINE_boolean("sync_mode", True, "sync_mode or async_mode")
tf.app.flags.DEFINE_boolean("is_local", True, "local or cloud")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tensorflow")
logger.setLevel(logging.INFO)

def print_log(log_str):
    """
    :param log_str: log info
    :return: no return
    """
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',
                               time.localtime(time.time()))
    print(str(time_stamp) + " " + log_str)

def get_file_list(is_train, trainer_nums=1, trainer_id=0):
    """
    :param is_train: True for training, and False for testing.
    :param trainer_nums: trainer nums
    :param trainer_id of current trainer
    :return: File list for current trainer.
    """
    if is_train:
        data_dir = FLAGS.train_data_dir
    else:
        data_dir = FLAGS.test_data_dir
    data_files = [data_dir + '/' + data_file for data_file in  os.listdir(data_dir)]
    if not FLAGS.is_local:
        return data_files

    remainder = len(data_files) % trainer_nums
    blocksize = len(data_files) / trainer_nums

    blocks = [blocksize] * trainer_nums
    for i in range(remainder):
        blocks[i] += 1

    trainer_files = [[]] * trainer_nums
    begin = 0
    for i in range(trainer_nums):
        trainer_files[i] = data_files[begin:begin + blocks[i]]
        begin += blocks[i]

    return trainer_files[trainer_id]


C_COLUMNS = ['I' + str(i) for i in range(1, 14)]
D_COLUMNS = ['C' + str(i) for i in range(14, 40)]
LABEL_COLUMN = "label"
CSV_COLUMNS = [LABEL_COLUMN] + C_COLUMNS + D_COLUMNS
# Columns Defaults
CSV_COLUMN_DEFAULTS = [[0]]
C_COLUMN_DEFAULTS = [[0.0] for i in range(FLAGS.dense_nums)]
D_COLUMN_DEFAULTS = [[0] for i in range(FLAGS.slot_nums)]
CSV_COLUMN_DEFAULTS = CSV_COLUMN_DEFAULTS + C_COLUMN_DEFAULTS + D_COLUMN_DEFAULTS

def input_fn(filenames, num_epochs, batch_size=1):
    def parse_csv(line):
        columns = tf.decode_csv(line, record_defaults=CSV_COLUMN_DEFAULTS)
        features = dict(zip(CSV_COLUMNS, columns))
        return features

    dataset = tf.data.TextLineDataset(filenames)
    dataset = dataset.map(parse_csv, num_parallel_calls=FLAGS.num_threads).prefetch(buffer_size=batch_size * 10)

    dataset = dataset.shuffle(buffer_size=10*batch_size)
    dataset = dataset.batch(batch_size)
    dataset = dataset.repeat(num_epochs)

    iterator = dataset.make_one_shot_iterator()
    features = iterator.get_next()

    return features

def upload(trainer_id, model_path):
    sys_job_id = os.getenv("SYS_JOB_ID")
    output_path = os.getenv("OUTPUT_PATH")
    remote_path = output_path + "/" + sys_job_id + "/model_trainer_" + str(trainer_id)
    upload_rst = upload_utils.upload_to_hdfs(local_file_path=model_path, remote_file_path=remote_path)
    logger.info("remote_path: {}, upload_rst: {}".format(remote_path, upload_rst))

def get_example_num(file_list):
    count = 0
    for f in file_list:
        last_count = count
        for index, line in enumerate(open(f, 'r')):
            count += 1
        print_log("file: %s has %s examples"%(f,count-last_count))
    logger.info("Total example: %s"%count)
    return count

def main(_):
    ps_hosts = os.getenv("PADDLE_PSERVERS_IP_PORT_LIST").split(",")
    worker_hosts = os.getenv("PADDLE_WORKERS_IP_PORT_LIST").split(",")
    role = os.getenv("TRAINING_ROLE")
    cluster = tf.train.ClusterSpec({"ps": ps_hosts,
                                    "worker": worker_hosts})

    if role == "PSERVER":
        pserver_id = int(os.getenv("PADDLE_TRAINER_ID", "0"))
        print(pserver_id)
        server = tf.train.Server(cluster,
                                 job_name="ps",
                                 task_index=pserver_id)
        server.join()
    elif role == "TRAINER":
        trainer_id = int(os.getenv("PADDLE_TRAINER_ID", "0"))
        server = tf.train.Server(cluster, job_name="worker",
                                 task_index=trainer_id)
        is_chief = (trainer_id == 0)
        num_workers = len(worker_hosts)
        device_setter = tf.train.replica_device_setter(
            worker_device="/job:worker/task:%d" % trainer_id,
            cluster=cluster)
        with tf.device(device_setter):    
            global_step = tf.Variable(0, name='global_step',
                                      trainable=False)
            train_file_list = get_file_list(True, num_workers, trainer_id)
            logger.info("train_file_list: %s" % str(train_file_list))
            logger.info("there are a total of %d files" % len(train_file_list))
            total_examples = get_example_num(train_file_list)
            features = input_fn(train_file_list, FLAGS.num_epochs, FLAGS.batch_size)
            embeddings = tf.get_variable("emb", [FLAGS.dict_size, FLAGS.embedding_size], tf.float32,
                    initializer=tf.random_uniform_initializer(-1.0,1.0))
            words = []
            for i in range(14, 40):
                key = 'C' + str(i)
                words.append(tf.nn.embedding_lookup(embeddings, features[key]))
            for i in range(1, 14):
                key = 'I' + str(i)
                words.append(tf.reshape(features[key], [-1, 1]))
            concat = tf.concat(words, axis=1)
            label_y = features[LABEL_COLUMN]
            fc0_w = tf.get_variable("fc0_w", [FLAGS.embedding_size * FLAGS.slot_nums + FLAGS.dense_nums, 400],
                                    tf.float32,
                                    initializer=tf.random_normal_initializer(stddev=1.0/tf.sqrt(tf.to_float(FLAGS.embedding_size * FLAGS.slot_nums + FLAGS.dense_nums))))
            fc0_b = tf.get_variable("fc0_b", [400], tf.float32,
                                    initializer=tf.constant_initializer(value=0))
            fc1_w = tf.get_variable("fc1_w", [400, 400], tf.float32,
                                    initializer=tf.random_normal_initializer(stddev=1.0/tf.sqrt(tf.to_float(400))))
            fc1_b = tf.get_variable("fc1_b", [400], tf.float32,
                                    initializer=tf.constant_initializer(value=0))
            fc2_w = tf.get_variable("fc2_w", [400, 400], tf.float32,
                                    initializer=tf.random_normal_initializer(stddev=1.0/tf.sqrt(tf.to_float(400))))
            fc2_b = tf.get_variable("fc2_b", [400], tf.float32,
                                    initializer=tf.constant_initializer(value=0))
            fc3_w = tf.get_variable("fc3_w", [400, 2], tf.float32,
                                    initializer=tf.random_normal_initializer(stddev=1.0/tf.sqrt(tf.to_float(400))))
            fc3_b = tf.get_variable("fc3_b", [2], tf.float32,
                                    initializer=tf.constant_initializer(value=0))

            fc0 = tf.nn.relu(tf.matmul(concat, fc0_w) + fc0_b)
            fc1 = tf.nn.relu(tf.matmul(fc0, fc1_w) + fc1_b)
            fc2 = tf.nn.relu(tf.matmul(fc1, fc2_w) + fc2_b)
            fc_predict = tf.matmul(fc2, fc3_w) + fc3_b
            
            logits = fc_predict
            predict = tf.nn.softmax(logits=logits)
            cost = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label_y, logits=logits)
            avg_cost = tf.reduce_mean(cost)
            positive_p = predict[:, 1]
            train_auc, train_update_op = tf.metrics.auc(
                labels=label_y,
                predictions=positive_p,
                name="auc")
            optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate)
            hooks = []
            if FLAGS.sync_mode:
                optimizer = sync_opt = tf.train.SyncReplicasOptimizer(
                        optimizer,
                        replicas_to_aggregate=num_workers,
                        total_num_replicas=num_workers)
                hooks.append(optimizer.make_session_run_hook(is_chief))
            train_op = optimizer.minimize(avg_cost, global_step=global_step) 
            saver = tf.train.Saver(max_to_keep=None)
            log_dir = "%s/checkpoint/" % FLAGS.model_dir
            if FLAGS.sync_mode:
                log_dir += 'sync'
            else:
                log_dir += 'async'
            saver_hook = tf.train.CheckpointSaverHook(checkpoint_dir=log_dir,
                                                      save_steps=44000,
                                                      saver=saver)
            hooks.append(saver_hook)
            sess_config = tf.ConfigProto(allow_soft_placement=True,
                                         log_device_placement=False)
            with tf.train.MonitoredTrainingSession(master=server.target,
                                                   is_chief=is_chief,
                                                   hooks=hooks,
                                                   config=sess_config) as sess:
                try:
                    batch_id = 0
                    start_time = time.time()
                    while True:
                        _, auc_v, update_op_v, loss_v, step = sess.run([train_op, train_auc, train_update_op, avg_cost, global_step])
                        batch_id += 1
                        if (batch_id - 1) % 1000 == 0 and (batch_id - 1) > 0:
                       #     now = time.time()
                       #     examples_num = (batch_id - last_step) * FLAGS.batch_size
                       #     rate = examples_num / (now - start_time)
                            logger.info("step: %d, local step: %d, auc: %f, loss: %f" % (step, batch_id, auc_v, loss_v))
                       #     last_step = batch_id
                       #     start_time = now
                except tf.errors.OutOfRangeError:
                    print("there are a total of %d batchs" % step)
                end_time = time.time()
                rate = total_examples / (end_time - start_time)
                logger.info("speed: %f examples/secs" % (rate))
                if not FLAGS.is_local:
                    upload(trainer_id, log_dir)
   
if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
