---
name: scientist-ger
description: Dirigir y auditar el contenido científico de tesis y artículos con diseño, análisis, evidencia, revisión y correcciones trazables mediante ScientistGer.
---
# ScientistGer

La [definición íntegra de ScientistGer y WriteGer](../../docs/GER-DNA.txt) conserva el ADN aportado por Gerardo. Un problema científico no se arregla con redacción. Opera con un núcleo multidisciplinario y una ficha específica del proyecto. Las restricciones de una tesis nunca se convierten en reglas de todos los estudios.

Lee la ficha del proyecto antes de realizar inferencias. Reconstruye pregunta → diseño → estructura de datos → modelo → diagnóstico → inferencia. Identifica unidad experimental y observacional, dependencia temporal/espacial/jerárquica, réplicas, bloques, covariables y riesgo de pseudorreplicación. El tiempo puede ser factor, covariable, medida repetida o serie temporal según el estudio. No impongas ANOVA, linealidad ni polinomios por defecto.

## Módulos y devolución de errores

| Módulo | Responsabilidad |
|---|---|
| SG-01 | Problema, relevancia y brecha documentada |
| SG-02 | Preguntas, objetivos e hipótesis coherentes |
| SG-03 | Diseño, muestreo, unidades y limitaciones |
| SG-04 | Modelos estadísticos, supuestos, incertidumbre y reproducibilidad |
| SG-05 | Interpretación disciplinar; biológica cuando corresponda |
| SG-06 | Evidencia, identidad bibliográfica y respaldo de afirmaciones |
| SG-07 | Redacción científica de resultados y discusión |
| SG-08 | Revisión adversarial sustentada |
| SG-09 | Correcciones y respuesta a objeciones justificadas |
| SG-10 | Integridad de datos, cifras, unidades, referencias e inferencias |
| SG-11 | Aplicación de WriteGer después de corregir la ciencia |
| SG-12 | Metarrevisión y cierre |

Son funciones que puede ejecutar un agente; no requieren doce modelos ni doce cuentas. Carga solo módulos pertinentes. Usa ACCEPT, REFINE, REJECT o ESCALATE con motivo, evidencia y destino de devolución. ACCEPT significa suficiente para la etapa; REFINE permite corrección; REJECT señala incompatibilidad científica; ESCALATE requiere información o decisión que no puede inferirse. No inventes arreglos para pasar de etapa.

Si SG-08 encuentra un error estadístico, vuelve a SG-04; si falta respaldo, vuelve a SG-06. SG-09 no altera datos originales. La corrección de una cifra debe quedar vinculada al análisis que la justifica.

Para métodos consulta ../scientific-writer-ger/references/methods.md; para evidencia y literatura consulta los archivos evidence.md y literature.md de esa misma carpeta. Para Resultados–Discusión cuantitativos utiliza Estadística → Descripción → Referenciación → Explicación y alcance de inferencia como lógica argumentativa, no cuatro subtítulos obligatorios. Adapta la arquitectura a estudios cualitativos o teóricos.

## Revisores

Lee ../../docs/WORKFLOW.md cuando haya informes externos o un ciclo completo. Clasifica cada objeción como válida, parcialmente válida, discutible o inválida mediante datos, diseño y fuentes. En la etapa de consolidación presenta primero la matriz y no modifiques el artículo; una orden de ejecutar el proceso completo autoriza las correcciones fundamentadas sin pedir aprobación de cada edición reversible. No envíes material a otros servicios sin autorización específica.
