# scale-sdk

python library for skt scale

## Install

```bash
pip install skt-scale
```

## Config set up

```bash
$ scalecli config set url http://0.0.0.0:13202
Updated config

$ scalecli login
Enter paas id: user_id
Enter paas password:
login success
```

## Usage

### sdk

source.py

```python
# -*- coding: utf-8 -*-
# pylint disable

import tensorflow as tf


tf.logging.set_verbosity(tf.logging.INFO)


def input_fn():
    features = tf.data.Dataset.from_tensors([[1.0]]).repeat()
    labels = tf.data.Dataset.from_tensors(1.0).repeat()
    return tf.data.Dataset.zip((features, labels))


def model_fn(features, labels, mode, params):
    layer = tf.layers.Dense(1)
    logits = layer(features)
    loss = tf.losses.mean_squared_error(
        labels=labels, predictions=tf.reshape(logits, [])
    )
    if mode == tf.estimator.ModeKeys.TRAIN:
        step = tf.train.get_or_create_global_step()
        train_op = tf.train.AdamOptimizer().minimize(loss, step)
        return tf.estimator.EstimatorSpec(
            mode=mode, loss=loss, train_op=train_op
        )


def main():
    estimator = tf.estimator.Estimator(model_fn=model_fn)
    estimator.train(input_fn=input_fn, steps=1000)


main()
```

cpu_example.py

```python
import os
import random
import string
from scale import Client


def main():
    client = Client()
    random_job_name = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    image_name = "scale/tensorflow:1.14-v1-py3"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    source_file = os.path.join(current_dir, "source.py")
    client.create_job(
        job_name=random_job_name, image_name=image_name, source_file=source_file
    )


if __name__ == "__main__":
    main()
```

gpu_example.py
```python
import os
import random
import string
from scale import Client


def main():
    client = Client(
        host="http://0.0.0.0:13202", user_id="user", token="secret_token"
    )
    random_job_name = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    image_name = "scale/tensorflow:1.14-v1-py3"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    source_file = os.path.join(current_dir, "source.py")
    gpu_type = "Tesla_P100-PCIE-16GB"
    client.create_job(
        job_name=random_job_name,
        image_name=image_name,
        source_file=source_file,
        gpu_type=gpu_type,
        cpu=1,
        mem=2,
        gpu=1,
    )


if __name__ == "__main__":
    main()
```

result

