#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================
"""
@Desc: dist_base_fleet module
@File: dist_base_fleet.py
@Author: liangjinhua
@Date: 2019/8/26 19:21
"""
import argparse
import os
import pickle
import json
import signal
import subprocess
import sys
import time

import decorator
import paddle.fluid.incubate.fleet.base.role_maker as role_maker
from paddle.fluid.transpiler.distribute_transpiler import DistributeTranspilerConfig


RUN_STEP = 5
LEARNING_RATE = 0.01


class FleetDistRunnerBase(object):
    """fleet"""
    def __init__(self, batch_num=5, batch_size=32):
        self.batch_num = batch_num
        self.batch_size = batch_size

    def run_pserver(self, args):
        """run pserver"""
        from paddle.fluid.incubate.fleet.parameter_server.distribute_transpiler import fleet
        import paddle.fluid as fluid
        from paddle.fluid.transpiler.ps_dispatcher import RoundRobin
        from paddle.fluid.transpiler.ps_dispatcher import HashName
        fluid.default_startup_program().random_seed = 1
        fluid.default_main_program().random_seed = 1
        if args.role.upper() != "PSERVER":
            raise ValueError("args role must be PSERVER")
        role = role_maker.UserDefinedRoleMaker(
            current_id=args.current_id,
            role=role_maker.Role.SERVER,
            worker_num=args.trainers,
            server_endpoints=args.endpoints.split(","))
        fleet.init(role)
        strategy = DistributeTranspilerConfig()
        strategy.sync_mode = args.run_params["sync_mode"]
        strategy.async_mode = args.run_params["async_mode"]
        strategy.mode = "pserver"
        strategy.slice_var_up = args.run_params['slice_var_up']
        strategy.enable_dc_asgd = args.run_params['enable_dc_asgd']
        if args.run_params['split_method']:
            strategy.split_method = HashName
        strategy.split_method = RoundRobin
        strategy.wait_port = args.run_params['wait_port']
        strategy.runtime_split_send_recv = args.run_params['runtime_split_send_recv']
        strategy.use_hierarchical_allreduce = args.run_params['use_hierarchical_allreduce']
        #strategy.hierarchical_allreduce_exter_nranks = args.run_params['hierarchical_allreduce_exter_nranks']
        #strategy.hierarchical_allreduce_inter_nranks = args.run_params['hierarchical_allreduce_inter_nranks']
        strategy.geo_sgd_mode = args.run_params['geo_sgd']
        strategy.geo_sgd_need_push_nums = args.run_params['push_nums']
        avg_cost = self.net(args)
        optimizer = fluid.optimizer.SGD(LEARNING_RATE)
        optimizer = fleet.distributed_optimizer(optimizer, strategy)
        optimizer.minimize(avg_cost)
        fleet.init_server()
        fleet.run_server()

    def run_trainer(self, args):
        """run trainer"""
        from paddle.fluid.incubate.fleet.parameter_server.distribute_transpiler import fleet
        import paddle.fluid as fluid
        from paddle.fluid.transpiler.ps_dispatcher import RoundRobin
        from paddle.fluid.transpiler.ps_dispatcher import HashName
        fluid.default_startup_program().random_seed = 1
        fluid.default_main_program().random_seed = 1
        if args.role.upper() != "TRAINER":
            raise ValueError("args role must be TRAINER")
        role = role_maker.UserDefinedRoleMaker(
            current_id=args.current_id,
            role=role_maker.Role.WORKER,
            worker_num=args.trainers,
            server_endpoints=args.endpoints.split(","))
        fleet.init(role)
        strategy = DistributeTranspilerConfig()
        strategy.sync_mode = args.run_params["sync_mode"]
        strategy.async_mode = args.run_params["async_mode"]
        strategy.mode = "pserver"
        strategy.slice_var_up = args.run_params['slice_var_up']
        strategy.enable_dc_asgd = args.run_params['enable_dc_asgd']
        if args.run_params['split_method']:
            strategy.split_method = HashName
        strategy.split_method = RoundRobin
        strategy.wait_port = args.run_params['wait_port']
        strategy.runtime_split_send_recv = args.run_params['runtime_split_send_recv']
        strategy.use_hierarchical_allreduce = args.run_params['use_hierarchical_allreduce']
       # strategy.hierarchical_allreduce_exter_nranks = args.run_params['hierarchical_allreduce_exter_nranks']
       # strategy.hierarchical_allreduce_inter_nranks = args.run_params['hierarchical_allreduce_inter_nranks']
        strategy.geo_sgd_mode = args.run_params['geo_sgd']
        strategy.geo_sgd_need_push_nums = args.run_params['push_nums']
        avg_cost = self.net()
        optimizer = fluid.optimizer.SGD(LEARNING_RATE)
        optimizer = fleet.distributed_optimizer(optimizer, strategy)
        optimizer.minimize(avg_cost)
        losses = self.do_training(fleet, args)
        losses = "" if not losses else losses
        print(losses)

    def run_nccl_trainer(self, args):
        """run fleet api"""
        assert args.update_method == "nccl"
        import paddle.fluid as fluid
        import six
        from paddle.fluid.incubate.fleet.collective import fleet
        exec_strategy = fluid.ExecutionStrategy()
        exec_strategy.num_threads = args.run_params['num_threads']
        #dist_strategy = DistributedStrategy()
        #dist_strategy.exec_strategy = exec_strategy
        #dist_strategy.fuse_memory_size = 1  # MB
        #dist_strategy.fuse_laryer_size = 1
        if args.role.upper() != "TRAINER":
            raise ValueError("args role must be TRAINER")
        role = role_maker.PaddleCloudRoleMaker(is_collective=True)
        fleet.init(role)
        strategy = DistributeTranspilerConfig()
        avg_cost = self.net(args)
        losses = self.do_training(fleet,args)
        losses = "" if not losses else losses
        print(losses)

    def net(self, args=None):
        """net """
        raise NotImplementedError(
            "get_model should be implemented by child classes.")

    def do_training(self, fleet, args=None):
        """training"""
        raise NotImplementedError(
            "do_training should be implemented by child classes.")

    def py_reader(self):
        """py reader"""
        raise NotImplementedError(
            "py_reader should be implemented by child classes."
        )

    def dataset_reader(self):
        """dataset reader"""
        raise NotImplementedError(
            "dataset_reader should be implemented by child classes.")


