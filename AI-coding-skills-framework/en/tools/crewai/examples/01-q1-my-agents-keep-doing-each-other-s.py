reviewer = Agent(role='Reviewer', goal='Find bugs and security issues',
                 backstory='You never modify code, you only report findings',
                 tools=[])
review_task = Task(description='Review the login API code',
                   expected_output='Numbered list of file:line findings')
