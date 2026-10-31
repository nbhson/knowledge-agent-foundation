# before spawning a worktree
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# after finishing
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
