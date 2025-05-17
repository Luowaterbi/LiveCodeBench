#!/bin/bash

# 设置日志文件
log_file="empty.log"

# 清空日志文件
> "$log_file"

# 查找并遍历包含checkpoint的目录
find ./output -type d -name "*checkpoint*" | while read dir; do
    
    model_name=$(basename "$dir")

    # 跳过包含codegemma的目录
    if [[ "$model_name" == *"codegemma"* ]]; then
        echo $model_name >> "$log_file"
        continue
    fi
    
    # 检查目录是否为空
    if [ -z "$(ls -A "$dir")" ]; then
        echo $model_name >> "$log_file"
    else
        # 这里替换为你需要执行的命令
        echo "Processing $dir"
        python -m lcb_runner.runner.main \
            --model ${model_name} \
            --scenario codegeneration \
            --continue_existing \
            --continue_existing_with_eval \
            --evaluate \
            --num_process_evaluate 128 \
            --release_version release_v5 \
            --start_date
    fi
done