# zero-to-trade

**Un sistema operativo de código abierto para exportar cuando no tienes experiencia. Siete etapas, de elegir un mercado a cobrar la orden — más scripts de Python que realmente funcionan.**

> La premisa en una línea: **la IA hace el trabajo pesado, tú tomas las decisiones.**

> 🔥 **Enviaste 200 correos en frío (*cold emails*) y no obtuviste ni una respuesta. No es tu inglés — es el orden de los pasos.** Este repositorio divide "de elegir un mercado a cobrar" en 7 pasos ejecutables más 4 scripts, para que cada paso te diga exactamente qué sitio abrir, qué escribir y qué cuenta como "aprobado".

Licencia MIT · v0.1.5 · [中文版](README.md) · [English](README_EN.md)

🟡 Traducción *starter* al español — se busca colaborador para revisar y completar. La versión autoritativa es [README_EN.md](README_EN.md).

---

## El problema que resuelve

Buscas "cómo empezar a exportar" y obtienes un montón de cosas: un gurú de éxito, doscientos posts SEO, la vista previa gratuita de un curso de pago, un video de YouTube con miniatura de dinero rápido. Los lees todos, sientes que entiendes, abres un sitio de datos aduaneros a la mañana siguiente y aún no sabes qué escribir en la primera casilla.

El problema no es falta de información. Es que la información viene fragmentada, editada desde la perspectiva del ganador, y nunca te dice la siguiente acción.

Cómo lo maneja este repo: **toma una tarea y la desmenuza hasta que se convierte en una acción concreta.**

| Lo que dice un tutorial | Lo que dice este repo |
|---|---|
| "Haz una investigación de antecedentes" | La verificación L1 comprueba exactamente tres cosas: ¿existe el sitio?, ¿cuánto lleva registrada la empresa?, ¿están activas las redes sociales? Falla una y el lead está muerto. |
| "La calidad importa más que la cantidad" | 10 leads se ordenan en T0/T1/T2/T3, y cada nivel tiene su propia acción y presupuesto de tiempo. |
| "Hazles seguimiento" | Día 1, 3, 5, 7. Ángulo distinto cada vez. El día 7 termina con un cierre claro o un descarte claro. |
| "La IA está cambiando el comercio" | Cuatro scripts en Python puro (solo biblioteca estándar, sin dependencias). `python scripts/lead_score.py examples/leads_example.csv` te da la clasificación completa en 30 segundos. |

---

## Las siete etapas

| Etapa | Qué haces | Resultado |
|---|---|---|
| **01 Elegir mercado** | Puntúa idioma, demanda y barrera | 1 mercado inicial + 3 razones |
| **02 Encontrar leads** | Cuatro rutas: aduanas, redes, búsqueda, ferias | ≥20 leads verificados al día |
| **03 Evaluar comprador** | L1 pantalla → L2 estándar → L3 profundo | Rating A/B/C; estafadores filtrados |
| **04 Contactar** | Niveles T0-T3; tres canales en el primer contacto | Lista por nivel + plan de 7 días |
| **05 Hablar especificaciones** | Pequeñas peticiones primero. El precio siempre al final | Spec / cantidad / puerto destino |
| **06 Cotizar y negociar** | Disciplina: cada concesión compra algo a cambio | Hoja de cotización + escalera + guiones |
| **07 Entregar la orden** | Contrato, producción, inspección, documentos, pago, flete | Bucle cerrado + plan de recompra |

Los docs de cada etapa están en `docs/`, un archivo por etapa, todos con la misma estructura de seis partes. **¿Principiante total?** Lee [`docs/00-getting-started.md`](docs/00-getting-started.md) primero. ¿Quieres la ruta rápida? [`docs/fast-path.md`](docs/fast-path.md): cinco días de cero a tu primera respuesta.

---

## Inicio rápido de 30 segundos

**¿Sin Python?** Abre [`index.html`](index.html) en el navegador — pega un CSV y ve la clasificación T0-T3, cero instalación.

