#!/bin/bash

echo "🔧 修复 langchain 版本冲突..."

# 卸载旧版本
pip uninstall -y langchain langchain-core langchain-community langsmith

# 安装兼容版本（使用实际存在的版本）
pip install "langchain==0.1.9" "langchain-core==0.1.53" "langchain-community==0.0.38" -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "✅ langchain 依赖已更新"