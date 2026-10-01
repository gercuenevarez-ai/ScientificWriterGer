# Contrato de evidencia

sources.json es una lista de fuentes: id, title, authors, year, locator, access, verification_note. locator puede ser DOI, URL o ruta del documento. access admite metadata, abstract o fulltext. verification_note registra cómo se comprobó la identidad y qué se leyó; si no se verificó, dilo.

claims.json es una lista: id, text, kind, source_ids, status, evidence_note. kind admite literature, result, interpretation o proposal. status admite pending, supported, disputed o unsupported. Solo usa supported después de comprobar la evidencia pertinente. evidence_note debe localizar el pasaje, tabla, página o archivo de análisis y explicar su relación con la afirmación.

Confirmar DOI/título/autores demuestra identidad bibliográfica, no respaldo científico. Lee el pasaje relevante para evaluar población, diseño, magnitud y límites de la afirmación. Si solo hay un resumen, limita las conclusiones a su contenido. No cites una fuente secundaria como si hubieras leído la primaria.

Para resultados, registra datos y salida del análisis; no requiere una fuente bibliográfica en source_ids. Para interpretaciones, distingue inferencia del autor y evidencia observada. Las propuestas describen trabajo futuro, no experimentos realizados.

Preserva las afirmaciones disputadas y evidencia contraria. No conviertas pending en supported para que pase el comprobador. Un manuscrito puede avanzar como borrador con pendientes identificados; no lo declares listo para envío mientras sus afirmaciones centrales sigan sin respaldo.
