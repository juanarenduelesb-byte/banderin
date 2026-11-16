#!/usr/bin/env python3
"""Banderín - genera las plantillas de correo de las cuentas (Supabase) con el diseño de correo.py.

  python3 pipeline/correos_supabase.py
Escribe db/correos-supabase/*.html. Después hay que pegar cada una en Supabase →
Authentication → Emails → Templates (Confirm signup, Reset password, Change email address).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import correo as c  # noqa: E402

URL = '{{ .ConfirmationURL }}'
FOOT = ('Recibes este correo porque se ha pedido desde banderin.es.<br>'
        'Banderín - un proyecto de Esclusa - Confirma siempre fechas y condiciones con el organizador.')
NOTA = lambda t: c.para(c.e(t) + '<br><span style="color:#8A958E">If you didn\'t request this, ignore this email.</span>', 13, '#6B776F', '26px 0 0')
PLANTILLAS = {
    'confirmar': ('Confirma tu cuenta de Banderín', 'Un clic y tu golf queda guardado en tu cuenta.', 'Confirma tu correo',
                  'Pulsa el botón para activar tu cuenta. A partir de ahí, tu perfil, lo que sigues, tus guardados y tus avisos '
                  'estarán en cualquier dispositivo en el que entres.', 'Activar mi cuenta',
                  'Si no has creado una cuenta en Banderín, ignora este correo y no pasará nada.'),
    'recuperar': ('Cambia tu contraseña de Banderín', 'Enlace para elegir una contraseña nueva.', 'Elige una contraseña nueva',
                  'Has pedido cambiar la contraseña de tu cuenta. El enlace caduca en una hora.', 'Cambiar contraseña',
                  'Si no lo has pedido tú, ignora este correo: tu contraseña sigue igual.'),
    'cambio-correo': ('Confirma tu nuevo correo en Banderín', 'Confirma el cambio de correo de tu cuenta.', 'Confirma tu nuevo correo',
                      'Pulsa el botón para que tu cuenta de Banderín use esta dirección a partir de ahora.', 'Confirmar el cambio',
                      'Si no lo has pedido tú, ignora este correo.'),
}
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'correos-supabase')
for name, (title, pre, h, body, btn, note) in PLANTILLAS.items():
    inner = c.h1(h) + c.para(c.e(body)) + c.button(URL, btn) + NOTA(note)
    # el botón lleva la variable de Supabase sin escapar
    html = c.shell('es', title, pre, 'Tu cuenta', inner, FOOT).replace(c.e(URL), URL)
    open(os.path.join(dest, name + '.html'), 'w', encoding='utf-8').write(html)
    print('escrita', name)
