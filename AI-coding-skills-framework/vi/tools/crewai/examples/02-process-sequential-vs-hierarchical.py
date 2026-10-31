# Sequential — pipeline tuyến tính: plan → execute → review
harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task],
    process=Process.sequential
)

# Hierarchical — manager agent điều phối, assign tasks
harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,  # bổ sung "harness manager"
    manager_llm=llm
)
