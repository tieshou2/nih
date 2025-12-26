from .evaluator import Evaluator


class SimpleEvaluator(Evaluator):
    """简单的关键词匹配评估器，不依赖外部API"""
    
    def __init__(self, question_asked: str = None, true_answer: str = None, **kwargs):
        self.question_asked = question_asked
        self.true_answer = true_answer

    def evaluate_response(self, response: str) -> int:
        """
        简单评分：检查响应中是否包含真实答案的关键词
        返回0-10的分数
        """
        if not response or not self.true_answer:
            return 0
        
        response_lower = response.lower()
        answer_lower = self.true_answer.lower()
        
        # 提取关键词（去除常见停用词）
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'to'}
        answer_words = [w.strip('.,!?;:') for w in answer_lower.split() if w not in stop_words and len(w) > 2]
        
        if not answer_words:
            return 5
        
        # 计算匹配的关键词数量
        matched = sum(1 for word in answer_words if word in response_lower)
        score = int((matched / len(answer_words)) * 10)
        
        return min(10, max(0, score))