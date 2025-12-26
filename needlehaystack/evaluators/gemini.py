import os
from typing import Optional
import google.generativeai as genai

from .evaluator import Evaluator


class GeminiEvaluator(Evaluator):
    DEFAULT_MODEL_KWARGS: dict = dict(temperature=0)
    CRITERIA = {"accuracy": """
                Score 1: The answer is completely unrelated to the reference.
                Score 3: The answer has minor relevance but does not align with the reference.
                Score 5: The answer has moderate relevance but contains inaccuracies.
                Score 7: The answer aligns with the reference but has minor omissions.
                Score 10: The answer is completely accurate and aligns perfectly with the reference.
                Only respond with a numberical score"""}

    def __init__(self,
                 model_name: str = "gemini-pro",
                 question_asked: str = None,
                 true_answer: str = None,
                 model_kwargs: dict = DEFAULT_MODEL_KWARGS):
        
        api_key = os.getenv('NIAH_EVALUATOR_API_KEY')
        if not api_key:
            raise ValueError("NIAH_EVALUATOR_API_KEY must be in env for Gemini evaluator")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.model = genai.GenerativeModel(model_name)
        self.question_asked = question_asked
        self.true_answer = true_answer

    def evaluate_response(self, response: str) -> int:
        prompt = f"""You are evaluating the accuracy of an answer compared to a reference answer.
        
Question: {self.question_asked}
Reference Answer: {self.true_answer}
Model's Answer: {response}

{self.CRITERIA['accuracy']}

Score:"""
        
        evaluation = self.model.generate_content(prompt, generation_config=genai.types.GenerationConfig(**self.model_kwargs))
        
        try:
            score = int(evaluation.text.strip())
            return score
        except:
            return 0