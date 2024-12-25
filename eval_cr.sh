model=$1

# python -m lcb_runner.runner.main \
#     --model DeepSeek-V2.5-1210 \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/DeepSeek-V2.5-1210 \
#     --scenario selfrepair \
#     --evaluate \
#     --continue_existing \
#     --num_process_evaluate 180 \
#     --tensor_parallel_size 4 \
#     --start_date True \
#     --codegen_n 10 \
#     --n 1 \
#     --student_model Qwen/Qwen2.5-Coder-7B-Instruct \
#     --teacher_prompt oracle


model_size=$1
tensor_parallel_size=8
if [[ $model_size == "7" ]]; then
    tensor_parallel_size=4
fi
python -m lcb_runner.runner.main \
    --model Qwen/${model} \
    --local_model_path /mnt/jfs/ckpt/checkpoints/${model} \
    --use_cache --scenario codegeneration \
    --evaluate \
    --num_process_evaluate 180 \
    --continue_existing_with_eval \
    --release_version release_v4 \
    --tensor_parallel_size ${tensor_parallel_size} \
    --start_date True && \
python -m lcb_runner.evaluation.compute_scores \
    --eval_all_file output/${model}/Scenario.codegeneration_10_0.2_eval_all.json