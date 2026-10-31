sensitive_harness = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",  # chỉ dừng khi cần xác nhận
    code_execution_config=False
)
