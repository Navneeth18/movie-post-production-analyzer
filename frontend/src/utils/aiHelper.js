import { strategyAPI } from '../services/api';

export const callAI = async (prompt) => {
  try {
    const response = await strategyAPI.getAIReasoning(prompt);
    return response.data.result || "No response.";
  } catch (error) {
    console.error('AI call failed:', error);
    return "Error generating AI response. Please try again.";
  }
};
