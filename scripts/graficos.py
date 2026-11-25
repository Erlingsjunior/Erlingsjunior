"""Gera os gráficos SVG do perfil (tema claro e escuro) a partir de números conferidos no repositório do KARMIKA.
Para atualizar: troque os números em DADOS e rode `python3 scripts/graficos.py` na raiz do repositório."""
from pathlib import Path

DADOS = {
    'conferido_em': '24/11/2026',
    # registros (commits) na branch main do KARMIKA, por semana ISO; a última semana está incompleta
    'semanas': [('24–25 out', 49), ('26 out–1 nov', 139), ('2–8 nov', 186), ('9–15 nov', 262), ('16–22 nov', 56), ('23–24 nov', 34)],
    'tiles': [('726', 'registros em 32 dias'), ('98%', 'feitos em par com IA'), ('57 mil', 'linhas de TypeScript'), ('1.721', 'missões escritas'), ('4', 'idiomas no livro')],
}
# Tagged: repositório do app (todas as branches, registros únicos), do primeiro registro (ago/2025) ao último (set/2026)
TAGGED = {
    'meses': [('ago', 1), ('set', 12), ('out', 0), ('nov', 0), ('dez', 0), ('jan', 89), ('fev', 7), ('mar', 3), ('abr', 7), ('mai', 0), ('jun', 6), ('jul', 40), ('ago', 78), ('set', 102)],
    'anos': [(0, '2025'), (5, '2026')],
    'tiles': [('345', 'registros no app'), ('14', 'meses de histórico'), ('51%', 'feitos em par com IA'), ('59', 'registros na landing'), ('9', 'branches de trabalho')],
}
TEMAS = {
    'claro': dict(bg='#ffffff', borda='#d1d9e0', fg='#1f2328', mudo='#59636e', grade='#e6eaef', barra='#9a6b12', fraca='#d8c39a', laranja='#c2410c'),
    'escuro': dict(bg='#0d1117', borda='#30363d', fg='#e6edf3', mudo='#9198a1', grade='#21262d', barra='#c08c28', fraca='#5c4a26', laranja='#e0542a'),
}
FONTE = "font-family='-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif'"
OUT = Path(__file__).resolve().parent.parent / 'assets'

def tiles(t, D=DADOS):
    W, H, n = 840, 132, len(D['tiles']); w = (W - 32 - (n - 1) * 12) / n
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='{D.get("nome", "KARMIKA")} em números'>",
         f"<rect x='0.5' y='0.5' width='{W-1}' height='{H-1}' rx='12' fill='{t['bg']}' stroke='{t['borda']}'/>"]
    for i, (num, rot) in enumerate(D['tiles']):
        x = 16 + i * (w + 12)
        s.append(f"<rect x='{x:.1f}' y='16' width='{w:.1f}' height='{H-32}' rx='8' fill='none' stroke='{t['grade']}'/>")
        s.append(f"<rect x='{x+14:.1f}' y='30' width='22' height='4' rx='2' fill='{t['barra']}'/>")
        s.append(f"<text x='{x+14:.1f}' y='72' {FONTE} font-size='30' font-weight='700' fill='{t['fg']}'>{num}</text>")
        s.append(f"<text x='{x+14:.1f}' y='96' {FONTE} font-size='12.5' fill='{t['mudo']}'>{rot}</text>")
    s.append('</svg>'); return '\n'.join(s)

