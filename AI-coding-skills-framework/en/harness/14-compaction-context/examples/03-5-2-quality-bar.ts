/** The acceptance test for a resume block: can a cold agent continue? */
export function resumeIsSufficient(block: ResumeBlock, nextAction: string): boolean {
  return block.goal.length > 0                                    // no goal, no task
      && block.open.length > 0                                    // must know what is still open
      && block.repro.command.length > 0                           // must be able to re-trigger the bug
      && block.next.length > 0                                    // must know what to do next
      && countTokens(block) <= 300;                               // hard budget
}
