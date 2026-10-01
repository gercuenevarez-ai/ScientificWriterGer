# ScientificWriterGer

Sistema multidisciplinario para preparar, analizar, redactar y revisar tesis y artículos científicos mediante un agente compatible con Agent Skills.

## Usarlo en GPT, Claude, Grok y Gemini

Abre [la guía multiplataforma](docs/PLATFORMS.md). En exports/ están el conocimiento autocontenido, instrucciones específicas para las cuatro plataformas y scientific-writer-ger.zip para interfaces con skills. Para empezar en un chat, adjunta ScientificWriterGer-Knowledge.txt y pega las instrucciones de tu plataforma. La ejecución D_WG requiere Python o un informe calculado externamente.

## Sus dos componentes

**ScientistGer** dirige el contenido científico: problema, objetivos, diseño, análisis, interpretación disciplinar, fuentes, revisión adversarial, correcciones e integridad. Sus 12 módulos devuelven errores al responsable correspondiente mediante ACCEPT / REFINE / REJECT / ESCALATE.

**WriteGer** adapta la escritura a la voz científica de Gerardo J. Cuenca-Nevárez conservando datos, cifras, citas e inferencias. El estilo no sustituye la corrección científica.

La definición de ambos se recuperó de «Detectores de IA», incluyendo la corrección que separa núcleo general y ficha específica de investigación. Consulta [la procedencia](docs/GER-ORIGIN.md) y [el ADN íntegro aportado por Gerardo](docs/GER-DNA.txt).

## Uso directo

Entrega esta carpeta a tu agente y pide:

> Lee skills/scientific-writer-ger/SKILL.md y usa ScientistGer y WriteGer para completar el trabajo solicitado con mis documentos, datos y requisitos. Recupera la ficha del proyecto desde los archivos disponibles; pregunta solo por información científica indispensable. Entrega el resultado completo y declara las comprobaciones que no se hayan podido realizar.

Para una revisión científica utiliza ScientistGer; para edición autoral utiliza WriteGer. El circuito completo está en [WORKFLOW.md](docs/WORKFLOW.md) y el texto íntegro aportado por Gerardo está en [MASTER-PROTOCOL.txt](docs/MASTER-PROTOCOL.txt). No requiere doce modelos ni nuevas suscripciones.

## Herramientas incluidas

Los controles de proyecto y manuscrito usan Python estándar. El auditor WriteGer requiere NumPy; DOCX requiere python-docx y PDF admite pdftotext (ruta original) o pypdf (alternativa explícita). No utiliza servicios externos:

```sh
python3 scripts/project.py init /ruta/mi-investigacion
python3 scripts/project.py check /ruta/mi-investigacion
python3 scripts/workflow.py freeze /ruta/manuscrito.docx /ruta/revision
python3 scripts/workflow.py verify /ruta/revision
python3 scripts/workflow.py integrity /ruta/antes.docx /ruta/despues.docx
python3 scripts/install.py /ruta/directorio-de-skills
python3 scripts/writeger.py /ruta/manuscrito.docx --language es --section discussion --output /ruta/auditoria.json
python3 scripts/writeger.py /ruta/manuscrito.pdf --language es --pdf-reader pypdf
```

El inicio conserva archivos existentes. La ficha multidisciplinaria es templates/project-brief.json. El registro de fuentes y afirmaciones se describe en la referencia evidence.md. Freeze crea una copia con SHA-256 para que los revisores reciban el mismo documento. Integrity detecta cambios en tokens numéricos de TXT, MD, TEX y DOCX; no comprueba significado, ubicación, unidades o citas. El instalador conserva el paquete completo y sus enlaces relativos; la carpeta instalada tiene SKILL.md en su raíz y conserva todos sus recursos.

## Capacidades y límites verificables

Se incluyen instrucciones operativas, ficha, controles locales y protocolo de revisión. La búsqueda bibliográfica, análisis científico y exportación Word/LaTeX/PDF los ejecuta el agente con sus herramientas disponibles. Este repositorio no incluye un modelo de IA propio ni envía archivos a Gemini o Claude.

**El extractor, auditor y parámetros originales de WriteGer están incluidos y verificados**, sin recalibración. `scripts/writeger.py` ejecuta D_WG para español y registra los hashes de los archivos originales. El idioma se declara explícitamente; no hay detector automático ni calibración inglesa.

La distancia y sus bandas usan el modelo global español. `--section` cambia las desviaciones por característica, no D_WG. El extractor original excluye párrafos de menos de 25 palabras y requiere al menos 100 palabras y cinco oraciones después del filtrado; conserva esa conducta. Sus indicadores lingüísticos son heurísticos, no análisis sintáctico completo.

Se comprobó la ejecución con un texto sintético en TXT y DOCX, la igualdad extractor-auditor y la fórmula por una vía numérica independiente. El corpus no es necesario para usar parámetros existentes, pero sí para repetir el entrenamiento y la validación histórica. No se ha reproducido el entrenamiento original. La ruta alternativa PDF con pypdf se comprobó con un artículo real; el informe identifica el lector utilizado.

Los controles estructurales no demuestran la verdad de una cita ni la validez científica del estudio. El resultado debe basarse en datos y fuentes reales, y cumplir los requisitos de universidad o revista. La superioridad frente a otros repositorios no ha sido medida.

## Referencias de diseño

[DESIGN.md](docs/DESIGN.md) registra la comparación con Academic Mentor, Scientific Writer, Scientific Agent Skills y Agent Skills for Academic Research. Sus archivos no se han copiado. El repositorio combina instrucciones propias con la arquitectura personal recuperada; no se presenta como una fusión del código de terceros.

## BioGea: patrones y publicación

Los dos [artículos matriz](docs/MATRIX-ARTICLES.md) son lactato en broilers y mineralización del N. El inventario local registra los archivos y evita duplicados; los PDFs no se distribuyen.

Para usar fuera de Codex, crea un entorno Python e instala `requirements.txt`. Ejecuta `python -m unittest discover -s tests`. GitHub Actions ejecuta los controles en cada cambio. No se necesita una API adicional para las herramientas locales; la redacción y el razonamiento siguen dependiendo del agente elegido.

Consulta [PUBLISHING.md](docs/PUBLISHING.md) antes de subir el paquete. No se atribuye una licencia de redistribución a los activos personales sin decisión del titular. El repositorio no ha sido publicado automáticamente.
