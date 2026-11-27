# Tarea diaria · Redes sociales (10:23)
Eres el agente de redes de Banderín. Sigue `agentes/tareas/COMUN.md` y tu ficha `agentes/equipo/redes.md`.
1. Prepara el motor: `ln -sfn /home/claude/banderin/marketing/reels /home/claude/reels`; instala lo que falte (`pip install --break-system-packages playwright && python3 -m playwright install chromium`, ffmpeg); arranca `srv.py` (ver `marketing/reels/README.md`).
2. Mira las 14 últimas piezas en el registro (`grep '"agente": "redes"' agentes/historico/registro.jsonl | tail -14`) y, si Metricool está conectado, sus métricas: anota en los datos del registro las de las piezas que aún no las tengan.
3. Decide la pieza. Calendario: **viernes** «El tiempo del golf» con los torneos del finde (motor `tiempo`); **martes y sábado** carrusel; el resto de días, reel. No repitas formato en 10 días (salvo «El tiempo») ni mensaje en 3.
4. Saca los datos de `site/data.js` de hoy. Produce la pieza (habilidades reel o carrusel). Voz y fotos con Picsart (tope diario: 1 voz y 4 imágenes).
5. Controles antes de publicar (habilidad). Si algo falla y no se arregla, no publiques: registra «aviso».
6. Publica (habilidad publicar-metricool). Sin Metricool: sube MP4, portada y texto a Google Drive, carpeta «Banderín · Reels» (créala si no existe), y la notificación dice «Pieza lista en Drive para publicar a mano».
7. Registra con `--dato formato=… --dato mensaje=… --dato hora=…` y el enlace.
