sensitive_harness = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",  # only stops when confirmation is needed
    code_execution_config=False
)