def semanas(t):
    W, H = 840, 300; L, R, T, B = 56, 24, 64, 56; pw, ph = W - L - R, H - T - B
    dados = DADOS['semanas']; mx = 300; n = len(dados); slot = pw / n; bw = min(64, slot * 0.5)
    y = lambda v: T + ph - v / mx * ph
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='Registros por semana no KARMIKA'>",
         f"<rect x='0.5' y='0.5' width='{W-1}' height='{H-1}' rx='12' fill='{t['bg']}' stroke='{t['borda']}'/>",
         f"<text x='24' y='32' {FONTE} font-size='15' font-weight='600' fill='{t['fg']}'>KARMIKA: registros por semana na branch main</text>",
         f"<text x='24' y='50' {FONTE} font-size='12' fill='{t['mudo']}'>Do primeiro registro (24/10) a {DADOS['conferido_em']}. A última semana ainda está em andamento.</text>"]
    for v in (0, 100, 200, 300):
        s.append(f"<line x1='{L}' x2='{W-R}' y1='{y(v):.1f}' y2='{y(v):.1f}' stroke='{t['grade']}' stroke-width='1'/>")
        s.append(f"<text x='{L-8}' y='{y(v)+4:.1f}' text-anchor='end' {FONTE} font-size='11' fill='{t['mudo']}'>{v}</text>")
    for i, (rot, v) in enumerate(dados):
        cx = L + slot * (i + 0.5); x = cx - bw / 2; top = y(v); h = T + ph - top; parcial = i == n - 1
        cor = t['fraca'] if parcial else t['barra']
        s.append(f"<path d='M{x:.1f},{T+ph} V{top+4:.1f} Q{x:.1f},{top:.1f} {x+4:.1f},{top:.1f} H{x+bw-4:.1f} Q{x+bw:.1f},{top:.1f} {x+bw:.1f},{top+4:.1f} V{T+ph} Z' fill='{cor}'><title>{rot}: {v} registros{' (semana em andamento)' if parcial else ''}</title></path>")
        s.append(f"<text x='{cx:.1f}' y='{top-8:.1f}' text-anchor='middle' {FONTE} font-size='12' font-weight='600' fill='{t['fg']}'>{v}</text>")
        s.append(f"<text x='{cx:.1f}' y='{T+ph+20:.1f}' text-anchor='middle' {FONTE} font-size='11.5' fill='{t['mudo']}'>{rot}{' *' if parcial else ''}</text>")
    s.append(f"<line x1='{L}' x2='{W-R}' y1='{T+ph}' y2='{T+ph}' stroke='{t['mudo']}' stroke-width='1'/>")
    s.append('</svg>'); return '\n'.join(s)

def meses(t):
    W, H = 840, 300; L, R, T, B = 56, 24, 64, 64; pw, ph = W - L - R, H - T - B
    dados = TAGGED['meses']; mx = 120; n = len(dados); slot = pw / n; bw = min(34, slot * 0.6)
    y = lambda v: T + ph - v / mx * ph
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='Registros por mês no app da Tagged'>",
         f"<rect x='0.5' y='0.5' width='{W-1}' height='{H-1}' rx='12' fill='{t['bg']}' stroke='{t['borda']}'/>",
         f"<text x='24' y='32' {FONTE} font-size='15' font-weight='600' fill='{t['fg']}'>Tagged: registros por mês no app</text>",
         f"<text x='24' y='50' {FONTE} font-size='12' fill='{t['mudo']}'>Todas as branches, de agosto de 2025 a setembro de 2026.</text>"]
    for v in (0, 40, 80, 120):
        s.append(f"<line x1='{L}' x2='{W-R}' y1='{y(v):.1f}' y2='{y(v):.1f}' stroke='{t['grade']}' stroke-width='1'/>")
        s.append(f"<text x='{L-8}' y='{y(v)+4:.1f}' text-anchor='end' {FONTE} font-size='11' fill='{t['mudo']}'>{v}</text>")
    for i, (rot, v) in enumerate(dados):
        cx = L + slot * (i + 0.5); x = cx - bw / 2; top = y(v)
        if v: s.append(f"<path d='M{x:.1f},{T+ph} V{top+4:.1f} Q{x:.1f},{top:.1f} {x+4:.1f},{top:.1f} H{x+bw-4:.1f} Q{x+bw:.1f},{top:.1f} {x+bw:.1f},{top+4:.1f} V{T+ph} Z' fill='{t['laranja']}'><title>{rot}: {v} registros</title></path>")
        if v >= 10: s.append(f"<text x='{cx:.1f}' y='{top-8:.1f}' text-anchor='middle' {FONTE} font-size='12' font-weight='600' fill='{t['fg']}'>{v}</text>")
        s.append(f"<text x='{cx:.1f}' y='{T+ph+18:.1f}' text-anchor='middle' {FONTE} font-size='11' fill='{t['mudo']}'>{rot}</text>")
    for i, ano in TAGGED['anos']:
        s.append(f"<text x='{L + slot * i + 4:.1f}' y='{T+ph+36:.1f}' {FONTE} font-size='11' font-weight='600' fill='{t['fg']}'>{ano}</text>")
    s.append(f"<line x1='{L}' x2='{W-R}' y1='{T+ph}' y2='{T+ph}' stroke='{t['mudo']}' stroke-width='1'/>")
    s.append('</svg>'); return '\n'.join(s)

for nome, t in TEMAS.items():
    (OUT / f'tagged-numeros-{nome}.svg').write_text(tiles({**t, 'barra': t['laranja']}, {**TAGGED, 'nome': 'Tagged'}), encoding='utf8')
    (OUT / f'tagged-meses-{nome}.svg').write_text(meses(t), encoding='utf8')
    (OUT / f'karmika-numeros-{nome}.svg').write_text(tiles(t), encoding='utf8')
    (OUT / f'karmika-semanas-{nome}.svg').write_text(semanas(t), encoding='utf8')
print('ok')
