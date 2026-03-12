
import pytest 
import logging
from nba_agent import get_scores
from monocle_test_tools import TraceAssertion

@pytest.mark.asyncio
async def test_tool_invocation(monocle_trace_asserter:TraceAssertion):
    """Test that the correct tool is invoked and returns expected output."""
    get_scores("What happened in Clippers game on 22 Nov 2025")

    monocle_trace_asserter.called_tool("get_nba_past_scores")

    monocle_trace_asserter.called_agent("Nba Score Agent")

    monocle_trace_asserter.called_tool("get_nba_past_scores").contains_input("Clippers").contains_output("Hornets")

    monocle_trace_asserter.called_agent("Nba Score Agent").has_input("What happened in Clippers game on 22 Nov 2025").contains_output("Hornets").contains_output("131-116")

@pytest.mark.asyncio
async def test_sentiment_bias_evaluation(monocle_trace_asserter: TraceAssertion):
    """v0: Basic sentiment, bias evaluation on trace - only specify eval name and expected value."""
    get_scores("What happened in Heat game on 22 Nov 2025")
    # Fact is implicit (trace), only specify eval template name and expected value
    monocle_trace_asserter.with_evaluation("okahu").check_eval("sentiment", "positive")\
        .check_eval("bias", "unbiased")

@pytest.mark.asyncio
async def test_quality_evaluation(monocle_trace_asserter: TraceAssertion):
    """v0: Multiple evaluations on trace - frustration, hallucination, contextual_precision."""
    nba_query = "What are the standings for the Warriors? Also tell me what happened in their game on 22 Nov 2025."
    get_scores(nba_query)
    # You can chain multiple check_eval calls for different eval templates. 
    # The expected value is based on the eval template definition. 
    monocle_trace_asserter.with_evaluation("okahu").check_eval("frustration", "ok")\
        .check_eval("hallucination", "no_hallucination")
    # You only have to declare the evaluator once
    monocle_trace_asserter.check_eval("contextual_precision", "high_precision")

if __name__ == "__main__":
    pytest.main([__file__]) 
