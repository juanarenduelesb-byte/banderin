-- Banderín · base de datos de avisos por correo (Cloudflare D1)
-- Se guarda lo mínimo: el correo, el idioma y lo que sigue cada persona.
-- Aplicar con: wrangler d1 execute banderin --remote --file db/schema.sql

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS suscriptores (
  id               TEXT PRIMARY KEY,                 -- aleatorio, 32 caracteres hex
  email            TEXT NOT NULL UNIQUE,             -- en minúsculas
  estado           TEXT NOT NULL CHECK (estado IN ('pendiente', 'activo')),
  idioma           TEXT NOT NULL DEFAULT 'es' CHECK (idioma IN ('es', 'en')),
  creado           TEXT NOT NULL,                    -- ISO 8601 UTC
  confirmado       TEXT,                             -- cuándo pulsó el enlace de confirmación
  ultimo_correo    TEXT,                             -- último correo de alta o gestión (máx. 1 cada 5 min)
  ultimo_aviso     TEXT,                             -- último resumen de avisos (máx. 1 al día)
  ultima_actividad TEXT                              -- para borrar cuentas inactivas a los 24 meses
);

CREATE TABLE IF NOT EXISTS seguimientos (
  suscriptor TEXT NOT NULL REFERENCES suscriptores(id) ON DELETE CASCADE,
  tipo       TEXT NOT NULL CHECK (tipo IN ('club', 'prov', 'torneo')),
  clave      TEXT NOT NULL,                          -- nombre del club o provincia, o URL del torneo
  PRIMARY KEY (suscriptor, tipo, clave)
);

-- Avisos ya enviados, para no repetir el mismo aviso dos veces.
CREATE TABLE IF NOT EXISTS enviados (
  suscriptor TEXT NOT NULL REFERENCES suscriptores(id) ON DELETE CASCADE,
  clave      TEXT NOT NULL,                          -- URL del torneo + tipo de aviso
  fecha      TEXT NOT NULL,
  PRIMARY KEY (suscriptor, clave)
);

CREATE INDEX IF NOT EXISTS seguimientos_clave ON seguimientos (tipo, clave);
CREATE INDEX IF NOT EXISTS enviados_fecha ON enviados (fecha);
