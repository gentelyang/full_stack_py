#!/bin/#!/usr/bin/env bash
set -xe

if [[ $# -lt 4 ]]; then
  echo "Usage: "
  echo "CUDA_VISIBLE_DEVICES=0 bash run.sh speed 32 model_name sp /ssd1/liyang/benchmark/benchmark/models"
  exit
fi

function _set_params() {
  index=$1
  base_batch_size=$2
  model_name=$3
  run_mode=${4:-"sp"}
  run_log_root=${5:-$(pwd)}

  skip_steps=2
  keyword="elapse"
  position=-2
  model_mode=0


  device=${CUDA_VISIBLE_DEVICES//,/ }
  arr=($device)
  num_gpu_devices=${#arr[*]}

  if [ $run_mode = "sp" ]; then
    batch_size=`expr $base_batch_size \* $num_gpu_devices`
  else
    batch_size=$base_batch_size
  fi
  log_file=${run_log_root}/${model_name}_${index}_${num_gpu_devices}_${run_mode}
  log_parse_file=${log_file}

}

function _set_env() {
  #开启gc
  export FLAGS_eager_delete_tensor_gb=0.0
  export FLAGS_fraction_of_gpu_memory_to_use=0.98
  if [[ ${model_name} == "ResNet50" && ${num_gpu_devices} == 1 ]]; then
    export FLAGS_cudnn_exhaustive_search=1
  fi

}

function _train() {
    echo "current CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES, gpus=$num_gpu_devices, batch_size=$batch_size"
    WORK_ROOT=$PWD
    num_epochs=2
    echo "${model_name}, batch_size: ${batch_size}"
    if echo {ResNet50 ResNet101} | grep -w $model_name &>/dev/null
    then
       train_cmd="  --model=${model_name} \
           --batch_size=${batch_size} \
           --total_images=1281167 \
           --class_dim=1000 \
           --image_shape=3,224,224 \
           --model_save_dir=output/ \
           --lr_strategy=piecewise_decay \
           --num_epochs=${num_epochs} \
           --lr=0.1 \
           --l2_decay=1e-4"
    elif echo {SE_ResNeXt50_32x4d} | grep -w $model_name &>/dev/null
    then
        train_cmd=" --model=${model_name} \
           --batch_size=${batch_size} \
           --total_images=1281167 \
           --class_dim=1000 \
           --image_shape=3,224,224 \
           --model_save_dir=output/ \
           --data_dir=data/ILSVRC2012 \
           --lr_strategy=cosine_decay \
           --lr=0.1 \
           --l2_decay=1.2e-4 \
           --num_epochs=${num_epochs}"
    else
        echo "model: $model_name not support!"
	exit
    fi
  case ${run_mode} in
  sp) train_cmd="python -u train.py "${train_cmd} ;;
  mp)
    train_cmd="python -m paddle.distributed.launch --log_dir=./mylog --selected_gpus=${CUDA_VISIBLE_DEVICES} train.py "${train_cmd}
    log_parse_file="mylog/worklog.0" ;;
  *) echo "choose run_mode(sp or mp)"; exit 1;
  esac

  ${train_cmd} > ${log_file} 2>&1 &
  train_pid=$!
  sleep 300
  kill -9 `ps -ef|grep python|awk '{print $2}'`

  if [ $run_mode = "mp" -a -d mylog ]; then
    rm ${log_file}
    cp mylog/worklog.0 ${log_file}
  fi

  cd ${WORK_ROOT}


}

source run_model.sh

_set_params $@
_set_env
_run
