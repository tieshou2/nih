import os
import json
import logging
from modelscope import snapshot_download

LOCAL_CACHE_DIR = "/root/insight_benchmark/examples/autotest/model_cache"
IGNORE_FILE_PATTERNS = [
    "*.bin",
    "*.safetensors",
    "*.pt",
    "*.pth",
    "*.ckpt",
    "*.h5",
    "*.msgpack",
    "*.onnx",
]


# 解析模型配置
def get_model_config(model_path: str):
    config_path = os.path.join(model_path, "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.error(f"错误：找不到文件 {config_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"错误：文件 {config_path} 不是有效的 JSON 格式。详细信息：{e}")
        raise


# 模型文件下载
def model_download(model_id: str, local_cache_dir: str = LOCAL_CACHE_DIR):
    model_path = os.path.join(local_cache_dir, model_id)
    config_path = os.path.join(model_path, "config.json")

    # 检查模型路径是否存在，以及是否包含必要的配置文件
    if os.path.exists(model_path) and os.path.exists(config_path):
        try:
            # 尝试加载配置文件验证完整性
            with open(config_path, "r", encoding="utf-8") as file:
                json.load(file)
            logging.info(
                f"Model {model_id} already exists and is complete at {local_cache_dir}"
            )
            return model_path
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(
                f"Model {model_id} exists but appears incomplete or corrupted: {e}"
            )
            logging.info("Removing incomplete model and re-downloading...")
            # 清理不完整的模型目录
            import shutil

            shutil.rmtree(model_path, ignore_errors=True)

    if os.path.exists(model_path):
        logging.info(f"Downloading model {model_id} to {model_path}")
    else:
        logging.info(
            f"Model {model_id} not found or incomplete. Downloading to {model_path}"
        )

    snapshot_download(
        model_id=model_id,
        cache_dir=local_cache_dir,
        ignore_file_pattern=IGNORE_FILE_PATTERNS,
    )
    return model_path