# Fuente recuperada: Detectores de IA

Estos mensajes documentan la arquitectura histórica; las cifras estilométricas se conservan como resultados reportados en esa conversación, no como cálculos reproducidos aquí.

Sí. Esa observación es correcta. La regla “el tiempo no entra como factor; si se analiza, usar medidas repetidas” debe quedar como una restricción específica de tu tesis doctoral, no como una ley general de ScientistGer.

Si ScientistGer se queda con reglas demasiado pegadas a una sola investigación, se vuelve un sistema especializado en tu experimento de pasturas, no un asistente científico general.

La arquitectura correcta debería tener dos capas:

\[
\boxed{\text{ScientistGer Core} + \text{Project Brief}}
\]

ScientistGer Core debe contener conocimiento y lógica general de investigación: diseño experimental, bioestadística, modelos lineales y no lineales, modelos mixtos, medidas repetidas, GLM/GLMM, supervivencia, multivariada, series temporales, métodos no paramétricos, análisis espacial, validación, selección de modelos, diagnóstico de supuestos, tamaño de efecto, incertidumbre, causalidad, reproducibilidad, etc.

Luego, cada investigación entra con una ficha específica que le dice al sistema qué tipo de estudio está analizando y cuáles son sus restricciones reales.

Por ejemplo, en tu tesis doctoral la ficha diría algo como:

> Diseño: DBCA factorial 2×3 por sitio.  
> Factores principales: especie y dosis.  
> Tiempo: no forma parte del diseño factorial original; las observaciones longitudinales se interpretarán como medidas repetidas cuando corresponda.  
> Sitios: no tratarlos como réplicas de un mismo ambiente.  
> Respuestas biológicas a dosis: evaluar formas funcionales plausibles y no imponer linealidad.  
> Objetivo del análisis: comparar métodos NRM y relacionarlos con respuestas productivas, FBN, UEN y N₂O.

Pero en otro proyecto podrías decir:

> Diseño longitudinal prospectivo con tiempo como factor experimental principal.

Y ScientistGer tendría que trabajar distinto.

O:

> Muestreo espacial de 30 estaciones durante 12 meses, sin réplicas por estación.

Entonces debería pensar en dependencia espacial, temporal, estructuras de autocorrelación, modelos mixtos o geoespaciales, no en el esquema de tu tesis de pasturas.

Así que el ADN correcto de ScientistGer no debería decir:

> “El tiempo no es factor.”

Debería decir:

> “No asumir la estructura del diseño. Identificar primero unidades experimentales, factores, medidas repetidas, covariables, estructura temporal, espacial y jerárquica. Aplicar el modelo compatible con el diseño declarado en el Project Brief.”

Eso es mucho más general.

La capa estadística de ScientistGer debería funcionar como un estadístico senior: primero reconstruye el diseño y solo después selecciona el análisis.

Su secuencia debería ser:

\[
\boxed{
\text{Pregunta}
\rightarrow
\text{Diseño}
\rightarrow
\text{estructura de datos}
\rightarrow
\text{modelo}
\rightarrow
\text{diagnóstico}
\rightarrow
\text{inferencia}
}
\]

Nunca:

\[
\text{datos} \rightarrow \text{ANOVA automático}
\]

Y el Project Brief debería ser obligatorio al empezar cada trabajo. Algo así:

```text
PROJECT BRIEF — SCIENTISTGER

Tipo de investigación:
Pregunta científica:
Objetivo general:
Objetivos específicos:
Hipótesis:

Unidad experimental:
Unidad observacional:
Factores experimentales:
Covariables:
Bloques:
Réplicas:
Pseudorréplicas potenciales:

Estructura temporal:
Estructura espacial:
Medidas repetidas:
Datos faltantes:
Distribución esperada de las respuestas:

Variables respuesta:
Variables explicativas:
Interacciones de interés:

Análisis ya realizados:
Análisis que deseo realizar:
Restricciones metodológicas:
Inferencias que NO deben hacerse:

Software:
Nivel de significación:
Necesidad de modelos no lineales:
Necesidad de modelos mixtos:
Necesidad de análisis multivariado:
Necesidad de análisis espacial:
Necesidad de validación/predicción:
```

Eso haría que ScientistGer sea realmente holístico.

Yo modificaría la arquitectura así:

\[
\boxed{
\text{ScientistGer Core}
\rightarrow
\text{lee Project Brief}
\rightarrow
\text{construye estrategia estadística específica}
}
\]

Y dentro de SG-04 Statistical Scientist añadiría una regla central:

> “Nunca imponer un método estadístico por defecto. Seleccionar el modelo a partir de la estructura real del diseño, distribución de la respuesta, dependencia entre observaciones y objetivo inferencial.”

