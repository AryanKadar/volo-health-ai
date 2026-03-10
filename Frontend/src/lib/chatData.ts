export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export const suggestions = [
  "What documents are required for hospital admission?",
  "What should a patient carry before surgery?",
  "What happens during discharge?",
  "What follow-ups may be required after hospitalisation?",
] as const;
