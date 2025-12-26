#!/bin/bash

# 设置环境变量
export QWEN_MODEL_PATH="/models/qwen/Qwen2-1___5B-Instruct"
export NIAH_EVALUATOR_API_KEY="AIzaSyD_mOpvaepyjYnaF8ZTQPKH7-VEQr2NAkI"

# 运行150K token上下文测试，使用Gemini作为评估器
python -m needlehaystack.run \
  --provider qwen \
  --model_name "Qwen2-1.5B-Instruct" \
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