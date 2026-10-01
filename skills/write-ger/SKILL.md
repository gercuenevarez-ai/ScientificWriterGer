---
name: write-ger
description: Ajustar prosa científica a la voz de Gerardo J. Cuenca-Nevárez preservando evidencia, cifras y citas, con auditoría estilométrica cuando se disponga de su modelo auténtico.
---
# WriteGer

Trabaja sobre ciencia ya revisada por ScientistGer. No uses estilo para resolver defectos de diseño o evidencia. Su identidad se deriva de textos que Gerardo confirma como propios, separados por idioma y deduplicados por documento. No es un detector de IA ni un procedimiento para eludir detectores.

Lee [los artículos matriz](../../docs/MATRIX-ARTICLES.md) cuando trabajes la arquitectura argumentativa. Lactato en broilers y mineralización de N tienen prioridad retórica sobre el corpus complementario; ambos son referencias inglesas y no cambian la calibración española.

## Invariantes antes y después

Conserva datos, cifras, unidades, especies, tratamientos, p, F, R², referencias, conclusiones estadísticas y alcance inferencial. Registra el texto anterior y la justificación de cambios relevantes. Usa ../../scripts/workflow.py integrity como alarma de cambios en tokens numéricos; ese control no reemplaza lectura semántica ni verifica citas.

Puede ajustar sintaxis, ritmo, conectores y párrafos. No alteres el significado para acercarlo a una distribución estilística. La interpretación científica prevalece sobre similitud métrica.

Consulta ../scientific-writer-ger/references/writing.md para los principios autorales disponibles. No afirmes haber cargado las 29 secciones originales: la recuperación de ese documento es parcial. La definición propia de WriteGer está conservada íntegramente en ../../docs/GER-ORIGIN.md.

## Especificación matemática recuperada

La [definición íntegra aportada por Gerardo](../../docs/GER-DNA.txt) documenta:

- Normalización: z_j = (x_j − μ_j) / σ_j.
- Distancia: D_WG = sqrt(zᵀ Σ_shrink⁻¹ z), con covarianza regularizada mediante Ledoit–Wolf.
- Centro por sección: μ_S* = λ μ_S + (1 − λ) μ_G, λ = n_S / (n_S + 4).
- Separación por idioma, deduplicación de documentos y validación leave-one-document-out.
- Restricciones: ScientificFidelity, NumericalIntegrity, CitationIntegrity e InferentialValidity deben conservarse. Son obligaciones de revisión, no cuatro verificadores automáticos implementados.

El documento reporta mediana 3.735, Q75 4.220, Q90 4.592 y máximo observado 5.906. Reporta bandas: ≤4.220 núcleo compatible; hasta 4.592 compatible periférico; hasta 5.906 atípico pero observado; >5.906 fuera del espacio observado. Conserva esos números como resultados históricos del corpus original, sin tratarlos como una calibración reconstruida o validada aquí.

Si se recupera el auditor original, entrega distancia antes/después y desviaciones principales por dimensión. Si se reconstruye un nuevo extractor o se modifica el corpus, revalida las bandas por documento e idioma y distingue la nueva calibración de la histórica; no reutilices automáticamente estos límites.

## Auditoría D_WG

El chat documenta diez dimensiones: longitud media y dispersión de oraciones, MATTR-100, conectores por 1000 palabras, subordinación, nominalizaciones, pasiva/impersonal, palabras funcionales, comas y longitud de párrafos. Documenta normalización por media/desviación, distancia de Mahalanobis con covarianza Ledoit-Wolf, PCA, modelos por sección con contracción n/(n+4) y validación dejando fuera un documento.

Los tres activos originales suministrados por Gerardo están en ../../writeger/, conservados sin modificaciones. Ejecuta `python scripts/writeger.py manuscrito.docx --language es --section discussion` desde la raíz del repositorio usando un entorno con las dependencias de requirements.txt. Para PDF, la ruta original necesita pdftotext. `--pdf-reader pypdf` permite extracción alternativa comprobada, registrada en el informe; puede producir resultados distintos y no reproduce automáticamente las distancias históricas. TXT y MD no necesitan lector adicional.

La herramienta valida matrices y orden de características, contrasta el extractor con el auditor, calcula D_WG y registra hashes. La distancia y las bandas son globales españolas; la sección solo condiciona las desviaciones mostradas. Declara el idioma real: el modelo no está calibrado para inglés. El corpus original sería necesario para volver a entrenar o reproducir la validación histórica, no para ejecutar los parámetros entregados.

El extractor conserva párrafos con al menos 25 palabras y exige al menos 100 palabras y cinco oraciones válidas después de filtrar. Sus indicadores de subordinación y pasiva son heurísticos. Usa el cuerpo pertinente, identifica qué texto se auditó y revisa cifras, citas y significado aparte del resultado estilométrico.

Entrega distancia antes/después, banda y desviaciones principales. No presentes el resultado como probabilidad de autoría, detector de IA o comprobación de integridad científica. Si faltan dependencias o el texto no es admisible, explica el error y no inventes una distancia.

## Parada

Con integridad científica y compatibilidad estilométrica validada, detente: no busques D_WG=0. Sin modelo, termina la edición solicitada con revisión de fidelidad y declara pendiente únicamente la medición cuantitativa; no prolongues reescrituras para simularla. Después del WriteGer final no reinicies revisores o humanizadores sin nuevos datos, un error material o una solicitud editorial real.
