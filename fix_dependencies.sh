#!/bin/bash

echo "🔧 安装Qwen2所需的依赖..."

# 安装transformers_stream_generator（Qwen2Tokenizer需要）
pip install transformers_stream_generator -i https://pypi.tuna.tsinghua.edu.cn/simple

# 确保transformers版本支持Qwen2
pip install --upgrade transformers -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "✅ 依赖已安装"