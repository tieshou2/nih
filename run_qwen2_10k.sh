#!/bin/bash

# 设置环境变量 - Qwen2-1.5B-Instruct模型
export QWEN_MODEL_PATH="/models/qwen_backup/Qwen2-1___5B-Instruct"

# 禁用 Hugging Face 远程下载
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

echo "🚀 开始 Qwen2-1.5B-Instruct 10K token 测试（使用简单评估器）..."

python3 -m needlehaystack.run \
  --provider qwen \
  --model_name "Qwen2-1.5B-Instruct" \
  --evaluator simple \
  --context_lengths_min 10000 \
  --context_lengths_max 10000 \
  --context_lengths_num_intervals 1 \
  --document_depth_percent_min 0 \
  --document_depth_percent_max 100 \
  --document_depth_percent_intervals 10 \
  --num_concurrent_requests 1 \
  --save_results true \
  --save_contexts false \
  --final_context_length_buffer 200

echo "✅ 测试完成！结果保存在 /workspace/results/ 目录下"