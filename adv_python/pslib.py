import numpy as np
import os
import sys
import paddle
import paddle.fluid as fluid
import threading
import time
import config
from paddle.fluid.incubate.fleet.parameter_server.pslib import fleet
from paddle.fluid.incubate.fleet.utils.hdfs import HDFSClient
from model_new import Model
from model_new_jc import ModelJoinCommon
from util import *
from paddle.fluid.incubate.fleet.utils.fleet_util import FleetUtil
fleet_util = FleetUtil()
import config_fleet

def create_model(slot_file, slot_common_file, all_slot_file):
    join_common_model = ModelJoinCommon(slot_file, slot_common_file, all_slot_file, 20)
    update_model = Model(slot_file, all_slot_file, False, 0, True)
    with open("join_common_main_program.pbtxt", "w") as fout:
        print >> fout, join_common_model._train_program
    with open("join_common_startup_program.pbtxt", "w") as fout:
        print >> fout, join_common_model._startup_program
    with open("update_main_program.pbtxt", "w") as fout:
        print >> fout, update_model._train_program
    with open("update_startup_program.pbtxt", "w") as fout:
        print >> fout, update_model._startup_program
    return [join_common_model, update_model]

def create_dataset(use_var_list, my_filelist):
    dataset = fluid.DatasetFactory().create_dataset(config.dataset_type)
    dataset.set_batch_size(config.batch_size)
    dataset.set_thread(config.thread_num)
    dataset.set_hdfs_config(config.fs_name, config.fs_ugi)
    dataset.set_pipe_command("./read_feasign | python ins_weight.py | awk -f format_newcate_hotnews.awk | ./parse_feasign all_slot.dict")
    dataset.set_filelist(["part-00000_1"])
    dataset.set_use_var(use_var_list)
    return dataset

def save_delta(day, pass_index, xbox_base_key, cur_path, scope_join, scope_common, scope_update, join_model,
               join_common_model, update_model, join_save_params, common_save_params, update_save_params):

    fleet_util.rank0_print("no save")
    return
               
    fleet_util.rank0_print("begin save delta model")
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    begin = time.time()
    if pass_index == -1:
        fleet_util.save_xbox_base_model(config.output_path, day)
    else:
        fleet_util.save_delta_model(config.output_path, day, pass_index)
    end = time.time()
    fleet_util.save_paddle_params(exe, scope_join, join_model._train_program, "paddle_dense.model.0",
                                  config.output_path, day, pass_index, config.fs_name, config.fs_ugi,
                                  var_names=join_save_params)
    fleet_util.save_paddle_params(exe, scope_common, join_common_model._train_program, "paddle_dense.model.1",
                                  config.output_path, day, pass_index, config.fs_name, config.fs_ugi,
                                  var_names=common_save_params)
    fleet_util.save_paddle_params(exe, scope_update, update_model._train_program, "paddle_dense.model.2",
                                  config.output_path, day, pass_index, config.fs_name, config.fs_ugi,
                                  var_names=update_save_params)
    fleet_util.rank0_print("end save delta cost %s min" % ((end - begin) / 60.0))
    fleet_util.rank0_print("begin save cache")
    begin = time.time()
    if pass_index == -1:
        key_num = fleet_util.save_cache_base_model(config.output_path, day)
    else:
        key_num = fleet_util.save_cache_model(config.output_path, day, pass_index)
    fleet_util.write_cache_donefile(config.output_path, day, pass_index, key_num, config.fs_name, config.fs_ugi)
    end = time.time()
    fleet_util.rank0_print("end save cache cost %s min, key_num=%s" % ((end - begin) / 60.0, key_num))
    fleet_util.write_xbox_donefile(config.output_path, day, pass_index, xbox_base_key, ",".join(cur_path),
                                   config.fs_name, config.fs_ugi)

