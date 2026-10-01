# GPT, Claude, Grok y Gemini

El repositorio distribuye el mismo núcleo científico en dos formas:

1. **Instrucciones universales:** exports/ScientificWriterGer-Knowledge.txt y las INSTRUCTIONS.txt de cada plataforma. Se pueden cargar en chats, proyectos, GPTs, Gems u otras superficies que admitan archivos/instrucciones. Esta ruta no exige un estándar de instalación compartido.
2. **Skill autocontenida:** exports/scientific-writer-ger.zip. Incluye SKILL.md en la raíz de su carpeta, conocimiento, Python, parámetros y dependencias. No depende de skills instaladas aparte ni carpetas hermanas. Puede importarse en superficies compatibles con Agent Skills o copiarse a su directorio de skills.

Las cuatro guías están en exports/gpt, exports/claude, exports/grok y exports/gemini. Las aplicaciones y agentes de desarrollo del mismo proveedor no necesariamente ofrecen las mismas funciones. Una carga de conocimiento no instala un motor Python ni cambia los pesos del modelo.

## Ejecución científica

Sin ejecución de código: dirección, redacción y revisión mediante instrucciones y documentos; D_WG solo puede interpretarse desde un informe real proporcionado.

Con ejecución Python: extraer el paquete, instalar requirements.txt si el entorno lo permite y ejecutar scripts/writeger.py. La herramienta funciona sin una API de proveedor. No se ofrece un conector remoto ni servidor MCP en este paquete.

Con un agente local: instalar la carpeta autocontenida con scripts/install.py apuntando al directorio que documente el agente. No se modifican cuentas ni configuración automáticamente.

## Fuentes oficiales consultadas el 1 de octubre de 2026

- OpenAI, skills: https://learn.chatgpt.com/docs/build-skills
- OpenAI, ejecución de código API: https://developers.openai.com/api/docs/guides/tools-code-interpreter
- Claude, skills: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Gemini, skills: https://support.google.com/gemini/answer/17094296?hl=en
- Gemini, instrucciones y conocimiento de Gems: https://support.google.com/gemini/answer/15235603?hl=en
- Grok Build, skills: https://docs.x.ai/build/features/skills-plugins-marketplaces

Estas fuentes respaldan las rutas documentadas, no certifican que este paquete haya sido aceptado por cada cuenta. Se comprobaron generación, integridad del ZIP, autosuficiencia de archivos y ejecución local. No se inició sesión ni se probó importación en cuentas de GPT, Claude, Grok o Gemini.
