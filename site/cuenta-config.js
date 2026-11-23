// Configuración pública de cuentas (Supabase). Esta clave es pública por diseño:
// los datos los protege la seguridad por filas (RLS) de la base de datos.
// NUNCA pongas aquí la clave secret ni la service_role.
window.CUENTA = {
  url: 'https://jdyawzbvxucamibbqdzg.supabase.co',
  key: 'sb_publishable_hepM5qxH6v3oaICMJLnPLw_Ynz7d7hw',
  // Clave PÚBLICA (site key) de Cloudflare Turnstile; vacía = desactivado. La secreta va solo en Cloudflare Pages y en Supabase.
  turnstile: '0x4AAAAAAGPocc-riUys0BAX',
  google: false // pasar a true cuando Google esté activado en Supabase → Authentication → Providers
};
