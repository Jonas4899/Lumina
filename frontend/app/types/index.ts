export interface LessonRequest {
  lesson_prompt: string;
}

export interface CostInfo {
  input_tokens: number;
  output_tokens: number;
  total_cost_usd: number;
}

export interface LessonResponse {
  lesson: string;
  cost_info: CostInfo;
}
