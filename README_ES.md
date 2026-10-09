# zero-to-trade

**Un sistema operativo de código abierto para sacar adelante tu primera exportación si empiezas de cero: 7 etapas, 4 scripts de Python sin dependencias y una demo que abre en el navegador. De elegir el mercado a cobrar el pedido.**

> La idea cabe en una línea: **la IA hace el trabajo pesado; tú decides.**

> **Mandaste 200 correos en frío (*cold emails*) y recibiste 0 respuestas. El correo funcionó; el proceso, no.** Este repo ordena el trabajo en 7 etapas y 4 scripts. En cada etapa te dice qué sitio abrir, qué escribir y qué resultado cuenta como «aprobado».

Licencia MIT · v0.1.5 · autoría anónima: zero-to-trade · [中文版](README.md) · [English](README_EN.md)

Esta versión en español es un *starter*. Buscamos a gente que la revise y la complete. Si algo suena raro, abre un issue o manda un PR; la versión de referencia sigue siendo [README_EN.md](README_EN.md).

---

## Qué problema resuelve

Buscas «cómo empezar a exportar» y aparece de todo: un gurú que solo cuenta la parte bonita, doscientos artículos SEO, el adelanto gratis de un curso de pago y un video de YouTube con cara de dinero fácil. Lo lees, crees que ya entendiste y, a la mañana siguiente, abres una web de datos aduaneros. La primera casilla te devuelve a la realidad.

No falta información. Sobra información suelta, contada desde el final feliz y sin una próxima acción clara.

Un tutorial te dice «haz una investigación de antecedentes» y se va. Este repo hace otra cosa: **desarma la tarea hasta que queda una acción concreta.**

| Lo que dice un tutorial | Lo que dice este repo |
|---|---|
| «Haz una investigación de antecedentes» | El filtro L1 revisa tres cosas: si la empresa tiene web, cuántos años lleva registrada y si sus redes siguen activas. Si una falla, el lead se descarta. |
| «La calidad importa más que la cantidad» | Ordena 10 leads en T0/T1/T2/T3. Cada nivel trae su próxima acción y su propio límite de tiempo. |
| «Haz seguimiento» | Días 1, 3, 5 y 7. Cambias el enfoque cada vez. El día 7 hay dos opciones: cierre claro o descarte claro. Dejarlo flotando no cuenta como estrategia. |
| «La IA está cambiando el comercio exterior» | Hay 4 scripts en Python puro, solo con la biblioteca estándar y sin dependencias. `python scripts/lead_score.py examples/leads_example.csv` devuelve los niveles en 30 segundos. |

---

## Las siete etapas

| Etapa | Qué haces | Resultado |
|---|---|---|
| **01 Elegir mercado** | Puntúas idioma, demanda y barreras | 1 mercado inicial + 3 razones |
| **02 Encontrar leads** | Buscas por cuatro rutas: aduanas, redes, buscadores y ferias | ≥20 leads verificados al día |
| **03 Evaluar al comprador** | Filtro L1 → revisión L2 → investigación L3 | Calificación A/B/C; estafadores fuera |
| **04 Contactar** | Clasificas en T0-T3 y usas tres canales en el primer contacto | Lista por nivel + plan de 7 días |
| **05 Hablar de especificaciones** | Primero pides lo fácil. El precio va al final | Especificación / cantidad / puerto de destino |
| **06 Cotizar y negociar** | Si cedes algo, pides algo a cambio | Hoja de cotización + escalera de concesiones + guiones |
| **07 Entregar el pedido** | Contrato, producción, inspección, documentos, pago y flete | Ciclo cerrado + plan de recompra |

Cada etapa tiene su archivo en `docs/` y sigue la misma estructura de seis partes. Si arrancas desde cero, empieza por [`docs/00-getting-started.md`](docs/00-getting-started.md). Si prefieres ir directo, usa [`docs/fast-path.md`](docs/fast-path.md): siete días desde cero hasta tu primera respuesta.

---

## Inicio rápido en 30 segundos

**¿No tienes Python?** Abre [`index.html`](index.html) en el navegador, pega un CSV y mira la clasificación T0-T3. No instalas nada.

Hay 4 scripts. Uno es el motor de cotización v0.2 en fase alfa. No usan paquetes de terceros y funcionan con Python 3.8+.

