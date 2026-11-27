<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->

# Hacer un reel

`reel` · **Cuándo:** Pieza diaria del agente de redes.

## Pasos

1. Elige formato (tabla de cerebro/06 o uno nuevo) y UN mensaje.
2. Guion de 25–35 s: gancho (0–2 s), desarrollo con datos reales, giro, final que pide comentar o etiquetar.
3. Voz con Picsart eleven-v4 (parámetros en cerebro/06). Guarda <id>_vo.mp3.
4. Configuración <id>.py con una frase por tramo de voz (`python3 build.py <id> cfg` debe casar el número).
5. Si hace falta motor nuevo, copia el más parecido y cámbialo; no reescribas build.py.
6. Fotogramas de prueba con cap.py en los momentos con más cosas en pantalla y míralos.
7. Render final, limitador de audio, portada del fotograma más llamativo.

## Resultado

MP4 1080×1920 + portada + texto.

## Lista de control

- ¿Gancho en el primer segundo?
- ¿Todos los datos salen de site/data.js de hoy?
- ¿Subtítulos legibles y sin tapar nada?

## Quién la usa

- [Redes sociales](../equipo/redes.md)
