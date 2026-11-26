# zero-to-trade

[中文](README.md) · [English](README_EN.md) · **Español** · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

**Un flujo de trabajo abierto para sacar adelante tu primera exportación si empiezas de cero: 7 etapas, 15 scripts de Python sin dependencias y una demo que abre en el navegador. De elegir el mercado a cobrar el pedido.**

> La idea cabe en una línea: **la IA hace el trabajo pesado; tú decides.**

> **Mandaste 200 correos en frío (*cold emails*) y recibiste 0 respuestas. El correo funcionó; el proceso, no.** Este repo ordena el trabajo en 7 etapas y 15 scripts. En cada etapa te dice qué sitio abrir, qué escribir y qué resultado cuenta como «aprobado».

Licencia MIT · V20 · autoría anónima: zero-to-trade

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
| «Haz seguimiento» | Días 0, 2 y 5: tres toques en 6 días. Cambias el enfoque cada vez. El día 5 hay dos opciones: cierre claro o descarte claro. Dejarlo flotando no cuenta como estrategia. |
| «La IA está cambiando el comercio exterior» | Hay 15 scripts en Python puro, solo con la biblioteca estándar y sin dependencias. `python scripts/lead_score.py examples/leads_example.csv` devuelve los niveles en 30 segundos. |

---

## Las siete etapas

| Etapa | Qué haces | Resultado |
|---|---|---|
| **01 Elegir mercado** | Puntúas idioma, demanda y barreras | 1 mercado inicial + 3 razones |
| **02 Encontrar leads** | Buscas por cuatro rutas: aduanas, redes, buscadores y ferias | ≥20 leads verificados al día |
| **03 Evaluar al comprador** | Filtro L1 → revisión L2 → investigación L3 | Calificación A/B/C; estafadores fuera |
| **04 Contactar** | Clasificas en T0-T3 y usas tres canales en el primer contacto | Lista por nivel + plan D0/D2/D5 |
| **05 Hablar de especificaciones** | Primero pides lo fácil. El precio va al final | Especificación / cantidad / puerto de destino |
| **06 Cotizar y negociar** | Si cedes algo, pides algo a cambio | Hoja de cotización + escalera de concesiones + guiones |
| **07 Entregar el pedido** | Contrato, producción, inspección, documentos, pago y flete | Ciclo cerrado + plan de recompra |

Cada etapa tiene su archivo en `docs/` y sigue la misma estructura de seis partes. Si arrancas desde cero, empieza por [`docs/00-getting-started.md`](docs/00-getting-started.md). Si prefieres ir directo, usa [`docs/fast-path.md`](docs/fast-path.md): siete días desde cero hasta tu primera respuesta.

---

## Inicio rápido en 30 segundos

**¿No tienes Python?** Abre el sitio: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Tiene cuatro herramientas que funcionan en el navegador —clasificación de leads, primer contacto, plan de seguimiento y cotización— con la interfaz en 12 idiomas. Pega un CSV y mira la clasificación T0-T3. No instalas nada y tu lista no sale del navegador.

