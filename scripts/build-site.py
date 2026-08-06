#!/usr/bin/env python3
"""Build the private (prep) and public (portfolio) editions from one source."""
import re, sys, pathlib

SRC = pathlib.Path('wwe-prep-hub.html')
CSS = pathlib.Path('newstyle.css')
OUT = pathlib.Path('build'); OUT.mkdir(exist_ok=True)

# emoji that must go; everything else (★ ← → · ▍) must survive
EMOJI = ['🟢', '🟡', '🔴', '⚠', '📊', '⭐', '❌', '✓', '✕']


def restyle(h):
    css = CSS.read_text()
    for m in reversed(list(re.finditer(r'<style>.*?</style>', h, re.S))):
        h = h[:m.start()] + h[m.end():]
    return '<style>\n' + css + '\n</style>\n' + h.lstrip('\n')


def deemoji(h):
    for e in EMOJI:
        h = h.replace(e + ' ', '').replace(e, '')
    return h


def renumber(h):
    n = [0]
    def rep(m):
        n[0] += 1
        return '<p class="kicker">Section %02d</p>' % n[0]
    return re.sub(r'<p class="kicker">Section[^<]*</p>', rep, h)


def drop_section(h, sid):
    m = re.search(r'\n\s*<!-- =+[^\n]*-->\n\s*<section id="%s">' % sid, h)
    start = m.start() if m else h.index('<section id="%s">' % sid)
    end = h.index('</section>', start) + len('</section>')
    return h[:start] + h[end:]


def span_replace(h, start_txt, end_txt, new):
    """Replace from start_txt through end_txt inclusive. Whitespace-safe."""
    i = h.find(start_txt)
    if i == -1:
        print('  ! not found:', start_txt[:52]); return h
    j = h.index(end_txt, i) + len(end_txt)
    return h[:i] + new + h[j:]


