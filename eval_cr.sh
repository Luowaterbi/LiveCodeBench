# model=$1

python -m lcb_runner.runner.main \
    --model Qwen/Qwen2.5-Coder-32B-Instruct \
    --local_model_path /mnt/jfs/ckpt/checkpoints/Qwen2.5-Coder-32B-Instruct \
    --scenario selfrepair \
    --evaluate \
    --num_process_evaluate 180 \
    --tensor_parallel_size 4 \
    --start_date \
    --codegen_n 10 \
    --n 1 \
    # --student_model Qwen/Qwen2.5-Coder-7B-Instruct \
    # --gar /home/i-luoxianzhen/GAR/LiveCodeBench/output/Qwen2.5-Coder-Ins-32B/gar.json

    # --continue_existing \