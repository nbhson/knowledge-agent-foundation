from crewai import Agent, Task, Crew

# Multi-agent harness
planner = Agent(role='Planner', goal='Create plan')
executor = Agent(role='Executor', goal='Execute plan')
reviewer = Agent(role='Reviewer', goal='Review output')

harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task]
)