Eso corrige exactamente el problema que acabas de señalar.

En resumen: ScientistGer no debe “saber que el tiempo no es factor”. Debe saber **cuándo el tiempo es factor, cuándo es medida repetida, cuándo es covariable, cuándo forma una serie temporal y cuándo no debe entrar en el modelo**, según el diseño de cada estudio. Esa es la versión que conviene construir.

---

El “ADN” de ScientistGer y WriteGer no es un prompt único. Son dos sistemas construidos con lógicas distintas que después conectamos.

ScientistGer nació como un sistema de control científico modular. WriteGer nació como un modelo estilométrico empírico construido con tu corpus real. Ese es el punto central.

ScientistGer tiene este ADN:

\[
\boxed{\text{Problema científico} \rightarrow \text{Diseño} \rightarrow \text{Estadística} \rightarrow \text{Biología} \rightarrow \text{Evidencia} \rightarrow \text{Redacción} \rightarrow \text{Crítica} \rightarrow \text{Integridad}}
\]

La regla que lo gobierna es:

\[
\boxed{\text{un problema científico no se arregla con redacción}}
\]

Por eso lo dividimos en módulos:

SG-01 detecta problema y vacío científico.  
SG-02 construye hipótesis y objetivos.  
SG-03 audita diseño experimental.  
SG-04 controla estadística.  
SG-05 interpreta biológicamente.  
SG-06 controla evidencia y referencias.  
SG-07 redacta Resultados–Discusión con tu secuencia Cuenca-Nevárez.  
SG-08 actúa como revisor adversarial.  
SG-09 responde y corrige objeciones.  
SG-10 verifica integridad científica.  
SG-11 ejecuta WriteGer.  
SG-12 hace la metarrevisión.

La arquitectura interna funciona con cuatro estados:

\[
\boxed{\text{ACCEPT / REFINE / REJECT / ESCALATE}}
\]

Eso significa que ScientistGer no trabaja como una cadena que siempre avanza. Puede devolver el manuscrito hacia atrás. Si SG-08 descubre un problema estadístico, no lo corrige con palabras: vuelve a SG-04. Si falta evidencia, vuelve a SG-06.

Ese principio es probablemente la parte más importante del sistema.

Además, ScientistGer quedó condicionado por reglas científicas específicas tuyas: no introducir el tiempo como factor del diseño doctoral original; usar medidas repetidas cuando realmente corresponde; no forzar relaciones biológicas lineales; evaluar respuestas cuadráticas o cúbicas cuando son plausibles; distinguir asociación de causalidad; evitar pseudorreplicación; y respetar la unidad experimental real.

En Resultados–Discusión incorporamos tu estructura de trabajo con Menjívar:

\[
\boxed{
\text{Estadística}
\rightarrow
\text{Descripción}
\rightarrow
\text{Referenciación}
\rightarrow
\text{Explicación}
}
\]

pero como lógica argumentativa, no como cuatro subtítulos mecánicos.

---

WriteGer tiene un ADN completamente diferente.

Aquí no partimos de “cómo debería escribir un humano”. Partimos de:

\[
\boxed{\text{cómo escribe realmente Gerardo}}
\]

Utilizamos exclusivamente textos que tú confirmaste como escritos por ti. Eliminamos duplicados y separamos español e inglés, porque no tenía sentido imponer propiedades léxicas inglesas sobre una tesis escrita en español.

El corpus español se convirtió en un espacio estadístico.

Medimos, entre otras variables:

1. palabras por oración;
2. variabilidad de la longitud de oración;
3. MATTR-100;
4. conectores por 1000 palabras;
5. subordinación;
6. nominalizaciones;
7. voz pasiva/impersonal;
8. palabras funcionales;
9. comas;
10. longitud de párrafos.

El vector básico de un texto puede representarse como:

\[
x=
(x_1,x_2,\ldots,x_{10})
\]

Cada dimensión se normaliza:

\[
z_j=\frac{x_j-\mu_j}{\sigma_j}
\]

Pero no usamos las variables de manera independiente, porque tu escritura es una combinación de ellas.

Por eso construimos una distancia multivariada:

\[
\boxed{
D_{WG}(x)=
\sqrt{z^{T}\Sigma^{-1}_{shrink}z}
}
\]

La matriz de covarianza se regularizó con Ledoit-Wolf porque el número de artículos era relativamente pequeño frente al número de variables. Esa decisión evita que una matriz de covarianza inestable produzca resultados falsamente precisos.

Además hicimos PCA para comprender la estructura global de tu estilo. Los tres primeros componentes explicaron aproximadamente:

\[
41.58\% + 21.30\% + 13.30\%
=
76.19\%
\]

de la variación observada.