```bash
$ python test.py
job id:  78305d8f-06bd-495b-91fc-0f429a9f0dae
wait for container to start
[SYSTEM] Train start.
[2020-03-05 07:32:05:1] WARNING: Logging before flag parsing goes to stderr.
[2020-03-05 07:32:05:2] W0305 07:32:00.048396 139884626732864 deprecation_wrapper.py:119] From app.py:7: The name tf.logging.set_verbosity is deprecated. Please use tf.compat.v1.logging.set_verbosity instead.
[2020-03-05 07:32:05:3] 
[2020-03-05 07:32:05:4] W0305 07:32:00.048584 139884626732864 deprecation_wrapper.py:119] From app.py:7: The name tf.logging.INFO is deprecated. Please use tf.compat.v1.logging.INFO instead.
[2020-03-05 07:32:05:5] 
[2020-03-05 07:32:05:6] I0305 07:32:00.048879 139884626732864 estimator.py:1790] Using default config.
[2020-03-05 07:32:05:7] W0305 07:32:00.049320 139884626732864 estimator.py:1811] Using temporary folder as model directory: /tmp/tmpoliwaf9g
[2020-03-05 07:32:05:8] I0305 07:32:00.049926 139884626732864 estimator.py:209] Using config: {'_model_dir': '/tmp/tmpoliwaf9g', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
[2020-03-05 07:32:05:9] graph_options {
[2020-03-05 07:32:05:10]   rewrite_options {
[2020-03-05 07:32:05:11]     meta_optimizer_iterations: ONE
[2020-03-05 07:32:05:12]   }
[2020-03-05 07:32:05:13] }
[2020-03-05 07:32:05:14] , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_service': None, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7f3947dc7cc0>, '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
[2020-03-05 07:32:05:15] W0305 07:32:00.050079 139884626732864 model_fn.py:630] Estimator's model_fn (<function model_fn at 0x7f3947e21d90>) includes params argument, but params are not passed to Estimator.
[2020-03-05 07:32:05:16] W0305 07:32:00.068118 139884626732864 deprecation.py:323] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/training/training_util.py:236: Variable.initialized_value (from tensorflow.python.ops.variables) is deprecated and will be removed in a future version.
[2020-03-05 07:32:05:17] Instructions for updating:
[2020-03-05 07:32:05:18] Use Variable.read_value. Variables in 2.X are initialized automatically both in eager and graph (inside tf.defun) contexts.
[2020-03-05 07:32:05:19] I0305 07:32:00.129392 139884626732864 estimator.py:1145] Calling model_fn.
[2020-03-05 07:32:05:20] W0305 07:32:00.129571 139884626732864 deprecation_wrapper.py:119] From app.py:17: The name tf.layers.Dense is deprecated. Please use tf.compat.v1.layers.Dense instead.
[2020-03-05 07:32:05:21] 
[2020-03-05 07:32:05:22] W0305 07:32:00.131662 139884626732864 deprecation.py:506] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/init_ops.py:1251: calling VarianceScaling.__init__ (from tensorflow.python.ops.init_ops) with dtype is deprecated and will be removed in a future version.
[2020-03-05 07:32:05:23] Instructions for updating:
[2020-03-05 07:32:05:24] Call initializer instance with the dtype argument instead of passing it to the constructor
[2020-03-05 07:32:05:25] W0305 07:32:00.662171 139884626732864 deprecation_wrapper.py:119] From app.py:19: The name tf.losses.mean_squared_error is deprecated. Please use tf.compat.v1.losses.mean_squared_error instead.
[2020-03-05 07:32:05:26] 
[2020-03-05 07:32:05:27] W0305 07:32:00.675267 139884626732864 deprecation.py:323] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/losses/losses_impl.py:121: add_dispatch_support.<locals>.wrapper (from tensorflow.python.ops.array_ops) is deprecated and will be removed in a future version.
[2020-03-05 07:32:05:28] Instructions for updating:
[2020-03-05 07:32:05:29] Use tf.where in 2.0, which has the same broadcast rule as np.where
[2020-03-05 07:32:05:30] W0305 07:32:00.679626 139884626732864 deprecation_wrapper.py:119] From app.py:23: The name tf.train.get_or_create_global_step is deprecated. Please use tf.compat.v1.train.get_or_create_global_step instead.
[2020-03-05 07:32:05:31] 
[2020-03-05 07:32:05:32] W0305 07:32:00.679796 139884626732864 deprecation_wrapper.py:119] From app.py:24: The name tf.train.AdamOptimizer is deprecated. Please use tf.compat.v1.train.AdamOptimizer instead.
[2020-03-05 07:32:05:33] 
[2020-03-05 07:32:05:34] I0305 07:32:00.886904 139884626732864 estimator.py:1147] Done calling model_fn.
[2020-03-05 07:32:05:35] I0305 07:32:00.888659 139884626732864 basic_session_run_hooks.py:541] Create CheckpointSaverHook.
[2020-03-05 07:32:05:36] I0305 07:32:01.269991 139884626732864 monitored_session.py:240] Graph was finalized.
[2020-03-05 07:32:05:37] 2020-03-05 07:32:01.270457: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[2020-03-05 07:32:05:38] 2020-03-05 07:32:01.286304: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcuda.so.1
[2020-03-05 07:32:05:39] 2020-03-05 07:32:01.290929: E tensorflow/stream_executor/cuda/cuda_driver.cc:318] failed call to cuInit: CUDA_ERROR_NO_DEVICE: no CUDA-capable device is detected
[2020-03-05 07:32:05:40] 2020-03-05 07:32:01.290978: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:163] no NVIDIA GPU device is present: /dev/nvidia0 does not exist
[2020-03-05 07:32:05:41] 2020-03-05 07:32:01.348206: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2599925000 Hz
[2020-03-05 07:32:05:42] 2020-03-05 07:32:01.353221: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x227ec10 executing computations on platform Host. Devices:
[2020-03-05 07:32:05:43] 2020-03-05 07:32:01.353270: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): <undefined>, <undefined>
[2020-03-05 07:32:05:44] 2020-03-05 07:32:01.448839: W tensorflow/compiler/jit/mark_for_compilation_pass.cc:1412] (One-time warning): Not using XLA:CPU for cluster because envvar TF_XLA_FLAGS=--tf_xla_cpu_global_jit was not set.  If you want XLA:CPU, either set that envvar, or use experimental_jit_scope to enable XLA:CPU.  To confirm that XLA is active, pass --vmodule=xla_compilation_cache=1 (as a proper command-line flag, not via TF_XLA_FLAGS) or set the envvar XLA_FLAGS=--xla_hlo_profile.
[2020-03-05 07:32:05:45] I0305 07:32:01.471862 139884626732864 session_manager.py:500] Running local_init_op.
[2020-03-05 07:32:05:46] I0305 07:32:01.475904 139884626732864 session_manager.py:502] Done running local_init_op.
[2020-03-05 07:32:05:47] I0305 07:32:01.870096 139884626732864 basic_session_run_hooks.py:606] Saving checkpoints for 0 into /tmp/tmpoliwaf9g/model.ckpt.
[2020-03-05 07:32:05:48] I0305 07:32:02.093250 139884626732864 basic_session_run_hooks.py:262] loss = 0.000752323, step = 1
[2020-03-05 07:32:05:49] I0305 07:32:02.268341 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 569.372
[2020-03-05 07:32:05:50] I0305 07:32:02.269199 139884626732864 basic_session_run_hooks.py:260] loss = 2.3888447e-11, step = 101 (0.176 sec)
[2020-03-05 07:32:05:51] I0305 07:32:02.458733 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 524.98
[2020-03-05 07:32:05:52] I0305 07:32:02.459607 139884626732864 basic_session_run_hooks.py:260] loss = 2.877698e-13, step = 201 (0.190 sec)
[2020-03-05 07:32:05:53] I0305 07:32:02.648005 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 529.569
[2020-03-05 07:32:05:54] I0305 07:32:02.649275 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 301 (0.190 sec)
[2020-03-05 07:32:05:55] I0305 07:32:02.774062 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 791.023
[2020-03-05 07:32:05:56] I0305 07:32:02.774733 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 401 (0.125 sec)
[2020-03-05 07:32:05:57] I0305 07:32:02.866282 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 1082.71
[2020-03-05 07:32:05:58] I0305 07:32:02.866768 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 501 (0.092 sec)
[2020-03-05 07:32:05:59] I0305 07:32:02.965521 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 1008.81
[2020-03-05 07:32:05:60] I0305 07:32:02.966336 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 601 (0.100 sec)
[2020-03-05 07:32:05:61] I0305 07:32:03.069179 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 963.884
[2020-03-05 07:32:05:62] I0305 07:32:03.069773 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 701 (0.103 sec)
[2020-03-05 07:32:05:63] I0305 07:32:03.154792 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 1168.15
[2020-03-05 07:32:05:64] I0305 07:32:03.155704 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 801 (0.086 sec)
[2020-03-05 07:32:05:65] I0305 07:32:03.266279 139884626732864 basic_session_run_hooks.py:692] global_step/sec: 897.621
[2020-03-05 07:32:05:66] I0305 07:32:03.267081 139884626732864 basic_session_run_hooks.py:260] loss = 0.0, step = 901 (0.111 sec)
[2020-03-05 07:32:05:67] I0305 07:32:03.354782 139884626732864 basic_session_run_hooks.py:606] Saving checkpoints for 1000 into /tmp/tmpoliwaf9g/model.ckpt.
[2020-03-05 07:32:05:68] I0305 07:32:03.395870 139884626732864 estimator.py:368] Loss for final step: 0.0.
[SYSTEM] Train completed.
```

