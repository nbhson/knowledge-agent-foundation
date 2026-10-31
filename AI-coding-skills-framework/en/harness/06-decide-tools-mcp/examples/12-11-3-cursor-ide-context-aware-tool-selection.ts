// Cursor dynamically selects tools based on:
// 1. Current file type
// 2. Selected code
// 3. Editor mode (insert vs replace)
// 4. Git status

const toolsForContext = {
  python: ["execute_python", "lint", "format"],
  typescript: ["run_tests", "type_check", "lint"],
  markdown: ["spell_check", "format"],
};