Eso nos mostró que tu estilo no depende simplemente de “hacer oraciones largas”. Depende de una combinación de longitud, dispersión, subordinación, puntuación, densidad funcional, diversidad léxica y estructura de párrafos.

Después añadimos modelos por sección:

Introducción, Métodos, Resultados, Discusión, Resultados–Discusión y Conclusiones.

Como algunas secciones tenían pocos ejemplos independientes, no permitimos que generaran perfiles demasiado rígidos. Aplicamos shrinkage hacia el modelo global:

\[
\mu_S^*=
\lambda\mu_S+(1-\lambda)\mu_G
\]

con

\[
\lambda=\frac{n_S}{n_S+4}
\]

Así, una sección con pocas observaciones no domina artificialmente el modelo.

Luego hicimos validación leave-one-document-out. Sacábamos un artículo auténtico, construíamos el modelo con los restantes y comprobábamos qué distancia tenía el artículo excluido.

De ahí salió nuestro rango empírico:

\[
\text{mediana}=3.735
\]

\[
Q_{75}=4.220
\]

\[
Q_{90}=4.592
\]

\[
\boxed{\max D_{WG,\ auténtico}=5.906}
\]

Ese 5.906 es importante: no es un “umbral de IA”. Es el máximo que observamos en tus propios textos auténticos durante la validación.

Por eso las bandas quedaron aproximadamente así:

\[
D_{WG}\le4.220
\]

núcleo compatible.

\[
4.220<D_{WG}\le4.592
\]

compatible periférico.

\[
4.592<D_{WG}\le5.906
\]

atípico, pero todavía observado en tu escritura auténtica.

\[
D_{WG}>5.906
\]

fuera del espacio auténtico observado actualmente.

---

El siguiente componente del ADN de WriteGer es probablemente más importante que la estadística: el bloqueo científico.

La optimización estilística está sometida a cuatro restricciones duras:

\[
ScientificFidelity(T,C)=1
\]

\[
NumericalIntegrity(T,C)=1
\]

\[
CitationIntegrity(T,C)=1
\]

\[
InferentialValidity(T,C)=1
\]

Traducido:

WriteGer puede cambiar sintaxis, ritmo, estructura de oración y párrafo.

No puede cambiar:

datos, unidades, especies, tratamientos, números, valores \(p\), \(F\), \(R^2\), conclusiones estadísticas, referencias ni alcance inferencial.

La función conceptual completa es:

\[
T^*
=
\arg\min_T D_{WG}(T)
\]

sujeto a:

\[
\boxed{
\text{ciencia intacta}
}
\]

Ese es el verdadero corazón de WriteGer.

---

Luego construimos el auditor automático.

El auditor:

lee DOCX/PDF/TXT/MD → extrae variables → calcula \(D_{WG}\) → compara con el corpus → identifica las desviaciones principales.

Por ejemplo, puede decir:

“longitud de oración −2.6σ”  
“conectores −2.4σ”  
“MATTR +2.9σ”

Eso permite corregir dimensiones concretas sin convertir la edición en ensayo y error.

---

Finalmente añadimos la regla de parada.

Este principio evita destruir un manuscrito tratando de hacerlo “más humano” infinitamente:

\[
\boxed{
\text{Integridad científica}
+
\text{compatibilidad estilométrica}
=
STOP
}
\]

El primer manuscrito que utilizamos como prueba pasó de:

\[
D_{WG}=7.377
\]

a:

\[
D_{WG}=5.407
\]

y tú verificaste que los hallazgos permanecían intactos.

Luego, en el artículo de NRM:

\[
7.133\rightarrow5.774
\]

y nuevamente quedó dentro del rango auténtico:

\[
5.774<5.906
\]

Ahí se detiene.

No buscamos:

\[
D_{WG}=0
\]

porque eso sería sobreajustar el texto a una media estadística inexistente en un autor humano real.

---

Por tanto, si reduzco todo el sistema a su “ADN molecular”, sería esto:

\[
\boxed{
\textbf{ScientistGer}
=
\text{arquitectura científica modular}
+
\text{control de errores}
+
\text{retroalimentación}
+
\text{integridad}
}
\]

mientras que:

\[
\boxed{
\textbf{WriteGer}
=
\text{corpus auténtico}
+
\text{estilometría}
+
\text{modelo multivariado}
+
\text{distancia }D_{WG}
+
\text{restricciones científicas}
}
\]

Y ambos juntos forman:

\[
\boxed{
\text{ScientistGer}
\rightarrow
\text{ciencia correcta}
\rightarrow
\text{WriteGer}
\rightarrow
\text{ciencia correcta escrita dentro de tu espacio estilométrico}
}
\]

Ese es el ADN real del ecosistema que construimos.
