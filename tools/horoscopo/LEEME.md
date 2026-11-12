# Horóscopo automático para Instagram

Genera las placas del horóscopo del día (tapa, 12 signos y cierre) con los mismos
textos que muestra la página, y las deja publicadas en
`https://santeriaarcanoss.com.ar/horoscopo/AAAA-MM-DD/`.

- `datos.mjs` corre el script de `public/index.html` y saca el horóscopo de cada signo.
- `placas.py` dibuja las 14 placas (1080×1350) y escribe `publicacion.json` con el texto del posteo y las URLs.
- `generar.sh AAAA-MM-DD [...]` hace las dos cosas y borra carpetas de más de 21 días.

Si cambiás los textos del horóscopo en la página, las placas toman el cambio solas.

Una tarea programada de Claude corre cada domingo: genera las placas del lunes y jueves
siguientes, las sube acá, y las programa en Posty en @santiagojara.tarot a las 8:00.
