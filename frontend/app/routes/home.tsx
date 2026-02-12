import type { Route } from "./+types/home";
import { useFetcher } from "react-router";
import type { LessonResponse } from "~/types";
import { generateLesson } from "~/services/api";
import Markdown from "react-markdown";

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

const MOCK_LESSON = `
# Dominando Polars: DataFrames Ultra-rápidos 🚀
Bienvenido a esta lección donde aprenderás por qué **Polars** está reemplazando a Pandas en entornos de alto rendimiento.
## 1. ¿Por qué usar Polars?
Polars está escrito en **Rust** y utiliza *Apache Arrow* para el manejo de memoria. Sus principales ventajas son:

* **Multithreading:** Usa todos los núcleos de tu CPU automáticamente.
* **Lazy Evaluation:** Optimiza tus consultas antes de ejecutarlas.
* **Memoria:** Es mucho más eficiente que Pandas copiando datos.

## 2. Instalación

Para comenzar, instala la librería usando pip:

\`\`\`bash
pip install polars
\`\`\`

## 3. Comparación de Sintaxis

A diferencia de Pandas, Polars favorece el encadenamiento de métodos (*method chaining*).
### Ejemplo: Filtrado y Selección

Supongamos que queremos filtrar usuarios mayores de 25 años y seleccionar solo su nombre.

\`\`\`python
import polars as pl

# Creamos un DataFrame de prueba
df = pl.DataFrame({
    "nombre": ["Ana", "Carlos", "Beatriz"],
    "edad": [22, 30, 28],
    "rol": ["Junior", "Senior", "Lead"]
})

# La forma "Polars" de hacerlo:
resultado = (
    df.lazy()
    .filter(pl.col("edad") > 25)
    .select(["nombre", "rol"])
    .collect()
)

print(resultado)
\`\`\`

> **Nota:** Usar \`.lazy()\` permite a Polars optimizar el plan de ejecución antes de procesar un solo byte.

## Conclusión

Si vienes de Pandas, la transición es fácil. Recuerda siempre: _"Si puedes usar Lazy, usa Lazy"_.

Para más info, visita la [documentación oficial](https://pola.rs).
`;

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
            <div className="bg-gray-50 p-4 rounded-md">
              <article className="
                prose prose-zinc prose-sm max-w-none
                prose-headings:font-bold prose-headings:text-gray-900
                prose-a:text-blue-600 hover:prose-a:text-blue-500
                prose-headings:mb-1 prose-headings:mt-4
                prose-p:my-1.5 prose-p:leading-snug
                prose-ul:my-1.5 prose-li:my-0.5
                prose-pre:my-3
              ">
                <Markdown>
                  {/* {successData.lesson} */}
                  {MOCK_LESSON}
                </Markdown>
              </article>
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
