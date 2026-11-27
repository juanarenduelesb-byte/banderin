# Motor de reels de Banderín

Hace reels verticales de 1080×1920 a partir de una página HTML animada (el «motor») y un archivo de configuración
con las frases de la voz y las escenas. Lo usa el agente de redes (`agentes/equipo/redes.md`).

## Cómo se usa

```bash
# 1. El motor espera vivir en /home/claude/reels y la web en /home/claude/banderin/site
ln -sfn "$PWD/marketing/reels" /home/claude/reels
# 2. Servidor local que sirve la web (fuentes, iconos, capturas) y las configuraciones
(cd /home/claude/reels && setsid nohup python3 srv.py >/tmp/srv.log 2>&1 &)
# 3. Voz: generar con Picsart (modelo eleven-v4, voz nPczCjzI2devNBz1zQrb, es, stability 0.5, similarityBoost 0.8)
#    y guardarla como <id>_vo.mp3 en esta carpeta.
# 4. Comprobar que las frases casan con los tramos de la voz (mismo número):
python3 build.py <id> cfg
# 5. Fotogramas de prueba y revisión:
PAGE=<motor> python3 cap.py <id> stills 1.5 6 12
# 6. Render final (≈5–9 min):
PAGE=<motor> python3 build.py <id>
# 7. Limitar picos de audio antes de publicar:
ffmpeg -i <salida>.mp4 -c:v copy -af alimiter=limit=0.89 -c:a aac -b:a 192k final.mp4
```

## Motores disponibles (PAGE=…)
| Motor | Estilo | Ejemplo de configuración |
|---|---|---|
| `split` | Expectativa / realidad, pantalla partida | `fit.py` |
| `mision` | Videojuego de mundo abierto (HUD, minimapa, «AL AGUA») | `mision.py` |
| `match` | App de ligar con torneos (deslizar, «¡Es un match!») | `match.py` |
| `tiempo` | Parte del tiempo de la tele con datos del finde | `tiempo.py` |
| `fichajes` | Mercado de fichajes de fútbol | `fichajes.py` |
| `sabias` | «¿Sabías que…?» con fotos y pegatinas | `sabias.py` |
| `meteoro` | Animación: crema solar y meteorito → la web por dentro | `meteoro.py` |
| `doc`, `wrap` | Expediente y «Wrapped» | `doc.py`, `wrap.py` |

Reglas de un buen reel: gancho en el primer segundo, un solo mensaje, datos reales de `site/data.js`,
final que pida etiquetar o comentar, 25–35 s. Más en `agentes/habilidades/reel.md`.
