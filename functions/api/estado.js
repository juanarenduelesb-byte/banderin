import { enabled, json } from '../../lib/avisos.js';

// La web pregunta si los avisos están disponibles para mostrar el formulario o «Próximamente».
export const onRequestGet = ({ env }) => json({ avisos: enabled(env) });
