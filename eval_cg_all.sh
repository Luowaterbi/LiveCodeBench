#!/bin/bash

# 基础路径
BASE_PATH="/mnt/jfs/xysj/code/checkpoints"

# 检查基础路径是否存在
if [ ! -d "$BASE_PATH" ]; then
    echo "Error: Directory $BASE_PATH does not exist"
    exit 1
fi
echo "start eval cg all"
# 遍历所有模型文件夹
for model_dir in "$BASE_PATH"/*/; do
    # 如果model_dir包含gemma跳过
    if [[ "$model_dir" == *gemma* ]]; then
        continue
    fi
    if [ -d "$model_dir" ]; then
        model_name=$(basename "$model_dir")
        echo "Processing model: $model_name"
        
        # 遍历每个模型文件夹下的checkpoint文件
        for checkpoint_dir in "$model_dir"/*/; do
            if [ -d "$checkpoint_dir" ]; then
                checkpoint_name=$(basename "$checkpoint_dir")
                echo "Found checkpoint: $checkpoint_name"
                
                python -m lcb_runner.runner.main \
                    --model $model_name-$checkpoint_name \
                    --local_model_path $checkpoint_dir \
                    --scenario codegeneration \
                    --release_version release_v5 \
                    --tensor_parallel_size 8 \
                    --start_date ;
                
                if [ $? -ne 0 ]; then
                    echo "Error: Failed to evaluate model $model_name-$checkpoint_name" | tee -a "eval_cg_all_wrong.log"
                fi
            fi
        done
    fi
done