if __name__ == "__main__":
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    fleet.init(exe)

    slot_file = "slot/slot"
    slot_common_file = "slot/slot_common"
    all_slot_file = "all_slot.dict"
    join_common_model, update_model = create_model(slot_file, slot_common_file, all_slot_file)
    scope2 = fluid.Scope()
    scope3 = fluid.Scope()
    adjust_ins_weight = {"need_adjust" : True, "nid_slot" : "6002", "nid_adjw_threshold" : 1000, "nid_adjw_ratio": 20,
                          "ins_weight_slot": update_model.ins_weight.name}
    config_fleet.config['adjust_ins_weight'] = adjust_ins_weight

    thread_stat_var_names = [join_common_model.join_auc_stat_list[2].name, join_common_model.join_auc_stat_list[3].name]
    thread_stat_var_names += [join_common_model.common_auc_stat_list[2].name, join_common_model.common_auc_stat_list[3].name]
    thread_stat_var_names += [update_model.auc_stat_list[2].name, update_model.auc_stat_list[2].name]
    thread_stat_var_names += [i.name for i in join_common_model.join_metric_list + join_common_model.common_metric_list + update_model.metric_list]
    thread_stat_var_names = list(set(thread_stat_var_names))
    config_fleet.config['stat_var_names'] = thread_stat_var_names

    adam = fluid.optimizer.Adam(learning_rate=0.000005)
    adam = fleet.distributed_optimizer(adam, strategy=config_fleet.config)
    # adam = fleet.distributed_optimizer(adam, strategy={"use_cvm" : True, "adjust_ins_weight" : adjust_ins_weight, "scale_datanorm" : 1e-4, "dump_slot": True, "stat_var_names": thread_stat_var_names})
    # adam = fleet.distributed_optimizer(adam, strategy={"use_cvm" : True, "adjust_ins_weight" : adjust_ins_weight, "scale_datanorm" : 1e-4, "dump_slot": True, "stat_var_names": thread_stat_var_names, "fleet_desc_file": "reqi_fleet_desc"})
    adam.minimize([join_common_model.joint_cost, update_model.avg_cost], [scope2, scope3])

    join_common_model._train_program._fleet_opt["program_configs"][str(id(join_common_model.joint_cost.block.program))]["push_sparse"] = []

    join_save_params = ["join.batch_size", "join.batch_sum", "join.batch_square_sum",
                        "join_0.w_0", "join_0.b_0", "join_1.w_0", "join_1.b_0", "join_2.w_0", "join_2.b_0",
                        "join_3.w_0", "join_3.b_0", "join_4.w_0", "join_4.b_0", "join_5.w_0", "join_5.b_0",
                        "join_6.w_0", "join_6.b_0", "join_7.w_0", "join_7.b_0"]
    common_save_params = ["common.batch_size", "common.batch_sum", "common.batch_square_sum",
                         "common_0.w_0", "common_0.b_0", "common_1.w_0", "common_1.b_0", "common_2.w_0", "common_2.b_0",
                         "common_3.w_0", "common_3.b_0", "common_4.w_0", "common_4.b_0", "common_5.w_0", "common_5.b_0",
                         "common_6.w_0", "common_6.b_0", "common_7.w_0", "common_7.b_0"]
    update_save_params = ["fc_0.w_0", "fc_0.b_0", "fc_1.w_0", "fc_1.b_0",
                           "fc_2.w_0", "fc_2.b_0", "fc_3.w_0", "fc_3.b_0",
                           "fc_4.w_0", "fc_4.b_0", "fc_5.w_0", "fc_5.b_0"]

    if fleet.is_server():
        fleet.run_server()
    elif fleet.is_worker():
        with fluid.scope_guard(scope3):
            exe.run(update_model._startup_program)
        with fluid.scope_guard(scope2):
            exe.run(join_common_model._startup_program)
        
        configs = {"fs.default.name": config.fs_name,"hadoop.job.ugi": config.fs_ugi}
        hdfs_client = HDFSClient("$HADOOP_HOME", configs)

        save_first_base = config.save_first_base
        path = config.train_data_path
        online_pass_interval = fleet_util.get_online_pass_interval(config.days, config.hours, config.split_interval, config.split_per_pass, False) 
        pass_per_day = len(online_pass_interval)
        last_day, last_pass, last_path, xbox_base_key = [-1,-1,"",123]#fleet_util.get_last_save_model(config.output_path, config.fs_name, config.fs_ugi)
        reqi = True if last_day != -1 else False

        if config.need_reqi_changeslot and config.reqi_dnn_plugin_day >= last_day and config.reqi_dnn_plugin_pass >= last_pass:
            pass
            # reqi_changeslot(config.hdfs_dnn_plugin_path, join_save_params, common_save_params, update_save_params, scope2, scope3)
        fleet.init_worker()
        
        dataset, next_dataset, cur_path, next_path, start_train = [None] * 5
        days = os.popen("echo -n " + config.days).read().split(" ")#不换行输出
        hours = os.popen("echo -n " + config.hours).read().split(" ")
        for day_index in range(len(days)):
            day = days[day_index]
            if last_day != -1 and int(day) < last_day:
                continue
            for pass_index in range(1, pass_per_day + 1):
                dataset = next_dataset
                next_dataset = None
                cur_path = next_path
                next_path = None
                if (last_day != -1 and int(day) == last_day) and (last_pass != -1 and int(pass_index) < last_pass):
                    continue
                if reqi:
                    begin = time.time()
                    fleet_util.rank0_print("going to load model %s" % last_path)
                    if config.need_reqi_changeslot and config.reqi_dnn_plugin_day >= last_day and config.reqi_dnn_plugin_pass >= last_pass:
                        pass
                        # fleet.load_one_table(0, last_path)
                    else:
                        pass
                        # fleet_util.load_fleet_model(last_path)

                    end = time.time()
                    fleet_util.rank0_print("load model cost %s min" % ((end - begin) / 60.0))
                    reqi = False
                    if (last_day != -1 and int(day) == last_day) and (last_pass != -1 and int(pass_index) == last_pass):
                        continue

                fleet_util.rank0_print("===========going to train day/pass %s/%s===========" % (day, pass_index))

                if save_first_base:
                    fleet_util.rank0_print("save_first_base=True")
                    save_first_base = False
                    last_base_day, last_base_path, tmp_xbox_base_key = \
                        fleet_util.get_last_save_xbox_base(config.output_path, config.fs_name, config.fs_ugi)
                    if int(day) > last_base_day:
                        fleet_util.rank0_print("going to save xbox base model")
                        xbox_base_key = int(time.time())
                        cur = []
                        for interval in online_pass_interval[pass_index - 1]:
                            for p in path:
                                cur.append(p + "/" + day + "/" + interval)
                        save_delta(day, -1, xbox_base_key, cur, scope2, scope2, scope3,
                                   join_common_model, join_common_model, update_model, 
                                   join_save_params, common_save_params, update_save_params)
                    elif int(day) == last_base_day:
                        xbox_base_key = tmp_xbox_base_key
                        fleet_util.rank0_print("xbox base model exists")
                    else:
                        fleet_util.rank0_print("xbox base model exists")

                start_train = True
                train_begin = time.time()

                if dataset is not None:
                    begin = time.time()
                    dataset.wait_preload_done()
                    end = time.time()
                    fleet_util.rank0_print("wait data preload done cost %s min" % ((end - begin) / 60.0))

                if dataset is None:
                    cur_pass = online_pass_interval[pass_index - 1]
                    cur_path = []
                    for interval in cur_pass:
                        for p in path:
                            cur_path.append(p + "/" + day + "/" + interval)
                    fleet_util.rank0_print("data path: " + ",".join(cur_path))
                    #for i in cur_path:
                    ##    while not hdfs_client.is_exist(i + "/to.hadoop.done"):
                    #        fleet_util.rank0_print("wait for data ready: %s" % i)
                    #        time.sleep(config.check_exist_seconds)
                    my_filelist = ["part-00000_1"]#fleet.split_files(hdfs_ls(cur_path))

                    dataset = create_dataset(join_common_model._all_slots, my_filelist)
                    fleet_util.rank0_print("going to load into memory")
                    begin = time.time()
                    dataset.load_into_memory()
                    end = time.time()
                    fleet_util.rank0_print("load into memory done, cost %s min" % ((end - begin) / 60.0))

                fleet_util.rank0_print("going to global shuffle")
                begin = time.time()
                dataset.global_shuffle(fleet, config.shuffle_thread)
                end = time.time()
                fleet_util.rank0_print("global shuffle done, cost %s min, data size %s" % ((end - begin) / 60.0, dataset.get_shuffle_data_size(fleet)))
                get_data_max(dataset.get_shuffle_data_size())
                get_data_min(dataset.get_shuffle_data_size())

                if config.prefetch and (pass_index < pass_per_day or pass_index == pass_per_day and day_index < len(days) - 1):
                    if pass_index < pass_per_day:
                        next_pass = online_pass_interval[pass_index]
                        next_day = day
                    else:
                        next_pass = online_pass_interval[0]
                        next_day = days[day_index + 1]
                    next_path = []
                    for interval in next_pass:
                        for p in path:
                            next_path.append(p + "/" + next_day + "/" + interval)
                    next_data_ready = True
                    # for i in next_path:
                    #    if not hdfs_client.is_exist(i + "/to.hadoop.done"):
                    #        next_data_ready = False
                    #        fleet_util.rank0_print("next data not ready: %s" % i)
                    if not next_data_ready:
                        next_dataset = None
                    else:
                        my_filelist = my_filelist = ["part-00000_1"]#fleet.split_files(hdfs_ls(next_path))
                        next_dataset = create_dataset(join_common_model._all_slots, my_filelist)
                        fleet_util.rank0_print("next pass data preload %s " % ",".join(next_path))
                        next_dataset.preload_into_memory(config.preload_thread)

                join_cost, common_cost, update_cost = [0] * 3
                with fluid.scope_guard(scope2):
                    fleet_util.rank0_print("Begin join + common pass")
                    begin = time.time()
                    exe.train_from_dataset(join_common_model._train_program,
                                           dataset,
                                           scope2,
                                           thread=config.join_common_thread,
                                           debug=False)
                    end = time.time()
                    avg_cost = get_avg_cost_mins(end - begin)                    
                    fleet_util.rank0_print("avg train time %s mins" % avg_cost)
                    get_max_cost_mins(end - begin)
                    get_min_cost_mins(end - begin)
                    common_cost = avg_cost
                   
                    join_metric_list = list(join_common_model.join_auc_stat_list) + list(join_common_model.join_metric_list)
                    join_metric_types = ["int64"] * len(join_common_model.join_auc_stat_list) + ["float32"] * len(join_common_model.join_metric_list)
                    common_metric_list = list(join_common_model.common_auc_stat_list) + list(join_common_model.common_metric_list)
                    common_metric_types = ["int64"] * len(join_common_model.common_auc_stat_list) + ["float32"] * len(join_common_model.common_metric_list)
                    join_metric_str = get_global_metrics_str(scope2, join_metric_list, "join pass:")                    
                    common_metric_str = get_global_metrics_str(scope2, common_metric_list, "common pass:")
                    fleet_util.rank0_print(join_metric_str)
                    fleet_util.rank0_print(common_metric_str)
                    # write_global_metrics(day, pass_index, "join", join_metric_str)
                    # write_global_metrics(day, pass_index, "common", common_metric_str)

                    clear_metrics(scope2, join_metric_list, join_metric_types)
                    clear_metrics(scope2, common_metric_list, common_metric_types)
                    fleet_util.rank0_print("End join+common pass")

                if config.save_xbox_before_update and pass_index % config.save_delta_frequency == 0:
                    fleet_util.rank0_print("going to save delta model")
                    last_xbox_day, last_xbox_pass, last_xbox_path, _ = fleet_util.get_last_save_xbox(config.output_path,  config.fs_name, config.fs_ugi)
                    if int(day) < last_xbox_day or int(day) == last_xbox_day and int(pass_index) <= last_xbox_pass:
                        fleet_util.rank0_print("delta model exists")
                    else:
                        save_delta(day, pass_index, xbox_base_key, cur_path, scope2, scope2, scope3,
                                   join_common_model, join_common_model, update_model,
                                   join_save_params, common_save_params, update_save_params)

                with fluid.scope_guard(scope3):
                    fleet_util.rank0_print("Begin update pass")
                    begin = time.time()
                    exe.train_from_dataset(update_model._train_program,
                                           dataset,
                                           scope3,
                                           thread=config.update_thread,
                                           debug=False)
                    end = time.time()
                    avg_cost = get_avg_cost_mins(end - begin)
                    get_max_cost_mins(end - begin)
                    get_min_cost_mins(end - begin)
                    update_cost = avg_cost
                    
                    update_metric_list = list(update_model.auc_stat_list) + list(update_model.metric_list)
                    update_metric_types = ["int64"] * len(update_model.auc_stat_list) + ["float32"] * len(update_model.metric_list)
                    metric_str = get_global_metrics_str(scope3, update_metric_list, "update pass:")
                    fleet_util.rank0_print(metric_str)
                    #write_global_metrics(day, pass_index, "update", metric_str)

                    clear_metrics(scope3, update_metric_list, update_metric_types)
                    fleet_util.rank0_print("End update pass")

                begin = time.time()
                dataset.release_memory()
                end = time.time()
                fleet_util.rank0_print("release_memory cost %s min" % ((end - begin) / 60.0))

                if (pass_index % config.checkpoint_per_pass) == 0 and pass_index != pass_per_day:
                    begin = time.time()
                    #fleet_util.save_model(config.output_path, day, pass_index)
                    #fleet_util.write_model_donefile(config.output_path, day, pass_index, xbox_base_key, config.fs_name, config.fs_ugi)
                    end = time.time()
                    fleet_util.rank0_print("save model cost %s min" % ((end - begin) / 60.0))
                if not config.save_xbox_before_update and pass_index % config.save_delta_frequency == 0:
                    fleet_util.rank0_print("going to save delta model")
                    last_xbox_day, last_xbox_pass, last_xbox_path, _ = fleet_util.get_last_save_xbox(config.output_path,  config.fs_name, config.fs_ugi)
                    if int(day) < last_xbox_day or int(day) == last_xbox_day and int(pass_index) <= last_xbox_pass:
                        fleet_util.rank0_print("delta model exists")
                    else:
                        save_delta(day, pass_index, xbox_base_key, cur_path, scope2, scope2, scope3,
                                   join_common_model, join_common_model, update_model,
                                   join_save_params, common_save_params, update_save_params)

                train_end = time.time()
                train_cost = (train_end - train_begin) / 60.0
                other_cost = train_cost - join_cost - common_cost - update_cost
                fleet_util.rank0_print(\
                    "finished train day %s pass %s time cost:%s min job time cost"
                    ":[join:%s min][join_common:%s min][update:%s min][other:%s min]" \
                    % (day, pass_index, train_cost, join_cost, common_cost, update_cost, other_cost))
            
            xbox_base_key = int(time.time())
            if not start_train:
                continue

            fleet_util.rank0_print("shrink table")
            begin = time.time()
            fleet.shrink_sparse_table()
            fleet.shrink_dense_table(0.98, scope=scope2, table_id=1)
            fleet.shrink_dense_table(0.98, scope=scope2, table_id=2)
            fleet.shrink_dense_table(0.98, scope=scope3, table_id=3)
            end = time.time()
            fleet_util.rank0_print("shrink table done, cost %s min" % ((end - begin) / 60.0))

            fleet_util.rank0_print("going to save batch model/base xbox model")
            last_base_day, last_base_path, _ = fleet_util.get_last_save_xbox_base(config.output_path, config.fs_name, config.fs_ugi)
            nextday = int(days[day_index + 1])
            if nextday <= last_base_day:
                fleet_util.rank0_print("batch model/base xbox model exists")
            else:
                save_delta(nextday, -1, xbox_base_key, cur_path, exe, scope2, scope2, scope3,
                           join_common_model, join_common_model, update_model,
                           join_save_params, common_save_params, update_save_params)
                begin = time.time()
                #fleet_util.save_batch_model(config.output_path, nextday)
                #fleet_util.write_model_donefile(config.output_path, nextday, -1, xbox_base_key, config.fs_name, config.fs_ugi)
                end = time.time()
                fleet_util.rank0_print("save batch model cost %s min" % ((end - begin) / 60.0))
