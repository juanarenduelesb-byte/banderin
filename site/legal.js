/* Textos legales de Banderín.
   DATOS DEL TITULAR: rellena este bloque. Mientras un campo esté vacío,
   la web muestra «pendiente» en su lugar. */
window.TITULAR = {
  nombre: "Juan Álvarez-Rendueles Basagoiti",        // Nombre y apellidos (autónomo) o razón social (sociedad)
  nif: "53730185T",           // NIF / CIF
  domicilio: "Avenida de los Pirineos, 33, 28703 San Sebastián de los Reyes (Madrid)",     // Dirección postal completa
  email: "avisos@banderin.es",                // Correo de contacto y de privacidad
  registro: "",      // Solo si es sociedad: Registro Mercantil, tomo, folio, hoja
  marca: "Esclusa",
  web: "Banderín"
};
window.LEGAL_ACTUALIZADO = "2026-11-11";

window.LEGALDOCS = {
"aviso-legal": {
 titulo: "Aviso legal",
 intro: "Quién está detrás de Banderín y en qué condiciones puedes usarlo.",
 html: `
<h3 id="al-1">1. Titular del sitio web</h3>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de 11 de julio, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), te informamos de que este sitio web, Banderín, es un proyecto de {{marca}} cuyo titular es:</p>
<ul class="datos">
<li><span>Titular</span><b>{{nombre}}</b></li>
<li><span>NIF</span><b>{{nif}}</b></li>
<li><span>Domicilio</span><b>{{domicilio}}</b></li>
<li><span>Correo electrónico</span><b>{{email}}</b></li>
{{registro_li}}
</ul>

<h3 id="al-2">2. Qué es Banderín</h3>
<p>Banderín es un buscador gratuito de torneos de golf amateur y profesional que se celebran en España. Reúne en un solo sitio la información que federaciones, clubes y plataformas de inscripción publican de forma abierta, y enlaza a la página oficial de cada torneo para que te inscribas allí.</p>
<p><b>Banderín no organiza torneos, no gestiona inscripciones ni cobra pagos.</b> La inscripción, el precio, las plazas, los requisitos y cualquier cambio o cancelación son responsabilidad exclusiva de cada organizador.</p>

<h3 id="al-3">3. Independencia</h3>
<p>Banderín es un proyecto independiente. No está afiliado ni patrocinado por la Real Federación Española de Golf, por las federaciones autonómicas, por los clubes ni por las plataformas de inscripción cuyos torneos muestra, como NextCaddy o Golf Directo. Los nombres y marcas de estas entidades pertenecen a sus titulares y se citan solo para identificar el origen de la información.</p>

<h3 id="al-4">4. Condiciones de uso</h3>
<p>El uso de Banderín está regulado por estos textos legales: este aviso legal, los <a href="#terminos">términos de uso</a>, la <a href="#privacidad">política de privacidad</a> y la <a href="#cookies">política de cookies</a>. Al usar el sitio aceptas estas condiciones. Si no estás de acuerdo, te pedimos que no lo utilices.</p>

<h3 id="al-5">5. Propiedad intelectual e industrial</h3>
<p>El diseño, el código, los textos propios, las ilustraciones y la marca Banderín pertenecen a su titular o se usan con licencia. Las tipografías Libre Caslon Display, Public Sans e Instrument Sans (logotipo) se usan bajo licencia SIL Open Font License 1.1, y el mapa de provincias procede de datos geográficos abiertos.</p>
<p>Los datos de los torneos (nombre, fecha, campo, precio, etc.) son información de hecho publicada por sus organizadores; Banderín no reclama derechos sobre ella.</p>

<h3 id="al-6">6. Enlaces a otros sitios</h3>
<p>Banderín enlaza a páginas de terceros, como las fichas de inscripción de los organizadores. No controlamos esos sitios ni respondemos de su contenido, de su disponibilidad ni de sus políticas de privacidad; te recomendamos leerlas antes de facilitarles tus datos.</p>

<h3 id="al-7">7. Responsabilidad</h3>
<p>Revisamos y actualizamos la información cada día y comprobamos que los enlaces funcionan, pero no podemos garantizar que todos los datos sean exactos, completos o estén al día en todo momento. Confirma siempre la información en la web del organizador antes de inscribirte o desplazarte. En la medida en que lo permita la ley, el titular no responde de los daños derivados de errores u omisiones en información procedente de terceros.</p>

<h3 id="al-8">8. Correcciones y retirada de información</h3>
<p>Si organizas un torneo y detectas un error, o prefieres que tu torneo no aparezca en Banderín, escríbenos a {{email}} y lo corregiremos o retiraremos en un plazo máximo de 72 horas hábiles.</p>

<h3 id="al-9">9. Legislación aplicable</h3>
<p>Estos textos se rigen por la legislación española. Para cualquier controversia, si actúas como consumidor serán competentes los juzgados y tribunales de tu domicilio; en otro caso, los del domicilio del titular.</p>
`},

"privacidad": {
 titulo: "Política de privacidad",
 intro: "Qué datos personales tratamos, para qué y cuáles son tus derechos. En resumen: hoy Banderín no te pide ningún dato para funcionar.",
 html: `
<div class="resumen"><b>En pocas palabras</b>
<ul>
<li>Para buscar torneos no tienes que registrarte ni darnos ningún dato.</li>
<li>Tus preferencias, tu perfil de golfista y lo que sigues se quedan en tu navegador; no nos llegan.</li>
<li>No usamos publicidad ni perfiles. Contamos las visitas de forma agregada y sin cookies.</li>
<li>Solo tratamos datos personales si nos escribes por correo.</li>
</ul></div>

<h3 id="pr-1">1. Responsable del tratamiento</h3>
<ul class="datos">
<li><span>Responsable</span><b>{{nombre}}</b></li>
<li><span>NIF</span><b>{{nif}}</b></li>
<li><span>Domicilio</span><b>{{domicilio}}</b></li>
<li><span>Contacto de privacidad</span><b>{{email}}</b></li>
</ul>
<p>Esta política cumple el Reglamento (UE) 2016/679, General de Protección de Datos (RGPD), y la Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD).</p>

<h3 id="pr-2">2. Qué datos tratamos y para qué</h3>
<table class="tabla">
<thead><tr><th>Situación</th><th>Datos</th><th>Finalidad</th><th>Base legal</th><th>Conservación</th></tr></thead>
<tbody>
<tr><td>Navegas por Banderín</td><td>Datos técnicos de la visita (página vista, navegador, país aproximado), sin cookies ni identificadores, mediante Cloudflare Web Analytics.</td><td>Contar las visitas de forma agregada para saber qué se usa y mejorar la web.</td><td>Interés legítimo en conocer el uso de la web sin identificarte (art. 6.1.f RGPD).</td><td>Solo se conservan cifras agregadas.</td></tr>
<tr><td>Guardas preferencias</td><td>Tema, ciudad de referencia, distancia, torneos guardados y jugados, solo en tu navegador.</td><td>Recordar tus ajustes en tu siguiente visita.</td><td>Tu consentimiento (art. 6.1.a RGPD), que puedes retirar en <a href="#" data-cookies>Configurar cookies</a>.</td><td>Hasta que los borres o retires el consentimiento.</td></tr>
<tr><td>Usas «Usar mi ubicación actual»</td><td>Tu posición aproximada (latitud y longitud) que te da el navegador, solo después de que aceptes su aviso de permiso.</td><td>Calcular a qué distancia están los torneos y mostrarte los más cercanos.</td><td>Tu consentimiento (art. 6.1.a RGPD), que das en el aviso del navegador y puedes retirar en sus ajustes.</td><td>No se conserva: se usa en tu dispositivo mientras tienes la web abierta y no se envía a Banderín ni a terceros. Solo se recuerda que elegiste esta opción.</td></tr>
<tr><td>Rellenas tu perfil o sigues clubes y provincias</td><td>Hándicap, año de nacimiento, sexo de competición, federación, clubes de los que eres socio y lo que sigues, solo en tu navegador.</td><td>Marcar qué torneos encajan contigo y mostrarte los de lo que sigues.</td><td>Servicio que solicitas al guardarlo (exento de consentimiento).</td><td>Hasta que lo borres desde «Mi perfil».</td></tr>
<tr><td>Creas una cuenta</td><td>Tu correo y una contraseña cifrada (o, si entras con Google, tu correo y nombre que nos facilita Google), y lo que guardas en Banderín: perfil, lo que sigues, torneos guardados y jugados.</td><td>Que entres desde cualquier dispositivo y encuentres tus datos.</td><td>Ejecución del servicio que solicitas al crear la cuenta (art. 6.1.b RGPD).</td><td>Hasta que borres la cuenta desde «Mi perfil», que lo elimina todo al instante.</td></tr>
<tr><td>Activas los avisos por correo</td><td>Tu correo, el idioma, lo que sigues (clubes, provincias y torneos guardados) y, si lo has rellenado, tu perfil de golfista, en la base de datos de Banderín en Cloudflare.</td><td>Enviarte los avisos que pides, como mucho un correo al día, sin sugerirte torneos que no encajan contigo.</td><td>Ejecución del servicio que solicitas (art. 6.1.b RGPD).</td><td>Hasta que te des de baja, que borra todo al instante. Las altas sin confirmar se borran a los 7 días y las inactivas a los 24 meses. Si tienes cuenta, se activan sin correo de confirmación porque tu dirección ya está verificada.</td></tr>
<tr><td>Eliges un idioma</td><td>El idioma, solo en tu navegador.</td><td>Mostrarte la web en el idioma que has elegido.</td><td>Servicio que solicitas (personalización de la interfaz, exenta de consentimiento).</td><td>12 meses.</td></tr>
<tr><td>Nos escribes por correo</td><td>Nombre, dirección de correo y lo que nos cuentes.</td><td>Responderte y, si es el caso, corregir o retirar un torneo.</td><td>Tu consentimiento al escribirnos (art. 6.1.a) y nuestro interés legítimo en atender solicitudes (art. 6.1.f).</td><td>El tiempo necesario para resolverlo y, después, hasta un año.</td></tr>
</tbody></table>
<p>Los datos de los torneos que mostramos se refieren a competiciones y entidades, no a personas. Banderín enlaza a los resultados oficiales, pero no copia nombres de jugadores. Si algún torneo incluye el nombre de una persona (por ejemplo, un memorial) es porque así lo publica su organizador; puedes pedirnos su corrección o retirada.</p>

<h3 id="pr-3">3. Alojamiento y proveedores</h3>
<p>La web está alojada en Cloudflare Pages (Cloudflare, Inc.), que actúa como encargado del tratamiento. Para servir la página y protegerla frente a ataques, Cloudflare trata datos técnicos de conexión, como la dirección IP y el navegador, conforme a su <a href="https://www.cloudflare.com/es-es/privacypolicy/" target="_blank" rel="noopener noreferrer">política de privacidad</a> y a su acuerdo de tratamiento de datos. Banderín no guarda registros de visitas. Las tipografías se sirven desde la propia web, sin conexión con Google.</p>
<p>Para evitar que se usen los formularios que envían correos (avisos y cuentas) de forma automatizada, Banderín cuenta los intentos con una huella cifrada de tu dirección IP que se borra sola en una hora, y puede usar Cloudflare Turnstile, una comprobación anti-robots sin cookies de seguimiento que analiza datos técnicos del navegador en ese momento.</p>
<p>Si activas los avisos por correo, tu correo y lo que sigues se guardan en una base de datos de Cloudflare, y los correos se envían a través de Brevo (Sendinblue SAS, Francia), que actúa como encargado del tratamiento con servidores en la Unión Europea, conforme a su <a href="https://www.brevo.com/es/legal/privacypolicy/" target="_blank" rel="noopener noreferrer">política de privacidad</a>. Cada correo incluye un enlace para darte de baja en un clic.</p>
<p>Si creas una cuenta, tus datos de acceso y lo que guardas se alojan en Supabase (Supabase, Inc.), que actúa como encargado del tratamiento con servidores en Fráncfort (Alemania), conforme a su <a href="https://supabase.com/privacy" target="_blank" rel="noopener noreferrer">política de privacidad</a> y a su acuerdo de tratamiento de datos con cláusulas contractuales tipo. Los correos de verificación y de cambio de contraseña se envían a través de Brevo. Si eliges «Continuar con Google», Google te identifica según su propia política y solo nos facilita tu correo y tu nombre.</p>
<p>Para no perder los datos si falla un proveedor, cada semana se hace una copia de seguridad de la base de datos de avisos (y, cuando se active, de la de cuentas) que se guarda cifrada en reposo y de forma privada en GitHub (GitHub, Inc.), como encargado del tratamiento. Cada copia se borra sola a los 35 días; si te das de baja o borras tu cuenta, tus datos desaparecen de las copias como mucho en ese plazo.</p>
<p>Si pulsas «Añadir a Google Calendar», «Inscribirme» o «Resultados», sales de Banderín hacia Google o hacia la web del organizador, que tratarán tus datos según sus propias políticas.</p>
<p>No vendemos ni cedemos datos personales a terceros, salvo obligación legal.</p>

<h3 id="pr-4">4. Transferencias internacionales</h3>
<p>Cloudflare puede tratar datos técnicos de conexión fuera del Espacio Económico Europeo. Lo hace al amparo del Marco de Privacidad de Datos UE-EE. UU., en el que está certificada, y de las cláusulas contractuales tipo aprobadas por la Comisión Europea.</p>
<p>Lo mismo ocurre con GitHub, donde se guardan las copias de seguridad: es filial de Microsoft, certificada en ese mismo Marco de Privacidad, y su acuerdo de tratamiento incluye las cláusulas contractuales tipo.</p>

<h3 id="pr-5">5. Tus derechos</h3>
<p>Puedes ejercer en cualquier momento tus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, y retirar tu consentimiento, escribiendo a {{email}} e indicando qué derecho ejerces. Si tienes cuenta, puedes descargar tus datos en un archivo desde Mi cuenta → «Descargar mis datos» y borrarla con «Eliminar mi cuenta». Te responderemos en el plazo máximo de un mes.</p>
<p>Si consideras que no hemos atendido bien tu solicitud, puedes presentar una reclamación ante la <a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer">Agencia Española de Protección de Datos</a>.</p>

<h3 id="pr-6">6. Menores</h3>
<p>Para crear una cuenta o activar los avisos por correo hay que tener 14 años o más, la edad a partir de la cual se puede consentir el tratamiento de los propios datos en España (artículo 7 de la Ley Orgánica 3/2018). Al crear la cuenta lo confirmas expresamente. Si eres menor de 14 años, puedes usar la web sin cuenta, pero no nos envíes tu correo ni otros datos personales.</p>
<p>Banderín muestra torneos de categorías juveniles, pero no publica ni guarda datos de los jugadores, tampoco de menores. Si sabes que un menor de 14 años nos ha dado sus datos, o eres su madre, padre o tutor, escríbenos a {{email}} y los borraremos.</p>

<h3 id="pr-7">7. Decisiones automatizadas</h3>
<p>No tomamos decisiones automatizadas ni elaboramos perfiles sobre ti. El orden de los torneos (por fecha, distancia o cierre de inscripción) lo eliges tú y se calcula en tu propio navegador.</p>
<p>La etiqueta «No encaja» también se calcula en tu navegador, comparando tu perfil con las condiciones que publica el organizador. Es orientativa: no te impide inscribirte y no se comunica a nadie.</p>

<h3 id="pr-8">8. Seguridad</h3>
<p>La web se sirve cifrada (HTTPS), no almacena contraseñas ni datos de pago y no tiene acceso a la información que guardas en tu navegador. Aplicamos el principio de minimización: si no necesitamos un dato, no lo pedimos.</p>

<h3 id="pr-9">9. Cambios en esta política</h3>
<p>Cuando Banderín incorpore funciones nuevas, como cuentas de usuario, actualizaremos esta política antes de activarlas y te lo indicaremos de forma visible.</p>
`},

"cookies": {
 titulo: "Política de cookies",
 intro: "Qué guarda Banderín en tu navegador, por qué y cómo cambiarlo.",
 html: `
<h3 id="co-1">1. Qué son las cookies y tecnologías similares</h3>
<p>Las cookies y tecnologías similares, como el almacenamiento local del navegador (<i>localStorage</i>), son pequeños archivos o datos que una web guarda en tu dispositivo para recordar información entre visitas. Esta política cumple el artículo 22.2 de la LSSI-CE y la Guía sobre el uso de las cookies de la AEPD.</p>

<h3 id="co-2">2. Qué usa Banderín</h3>
<p>Banderín no instala cookies de analítica, de publicidad ni de redes sociales. Las visitas se cuentan con Cloudflare Web Analytics, que no usa cookies ni almacenamiento local. Solo usa almacenamiento local del navegador, propio y sin seguimiento, con estos fines:</p>
<table class="tabla">
<thead><tr><th>Nombre</th><th>Tipo</th><th>Finalidad</th><th>Duración</th><th>¿Requiere consentimiento?</th></tr></thead>
<tbody>
<tr><td><code>banderin.consent</code></td><td>Técnica, propia</td><td>Recordar tu elección sobre cookies para no volver a preguntarte.</td><td>12 meses</td><td>No (necesaria)</td></tr>
<tr><td><code>banderin.lang</code></td><td>Personalización, propia</td><td>Recordar el idioma que has elegido.</td><td>12 meses</td><td>No (lo pides tú)</td></tr>
<tr><td><code>banderin.tema</code></td><td>Preferencias, propia</td><td>Recordar si prefieres el modo claro u oscuro.</td><td>Hasta que la borres</td><td>Sí</td></tr>
<tr><td><code>banderin.city</code> y <code>banderin.radius</code></td><td>Preferencias, propia</td><td>Recordar tu ciudad de referencia (o que elegiste usar tu ubicación, nunca tus coordenadas) y la distancia máxima para ordenar los torneos por cercanía.</td><td>Hasta que la borres</td><td>Sí</td></tr>
<tr><td><code>banderin.saved</code></td><td>Preferencias, propia</td><td>Guardar la lista de torneos que marcas con la estrella.</td><td>Hasta que la borres</td><td>Sí</td></tr>
<tr><td><code>banderin.played</code></td><td>Preferencias, propia</td><td>Guardar los torneos que marcas como jugados (tu historial).</td><td>Hasta que la borres</td><td>Sí</td></tr>
<tr><td><code>banderin.perfil</code></td><td>Personalización, propia</td><td>Guardar tu perfil de golfista para marcar los torneos que encajan contigo.</td><td>Hasta que lo borres</td><td>No (lo pides tú al guardarlo)</td></tr>
<tr><td><code>banderin.avpop</code></td><td>Interfaz, propia</td><td>Recordar que cerraste la ventana de avisos para no volver a mostrarla en 30 días.</td><td>30 días</td><td>No (necesaria para respetar tu elección)</td></tr>
<tr><td><code>banderin.sigo</code></td><td>Personalización, propia</td><td>Guardar los clubes y provincias que sigues.</td><td>Hasta que lo borres</td><td>No (lo pides tú al seguirlos)</td></tr>
<tr><td><code>banderin.sincuenta</code></td><td>Interfaz, propia</td><td>Recordar que elegiste usar el perfil sin cuenta.</td><td>Hasta que lo borres</td><td>No (necesaria para respetar tu elección)</td></tr>
<tr><td><code>sb-…-auth-token</code></td><td>Sesión, propia (Supabase)</td><td>Mantener abierta tu sesión si has entrado en tu cuenta.</td><td>Hasta que cierres sesión</td><td>No (estrictamente necesaria para el servicio que pides)</td></tr>
</tbody></table>
<p>Estos datos se quedan en tu dispositivo. Banderín no los recibe ni los comparte.</p>

<h3 id="co-3">3. Cookies de terceros</h3>
<p>Banderín no instala cookies de terceros. Cloudflare, el proveedor de alojamiento, puede usar cookies estrictamente técnicas de seguridad (por ejemplo, para distinguir visitas legítimas de tráfico automatizado), exentas de consentimiento según su <a href="https://www.cloudflare.com/es-es/cookie-policy/" target="_blank" rel="noopener noreferrer">política de cookies</a>. Banderín no carga ningún otro servicio de terceros al abrir la página.</p>

<h3 id="co-4">4. Cómo aceptar, rechazar o cambiar tu elección</h3>
<p>La primera vez que visitas Banderín te preguntamos con un aviso que tiene <b>Aceptar</b>, <b>Rechazar</b> y <b>Configurar</b> al mismo nivel. Si rechazas, la web funciona igual, pero no recordará tus preferencias al cerrar la página.</p>
<p>Puedes cambiar tu elección cuando quieras desde <a href="#" data-cookies>Configurar cookies</a>, en el pie de cualquier página. También puedes borrar los datos desde la configuración de tu navegador:</p>
<ul>
<li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer">Google Chrome</a></li>
<li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer">Safari</a></li>
<li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener noreferrer">Mozilla Firefox</a></li>
<li><a href="https://support.microsoft.com/es-es/microsoft-edge" target="_blank" rel="noopener noreferrer">Microsoft Edge</a></li>
</ul>

<h3 id="co-5">5. Actualizaciones</h3>
<p>Si en el futuro incorporamos estadísticas de uso u otros servicios, los añadiremos a esta tabla y no se activarán hasta que des tu consentimiento.</p>
`},

"terminos": {
 titulo: "Términos de uso",
 intro: "Las reglas del servicio, explicadas sin rodeos.",
 html: `
<h3 id="te-1">1. El servicio</h3>
<p>Banderín es un buscador gratuito de torneos de golf en España. Te permite buscar, filtrar, guardar, marcar como jugados y abrir la ficha oficial de cada torneo. No necesitas cuenta para usarlo.</p>
<p>Si eliges «Usar mi ubicación actual», el navegador te pedirá permiso. La ubicación solo sirve para calcular distancias en tu dispositivo, puede no ser exacta y no se guarda ni se envía a ningún sitio. Puedes retirar el permiso cuando quieras en los ajustes del navegador.</p>

<h3 id="te-2">2. De dónde sale la información</h3>
<p>Los torneos proceden de fuentes públicas: plataformas de inscripción, federaciones y organizadores. Puedes ver la lista completa en la sección <a href="#fuentes">Fuentes</a>. Revisamos los datos cada mañana y comprobamos que cada enlace responde antes de publicarlo.</p>
<p>Aun así, los organizadores pueden cambiar fechas, precios, plazas o condiciones en cualquier momento. <b>La información válida es siempre la que publica el organizador.</b> Las distancias son aproximadas y en línea recta.</p>

<h3 id="te-3">3. Inscripciones y resultados</h3>
<p>Al pulsar «Inscribirme» o «Resultados» sales de Banderín hacia la web del organizador o de su plataforma. La inscripción, el pago, las devoluciones, la admisión y la clasificación oficial se rigen por las condiciones de ese organizador. Banderín no interviene en esa relación ni responde de ella.</p>

<h3 id="te-4">4. Uso correcto</h3>
<p>Te comprometes a usar Banderín de forma lícita y a no intentar dañar su funcionamiento, acceder a partes no públicas ni suplantar a otras personas u organizaciones.</p>

<h3 id="te-5">5. Organizadores</h3>
<p>Si organizas un torneo, puedes pedirnos que corrijamos, completemos o retiremos su información escribiendo a {{email}}. Atendemos estas solicitudes en un plazo máximo de 72 horas hábiles.</p>

<h3 id="te-6">6. Disponibilidad y cambios</h3>
<p>Banderín se ofrece tal cual y puede interrumpirse temporalmente por mantenimiento o por fallos de las fuentes. Podemos modificar, ampliar o retirar funciones, y actualizar estos términos; la fecha de la última versión aparece al final de esta página.</p>

<h3 id="te-7">7. Responsabilidad</h3>
<p>En la medida en que lo permita la ley, el titular no responde de los perjuicios derivados de información inexacta o desactualizada facilitada por terceros, de cancelaciones o cambios decididos por los organizadores, ni del contenido de los sitios enlazados. Nada en estos términos limita los derechos que te reconoce la normativa de consumidores.</p>

<h3 id="te-8">8. Ley y jurisdicción</h3>
<p>Estos términos se rigen por la ley española. Si eres consumidor, podrás acudir a los juzgados de tu domicilio.</p>
`}
};
