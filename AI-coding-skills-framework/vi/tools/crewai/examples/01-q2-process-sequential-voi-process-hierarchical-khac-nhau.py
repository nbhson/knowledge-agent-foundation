harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,   # đóng vai harness orchestrator
    manager_llm=llm,
)
