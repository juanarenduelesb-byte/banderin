-- Banderín · límites de peticiones y registro de actividad sospechosa (Cloudflare D1)
-- Ejecutar una vez: Cloudflare → D1 → banderin → Console (o wrangler d1 execute banderin --remote --file ...)
-- No guarda IPs: solo una huella irreversible que cambia cada día.

CREATE TABLE IF NOT EXISTS limites (
  clave TEXT PRIMARY KEY,   -- regla/huella/ventana
  n     INTEGER NOT NULL,
  hasta TEXT NOT NULL       -- fin de la ventana (ISO 8601); se borra después
);
CREATE INDEX IF NOT EXISTS limites_hasta ON limites (hasta);

CREATE TABLE IF NOT EXISTS seguridad (
  ventana TEXT NOT NULL,    -- tramo de 10 minutos (ISO 8601)
  ip      TEXT NOT NULL,    -- huella de la IP, no la IP
  tipo    TEXT NOT NULL,    -- origen, llave, limite, robot, datos, tipo, sitio, interno
  ruta    TEXT NOT NULL,
  n       INTEGER NOT NULL,
  PRIMARY KEY (ventana, ip, tipo, ruta)
);
