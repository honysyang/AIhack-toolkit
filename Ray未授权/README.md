# Vulnerability Name
Unauthorized Access Vulnerability in Ray Framework

## Description of Ray Framework
The Ray framework is an open-source framework widely used in distributed applications, developed by the UC Berkeley RISELab. It aims to simplify distributed computing, enabling developers to easily perform scalable machine learning and parallel computing tasks on single machines or clusters.

Currently, the Ray framework is often combined with the vLLM framework, commonly used to implement multi-machine, multi-GPU distributed online large model inference. With its efficient distributed task scheduling and resource management capabilities, the Ray framework is widely applied in AI scenarios such as hyperparameter tuning for model training, scientific computing, and distributed model training.

## Data
- https://docs.ray.io/en/latest/index.html
- https://github.com/ray-project/ray

## Vulnerability Description
The Ray framework is often integrated with the vLLM framework. When the `dashboard-host` of Ray is configured as `0.0.0.0`, an unauthorized access vulnerability exists. Attackers can exploit this vulnerability to access API interfaces, enabling them to steal critical information, maliciously delete or stop tasks, and even execute commands.

## Manufacturer
Anyscale

## Version
All versions of the Ray framework prior to 2.46

## Vulnerability Reproduction
### 1. Local environment deployment
```bash
pip install -U "ray[default]"   # Here, the latest version 2.46.0 is installed by default, and you can also specify the version: pip install -U "ray[default]==2.9.3"
```

2.Running Environment
```bash
ray start --head --dashboard-host=0.0.0.0
```

1.Run the vulnerability exploitation code.
```bash
python3 exp.py --host http://10.0.2.15:8265 --cmd "ls"     //cmd It can be any code.
```
