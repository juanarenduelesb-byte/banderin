<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->

# Registrar y aprender

`registrar-y-aprender` · **Cuándo:** Al terminar cada ejecución.

## Pasos

1. `python3 agentes/tools/registrar.py --agente <id> --resultado ok|aviso|fallo --resumen "…" [--dato clave=valor] [--enlace url]`.
2. Si te equivocaste, Juan te corrigió o descubriste algo que la próxima vez ahorra tiempo, añade una lección a agentes/memoria/<id>.md: `- AAAA-MM-DD · lección en una frase · origen`.
3. Si tu memoria pasa de 40 lecciones, fusiona las parecidas y quita las obsoletas.
4. `python3 agentes/tools/generar.py` (actualiza ESTADO.md) y commit + push.

## Resultado

Histórico completo y memoria útil.

## Lista de control

- ¿El resumen se entiende sin abrir nada más?
- ¿La lección es concreta y aplicable?

## Quién la usa

- [Analista y estratega de negocio](../equipo/analista.md)
- [Operaciones (vigilante)](../equipo/operaciones.md)
- [Atención a usuarios](../equipo/atencion.md)
- [Redes sociales](../equipo/redes.md)
- [Posicionamiento en Google](../equipo/posicionamiento.md)
- [Comercial y alianzas](../equipo/comercial.md)
- [Estratega de producto](../equipo/estratega.md)
