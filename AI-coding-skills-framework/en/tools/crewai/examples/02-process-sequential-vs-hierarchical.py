# Sequential — linear pipeline: plan → execute → review
harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task],
    process=Process.sequential
)

# Hierarchical — manager agent orchestrates, assigns tasks
harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,  # adds a "harness manager"
    manager_llm=llm
)
