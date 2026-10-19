# auditoria.json -> auditoria.html: una página con el nombre del negocio, lo que pierde al mes y las 3 fugas con su prueba
#   python3 auditoria.py ~/Auditorias/<negocio>/
import html, json, sys, urllib.parse
from pathlib import Path

d = Path(sys.argv[1] if len(sys.argv) > 1 else '.').expanduser()
A = json.load(open(d / 'auditoria.json', encoding='utf-8'))
e = lambda s: html.escape(str(s or ''))
eur = lambda n: f'{round(n):,}'.replace(',', '.') + ' €'
MESES = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()
a, m, dd = (A.get('fecha') or '2026-01-01').split('-')
fecha = f'{int(dd)} de {MESES[int(m) - 1]} de {a}'
total = A.get('total_mes') or sum(f['euros_mes'] for f in A['fugas'])

au = A.get('autor', {}); c = au.get('contacto', {}); v = c.get('valor', '')
msg = f'Hola, he visto la auditoría de {A["negocio"]} y quiero hablarlo.'
if c.get('tipo') == 'whatsapp': href, cta = 'https://wa.me/' + ''.join(ch for ch in v if ch.isdigit()) + '?text=' + urllib.parse.quote(msg), 'Hablarlo por WhatsApp'
elif c.get('tipo') == 'email': href, cta = f'mailto:{v}?subject=' + urllib.parse.quote(f'Auditoría {A["negocio"]}') + '&body=' + urllib.parse.quote(msg), 'Contestar por email'
else: href, cta = v or '#', 'Reservar 15 minutos'

fugas = ''
for i, f in enumerate(A['fugas'], 1):
    p = f.get('prueba', {})
    fugas += f'''
  <article class="fuga">
    <div class="fcab"><span class="n">{i}</span><h3>{e(f["titulo"])}</h3><span class="eur">−{eur(f["euros_mes"])}<small>/mes</small></span></div>
    <blockquote>{e(p.get("texto"))}<cite>{e(p.get("fuente"))}</cite></blockquote>
    <p>{e(f["que_pasa"])}</p>
    <p class="calc"><b>Cómo lo calculamos</b>{e(f["calculo"])} ≈ <b class="r">{eur(f["euros_mes"])} al mes</b></p>
    <p class="sol"><b>Cómo se arregla</b>{e(f["solucion"])}</p>
  </article>'''
barras = ''.join(f'<i style="flex:{f["euros_mes"]}" title="{e(f["titulo"])}"></i>' for f in A['fugas'])
extras = ''.join(f'<li>{e(x)}</li>' for x in A.get('extras', []))
aviso = '<div class="aviso">Ejemplo con un negocio ficticio</div>' if A.get('ejemplo') else ''

page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Auditoría · {e(A["negocio"])}</title>
<meta name="robots" content="noindex">
<style>
:root{{--papel:#f6f2ea;--tinta:#16130f;--gris:#6d665c;--linea:#e2dacb;--rojo:#c8452c;--verde:#1f7a46;--amar:#ffe27a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--papel);color:var(--tinta);font:17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}}
main{{max-width:720px;margin:0 auto;padding:40px 20px 80px}}
.aviso{{background:var(--tinta);color:var(--papel);text-align:center;font-size:13px;padding:8px;letter-spacing:.04em}}
.eti{{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--gris)}}
h1{{font-size:clamp(34px,7vw,52px);line-height:1.05;letter-spacing:-.03em;margin:10px 0 18px}}
.total{{background:#fff;border:1px solid var(--linea);border-radius:20px;padding:28px 26px;margin:26px 0 12px}}
.total .k{{font-size:15px;color:var(--gris)}}
.total .v{{font-size:clamp(52px,13vw,88px);font-weight:800;letter-spacing:-.04em;color:var(--rojo);line-height:1;margin:6px 0 4px}}
.total .v small{{font-size:.32em;color:var(--gris);font-weight:600;letter-spacing:0}}
.barra{{display:flex;gap:4px;height:10px;margin-top:18px}}.barra i{{background:var(--rojo);border-radius:6px;opacity:.85}}.barra i:nth-child(2){{opacity:.6}}.barra i:nth-child(3){{opacity:.38}}
.lead{{font-size:19px;color:#3a352e}}
h2{{font-size:24px;letter-spacing:-.02em;margin:48px 0 14px}}
.fuga{{background:#fff;border:1px solid var(--linea);border-radius:18px;padding:22px 22px 8px;margin:14px 0}}
.fcab{{display:flex;align-items:center;gap:12px}}.fcab h3{{flex:1;margin:0;font-size:20px;letter-spacing:-.01em}}
.n{{width:30px;height:30px;border-radius:50%;background:var(--tinta);color:#fff;display:grid;place-items:center;font-weight:700;font-size:15px;flex:none}}
.eur{{font-weight:800;color:var(--rojo);font-size:20px;white-space:nowrap}}.eur small{{font-weight:600;font-size:13px;color:var(--gris)}}
blockquote{{margin:16px 0 10px;padding:12px 14px;background:#fbf8f1;border-left:4px solid var(--amar);border-radius:8px;font-size:15.5px}}
cite{{display:block;font-style:normal;font-size:12.5px;color:var(--gris);margin-top:6px}}
.calc,.sol{{font-size:15px;border-top:1px dashed var(--linea);padding-top:12px}}.calc b:first-child,.sol b:first-child{{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-bottom:2px}}
.calc .r{{color:var(--rojo)}}.sol{{color:var(--verde)}}.sol b:first-child{{color:var(--verde)}}
ul{{padding-left:20px}}li{{margin:6px 0}}
.metodo{{font-size:14.5px;color:var(--gris)}}
.cta{{display:block;text-align:center;background:var(--tinta);color:#fff;text-decoration:none;font-weight:700;font-size:18px;padding:18px;border-radius:14px;margin:34px 0 12px}}
.pie{{text-align:center;font-size:13.5px;color:var(--gris)}}
@media print{{.cta{{border:2px solid var(--tinta)}}.fuga,.total{{break-inside:avoid}}}}
</style></head><body>
{aviso}
<main>
  <div class="eti">Auditoría · {e(A["negocio"])} · {e(A.get("ciudad"))} · {fecha}</div>
  <h1>{e(A.get("saludo") or A["negocio"])}, se os escapan unos {eur(total)} al mes.</h1>
  <p class="lead">{e(A.get("resumen"))}</p>
  <div class="total"><div class="k">Lo que perdéis al mes, por lo bajo</div><div class="v">{eur(total)}<small> /mes</small></div>
    <div class="k">≈ {eur(total * 12)} al año</div><div class="barra">{barras}</div></div>
  <h2>Las 3 fugas</h2>{fugas}
  {f'<h2>Además</h2><ul>{extras}</ul>' if extras else ''}
  <h2>Cómo lo hemos calculado</h2>
  <p class="metodo">Todo sale de lo que se ve en público: vuestra web ({e(A.get("web"))}), vuestras reseñas y vuestras redes.
  Los precios son los vuestros cuando los publicáis y, si no, la media de vuestro sector. Hemos tirado siempre por lo bajo:
  lo más probable es que la cifra real sea mayor. Si algún dato no os cuadra, decídnoslo y lo recalculamos con el vuestro.</p>
  <a class="cta" href="{e(href)}">{cta}</a>
  <p class="pie">Preparado por {e(au.get("nombre"))}{" · " + e(au.get("marca")) if au.get("marca") else ""}</p>
</main></body></html>'''
(d / 'auditoria.html').write_text(page, encoding='utf-8')
print(d / 'auditoria.html')
