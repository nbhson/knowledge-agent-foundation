# Control script của loop, trước khi spawn worktree:
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# Sau khi xong:
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