### cli

```bash
scalecli create_job \
 --job_name=$RANDOM \
 --image_name=scale/tensorflow:1.14-v1-py3 \
 --source_file=./sample.py \
 --gpu_type=Tesla_P100-PCIE-16GB \
 --mem=2 \
 --gpu=1 \
 --cpu=1
job id:  43f7854d-fb58-42c3-b544-9c624a5ffdd9
wait for container to start
SYSTEM] Train start.
[2020-03-05 07:27:13:1] WARNING: Logging before flag parsing goes to stderr.
[2020-03-05 07:27:13:2] W0305 07:27:06.527273 139771468314432 deprecation_wrapper.py:119] From app.py:7: The name tf.logging.set_verbosity is deprecated. Please use tf.compat.v1.logging.set_verbosity instead.
[2020-03-05 07:27:13:3] 
[2020-03-05 07:27:13:4] W0305 07:27:06.527491 139771468314432 deprecation_wrapper.py:119] From app.py:7: The name tf.logging.INFO is deprecated. Please use tf.compat.v1.logging.INFO instead.
[2020-03-05 07:27:13:5] 
[2020-03-05 07:27:13:6] I0305 07:27:06.527805 139771468314432 estimator.py:1790] Using default config.
[2020-03-05 07:27:13:7] W0305 07:27:06.528320 139771468314432 estimator.py:1811] Using temporary folder as model directory: /tmp/tmpkaaysn7y
[2020-03-05 07:27:13:8] I0305 07:27:06.528981 139771468314432 estimator.py:209] Using config: {'_model_dir': '/tmp/tmpkaaysn7y', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
[2020-03-05 07:27:13:9] graph_options {
[2020-03-05 07:27:13:10]   rewrite_options {
[2020-03-05 07:27:13:11]     meta_optimizer_iterations: ONE
[2020-03-05 07:27:13:12]   }
[2020-03-05 07:27:13:13] }
[2020-03-05 07:27:13:14] , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_service': None, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7f1f0328db00>, '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
[2020-03-05 07:27:13:15] W0305 07:27:06.529155 139771468314432 model_fn.py:630] Estimator's model_fn (<function model_fn at 0x7f1f032e4d90>) includes params argument, but params are not passed to Estimator.
[2020-03-05 07:27:13:16] W0305 07:27:06.558148 139771468314432 deprecation.py:323] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/training/training_util.py:236: Variable.initialized_value (from tensorflow.python.ops.variables) is deprecated and will be removed in a future version.
[2020-03-05 07:27:13:17] Instructions for updating:
[2020-03-05 07:27:13:18] Use Variable.read_value. Variables in 2.X are initialized automatically both in eager and graph (inside tf.defun) contexts.
[2020-03-05 07:27:13:19] I0305 07:27:06.628736 139771468314432 estimator.py:1145] Calling model_fn.
[2020-03-05 07:27:13:20] W0305 07:27:06.628922 139771468314432 deprecation_wrapper.py:119] From app.py:17: The name tf.layers.Dense is deprecated. Please use tf.compat.v1.layers.Dense instead.
[2020-03-05 07:27:13:21] 
[2020-03-05 07:27:13:22] W0305 07:27:06.630848 139771468314432 deprecation.py:506] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/init_ops.py:1251: calling VarianceScaling.__init__ (from tensorflow.python.ops.init_ops) with dtype is deprecated and will be removed in a future version.
[2020-03-05 07:27:13:23] Instructions for updating:
[2020-03-05 07:27:13:24] Call initializer instance with the dtype argument instead of passing it to the constructor
[2020-03-05 07:27:13:25] W0305 07:27:07.550607 139771468314432 deprecation_wrapper.py:119] From app.py:19: The name tf.losses.mean_squared_error is deprecated. Please use tf.compat.v1.losses.mean_squared_error instead.
[2020-03-05 07:27:13:26] 
[2020-03-05 07:27:13:27] W0305 07:27:07.573339 139771468314432 deprecation.py:323] From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/losses/losses_impl.py:121: add_dispatch_support.<locals>.wrapper (from tensorflow.python.ops.array_ops) is deprecated and will be removed in a future version.
[2020-03-05 07:27:13:28] Instructions for updating:
[2020-03-05 07:27:13:29] Use tf.where in 2.0, which has the same broadcast rule as np.where
[2020-03-05 07:27:13:30] W0305 07:27:07.580497 139771468314432 deprecation_wrapper.py:119] From app.py:23: The name tf.train.get_or_create_global_step is deprecated. Please use tf.compat.v1.train.get_or_create_global_step instead.
[2020-03-05 07:27:13:31] 
[2020-03-05 07:27:13:32] W0305 07:27:07.580755 139771468314432 deprecation_wrapper.py:119] From app.py:24: The name tf.train.AdamOptimizer is deprecated. Please use tf.compat.v1.train.AdamOptimizer instead.
[2020-03-05 07:27:13:33] 
[2020-03-05 07:27:13:34] I0305 07:27:07.863347 139771468314432 estimator.py:1147] Done calling model_fn.
[2020-03-05 07:27:13:35] I0305 07:27:07.865198 139771468314432 basic_session_run_hooks.py:541] Create CheckpointSaverHook.
[2020-03-05 07:27:13:36] I0305 07:27:08.189621 139771468314432 monitored_session.py:240] Graph was finalized.
[2020-03-05 07:27:13:37] 2020-03-05 07:27:08.190115: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[2020-03-05 07:27:13:38] 2020-03-05 07:27:08.258076: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcuda.so.1
[2020-03-05 07:27:13:39] 2020-03-05 07:27:08.554655: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x3a1f340 executing computations on platform CUDA. Devices:
[2020-03-05 07:27:13:40] 2020-03-05 07:27:08.554703: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): Tesla P100-PCIE-16GB, Compute Capability 6.0
[2020-03-05 07:27:13:41] 2020-03-05 07:27:08.559790: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2599925000 Hz
[2020-03-05 07:27:13:42] 2020-03-05 07:27:08.565466: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x50b3880 executing computations on platform Host. Devices:
[2020-03-05 07:27:13:43] 2020-03-05 07:27:08.565508: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): <undefined>, <undefined>
[2020-03-05 07:27:13:44] 2020-03-05 07:27:08.568802: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1640] Found device 0 with properties:
[2020-03-05 07:27:13:45] name: Tesla P100-PCIE-16GB major: 6 minor: 0 memoryClockRate(GHz): 1.3285
[2020-03-05 07:27:13:46] pciBusID: 0000:83:00.0
[2020-03-05 07:27:13:47] 2020-03-05 07:27:08.569401: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcudart.so.10.0
[2020-03-05 07:27:13:48] 2020-03-05 07:27:08.572929: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcublas.so.10.0
[2020-03-05 07:27:13:49] 2020-03-05 07:27:08.575969: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcufft.so.10.0
[2020-03-05 07:27:13:50] 2020-03-05 07:27:08.576603: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcurand.so.10.0
[2020-03-05 07:27:13:51] 2020-03-05 07:27:08.580630: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcusolver.so.10.0
[2020-03-05 07:27:13:52] 2020-03-05 07:27:08.583665: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcusparse.so.10.0
[2020-03-05 07:27:13:53] 2020-03-05 07:27:08.591141: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcudnn.so.7
[2020-03-05 07:27:13:54] 2020-03-05 07:27:08.595661: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1763] Adding visible gpu devices: 0
[2020-03-05 07:27:13:55] 2020-03-05 07:27:08.595717: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcudart.so.10.0
[2020-03-05 07:27:13:56] 2020-03-05 07:27:08.598404: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1181] Device interconnect StreamExecutor with strength 1 edge matrix:
[2020-03-05 07:27:13:57] 2020-03-05 07:27:08.598433: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1187]      0
[2020-03-05 07:27:13:58] 2020-03-05 07:27:08.598454: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1200] 0:   N
[2020-03-05 07:27:13:59] 2020-03-05 07:27:08.602791: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1326] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 15216 MB memory) -> physical GPU (device: 0, name: Tesla P100-PCIE-16GB, pci bus id: 0000:83:00.0, compute capability: 6.0)
[2020-03-05 07:27:13:60] 2020-03-05 07:27:09.446952: W tensorflow/compiler/jit/mark_for_compilation_pass.cc:1412] (One-time warning): Not using XLA:CPU for cluster because envvar TF_XLA_FLAGS=--tf_xla_cpu_global_jit was not set.  If you want XLA:CPU, either set that envvar, or use experimental_jit_scope to enable XLA:CPU.  To confirm that XLA is active, pass --vmodule=xla_compilation_cache=1 (as a proper command-line flag, not via TF_XLA_FLAGS) or set the envvar XLA_FLAGS=--xla_hlo_profile.
[2020-03-05 07:27:13:61] I0305 07:27:09.449524 139771468314432 session_manager.py:500] Running local_init_op.
[2020-03-05 07:27:13:62] I0305 07:27:09.453503 139771468314432 session_manager.py:502] Done running local_init_op.
[2020-03-05 07:27:13:63] I0305 07:27:09.566854 139771468314432 basic_session_run_hooks.py:606] Saving checkpoints for 0 into /tmp/tmpkaaysn7y/model.ckpt.
[2020-03-05 07:27:13:64] 2020-03-05 07:27:09.657372: I tensorflow/stream_executor/platform/default/dso_loader.cc:42] Successfully opened dynamic library libcublas.so.10.0
[2020-03-05 07:27:13:65] I0305 07:27:09.957408 139771468314432 basic_session_run_hooks.py:262] loss = 3.136012, step = 0
[2020-03-05 07:27:13:66] I0305 07:27:10.459863 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 198.666
[2020-03-05 07:27:13:67] I0305 07:27:10.461008 139771468314432 basic_session_run_hooks.py:260] loss = 2.4800994, step = 100 (0.504 sec)
[2020-03-05 07:27:13:68] I0305 07:27:10.877429 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 239.453
[2020-03-05 07:27:13:69] I0305 07:27:10.878589 139771468314432 basic_session_run_hooks.py:260] loss = 1.9325358, step = 200 (0.418 sec)
[2020-03-05 07:27:13:70] I0305 07:27:11.364231 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 205.424
[2020-03-05 07:27:13:71] I0305 07:27:11.365450 139771468314432 basic_session_run_hooks.py:260] loss = 1.4822296, step = 300 (0.487 sec)
[2020-03-05 07:27:13:72] I0305 07:27:11.856773 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 203.032
[2020-03-05 07:27:13:73] I0305 07:27:11.858273 139771468314432 basic_session_run_hooks.py:260] loss = 1.1173365, step = 400 (0.493 sec)
[2020-03-05 07:27:13:74] I0305 07:27:12.346587 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 204.159
[2020-03-05 07:27:13:75] I0305 07:27:12.347812 139771468314432 basic_session_run_hooks.py:260] loss = 0.82648915, step = 500 (0.490 sec)
[2020-03-05 07:27:13:76] I0305 07:27:12.777956 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 231.805
[2020-03-05 07:27:13:77] I0305 07:27:12.779240 139771468314432 basic_session_run_hooks.py:260] loss = 0.59887236, step = 600 (0.431 sec)
[2020-03-05 07:27:13:78] I0305 07:27:13.067498 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 345.287
[2020-03-05 07:27:13:79] I0305 07:27:13.068227 139771468314432 basic_session_run_hooks.py:260] loss = 0.42432293, step = 700 (0.289 sec)
[2020-03-05 07:27:13:80] I0305 07:27:13.468511 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 249.398
[2020-03-05 07:27:13:81] I0305 07:27:13.469309 139771468314432 basic_session_run_hooks.py:260] loss = 0.29343566, step = 800 (0.401 sec)
[2020-03-05 07:27:13:82] I0305 07:27:13.955026 139771468314432 basic_session_run_hooks.py:692] global_step/sec: 205.564
[2020-03-05 07:27:13:83] I0305 07:27:13.956063 139771468314432 basic_session_run_hooks.py:260] loss = 0.19767413, step = 900 (0.487 sec)
[2020-03-05 07:27:14:84] I0305 07:27:14.172374 139771468314432 basic_session_run_hooks.py:606] Saving checkpoints for 1000 into /tmp/tmpkaaysn7y/model.ckpt.
[2020-03-05 07:27:14:85] I0305 07:27:14.248917 139771468314432 estimator.py:368] Loss for final step: 0.13003506.
[SYSTEM] Train completed.
```
