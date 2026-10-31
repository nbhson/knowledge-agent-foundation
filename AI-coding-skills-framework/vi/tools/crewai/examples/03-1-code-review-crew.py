planner = Agent(role='Planner', goal='Break down feature into tasks')
coder = Agent(role='Coder', goal='Implement tasks', tools=[code_editor])
reviewer = Agent(role='Reviewer', goal='Find bugs and security issues')

plan_task = Task(description='Plan the login API', expected_output='Task list')
code_task = Task(description='Implement per plan', expected_output='Working code')
review_task = Task(description='Review code', expected_output='Review report')

crew = Crew(
    agents=[planner, coder, reviewer],
    tasks=[plan_task, code_task, review_task],
    process=Process.sequential  # plan → code → review → (reviewer feedback loop)
)
