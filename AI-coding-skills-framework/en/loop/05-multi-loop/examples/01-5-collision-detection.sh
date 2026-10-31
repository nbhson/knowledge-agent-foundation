# In the loop's control script, before spawning a worktree:
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# After finishing:
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
