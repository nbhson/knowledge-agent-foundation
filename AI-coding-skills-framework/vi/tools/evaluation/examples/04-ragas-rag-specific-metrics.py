from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

dataset = load_your_qa_dataset()
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])

# faithfulness        → câu trả lời có đúng với context không
# answer_relevancy    → câu trả lời có liên quan câu hỏi không
# context_precision   → chunks retrieved có đủ/đúng không
