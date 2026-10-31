import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

def test_harness_answer():
    test_case = LLMTestCase(
        input="BHYT áp dụng cho đối tượng nào?",
        actual_output=harness.run("BHYT áp dụng cho đối tượng nào?"),
        retrieval_context=retrieved_chunks,
    )
    assert_test(test_case, [AnswerRelevancyMetric(), FaithfulnessMetric()])
