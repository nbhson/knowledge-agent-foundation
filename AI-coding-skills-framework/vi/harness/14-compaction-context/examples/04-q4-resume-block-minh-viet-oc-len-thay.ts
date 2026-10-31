export function resumeIsSufficient(b: ResumeBlock): boolean {
  return b.goal.length > 0 && b.open.length > 0
      && b.repro.command.length > 0 && b.next.length > 0
      && countTokens(b) <= 300;
}
