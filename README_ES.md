# zero-to-trade

**Un sistema operativo de código abierto para vender al exterior cuando no tienes experiencia. Siete etapas, de elegir un mercado a cobrar la orden — más scripts de Python que realmente funcionan.**

> La premisa en una línea: **la IA hace el trabajo pesado, tú tomas las decisiones.**

> 🔥 **Enviaste 200 correos en frío y no obtuviste ni una respuesta. No es tu inglés — es tu orden de operaciones.** Este repositorio divide "de elegir un mercado a cobrar" en 7 pasos ejecutables más 3 scripts, para que cada paso te diga exactamente qué sitio abrir, qué escribir y qué cuenta como "aprobado".

Licencia MIT · v0.1.5 · [中文版](README.md) · [English](README_EN.md)

---

## El problema que resuelve

Buscas "cómo empezar a exportar" y obtienes un montón de cosas: un gurú de éxito, doscientos posts SEO, la vista previa gratuita de un curso de pago, un video de YouTube con miniatura de dinero rápido. Los lees todos, sientes que entiendes, abres un sitio de datos aduaneros a la mañana siguiente y aún no sabes qué escribir en la primera casilla.

El problema no es falta de información. Es que la información viene fragmentada, editada desde la perspectiva del ganador, y nunca te dice la siguiente acción.

Cómo lo maneja este repo: **lleva una tarea hasta el final hasta que se convierte en una acción.**

| Lo que dice un tutorial | Lo que dice este repo |
|---|---|
| "Haz una investigación de antecedentes" | La pantalla L1 verifica exactamente tres cosas: ¿existe el sitio?, ¿cuánto lleva registrada la empresa?, ¿están activas las redes sociales? Falla una y el lead está muerto. |
| "La calidad importa más que la cantidad" | 10 leads se ordenan en T0/T1/T2/T3, y cada nivel tiene su propia acción y presupuesto de tiempo. |
| "Hazles seguimiento" | Día 1, 3, 5, 7. Ángulo distinto cada vez. El día 7 termina con un cierre claro o un descarte claro. |
| "La IA está cambiando el comercio" | Cuatro scripts de Python solo estándar. `python scripts/lead_score.py examples/leads_example.csv` te da la clasificación completa en 30 segundos. |

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

## Por qué herramientas de IA, no solo metodología

Muchos proyectos de "IA para negocios" meten la metodología en un prompt. Este hace lo contrario — **pon la disciplina primero, luego entrega las herramientas.**

- **La disciplina es el valor.** T0 recibe un correo hoy. T3 va a un cajón tres meses. Una concesión sin algo a cambio es un regalo, no una negociación.
- **La IA hace el trabajo pesado.** Filtrar 8 leads, borrar borradores de investigación de 50 empresas, generar variantes de 7 días de seguimiento.
- **Los scripts lo hacen repetible.** Si la clasificación se hace "por feeling", no es un estándar. Así que es un script de menos de 200 líneas, sin dependencias.

---

## Hoja de ruta

| Versión | Estado | Contenido |
|---|---|---|
| **v0.1.5** | Añadido | Demo en navegador (index.html) + motor de cotización alpha + manifiesto + checklist de lanzamiento + Fast Path + ejemplo de venta |
| **v0.1** | Listo | 7 docs de etapas, 3 scripts estándar, 27 prompts, README bilingüe |
| **v0.2** | 🟡 En progreso (alpha) | Motor de cotización AI: FOB/CIF + escalera de concesiones |
| **v0.3** | Planeado | Agente de investigación de compradores (L1/L2/L3) |

---

## Contribuir

La mayor falta en este repo no es documentación, es **detalle de campo por país.** Si vendes en un mercado que este repo no conoce, esa es la contribución de mayor valor. Tres formas: abrir un issue, traducir un doc de etapa, o añadir detalle de tu industria/país. Restricción de código: **Python 3.8+, solo biblioteca estándar.**

---

## Licencia

[MIT](LICENSE) © 2026 zero-to-trade contributors. Úsalo, cámbialo, véndelo — solo mantén el crédito.

---

## Preguntas y contribuciones

**Abre un issue: https://github.com/6hn68/zero-to-trade/issues**

> ⚠️ Esta es una traducción *starter* al español. Se busca colaborador para revisar y completar. La versión autoritativa es [README_EN.md](README_EN.md).
