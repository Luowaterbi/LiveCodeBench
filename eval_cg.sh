# python -m lcb_runner.evaluation.compute_scores --eval_all_file output/DSCoder-6.7b-Ins/Scenario.codegeneration_10_0.2_ctf_eval_all.json
# python -m lcb_runner.evaluation.compute_scores --eval_all_file output/DSCoder-6.7b-Ins/Scenario.codegeneration_10_0.2_easy_eval_all.json
# python -m lcb_runner.evaluation.compute_scores --eval_all_file output/DSCoder-33b-Ins/Scenario.codegeneration_10_0.2_ctf_eval_all.json
# python -m lcb_runner.evaluation.compute_scores --eval_all_file output/DSCoder-33b-Ins/Scenario.codegeneration_10_0.2_easy_eval_all.json





# python -m lcb_runner.runner.main \
#     --model deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/DeepSeek-Coder-V2-Lite-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --tensor_parallel_size 8 \
#     --suffix _easy;

# python -m lcb_runner.runner.main \
#     --model deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/DeepSeek-Coder-V2-Lite-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version ctf \
#     --tensor_parallel_size 8 \
#     --suffix _ctf;

# python -m lcb_runner.runner.main \
#     --model deepseek-ai/DeepSeek-V2-Lite-Chat \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/DeepSeek-V2-Lite-Chat \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --tensor_parallel_size 8 \
#     --suffix _easy;

# python -m lcb_runner.runner.main \
#     --model deepseek-ai/DeepSeek-V2-Lite-Chat \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/DeepSeek-V2-Lite-Chat \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version ctf \
#     --tensor_parallel_size 8 \
#     --suffix _ctf;

# python -m lcb_runner.runner.main \
#     --model Qwen/Qwen2.5-7B-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/Qwen2.5-7B-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --tensor_parallel_size 4 \
#     --suffix _easy;

# python -m lcb_runner.runner.main \
#     --model Qwen/Qwen2.5-7B-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/Qwen2.5-7B-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version ctf \
#     --tensor_parallel_size 4 \
#     --suffix _ctf;

# python -m lcb_runner.runner.main \
#     --model meta-llama/Meta-Llama-3.1-8B-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/other_ckpt/Meta-Llama-3.1-8B-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --tensor_parallel_size 8 \
#     --suffix _easy;

# python -m lcb_runner.runner.main \
#     --model meta-llama/Meta-Llama-3.1-8B-Instruct \
#     --local_model_path /mnt/jfs/ckpt/checkpoints/other_ckpt/Meta-Llama-3.1-8B-Instruct \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version ctf \
#     --tensor_parallel_size 8 \
#     --suffix _ctf

# deepseek-ai/deepseek-coder-33b-instruct
# /mnt/jfs/ckpt/checkpoints/deepseek-coder-33b-instruct
# deepseek-ai/deepseek-coder-6.7b-instruct
# /mnt/jfs/ckpt/checkpoints/deepseek-coder-6.7b-instruct
# deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct
# /mnt/jfs/ckpt/checkpoints/DeepSeek-Coder-V2-Lite-Instruct
# deepseek-ai/DeepSeek-V2-Lite-Chat
# /mnt/jfs/ckpt/checkpoints/DeepSeek-V2-Lite-Chat
# /mnt/jfs/ckpt/checkpoints/DeepSeek-R1
# Qwen/Qwen2.5-7B-Instruct
# /mnt/jfs/ckpt/checkpoints/Qwen2.5-7B-Instruct
# /mnt/jfs/ckpt/checkpoints/other_ckpt/Llama-3.3-70B-Instruct
# meta-llama/Meta-Llama-3.1-8B-Instruct
# /mnt/jfs/ckpt/checkpoints/other_ckpt/Meta-Llama-3.1-8B-Instruct
# /mnt/jfs/ckpt/checkpoints/other_ckpt/Yi-34B-Chat


# python -m lcb_runner.runner.main \
#     --model o1-preview \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --multiprocess 3 \
#     --n 1 \
#     --suffix _easy;

# python -m lcb_runner.runner.main \
#     --model deepseek-chat \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version ctf \
#     --multiprocess 3 \
#     --suffix _ctf;

# python -m lcb_runner.runner.main \
#     --model deepseek-chat \
#     --scenario codegeneration \
#     --evaluate \
#     --num_process_evaluate 128 \
#     --release_version easy \
#     --multiprocess 3 \
#     --suffix _easy


python -m lcb_runner.runner.main \
    --model o1-preview \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --multiprocess 3 \
    --n 1 \
    --suffix _ctf


python -m lcb_runner.runner.main \
    --model Qwen/Qwen2.5-Coder-7B-Instruct \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --tensor_parallel_size 4 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model Qwen/Qwen2.5-Coder-32B-Instruct \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --tensor_parallel_size 4 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model deepseek-ai/deepseek-coder-6.7b-instruct \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --tensor_parallel_size 4 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model deepseek-ai/deepseek-coder-33b-instruct \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --tensor_parallel_size 4 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model gpt-4o \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --multiprocess 3 \
    --n 10 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model claude-3-5-sonnet-20240620 \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --multiprocess 3 \
    --n 10 \
    --suffix _ctf

python -m lcb_runner.runner.main \
    --model o1-mini \
    --scenario codegeneration \
    --continue_existing \
    --continue_existing_with_eval \
    --evaluate \
    --num_process_evaluate 128 \
    --release_version ctf \
    --multiprocess 3 \
    --n 1 \
    --suffix _ctf