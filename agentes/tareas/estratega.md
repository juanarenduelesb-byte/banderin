# Tarea semanal · Estratega (jueves 10:51)
Eres el agente estratega de Banderín. Sigue `agentes/tareas/COMUN.md` y tu ficha `agentes/equipo/estratega.md`.
1. Issues aprobados: `gh api 'repos/juanarenduelesb-byte/banderin/issues?labels=aprobada&state=open'`. Si hay alguno, construye el más antiguo (habilidad construir-propuesta) y termina ahí esta semana.
2. Si no: cuenta los issues abiertos con `propuesta` y sin `aprobada`/`rechazada`. Si hay 3 o más, no propongas nada nuevo: la notificación le recuerda a Juan cuáles esperan respuesta.
3. Si hay sitio: investiga (habilidad referencias-otros-deportes) y escribe UNA propuesta (habilidad propuesta-mejora): archivo `agentes/propuestas/P-NNN-tema.md` + issue con etiqueta `propuesta` (`gh api -X POST repos/juanarenduelesb-byte/banderin/issues -f title=… -f body=… -f 'labels[]=propuesta'`).
4. Issues con `rechazada`: ciérralos y anota en tu memoria por qué no gustó.
5. Notificación: título de la propuesta + «Para aprobarla, ponle la etiqueta “aprobada” en GitHub».
