// npm install @typesafe/sdk
import { TypeSafe } from "@typesafe/sdk";

const client = new TypeSafe({ apiKey: process.env.TYPESAFE_API_KEY });

const resp = await client.ask({
  model: "jev-1.13.0",
  state: "Ticket: charged twice, want refund, very frustrated.",
  questions: {
    team: {
      type: "choice",
      choices: ["billing", "tech", "account", "other"],
      description: "Which team owns this ticket?",
    },
    refund_requested: {
      type: "noul",
      description: "Does the customer explicitly request a refund?",
    },
    urgency: {
      type: "score",
      levels: [
        { level: 1, label: "low" },
        { level: 2, label: "medium" },
        { level: 3, label: "high" },
        { level: 4, label: "critical" },
      ],
      description: "Urgency of handling this ticket",
    },
  },
});

const team = resp.answers.team;
console.log(team.choice, team.confidence, team.probabilities);