Cuatro scripts (uno es el motor de cotización alpha v0.2). Sin paquetes de terceros. Python 3.8+.

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
├── README.md              # Portada principal en chino
├── README_EN.md           # Versión completa en inglés (autoritativa)
├── README_ES.md           # Esta página (español, starter, se busca revisor)
├── index.html             # Demo en navegador, cero instalación (GitHub Pages)
├── MANIFESTO.md           # Anonimato y "no vendemos cursos": la postura de marca
├── CONTRIBUTING.md        # Cómo contribuir + normas de docs y código
├── GLOSSARY.md            # Términos comerciales en 中文 / English / Español
├── GITHUB_LAUNCH.md       # Checklist de lanzamiento y promoción
├── LICENSE                # MIT
├── docs/                  # Un archivo por etapa (misma estructura de seis partes)
│   ├── 00-getting-started.md   # Para principiantes totales: sin git/Python en 10 min
│   ├── fast-path.md            # 5 días de cero a tu primera respuesta
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md     # Recorrido de una primera venta real (ejemplo ficticio)
├── scripts/               # Scripts en Python, solo biblioteca estándar
│   ├── lead_score.py      # Clasifica leads en T0-T3
│   ├── outreach_gen.py    # Genera mensajes de contacto bilingües por nivel
│   ├── followup_plan.py   # Plan de seguimiento de 7 días, 3 contactos
│   └── quote_engine.py    # Motor de cotización v0.2 (alpha): FOB/CIF + escalera
├── examples/
│   └── leads_example.csv  # Datos de ejemplo, listos para ejecutar
├── prompts/
│   └── AI_PROMPTS.md      # 27 prompts en inglés, listos para pegar, por etapa
└── assets/                # Imágenes, capturas, diagramas
```

Los términos comerciales (FOB, CIF, L/C, T/T, D/P…) se mantienen en inglés y se explican en [GLOSSARY.md](GLOSSARY.md).

---

## Por qué herramientas de IA, no solo metodología

Muchos proyectos de "IA para negocios" meten la metodología en un prompt. Este hace lo contrario — **pon la disciplina primero, luego entrega las herramientas.**

- **La disciplina es el valor.** T0 recibe un correo hoy. T3 pasa a una lista fría tres meses. Una concesión sin algo a cambio es un regalo, no una negociación.
- **La IA hace el trabajo pesado.** Filtrar 8 leads, redactar borradores de due diligence de 3 niveles para 50 empresas, generar variantes de 7 días de seguimiento.
- **Los scripts lo hacen repetible.** Si la clasificación se hace "por feeling", no es un estándar. Así que es un script de menos de 200 líneas, sin dependencias.

---

## Hoja de ruta

| Versión | Estado | Contenido |
|---|---|---|
| **v0.1.5** | Añadido | Demo en navegador (index.html) + motor de cotización alpha + manifiesto + checklist de lanzamiento + Fast Path + ejemplo de venta |
| **v0.1** | Listo | 7 docs de etapas, 4 scripts estándar, 27 prompts, README bilingüe |
| **v0.2** | 🟡 En progreso (alpha) | Motor de cotización AI: FOB/CIF + escalera de concesiones |
| **v0.3** | Planeado | Agente de investigación de compradores (L1/L2/L3) |
| **Largo plazo** | Planeado | Paquetes por industria (neumáticos, materiales de construcción, maquinaria, ferretería); mensajes de contacto multilingües (español / árabe / francés / ruso) — clave para llegar a Latam; conjuntos de leads reales (datos desidentificados); conectar el motor de cotización v0.2 a datos aduaneros para anclar precios de la competencia |

---

## Contribuir

La mayor falta en este repo no es documentación, es **detalle de campo por país.** Sé cómo se hace el primer pedido de neumáticos en Medio Oriente; no sé cómo funciona la distribución de materiales de construcción en Ecuador, ni qué documentos exige la aduana de México. **Eso solo lo puede aportar quien vende allí.** Si vendes en un mercado que este repo no conoce, esa es la contribución de mayor valor. Tres formas: abrir un issue, traducir un doc de etapa, o añadir detalle de tu industria/país. Restricción de código: **Python 3.8+, solo biblioteca estándar.**

---

## ⭐ Si te sirvió, dale una estrella

zero-to-trade es un proyecto **de código abierto en mantenimiento activo** (commits recientes en el historial del repo). Si te ahorró dar un paso en falso, una estrella en la esquina superior derecha es la mejor forma de agradecer — y la más fácil de volver a encontrarlo.

[Ver la curva completa de Star History](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Licencia

[MIT](LICENSE) © 2026 zero-to-trade contributors. Úsalo, cámbialo, véndelo — solo mantén el crédito.

---

## Preguntas y contribuciones

**Abre un issue: https://github.com/6hn68/zero-to-trade/issues**

> ⚠️ Esta es una traducción *starter* al español. Se busca colaborador para revisar y completar. La versión autoritativa es [README_EN.md](README_EN.md).
