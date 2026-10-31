/** Bài test chấp nhận cho một resume block: agent lạnh có đi tiếp được không? */
export function resumeIsSufficient(block: ResumeBlock, nextAction: string): boolean {
  return block.goal.length > 0                                    // không mục đích thì không có nhiệm vụ
      && block.open.length > 0                                    // phải biết còn việc gì
      && block.repro.command.length > 0                           // phải lặp lại được lỗi
      && block.next.length > 0                                    // phải biết làm gì tiếp
      && countTokens(block) <= 300;                               // ngân sách cứng
}
