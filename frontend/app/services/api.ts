import type { LessonRequest, LessonResponse } from "~/types";

const API_URL = "http://localhost:8000/api/lessons";

export const generateLesson = async (
  data: LessonRequest,
): Promise<LessonResponse> => {
  const response = await fetch(`${API_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Error generando la lección");
  }

  return response.json();
};
