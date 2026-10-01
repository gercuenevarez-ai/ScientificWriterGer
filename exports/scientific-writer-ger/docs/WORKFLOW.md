# Circuito de ScientificWriterGer

El [protocolo maestro entregado por Gerardo](MASTER-PROTOCOL.txt) se conserva íntegro y gobierna el circuito de artículos. No se cambia la arquitectura al procesar cada manuscrito. Las restricciones científicas específicas se obtienen de la ficha de cada investigación.

| Etapa | Responsable | Entrada | Entrega |
|---|---|---|---|
| 1 | Gerardo / agente prepara insumos | Manuscrito, datos, figuras, tablas, referencias y ficha | Insumos organizados sin inventar ciencia |
| 2 | ScientistGer | Insumos | Manuscrito científicamente depurado |
| 3 | WriteGer | Manuscrito depurado | Manuscrito congelado; auditoría estilométrica si están disponibles los activos auténticos |
| 4 | Gemini | Manuscrito congelado y anexos autorizados | Informe ciego 1; sin reescritura |
| 5 | Claude | Exactamente el mismo manuscrito; sin informe de Gemini | Informe ciego 2; sin reescritura |
| 6 | ScientistGer | Manuscrito e informes 1 y 2 | Matriz consolidada; no modificar todavía el artículo |
| 7 | ScientistGer | Matriz y orden de ejecutar correcciones | Corrección científica fundada y registro de cambios |
| 8 | WriteGer | Manuscrito corregido | Edición final, comprobación de fidelidad y cierre |

## Independencia y consolidación

Los revisores son Gemini y Claude. Si no hay acceso, la revisión externa queda pendiente: una lectura interna no sustituye ni se presenta como estos informes. El repositorio no envía documentos ni necesita suscripciones adicionales para sus controles locales. Enviar un manuscrito requiere la instrucción del usuario para ese envío.

Ambos reciben el mismo archivo congelado. Ninguno conoce el informe del otro. `scripts/workflow.py freeze` crea una copia y un SHA-256; `verify` detecta cambios en ella. Las instrucciones generales del revisor están en REVIEWER.md; los textos originales están en MASTER-PROTOCOL.txt. Adapta la disciplina a la ficha del proyecto, sin imponer agronomía a todo estudio.

La matriz conserva identificador, revisor, sección, gravedad, observación, evidencia, coincidencia/contradicción, clasificación y justificación. Usa VÁLIDA, PARCIALMENTE VÁLIDA, DISCUTIBLE o INVÁLIDA. No aceptes automáticamente ninguna crítica. La etapa de consolidación por sí sola no autoriza a modificar el manuscrito. Si el usuario ya ordenó ejecutar todo el proceso, esa orden cubre las correcciones fundadas posteriores.

Corrige observaciones válidas o parcialmente válidas en lo que resulte justificado. No adoptes observaciones inválidas; las discutibles requieren resolver la evidencia o la decisión científica antes de cambiarla. Conserva datos originales y documenta cambios sustantivos.

## Cierre

Después de WriteGer final, entrega y detente. No reinicies Gemini, Claude, humanizadores ni reescrituras cosméticas. Una nueva solicitud del usuario o una petición editorial real puede autorizar una tarea posterior. La adaptación de extensión, referencias, figuras o plantilla no reinicia automáticamente el proceso científico. Gerardo conserva la decisión final y autorización del manuscrito.

El extractor y parámetros auténticos están incluidos: ejecuta D_WG en español mediante scripts/writeger.py antes y después de WriteGer. La edición cuantitativa se cierra cuando se satisface la regla del protocolo y se comprueba fidelidad científica. No interpretes una banda como prueba de ciencia correcta ni extiendas el modelo español al inglés.

Para tesis e investigaciones nuevas, usa ScientistGer en propuesta, diseño, evidencia, análisis y capítulos; el circuito de artículos se aplica al manuscrito resultante. Los tiempos del protocolo son estimaciones históricas de planificación, no garantías del repositorio.
