ROLES = {
    "implementer": {
        "goal_example": "Fix auth refresh in src/auth/refresh.ts; AC: refresh succeeds after expiry, no other files touched",
        "definition_of_done": ["diff limited to files[]", "build passes", "artifact PR-ready patch"],
        "forbidden": ["merge", "self-verify", "touch files outside worktree"],
    },
    "verifier": {
        "goal_example": "Verify patch ART-123 against rubric: build OK, tests OK, AC traced",
        "definition_of_done": ["verdict ACCEPT/REJECT with evidence", "failing test names + logs"],
        "default_stance": "REJECT until evidence sufficient",
        "forbidden": ["edit code", "approve without test output"],
    },
    "reviewer": {
        "goal_example": "Review diff for PR #1234; label Blocker/Major/Minor with file:line",
        "definition_of_done": ["severity list", "at least one actionable comment per Blocker"],
        "forbidden": ["run shell", "write files"],
    },
    "researcher": {
        "goal_example": "Where is token refresh handled? Return 3 candidate files with file:line + 5-line context",
        "definition_of_done": ["facts + citations", "no behavior change"],
        "forbidden": ["write memory", "propose patch without asking"],
    },
}
