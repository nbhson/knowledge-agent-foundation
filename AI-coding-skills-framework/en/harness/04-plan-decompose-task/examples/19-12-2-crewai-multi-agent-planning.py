from crewai import Agent, Task, Crew

# Create specialized planning Agents
planner = Agent(
    role="Task Planner",
    goal="Break down complex tasks into actionable steps",
    backstory="Expert at task decomposition and dependency analysis",
    tools=[analysis_tool, research_tool],
)

executor = Agent(
    role="Task Executor", 
    goal="Execute planned tasks efficiently",
    backstory="Expert at implementation and testing",
    tools=[code_tool, test_tool],
)

reviewer = Agent(
    role="Plan Reviewer",
    goal="Review and validate task plans",
    backstory="Expert at quality assurance and risk assessment",
)

# Create the tasks
planning_task = Task(
    description="Create execution plan for: {task}",
    agent=planner,
)

execution_task = Task(
    description="Execute the plan created by planner",
    agent=executor,
)

# Assemble the Crew
crew = Crew(
    agents=[planner, executor, reviewer],
    tasks=[planning_task, execution_task],
    verbose=True,
)