```bash
python scripts/lead_score.py examples/leads_example.csv
python scripts/outreach_gen.py examples/leads_example.csv --tier T0
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

Cabecera del CSV: `company,country,product,source,email,phone,years,contact,note`

---

## Estructura del repositorio

```
zero-to-trade/
├── README.md              # README principal en chino
├── README_EN.md           # Versión completa en inglés (la referencia)
├── README_ES.md           # Esta página: starter en español; buscamos revisores
├── index.html             # Demo en el navegador, sin instalar nada (GitHub Pages)
├── MANIFESTO.md           # Anonimato y cero cursos de pago
├── CONTRIBUTING.md        # Cómo contribuir + reglas para docs y código
├── GLOSSARY.md            # Términos comerciales en 中文 / English / Español
├── GITHUB_LAUNCH.md       # Lista de lanzamiento y promoción
├── LICENSE                # MIT
├── docs/                  # Un archivo por etapa, todos con seis partes
│   ├── 00-getting-started.md   # Para empezar de cero: sin git ni Python en 10 min
│   ├── fast-path.md            # 7 días desde cero hasta tu primera respuesta
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md     # Primera venta ficticia, pero verosímil, paso a paso
├── scripts/               # Python con biblioteca estándar y nada más
│   ├── lead_score.py      # Clasifica leads en T0-T3
│   ├── outreach_gen.py    # Genera mensajes bilingües según el nivel
│   ├── followup_plan.py   # Seguimiento de 7 días y 3 contactos
│   └── quote_engine.py    # Cotización v0.2 (fase alfa): FOB/CIF + escalera
├── examples/
│   └── leads_example.csv  # Datos de ejemplo listos para ejecutar
├── prompts/
│   └── AI_PROMPTS.md      # 27 prompts en inglés, por etapa y listos para pegar
└── assets/                # Imágenes, capturas y diagramas
```

Los términos comerciales (FOB, CIF, L/C, T/T, D/P…) se dejan en inglés y se explican en [GLOSSARY.md](GLOSSARY.md).

---

## Por qué hay herramientas de IA y no solo teoría

Muchos proyectos de «IA para negocios» meten toda la metodología en un prompt. Acá primero van las reglas; después, las herramientas.

El valor está en la disciplina. Un T0 recibe un correo hoy. Un T3 pasa tres meses en la lista fría. Si concedes algo sin pedir nada a cambio, no estás negociando: estás haciendo un regalo. El comprador, por supuesto, no va a protestar.

La IA se queda con el trabajo pesado: filtrar 8 leads, preparar borradores de *due diligence* en 3 niveles para 50 empresas y generar variantes para 7 días de seguimiento. Decidir a quién no escribirle sigue siendo cosa tuya.

Los scripts ponen el estándar en código. Si clasificas por intuición, cada día obtienes un criterio distinto. Por eso la clasificación vive en un script de menos de 200 líneas y sin dependencias.

---

## Hoja de ruta

| Versión | Estado | Contenido |
|---|---|---|
| **v0.1.5** | Añadido | Demo en el navegador (`index.html`) + motor de cotización en fase alfa + manifiesto + lista de lanzamiento + Fast Path + ejemplo de venta |
| **v0.1** | Listo | 7 documentos de etapas, 4 scripts con biblioteca estándar, 27 prompts y README bilingüe |
| **v0.2** | En progreso (fase alfa) | Motor de cotización con IA: FOB/CIF + escalera de concesiones |
| **v0.3** | Planeado | Agente de investigación de compradores (L1/L2/L3) |
| **Largo plazo** | Planeado | Paquetes por industria: neumáticos, materiales de construcción, maquinaria y ferretería.<br>Mensajes de contacto en español, árabe, francés y ruso; el español es clave para llegar a Latinoamérica.<br>Conjuntos de leads reales con datos desidentificados.<br>Conexión del motor de cotización v0.2 con datos aduaneros para anclar precios de la competencia. |

---

## Contribuir

A este repo no le faltan más páginas. Le faltan **detalles reales de cada país**.

Acá hay experiencia con el primer pedido de neumáticos en Medio Oriente. No con la distribución de materiales de construcción en Ecuador ni con los documentos que exige la aduana de México. Eso solo lo sabe quien vende allí. Si trabajas en uno de esos mercados, tu experiencia vale más que otro párrafo genérico.

Puedes ayudar de tres formas:

1. Abre un issue si encuentras un error.
2. Traduce el documento de una etapa.
3. Añade detalles de tu industria o de tu país.

Los PR son bienvenidos. Para el código hay una regla que no se negocia: **Python 3.8+ y solo biblioteca estándar**. El resto está en [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Si te sirvió, dale una estrella

zero-to-trade es un proyecto **de código abierto con mantenimiento activo**; los commits recientes están en el historial del repo. Si te evitó un paso en falso, dale una estrella en la esquina superior derecha. No te consigue un cliente, pero evita que vuelvas a buscar el repo desde cero.

[Ver la curva completa de Star History](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Licencia

[MIT](LICENSE) © 2026 zero-to-trade contributors. Úsalo, cámbialo o véndelo. Solo conserva el crédito.

---

## Preguntas y contribuciones

**Abre un issue: https://github.com/6hn68/zero-to-trade/issues**

¿Viste un error? Repórtalo. ¿Conoces un mercado que el repo no cubre? Manda un PR. ¿Quieres discutir el método? También sirve un issue.

Esta traducción al español sigue siendo un *starter* y todavía busca hablantes nativos que la revisen. La versión de referencia es [README_EN.md](README_EN.md).
