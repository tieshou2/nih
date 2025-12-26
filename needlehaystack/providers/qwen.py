import os
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from .model import ModelProvider


class Qwen(ModelProvider):
    DEFAULT_MODEL_KWARGS: dict = dict(max_new_tokens=300, temperature=0.1, do_sample=False)

    def __init__(self, model_name: str = "Qwen2-1.5B-Instruct", model_kwargs: dict = DEFAULT_MODEL_KWARGS):
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        model_path = os.getenv('QWEN_MODEL_PATH', model_name)
        
        # 检查路径是否存在
        if not os.path.exists(model_path):
            raise ValueError(f"Model path does not exist: {model_path}\nPlease check if the path is mounted in the container.")
        
        # 检查是否包含必要的模型文件
        required_files = ['config.json', 'tokenizer_config.json']
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(model_path, f))]
        if missing_files:
            print(f"⚠️  Warning: Missing files in {model_path}: {missing_files}")
            print(f"📁 Files in directory: {os.listdir(model_path)[:20]}")
        
        # 设置离线模式环境变量
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        
        print(f"🔍 Loading model from: {model_path}")
        
        # 使用use_fast=False避免Qwen2Tokenizer导入问题
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=True,
            local_files_only=True,
            use_fast=False
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto",
            trust_remote_code=True,
            local_files_only=True
        )
        self.model.eval()
        
        print(f"✅ Model loaded successfully")

    async def evaluate_model(self, prompt: str) -> str:
        messages = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs, **self.model_kwargs)
        
        response = self.tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
        return response.strip()

    def generate_prompt(self, context: str, retrieval_question: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": "You are a helpful AI bot that answers questions for a user. Keep your response short and direct"},
            {"role": "user", "content": context},
            {"role": "user", "content": f"{retrieval_question} Don't give information outside the document or repeat your findings"}
        ]

    def encode_text_to_tokens(self, text: str) -> list[int]:
        return self.tokenizer.encode(text, add_special_tokens=False)

    def decode_tokens(self, tokens: list[int], context_length: Optional[int] = None) -> str:
        return self.tokenizer.decode(tokens[:context_length] if context_length else tokens)