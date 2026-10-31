from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

dataset = load_your_qa_dataset()
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])

# faithfulness        → is the answer consistent with the context
# answer_relevancy    → is the answer relevant to the question
# context_precision   → are the retrieved chunks sufficient/correct
