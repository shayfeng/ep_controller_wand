#!/bin/bash

# 1. 切换到程序所在的目录
cd /home/shay/01project/ep_controller_wand

# --- Conda 环境设置（使用您确认的路径）---

# 2. 显式加载 Conda 初始化脚本
source /home/shay/miniconda3/etc/profile.d/conda.sh

# 3. 激活所需的 Conda 环境
conda activate ros_nav

# ----------------------------------

# 4. 执行您的 Python 程序
# 激活环境后，直接使用 'python' 命令
python main.py --port /dev/ttyACM0 --bps 460800
