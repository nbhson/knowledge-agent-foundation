deploy_task = Task(
    description="Deploy the reviewed commit to production",
    expected_output="Deployment confirmation with the commit SHA",
    human_input=True,
)
