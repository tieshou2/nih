#!/bin/bash

# 设置环境变量 - Qwen3-8B模型
export QWEN_MODEL_PATH="/nfs1/models/Qwen3-8B"
export NIAH_EVALUATOR_API_KEY="AIzaSyD_mOpvaepyjYnaF8ZTQPKH7-VEQr2NAkI"

# 禁用 Hugging Face 远程下载
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

echo "🚀 开始本地 Qwen3-8B 长上下文测试（150K tokens）..."

python3 -m needlehaystack.run \
  --provider qwen \
  --model_name "Qwen3-8B" \
  --evaluator gemini \
  --evaluator_model_name "gemini-pro" \
  --context_lengths_min 10000 \
  --context_lengths_max 150000 \
  --context_lengths_num_intervals 10 \
  --document_depth_percent_min 0 \
  --document_depth_percent_max 100 \
  --document_depth_percent_intervals 10 \
  --num_concurrent_requests 1 \
  --save_results true \
  --save_contexts false \
  --final_context_length_buffer 500

echo "✅ 测试完成！结果保存在 /workspace/results/ 目录下"