def make_public(h):
    for sid in ('files', 'lines'):
        h = drop_section(h, sid)
    h = re.sub(r'\n\s*<dl class="facts">.*?</dl>', '', h, flags=re.S)
    h = re.sub(r'\n\s*<div class="panel audit".*?</div>\s*(?=</section>)', '\n', h, flags=re.S)
    h = re.sub(r'\s*<a href="#(files|lines)">[^<]*</a>', '', h)

    # --- de-personalise ---
    h = span_replace(h,
        'Four artifacts, one argument', 'revenue guardrail.',
        'One argument: the growth opportunity on this title is an <strong>activation and '
        'social-on-ramp</strong> opportunity, diagnosed from a firsthand new-player playthrough and '
        '2,945 analysed player reviews — and every bet ships as an experiment with a revenue guardrail.')
    h = span_replace(h,
        'Your 3 Rs (Reach / Retention / Revenue)', 'speaking her framework.',
        'The 3 Rs — Reach, Retention, Revenue — mapped onto a player-lifecycle growth funnel, so every '
        'finding lands in the stage it belongs to: acquisition → activation → retention → DAU.')
    h = span_replace(h,
        'The single most defensible thing', 'our numbers."',
        'The discipline this analysis runs on: every claim is tagged, so player sentiment is never '
        'confused with measured fact.')
    h = span_replace(h,
        'This is current, specific', 'bet 2.',
        'It is current, specific, and it bears directly on bet 2.')
    h = span_replace(h,
        "If that's accurate, then walking in", 'best question instead.</b>',
        'If that is accurate, "protect the faction crown jewel" is the wrong framing — <b>the question '
        'is what the retention data showed around that change.</b>')
    h = span_replace(h,
        'Naming the gaps proactively', 'far better than you do.',
        "Every analysis should name what it can't see. The second list is claims that were investigated "
        'and refuted — recorded so they are not repeated.')
    h = span_replace(h,
        'Screenshots from your League 1–2 playthrough', 'has them.',
        'Screenshots captured during a League 1–2 playthrough in July 2026, with captions checked '
        'against what is actually on screen.')
    h = span_replace(h,
        'Quoted exactly, with handle, rating, date', 'than any summary.',
        'Quoted exactly, with handle, rating, date and upvote count where available. Highlights are mine.')

    h = span_replace(h,
        'Each bet traces', 'from your playthrough.',
        'Each bet traces back to a diagnostic card above and forward to a screenshot from the playthrough.')

    PAIRS = [
        ('<title>WWE Champions — Growth PM Prep Hub</title>', '<title>WWE Champions — A Growth Diagnosis</title>'),
        ('Prep hub for the Director loop', 'Independent product analysis · Aug 2026'),
        ('Everything in this folder,<br><em>and what each thing is for</em>',
         'A growth diagnosis of<br><em>WWE Champions</em>'),
        ('<h2>Your own tape, verified</h2>', '<h2>Firsthand playthrough</h2>'),
        ('<h2>Gaps to name, claims to avoid</h2>', '<h2>Known gaps &amp; refuted claims</h2>'),
        ('<h2>Something changed in late 2025 — ask about it</h2>', '<h2>Something changed in late 2025</h2>'),
        ('<h3>Say these are unknown</h3>', '<h3>Unknown without internal data</h3>'),
        ('<h3>Do not assert these</h3>', '<h3>Investigated and refuted</h3>'),
        ('Three caveats — volunteer all of them', 'Three caveats on this dataset'),
        ('>Your tape, verified<', '>Firsthand playthrough<'),
        (">Gaps &amp; don't-says<", '>Gaps &amp; refuted claims<'),
        ('Say this early — it frames everything after it', 'Evidence discipline, stated up front'),
        ('Directly answers the player-behavior &amp; segmentation requirement', 'Segmentation before prescription'),
        ('The sequencing answer — have this one cold', 'Sequencing logic'),
        ('If you only land one idea with the Director, land this one', 'The core strategic tension'),
        ('Closes the analytics-loop bar', 'The analytics loop'),
        ('Now backed by 6× the data and cross-platform replication — say it with confidence',
         'Replicated across both platforms on 2,945 reviews'),
        ('Ask this. It shows you read current signal, and it hands them the floor',
         'The open question this raises'),
        ('Your entire thesis in four words, from a player who still gave it 4★ after spending $600. Lead with this one.',
         'The whole thesis in four words, from a player who still gave it 4★ after spending $600.'),
        ("Say this one out loud; it's generous and it's true.", "Credit where it's due to the current team."),
        ('WWE Champions · Growth PM prep hub', 'WWE Champions · independent growth analysis'),
    ]
    for a, b in PAIRS:
        if a in h: h = h.replace(a, b)
        else: print('  ! pair missed:', a[:56])

    # link to the prototype
    h = h.replace('    <p class="dek">',
        '    <p><a href="/">← Play the interactive prototype</a></p>\n    <p class="dek">', 1)
    return h


def audit(h, label):
    bad = [w for w in ['Jenny', 'Jerome', 'hiring team', 'prep hub', 'Prep hub', 'the room',
                       'Lead with this', 'you should', 'rehearse', 'her framework', 'her language',
                       'Say this', 'have this one cold', "don't-says"] if w in h]
    stars = h.count('★')
    print(f'  [{label}] leaks={bad or "clean"}  stars={stars}  emoji={len(re.findall(chr(0x1F300)+"-"+chr(0x1FAFF), h))}')
    return not bad


src = SRC.read_text()

priv = renumber(deemoji(restyle(src)))
(OUT / 'private.html').write_text(priv)
print(f'  [private] built, stars={priv.count(chr(0x2605))}')

pub = renumber(deemoji(restyle(make_public(src))))
(OUT / 'public.html').write_text(pub)
ok = audit(pub, 'public')

print(f"  private {len(priv)/1024/1024:.2f} MB · public {len(pub)/1024/1024:.2f} MB")
sys.exit(0 if ok else 1)
