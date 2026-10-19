# Auditoría · skill de Claude Code

Un agente de Claude con un único trabajo: **descubrir cuánto dinero pierde un negocio**. Le das su web o su Instagram y lo que tú sabes montar, y:

1. **Inspecciona** su web, sus reseñas y su Instagram.
2. **Encuentra las 3 fugas** que más le cuestan y que tú sabes arreglar (reservas solo por teléfono, presupuestos a mano, mensajes sin contestar…), cada una con su prueba.
3. **Calcula lo que le cuesta** al mes, con números que el dueño puede comprobar.
4. Te deja **una página con su nombre** (ejemplo en [`ejemplo/auditoria.html`](ejemplo/auditoria.html)).
5. Te **escribe el mensaje** para mandárselo por WhatsApp, Instagram o email.

En vez de ignorarte, te contesta: ve su nombre y lo que pierde. Funciona con el plan de Claude que ya pagas (Pro o Max), sin API aparte. **Nada se envía solo: el mensaje lo mandas tú.**

Hecha por [Denis Corral · Sell Your AI](https://sellyourai.io).

## Instalación

```bash
git clone https://github.com/deniscorral3am/auditoria-skill.git ~/.claude/skills/auditoria
```

## Uso

Abre Claude Code (`claude`) y escribe **`/auditoria`** con la web o el Instagram del negocio:

```
/auditoria https://pizzerialuigi.es
```

La primera vez te pregunta qué sabes montar, tu nombre y cómo te contactan (se guarda en `~/Auditorias/perfil.json`).
Cada auditoría queda en `~/Auditorias/<negocio>/`: `inspeccion.md`, `auditoria.html` y `mensaje.md`.

Para mandar la página: imprímela a PDF o arrastra la carpeta a [Netlify Drop](https://app.netlify.com/drop) y te da un enlace.

## Qué hay dentro

| Archivo | Qué es |
|---|---|
| `SKILL.md` | El proceso paso a paso |
| `ref/fugas.md` | Catálogo de fugas por sector, con señales, fórmulas y medias orientativas |
| `motor/auditoria.py` | Genera la página de auditoría desde `auditoria.json` (solo Python, sin dependencias) |
| `ejemplo/` | Auditoría completa de un negocio ficticio |

## Licencia

MIT.