Hay 14 archivos de scripts: 13 de negocio y 1 de privacidad. Uno de negocio es el motor de cotización. No usan paquetes de terceros y funcionan con Python 3.10+.

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
├── index.html             # El sitio: 4 herramientas en el navegador, interfaz en 12 idiomas, sin dependencias (GitHub Pages)
├── MANIFESTO.md           # Anonimato y cero cursos de pago
├── CONTRIBUTING.md        # Cómo contribuir + reglas para docs y código
├── CHANGELOG.md           # Registro de cambios
├── ROADMAP.md             # Hoja de ruta
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
│   ├── outreach_gen.py    # Mensajes según el nivel (EN/ZH + ES/PT/AR con referencia en inglés, V13)
│   ├── followup_plan.py   # Seguimiento D0/D2/D5, 3 contactos en 6 días
│   ├── quote_engine.py    # Cotización: FOB/CIF + escalera
│   ├── due_diligence.py   # Agente V11 de investigación: L1/L2/L3 + calificación A/B/C + alertas
│   ├── tire_pack.py       # Paquete V12 de neumáticos: medida + mercado → GCC + documentos + notas
│   ├── landed_cost.py     # Coste en destino, V14: FOB + flete + seguro → CIF, más arancel + gastos en destino → DDP
│   └── trade_show.py      # Ferias, V15: expositores recogidos en la feria → plan de seguimiento de 24 horas (agradecimiento en 2 h, pista de cotización en 12 h, llamada/WhatsApp en 24 h)
│   ├── nudge.py           # Recordatorios, V16: D3/D7/D14/D30 × cotizado/muestra enviada/precio en negociación → versión corta de WhatsApp + versión larga de correo (inglés + chino)
│   ├── anchor_price.py    # Precio ancla de la competencia, V18: rango de precios de la competencia (datos de aduanas) + tu coste → tres niveles CIF agresivo/medio/conservador + lista de verificación de 5 puntos
│   ├── fast_path.py     # Ruta rápida interactiva de 7 días, V19: --day N muestra las tareas, --done N marca, --progress resume (alineada con docs/fast-path.md)
│   ├── market_rules.py    # Reglas de mercado: mercados objetivo, barreras de Turquía/Brasil, exclusiones México/EE. UU./UE
│   ├── daily_video_list.py  # Lista diaria de 5 vídeos (3 por la mañana, 2 por la tarde) con controles de medida, mercado, argumento de venta y rodaje
│   ├── fulfillment_checklist.py  # Lista de verificación de cumplimiento de pedidos: PI → anticipo → producción → inspección → saldo → reserva → aduana → B/L → documentos → posventa, con controles duros de dinero en anticipo/liberación/envío
│   └── check_private_data.py  # Guarda de privacidad: verifica datos reales de clientes antes del commit
├── examples/
│   ├── leads_example.csv  # Datos de ejemplo listos para ejecutar
│   └── trade_show_example.csv  # Expositores de ejemplo, uno por nivel de interés
├── tests/                 # 647 pruebas con la biblioteca estándar
├── prompts/
│   └── AI_PROMPTS.md      # 40 prompts en inglés, por etapa y listos para pegar
└── assets/                # Imágenes, capturas y diagramas
```

Los términos comerciales (FOB, CIF, L/C, T/T, D/P…) se dejan en inglés y se explican en [GLOSSARY.md](GLOSSARY.md).

---

## Por qué hay herramientas de IA y no solo teoría

Muchos proyectos de «IA para negocios» meten toda la metodología en un prompt. Acá primero van las reglas; después, las herramientas.

El valor está en la disciplina. Un T0 recibe un correo hoy. Un T3 pasa tres meses en la lista fría. Si concedes algo sin pedir nada a cambio, no estás negociando: estás haciendo un regalo. El comprador, por supuesto, no va a protestar.

La IA se queda con el trabajo pesado: filtrar 8 leads, preparar borradores de *due diligence* en 3 niveles para 50 empresas y generar variantes para el seguimiento D0/D2/D5. Decidir a quién no escribirle sigue siendo cosa tuya.

Los scripts ponen el estándar en código. Si clasificas por intuición, cada día obtienes un criterio distinto. Por eso la clasificación vive en un script de menos de 200 líneas y sin dependencias.

---

## Hoja de ruta

| Versión | Estado | Contenido |
|---|---|---|
| **V13** | ✅ Listo (2026-11-07) | Mensajes multilingües (`scripts/outreach_gen.py --lang es/pt/ar`: texto en español/portugués/árabe + original en inglés tras cada mensaje; plantillas en correspondencia uno a uno con las inglesas T0/T1/T2, un solo diccionario en el script) + nueva sección en `docs/04-outreach.md` (uso + 3 salidas reales pegadas tal cual) + `tests/` con 80 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 7 scripts |
| **V18** | ✅ Listo (2026-11-07) | Precio ancla de la competencia (`scripts/anchor_price.py`: rango de precios de la competencia (datos de aduanas) + tu coste → tres niveles CIF agresivo/medio/conservador, cada uno con margen, rentabilidad, equivalente FOB, recargo implícito y cuándo usarlo; lista de verificación de 5 puntos — coste, flete, tipo de cambio, condiciones de pago, vigencia — antes de cotizar, cualquier punto sin verificar se marca; aviso de precio por debajo del coste «por debajo del coste, no tomes el pedido, negocia volumen a cambio de precio primero»; sin mediana, se estima como (mínimo + máximo) / 2 y se marca como estimación; `--format json` / `--audience client`) + `docs/anchor-price.md` (uso + guía de anclaje + 2 salidas reales pegadas tal cual) + una línea en `docs/06-quote.md` (anclar antes de cotizar) + `tests/` con 187 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 11 scripts |
| **V20** | ✅ Actual (2026-11-14) | Fusión de incrementos locales + 10 rondas de endurecimiento: entradas CLI unificadas (errores en lenguaje claro, códigos de salida alineados) + pruebas reforzadas (modo de mensaje único, alias `--start-date`, registros de ejecución) + números de la documentación alineados + ejemplo fuera de neumáticos (8 leads de iluminación LED) + página de demostración sincronizada con V19 + errores claros para CSV defectuosos (columna ausente / archivo vacío / comillas sin cerrar ya no dan traceback) + prompts alineados (el comando de seguimiento P04-4 gana `--avoid-weekend`, la ventana P10-2 unificada en 48 horas) + registro de ejecución lanzado (`logs/trace-YYYY-MM-DD.jsonl`, una línea por ejecución de los tres scripts principales) + limpieza de código (funciones compartidas en un solo lugar, −151 líneas netas; dos fragmentos muertos eliminados) + `tests/` con 647 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 15 scripts |
| **V19** | ✅ Listo (2026-11-07) | Ruta rápida interactiva de 7 días (`scripts/fast_path.py`: `--day N` muestra las tareas del día — nombre de la tarea + qué hay que producir + qué script o documento usar; `--done N` marca un día con marca de tiempo, guardado en el JSON de `--state`, repetir el registro avisa que ya está marcado y no se duplica; `--progress` resume hechos / pendientes / vencidos (vencido = fecha prevista anterior a hoy y sin marcar, fecha prevista = primer día de `--start` + (N-1) días; sin `--start` no se cuentan vencidos, y se dice claro; `--list` muestra los 7 días; tareas alineadas línea por línea con `docs/fast-path.md`, sin inventar otra lista; `--help` trae ejemplos reales, un día o fecha inválidos dan un error en lenguaje claro) + `docs/fast-path-interactive.md` (uso + formato del archivo de estado + regla de vencimiento + panorama de 7 días + 2 salidas reales pegadas tal cual) + una línea arriba en `docs/fast-path.md` (entrada interactiva) + una línea en `docs/00-getting-started.md` paso B5 (8 scripts restantes → 9) + `tests/` con 226 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 12 scripts |
| **V17** | ✅ Listo (2026-11-07) | READMEs completos en portugués y árabe (nuevos `README_PT.md` en portugués brasileño y `README_AR.md` en árabe con diseño RTL, ambos traducidos por completo y alineados con README_EN.md: mismas secciones, tablas, comandos, nombres de scripts, nombres de archivos, versión y números; todas las empresas, precios y contactos de ejemplo son ficticios, marcados con 【示例】 y dominio reservado sample.example) + `tests/` con 167 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 10 scripts |
| **V16** | ✅ Listo (2026-11-07) | Biblioteca de recordatorios (`scripts/nudge.py`: D3/D7/D14/D30 × cotizado/muestra enviada/precio en negociación, 12 mensajes en total, versión corta de WhatsApp + versión larga de correo, inglés primero con traducción al chino después de cada mensaje; tono en escalera — D3 recordatorio suave, D7 preguntar cómo va, D14 tres opciones para salir del paso (precio más bajo / otra medida / plazo de pago más largo), D30 último mensaje sin quemar puentes; el día 0 es el día en que se envió la cotización, la muestra o empezó la negociación del precio, un ancla distinta a la cadencia de primer contacto de followup_plan, un hilo sigue una sola línea; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (uso + cómo encaja con followup_plan + 2 salidas reales pegadas tal cual) + una línea en `docs/00-getting-started.md` (lista de scripts 6 → 7) + `tests/` con 152 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 10 scripts |
| **V15** | ✅ Listo (2026-11-07) | Herramienta de ferias (`scripts/trade_show.py`: los expositores recogidos en la feria, ordenados por interés en un plan de seguimiento de 24 horas — agradecimiento + material en 2 h, pista de cotización en 12 h, llamada/WhatsApp en 24 h; `--add` uno a uno + `--csv` por lotes, `--format json` / `--out`; el primer mensaje sigue la plantilla T0/T1/T2 de outreach_gen) + `docs/trade-show.md` (uso + 1 salida real pegada tal cual) + `examples/trade_show_example.csv` (3 expositores de ejemplo, uno por nivel de interés) + una línea en `docs/00-getting-started.md` y otra en `docs/02-find-leads.md` (qué hacer con los contactos tras la feria) + `tests/` con 127 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 9 scripts |
| **V14** | ✅ Listo (2026-11-07) | Coste en destino (`scripts/landed_cost.py`: FOB + flete + seguro → CIF, más arancel + gastos en puerto de destino → DDP; coste por unidad + totales + margen si se da precio de venta; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (uso + tabla de fórmulas + 2 salidas reales pegadas tal cual) + una línea en `docs/00-getting-started.md` y otra en `docs/06-quote.md` (primero FOB/CIF con quote_engine, luego el coste total en destino con landed_cost) + `tests/` con 97 pruebas + 40 prompts sin cambios (28 básicos + 12 avanzados) + 8 scripts |
| **V12** | ✅ Listo (2026-11-07) | Paquete de neumáticos (`scripts/tire_pack.py`: medida + mercado → puntos de certificación GCC + documentos de despacho en puerto de destino + notas del mercado; 4 medidas TBR × 8 mercados) + `docs/tire-pack.md` (uso + 2 salidas reales pegadas tal cual) + lista de scripts actualizada en `docs/00-getting-started.md` + `tests/` con 68 pruebas + 40 prompts (28 básicos + 12 avanzados) + 7 scripts |
| **V11** | ✅ Listo (2026-11-07) | Agente de investigación de compradores (`scripts/due_diligence.py`: L1/L2/L3 + calificación A/B/C + lista de alertas + vista de cliente + salida JSON) + sección 13 en `docs/03-due-diligence.md` (salida real pegada tal cual) + prompt P03-5 + `tests/` con 52 pruebas + 40 prompts (28 básicos + 12 avanzados) + 6 scripts |
| **V10** | ✅ Listo (2026-11-07) | 6 módulos avanzados (08 web propia / 09 matriz social / 10 ferias / 11 logística y pago / 12 riesgo y cumplimiento / 13 cuentas clave) + 3 rutas de aprendizaje + manual de resolución de problemas y flujo de colaboración + motor de cotización reforzado (vista de cliente aislada, validación de límites) + `tests/` con 30 pruebas + 39 prompts (27 básicos + 12 avanzados) + demo del navegador alineada con Python |
| **v0.1.5** | Añadido | Demo en el navegador (`index.html`) + motor de cotización en fase alfa + manifiesto + lista de lanzamiento + Fast Path + ejemplo de venta |
| **v0.1** | Listo | 7 documentos de etapas, 4 scripts con biblioteca estándar, 27 prompts y README bilingüe |
| **v0.2** | ✅ Listo (fase alfa) | Motor de cotización con IA: FOB/CIF + escalera de concesiones |
| **Próxima versión** | Por decidir | Dirección por decidir (la ruta rápida interactiva de 7 días llegó en V19) |
| **Largo plazo** | Planeado | Paquetes por industria: neumáticos, materiales de construcción, maquinaria y ferretería.<br>Mensajes de contacto en francés y ruso (español, portugués y árabe llegaron en V13).<br>Conjuntos de leads reales con datos desidentificados.<br>Conexión del motor de cotización con datos aduaneros para anclar precios de la competencia. |

> Hoja de ruta completa: [ROADMAP.md](ROADMAP.md); historial de cambios: [CHANGELOG.md](CHANGELOG.md).

---

## Contribuir

A este repo no le faltan más páginas. Le faltan **detalles reales de cada país**.

Acá hay experiencia con el primer pedido de neumáticos en Medio Oriente. No con la distribución de materiales de construcción en Ecuador ni con los documentos que exige la aduana de México. Eso solo lo sabe quien vende allí. Si trabajas en uno de esos mercados, tu experiencia vale más que otro párrafo genérico.

Puedes ayudar de tres formas:

1. Abre un issue si encuentras un error.
2. Traduce el documento de una etapa.
3. Añade detalles de tu industria o de tu país.

Los PR son bienvenidos. Para el código hay una regla que no se negocia: **Python 3.10+ y solo biblioteca estándar**. El resto está en [CONTRIBUTING.md](CONTRIBUTING.md).

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

¿Viste un error? Repórtalo. ¿Conoces un mercado que el repo no cubre? Manda un PR. ¿Quieres discutir el método? También sirve un issue. Y si prefieres escribir en privado, usa el formulario al final del sitio: el mensaje llega al autor.

Esta traducción al español sigue siendo un *starter* y todavía busca hablantes nativos que la revisen. La versión de referencia es [README_EN.md](README_EN.md).
