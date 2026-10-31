import { TypeSafe } from "@typesafe/sdk"; // official TypeSafe JS SDK

const client = new TypeSafe({ apiKey: process.env.TYPESAFE_API_KEY });

const result = await client.systemone.ask({
  model: "jev-latest",
  state: "PR #220 deletes the payment retry limit check.",
  questions: {
    risky: {
      type: "noul",
      question: "Does this change remove a safety guardrail?",
      criteria: "Yes only if a limit, check, or permission gate is deleted or weakened.",
    },
    area: {
      type: "choice",
      options: ["payments", "api", "ui", "docs"],
      question: "Which area of the codebase does this touch?",
    },
  },
});

const risky = result.answers.risky.noul.p_yes;   // e.g. 0.87
const area = result.answers.area.choice.selected;

if (risky > 0.5 && Math.abs(risky - 0.5) * 2 >= 0.6) {
  blockAutoMerge(pr); // Noul intrinsic confidence ≥ 0.6 → hold for review
}
