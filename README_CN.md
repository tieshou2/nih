# Qwen2-1.5B-Instruct 150K上下文测试配置说明

## 已完成的配置

我已经为您的Qwen2-1.5B-Instruct模型配置好了150K token长上下文分析测试，使用Gemini API作为评估器。

### 1. 创建的文件

#### [`needlehaystack/providers/qwen.py`](needlehaystack/providers/qwen.py)
- 自定义的Qwen模型提供器
- 支持本地模型加载
- 使用transformers库进行推理

#### [`needlehaystack/evaluators/gemini.py`](needlehaystack/evaluators/gemini.py)
- Gemini评估器
- 使用您提供的Gemini API密钥进行评估

#### [`run_qwen_150k.sh`](run_qwen_150k.sh)
- 150K token测试的运行脚本
- 已配置您的Gemini API密钥
- 配置了10个上下文长度区间（10K到150K）
- 配置了10个文档深度区间（0%到100%）

### 2. 修改的文件

- [`needlehaystack/providers/__init__.py`](needlehaystack/providers/__init__.py) - 添加了Qwen导入
- [`needlehaystack/evaluators/__init__.py`](needlehaystack/evaluators/__init__.py) - 添加了GeminiEvaluator导入
- [`needlehaystack/run.py`](needlehaystack/run.py) - 添加了qwen provider和gemini evaluator支持

## 使用方法

### 步骤1: 安装依赖

确保安装了Google Generative AI库：

```bash
pip install google-generativeai
```

### 步骤2: 运行测试

```bash
chmod +x run_qwen_150k.sh
./run_qwen_150k.sh
```

或者直接使用Python命令：

```bash
export QWEN_MODEL_PATH="/models/qwen/Qwen2-1___5B-Instruct"
export NIAH_EVALUATOR_API_KEY="AIzaSyD_mOpvaepyjYnaF8ZTQPKH7-VEQr2NAkI"

python -m needlehaystack.run \
  --provider qwen \
  --model_name "Qwen2-1.5B-Instruct" \
  --evaluator gemini \
  --evaluator_model_name "gemini-pro" \
  --context_lengths_min 10000 \
  --context_lengths_max 150000 \
  --context_lengths_num_intervals 10 \
  --document_depth_percent_intervals 10
```

## 测试参数说明

- `--provider qwen` - 使用Qwen提供器
- `--model_name "Qwen2-1.5B-Instruct"` - 模型名称
- `--evaluator gemini` - 使用Gemini作为评估器
- `--evaluator_model_name "gemini-pro"` - Gemini模型名称
- `--context_lengths_min 10000` - 最小上下文长度（10K tokens）
- `--context_lengths_max 150000` - 最大上下文长度（150K tokens）
- `--context_lengths_num_intervals 10` - 上下文长度测试区间数量
- `--document_depth_percent_intervals 10` - 文档深度测试区间数量

## 测试原理

测试会在不同的上下文长度和文档深度位置插入一个"针"（特定信息），然后让模型在"草堆"（长文本）中找到这个信息，Gemini API会评估模型回答的准确性（1-10分）。

## 结果输出

测试结果将保存在 `results/` 目录下，包含：
- 每次测试的得分（由Gemini评估）
- 模型响应
- 测试配置信息

## 注意事项

1. **GPU显存要求**：150K tokens需要较大显存，确保您的GPU内存足够
2. **测试时间**：完整测试需要较长时间（10个长度区间 × 10个深度区间 = 100次测试）
3. **API调用**：每次测试都会调用Gemini API进行评估，请注意API配额
4. 如果遇到显存不足，可以：
   - 减小 `context_lengths_max`（例如改为100000）
   - 减少 `context_lengths_num_intervals`（例如改为5）
   - 在模型加载时使用量化（需修改qwen.py）

## 自定义配置

### 修改测试范围

编辑 [`run_qwen_150k.sh`](run_qwen_150k.sh) 中的参数：

```bash
--context_lengths_min 10000      # 起始长度
--context_lengths_max 150000     # 最大长度
--context_lengths_num_intervals 10  # 测试点数量
```

### 使用模型量化（节省显存）

如需使用量化版本，修改 [`needlehaystack/providers/qwen.py`](needlehaystack/providers/qwen.py:17-23)：

```python
self.model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True,
    load_in_8bit=True  # 添加8bit量化
)
```

## 查看所有参数

```bash
python -m needlehaystack.run --help
```

## API密钥说明

您的Gemini API密钥已配置在脚本中：`AIzaSyD_mOpvaepyjYnaF8ZTQPKH7-VEQr2NAkI`

如需更换，修改 [`run_qwen_150k.sh`](run_qwen_150k.sh:5) 中的 `NIAH_EVALUATOR_API_KEY` 环境变量。