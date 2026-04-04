import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelFactory:
    def __init__(self):
        self.MODEL_CONF = {
            'llama': {'alias': 'meta-llama/Llama-2-7b-chat-hf', 'vocab_size': 32000},
            'opt': {'alias': 'facebook/opt-125m', 'vocab_size': 50272}, # 테스트용 모델
            'gptj': {'alias': 'EleutherAI/gpt-j-6B', 'vocab_size': 50400},
            'falcon': {'alias': 'tiiuae/falcon-7b-instruct', 'vocab_size': 65024},
            'vicuna': {'alias': 'lmsys/vicuna-7b-v1.5', 'vocab_size': 32000}
        }

    def get_model(self, name):
        # PyTorch 2.0.1의 MPS 임베딩 버그를 차단하기 위해 CPU로 강제 할당
        device = torch.device("cpu")
        return AutoModelForCausalLM.from_pretrained(
            self.MODEL_CONF[name]['alias']
        ).to(device).eval()

    def get_tokenizer(self, name):
        tokenizer = AutoTokenizer.from_pretrained(self.MODEL_CONF[name]['alias'], use_fast=False)
        tokenizer.pad_token = tokenizer.eos_token
        return tokenizer
        
    def get_vocab_size(self, name):
        return self.MODEL_CONF[name]['vocab_size']
