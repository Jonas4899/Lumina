import type { Route } from "./+types/home";
import { useFetcher } from "react-router";
import type { LessonResponse } from "~/types";
import { generateLesson } from "~/services/api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Lumina - Aprende Tech" },
    { name: "description", content: "Generador de lecciones técnicas con AI." },
  ];
}

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const prompt = formData.get("lesson_prompt");

  if (typeof prompt !== "string" || !prompt) {
    return { error: "El prompt es requerido." };
  }

  try {
    const data = await generateLesson({ lesson_prompt: prompt });
    return data;
  } catch (error) {
    return { error: "Hubo un error conectando con Lumina AI." };
  }
}

export default function Home() {
  const fetcher = useFetcher<LessonResponse | { error: string }>();

  const isLoading = fetcher.state === "submitting" || fetcher.state === "loading";
  const data = fetcher.data;
  const isError = data && "error" in data;

  const successData = data && !("error" in data) ? (data as LessonResponse) : null;

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans p-8">
      <main className="max-w-3xl mx-auto space-y-8">
        {/* Header */}
        <header className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-blue-900">
            Lumina
          </h1>
          <p className="text-gray-600">¿Qué tecnología quieres dominar hoy?</p>
        </header>

        {/* Formulario */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          {/* fetcher.Form evita que la página se recargue completa */}
          <fetcher.Form method="post" className="flex flex-col gap-4">
            <label htmlFor="prompt" className="sr-only">
              Tu objetivo de aprendizaje
            </label>
            <textarea
              name="lesson_prompt"
              id="prompt"
              rows={3}
              className="w-full p-4 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
              placeholder="Ej: Quiero aprender a usar DataFrames en Polars..."
              required
            />

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {isLoading ? "Generando Lección..." : "Comenzar Aprendizaje"}
              </button>
            </div>
          </fetcher.Form>

          {isError && (
            <p className="mt-4 text-red-500 text-sm font-medium">
              Error: {(data as any).error}
            </p>
          )}
        </div>

        {/* Resultados */}
        {successData && (
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold mb-4 border-b pb-2">
              Lección Generada
            </h2>

            {/* OJO: Aquí mostramos el markdown crudo por ahora. 
                Luego instalaremos 'react-markdown' para que se vea bonito */}
            <div className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded-md text-gray-700">
              {successData.lesson}
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 text-xs text-gray-400 flex justify-between">
              <span>Input Tokens: {successData.cost_info.input_tokens}</span>
              <span>
                Costo: ${successData.cost_info.total_cost_usd.toFixed(4)}
              </span>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