class TestFleetBase(object):
    """
    TestDistRun
    """
    def __init__(self, pservers=2, trainers=2):
        self.trainers = trainers
        self.pservers = pservers
        self.ps_endpoints = ""
        for i in range(pservers):
            self.ps_endpoints += "127.0.0.1:912%s," % (i + 1)
        self.ps_endpoints = self.ps_endpoints[:-1]
        self.python_interp = "python"
        self.run_params = {}

    def start_pserver(self, model_file, check_error_log):
        """
        start_pserver
        """
        ps_endpoint_list = self.ps_endpoints.split(",")
        ps_pipe_list = []
        ps_proc_list = []
        run_params = json.dumps(self.run_params).replace(" ", "")

        for i, ps_endpoint in enumerate(ps_endpoint_list):
            ps_cmd = "{} {} --update_method pserver --role pserver --endpoints {} " \
                     "--current_id {} --trainers {} --run_params {}".format(
                     self.python_interp,
                     model_file,
                     self.ps_endpoints,
                     i,
                     self.trainers,
                     run_params)
            ps_pipe = subprocess.PIPE
            if check_error_log:
                print("ps_cmd:", ps_cmd)
                ps_pipe = open("/tmp/ps%s_err.log" % i, "wb")
            ps_proc = subprocess.Popen(ps_cmd.split(" "), stdout=subprocess.PIPE, stderr=ps_pipe)
            ps_pipe_list.append(ps_pipe)
            ps_proc_list.append(ps_proc)
        return ps_proc_list, ps_pipe_list

    def _wait_ps_ready(self, pid):
        retry_times = 50
        while True:
            assert retry_times >= 0, "wait ps ready failed"
            time.sleep(3)
            try:
                # the listen_and_serv_op would touch a file which contains the listen port
                # on the /tmp directory until it was ready to process all the RPC call.
                os.stat("/tmp/paddle.%d.port" % pid)
                return
            except os.error as e:
                sys.stderr.write('waiting for pserver: %s, left retry %d\n' %
                                 (e, retry_times))
                retry_times -= 1

    def get_result(self, model_file, check_error_log=True, update_method="pserver",
                   gpu_num=0, models_change_env=None):
        """
        get_result
        update_method:pserver or nccl
        """
        required_envs = {
            "PATH": os.getenv("PATH"),
            "LD_LIBRARY_PATH": os.getenv("LD_LIBRARY_PATH", ''),
            "PYTHONPATH": os.getenv("PYTHONPATH", ""),
            "FLAGS_fraction_of_gpu_memory_to_use": "0.15",
            "FLAGS_cudnn_deterministic": "1",
            "FLAGS_rpc_deadline": "5000",  # 5sec to fail fast
            "http_proxy": ""
        }
        if check_error_log:
            required_envs["GLOG_v"] = "1"
            required_envs["GLOG_logtostderr"] = "1"
        if models_change_env:
            required_envs.update(models_change_env)
        # Run local to get a base line
        if update_method == "pserver":
            ps_proc_list, ps_pipe_list = self.start_pserver(model_file,
                                                            check_error_log)
            for ps_proc in ps_proc_list:
                self._wait_ps_ready(ps_proc.pid)
        tr_cmd_lists = []
        tr_proc_list = []
        FNULL = open(os.devnull, 'w')
        run_params = json.dumps(self.run_params).replace(" ", "")
        if update_method == "pserver":
            for i in range(self.trainers):
                tr_cmd = "{} {} --update_method pserver --role trainer --endpoints {} " \
                         "--current_id {} --trainers {} --run_params {}".format(
                    self.python_interp,
                    model_file,
                    self.ps_endpoints,
                    i,
                    self.trainers,
                    run_params)
                devices_define = ""
                for j in range(gpu_num):
                    devices_define += "%d," % (i * gpu_num + j)
                envs = {"CUDA_VISIBLE_DEVICES": devices_define[:-1]}
                envs.update(required_envs)
                tr_cmd_lists.append({"cmd": tr_cmd, "envs": envs})
        elif update_method == "nccl":
            all_nodes_devices_endpoints = ""
            nranks = self.trainers * gpu_num
            for trainer_id in range(self.trainers):
                for i in range(gpu_num):
                    if all_nodes_devices_endpoints:
                        all_nodes_devices_endpoints += ","
                    all_nodes_devices_endpoints += "127.0.0.1:617%d" % (trainer_id * gpu_num + i)
            for real_id in range(nranks):
                envs = {}
                envs.update(required_envs)
                envs.update({
                    "FLAGS_selected_gpus": "%d" % real_id,
                    "PADDLE_TRAINER_ID": "%d" % real_id,
                    "PADDLE_CURRENT_ENDPOINT": "%s:617%d" % ("127.0.0.1", real_id),
                    "PADDLE_TRAINERS_NUM": "%d" % nranks,
                    "PADDLE_TRAINER_ENDPOINTS": all_nodes_devices_endpoints
                })
                tr_cmd = "{} {} --update_method nccl --role trainer --endpoints {} " \
                         "--current_id {} --trainers {} --run_params {}".format(
                          self.python_interp,
                          model_file,
                          all_nodes_devices_endpoints,
                          real_id,
                          nranks,
                          run_params)
                nccl_devs = {"NCCL_SOCKET_IFNAME": "eth0",
                             "NCCL_P2P_DISABLE": "1",
                             "NCCL_IB_DISABLE": "0",
                             "NCCL_IB_CUDA_SUPPORT": "1"}
                envs.update(nccl_devs)
                tr_cmd_lists.append({"cmd": tr_cmd, "envs": envs})
        for real_id, tr_cmd_dict in enumerate(tr_cmd_lists):
            tr_cmd = tr_cmd_dict["cmd"]
            envs = tr_cmd_dict["envs"]
            print tr_cmd, envs
            tr_pipe = subprocess.PIPE
            if check_error_log:
                print("tr_cmd:", tr_cmd)
                tr_pipe = open("/tmp/tr%s_err.log" % real_id, "wb")
            tr_proc = subprocess.Popen(
                tr_cmd.split(" "),
                stdout=subprocess.PIPE,
                stderr=tr_pipe,
                env=envs)
            tr_proc_list.append(tr_proc)
        for tr_proc in tr_proc_list:
            tr_proc.wait()
        # train data
        train_data = []
        for tr_proc in tr_proc_list:
            out, err = tr_proc.communicate()
            lines = out.split("\n")[-2]
            if lines:
                lines = lines[1:-2].split(",")
            loss = [eval(i) for i in lines]
            train_data.append(loss)
        if update_method == "pserver":
            for ps_proc in ps_proc_list:
                os.kill(ps_proc.pid, signal.SIGKILL)
        FNULL.close()
        print train_data
        return train_data


def runtime_main(test_class):
    """
    run main test_class
    :param test_class:
    :return:
    """
    parser = argparse.ArgumentParser(description='Run Fleet test.')
    parser.add_argument(
        '--update_method', type=str, required=True, choices=['pserver', 'nccl'])
    parser.add_argument(
        '--role', type=str, required=True, choices=['pserver', 'trainer'])
    parser.add_argument('--endpoints', type=str, required=False, default="")
    parser.add_argument('--current_id', type=int, required=False, default=0)
    parser.add_argument('--trainers', type=int, required=False, default=1)
    parser.add_argument('--run_params', type=str, required=True, default='{}')
    args = parser.parse_args()
    args.run_params = json.loads(args.run_params)
    model = test_class()
    if args.update_method == "nccl":
        model.run_nccl_trainer(args)
        return
    if args.role == "pserver":
        model.run_pserver(args)
    else:
        model.run_trainer(args)


def run_by_freq(freq):
    """testcase run by frequency, it contains DAILY, MONTH"""
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        if os.getenv("RUN_FREQUENCY", "DAILY") == freq:
            return func(*args, **kwargs)
        else:
            return
    return wrapper
