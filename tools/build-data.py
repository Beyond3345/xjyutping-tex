#!/usr/bin/env python3
"""Generate the xjyutping data files from the upstream sources.

    python3 tools/build-data.py [--sources DIR] [--py-data DIR]

Run it from anywhere; paths are resolved from this file.  The sources are
third-party data kept outside the repository, by default in the directory
that contains this repository (see tools/fetch-sources.sh):

  jyutping-table-master/list.tsv               LSHK Jyutping table, CC BY 4.0
  rime-cantonese/jyut6ping3.chars.dict.yaml    rime-cantonese, CC BY 4.0
  rime-cantonese/jyut6ping3.words.dict.yaml    rime-cantonese, CC BY 4.0
  opencc/HKVariants.txt, opencc/TWVariants.txt OpenCC, Apache-2.0

Outputs:
  xjyutping-chars.def   (this repository) default reading of every
                        character, polyphone flags, variant -> canonical
                        character map, run-final readings
  xjyutping-words.def   (this repository) word readings, max word length
                        per final character
  --py-data DIR         the same tables as UTF-8 TSV for the Python package
                        xjyutping-py (default: ../xjyutping-py/src/xjyutping/
                        data next to this repository, if it exists):
      chars.tsv     char, default, other readings (space separated), 1 if
                    polyphone else 0
      finals.tsv    char, reading at the end of a run
      variants.tsv  variant, canonical character
      words.tsv     word (and canonical-spelling alias), readings
"""
import collections
import math
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent     # xjyutping-tex
ROOT = REPO.parent                                         # the sources
PY_DATA = ROOT / 'xjyutping-py' / 'src' / 'xjyutping' / 'data'
SYL = re.compile(r'^[a-z]+[1-6]$')
VERSION = '2026/09/28 v1.1.0'

# Standalone default readings.  The first block settles characters that
# rime-cantonese leaves undecided (every reading has the same weight); the
# second overrides literary or rare defaults whose standalone use in Hong Kong
# text is clearly something else.  Words and phrases come from the word
# list; these only apply to a character standing alone.
CURATED_DEFAULTS = {
    '會': 'wui5',   # 我會去 (will/can); 開會, 社會 ... come from the word list
    '生': 'saang1', # 生仔, 生嘅; 生活/學生 come from the word list
    '行': 'haang4', # 行去 (walk); 銀行/行為 come from the word list
    '畫': 'waa2',   # 一幅畫
    '料': 'liu2',   # 有料, 材料 via words
    '咪': 'mai6',   # 咪係囉
    '咯': 'lok3',
    '率': 'leot2',
    '刊': 'hon2',
    '撈': 'lou1',
    '彙': 'wui6',
    '嗎': 'maa3',
    '嘎': 'gaa4',
    '咧': 'le4',
    '量': 'loeng6', # 廢物量, 交易量; the verb 量 comes from words

    '返': 'faan1',  # 得返, 返中環; literary 往返/返回 are words
    '呀': 'aa3',    # the ordinary particle (LSHK has no aa4)
    '驚': 'geng1',  # 好驚, 唔使驚; 驚喜/震驚 are words
    '吓': 'haa5',   # aspect marker 睇吓, 試吓
    '爭': 'zaang1', # 爭我一百蚊; 爭取/競爭 are words
    '划': 'waa4',   # 划算, 划船 (劃 carries waak6)
    '幢': 'zong6',  # classifier; LSHK has no dung6
    '呢': 'ni1',    # demonstrative 呢張床; see CURATED_FINALS
}

# A different reading when the character ends a run of Chinese characters
# (before punctuation, Latin text or the end): the particle 呢 in 你呢？
CURATED_FINALS = {
    '呢': 'ne1',
}

# Variant shapes missing from the OpenCC tables.
CURATED_VARIANTS = {
    '恒': '恆',
}

# Word readings to add or correct on top of rime-cantonese.  Several are
# guards: longer words that keep a new entry from capturing a phrase it
# should not (集中咗 for 中咗, 絕種咗 for 種咗 ...).
CURATED_WORDS = {
    # rime errors
    '畀咗': 'bei2 zo2', '畀咗你': 'bei2 zo2 nei5', '畀咗佢': 'bei2 zo2 keoi5',
    '畀咗我': 'bei2 zo2 ngo5', '畀咗未': 'bei2 zo2 mei6',
    '畀咗錢': 'bei2 zo2 cin2', '畀咗錢未': 'bei2 zo2 cin2 mei6',
    '有朋自遠方來': 'jau5 pang4 zi6 jyun5 fong1 loi4',
    '相處': 'soeng1 cyu5', '共處': 'gung6 cyu5',
    '前人種樹': 'cin4 jan4 zung3 syu6',
    '少壯': 'siu3 zong3', '少壯不努力': 'siu3 zong3 bat1 nou5 lik6',
    '世上無難事': 'sai3 soeng6 mou4 naan4 si6',
    '屢見不鮮': 'leoi5 gin3 bat1 sin1',
    '外銷量': 'ngoi6 siu1 loeng6', '碳排放量': 'taan3 paai4 fong3 loeng6',
    '輸送量': 'syu1 sung3 loeng6',
    '會唔會': 'wui5 m4 wui5', '幾度': 'gei2 dou6', '揣度': 'cyun2 dok6',
    '間房': 'gaan1 fong2', '成日': 'seng4 jat6', '係呀': 'hai6 aa3',
    # literary words that must keep their reading after a default change
    '返回': 'faan2 wui4', '返鄉': 'faan2 hoeng1', '返航': 'faan2 hong4',
    '返程': 'faan2 cing4', '返還': 'faan2 waan4', '返國': 'faan2 gwok3',
    '積重難返': 'zik1 zung6 naan4 faan2',
    '驚聞': 'ging1 man4', '驚見': 'ging1 gin3', '驚爆': 'ging1 baau3',
    '驚現': 'ging1 jin6', '驚叫': 'ging1 giu3', '驚傳': 'ging1 cyun4',
    '驚變': 'ging1 bin3', '驚艷': 'ging1 jim6', '驚悉': 'ging1 sik1',
    '大吃一驚': 'daai6 hek3 jat1 ging1',
    '量體溫': 'loeng4 tai2 wan1', '量血壓': 'loeng4 hyut3 aat3',
    # missing words
    '好正': 'hou2 zeng3', '好精': 'hou2 zeng1', '把聲': 'baa2 seng1',
    '好平': 'hou2 peng4', '咁平': 'gam3 peng4', '最平': 'zeoi3 peng4',
    '平嘢': 'peng4 je5',
    '瞓唔到覺': 'fan3 m4 dou2 gaau3',
    '成個鐘': 'seng4 go3 zung1', '成身': 'seng4 san1', '成間': 'seng4 gaan1',
    '彈琴': 'taan4 kam4', '彈鋼琴': 'taan4 gong3 kam4',
    '彈結他': 'taan4 git3 taa1', '彈吉他': 'taan4 gat1 taa1',
    '彈古箏': 'taan4 gu2 zang1',
    '張相': 'zoeng1 soeng2', '相集': 'soeng2 zaap6',
    '着咗件': 'zoek3 zo2 gin6', '着衫': 'zoek3 saam1',
    '着多件褸': 'zoek3 do1 gin6 lau1', '着多件衫': 'zoek3 do1 gin6 saam1',
    '著住': 'zoek3 zyu6',
    '訂位': 'deng6 wai2', '訂枱': 'deng6 toi2', '冇位': 'mou5 wai2',
    '問下': 'man6 haa5', '問下個月': 'man6 haa6 go3 jyut6',
    '問下個禮拜': 'man6 haa6 go3 lai5 baai3',
    '今晚會': 'gam1 maan5 wui5', '聽晚會': 'ting1 maan5 wui5',
    '琴晚會': 'kam4 maan5 wui5',
    '行車線': 'hang4 ce1 sin3', '而行': 'ji4 hang4',
    '恒生': 'hang4 sang1', '不亦說乎': 'bat1 jik6 jyut6 fu4',
    '中咗': 'zung3 zo2', '集中咗': 'zaap6 zung1 zo2',
    '人話': 'jan4 waa6', '講人話': 'gong2 jan4 waa2',
    '唔講人話': 'm4 gong2 jan4 waa2',
    '發佈會': 'faat3 bou3 wui2', '發布會': 'faat3 bou3 wui2',
    '調高': 'tiu4 gou1', '強調高': 'koeng4 diu6 gou1',
    '數吓': 'sou2 haa5', '數完': 'sou2 jyun4',
    '應聘': 'jing3 ping3', '個名': 'go3 meng2', '頂帽': 'deng2 mou2',
    '上咗': 'soeng5 zo2', '乾隆': 'kin4 lung4', '朝住': 'ciu4 zyu6',
    '種咗': 'zung3 zo2', '絕種咗': 'zyut6 zung2 zo2', '畫咗': 'waak6 zo2',
    '屏住': 'bing2 zyu6', '屏息': 'bing2 sik1', '盛飯': 'sing4 faan6',
    '行長': 'hong4 zoeng2',
    '做邊行': 'zou6 bin1 hong4', '轉咗工': 'zyun3 zo2 gung1',
    '一唱一和': 'jat1 coeng3 jat1 wo6', '小心地滑': 'siu2 sam1 dei6 waat6',
    '成個人': 'seng4 go3 jan4', '成個人生': 'seng4 go3 jan4 sang1',
    '成件事': 'seng4 gin6 si6', '件事': 'gin6 si6', '成頭家': 'seng4 tau4 gaa1',
    '輕輕': 'hing1 hing1', '輕輕地': 'hing1 hing1 dei2', '輕輕哋': 'heng1 heng1 dei2',
    '為配合': 'wai6 pui3 hap6', '為確保': 'wai6 kok3 bou2', '為免': 'wai6 min5',
    # 平啲 'cheaper', with guards for X平 words followed by 啲
    '平啲': 'peng4 di1', '公平啲': 'gung1 ping4 di1', '不公平啲': 'bat1 gung1 ping4 di1',
    '持平啲': 'ci4 ping4 di1', '擺平啲': 'baai2 ping4 di1', '扁平啲': 'bin2 ping4 di1',
    '躺平啲': 'tong2 ping4 di1', '燙平啲': 'tong3 ping4 di1', '鏟平啲': 'caan2 ping4 di1',
    '填平啲': 'tin4 ping4 di1', '水平啲': 'seoi2 ping4 di1', '太平啲': 'taai3 ping4 di1',
    '和平啲': 'wo4 ping4 di1', '開平啲': 'hoi1 ping4 di1', '攤平啲': 'taan1 ping4 di1',
    '整平啲': 'zing2 ping4 di1', '壓平啲': 'aat3 ping4 di1',
    # 1.1.0: 慢慢行 is wrong in rime; the others lose a tie to the longer
    # final word (屋|企住, 都|會話, 生|詞表)
    '慢慢行': 'maan6 maan2 haang4', '屋企住': 'uk1 kei2 zyu6',
    '都會話': 'dou1 wui5 waa6', '生詞表': 'saang1 ci4 biu2',
}


def is_han(c):
    o = ord(c)
    return (0x3400 <= o <= 0x4DBF or 0x4E00 <= o <= 0x9FFF or
            0xF900 <= o <= 0xFAFF or 0x20000 <= o <= 0x323AF or o == 0x3007)


def rime_rows(path):
    """Yield the tab-separated rows of a rime dict.yaml body."""
    body = False
    for line in open(path, encoding='utf8'):
        line = line.rstrip('\n')
        if line == '...':
            body = True
            continue
        if body and line and not line.startswith('#'):
            yield line.split('\t')


def load_lshk():
    readings = collections.defaultdict(list)
    with open(ROOT / 'jyutping-table-master/list.tsv', encoding='utf8') as f:
        next(f)
        for line in f:
            ch, _, jp = line.split('\t')[:3]
            if is_han(ch) and SYL.match(jp) and jp not in readings[ch]:
                readings[ch].append(jp)
    return readings


def load_rime_chars():
    """char -> [(reading, weight)], weight None for the primary reading."""
    chars = collections.defaultdict(list)
    for row in rime_rows(ROOT / 'rime-cantonese/jyut6ping3.chars.dict.yaml'):
        ch, jp = row[0], row[1]
        weight = float(row[2].rstrip('%')) if len(row) > 2 and row[2] else None
        if len(ch) == 1 and is_han(ch) and SYL.match(jp):
            chars[ch].append((jp, weight))
    return chars


def load_variants(freq):
    """Map HK/TW variant forms to the OpenCC standard form rime uses.

    freq counts how often each character occurs in rime's word list; a
    mapping is kept only when rime prefers the standard form (so 參 is not
    folded into the rare 蔘, nor 針 into 鍼)."""
    standard = set()
    targets = collections.defaultdict(set)
    for name in ('HKVariants.txt', 'TWVariants.txt'):
        for line in open(ROOT / 'opencc' / name, encoding='utf8'):
            if line.startswith('#') or not line.strip():
                continue
            key, values = line.rstrip('\n').split('\t')
            standard.add(key)
            for v in values.split():
                if v != key:
                    targets[v].add(key)
    # A form that is itself standard (才, 煙, 核 ...) or ambiguous (么) stays.
    canon = {v: s for v, (s,) in ((v, tuple(ks)) for v, ks in targets.items()
                                  if len(ks) == 1)
             if v not in standard and len(v) == 1 and freq[s] >= freq[v]}
    canon.update(CURATED_VARIANTS)
    return canon


def pick_default(ch, rime, lshk):
    if ch in CURATED_DEFAULTS:
        return CURATED_DEFAULTS[ch]
    order = lshk.get(ch, [])
    rank = lambda r: order.index(r) if r in order else len(order)
    if rime:
        primary = [r for r, w in rime if w is None]
        if not primary:
            top = max(w for _, w in rime)
            primary = [r for r, w in rime if w == top]
        return min(primary, key=rank)      # stable: ties keep rime order
    return order[0]


def main():
    global ROOT
    import argparse
    ap = argparse.ArgumentParser(description='Generate the xjyutping data files.')
    ap.add_argument('--sources', type=pathlib.Path, default=ROOT,
                    help='directory holding the source folders (default: %(default)s)')
    ap.add_argument('--py-data', type=pathlib.Path, default=None,
                    help='data directory of the Python package (default: %s, '
                         'skipped if that package is not there)' % PY_DATA)
    args = ap.parse_args()
    ROOT = args.sources.resolve()
    py_data = args.py_data or (PY_DATA if PY_DATA.parent.is_dir() else None)

    lshk = load_lshk()
    rime = load_rime_chars()
    rows = [(r[0], r[1].split()) for r in
            rime_rows(ROOT / 'rime-cantonese/jyut6ping3.words.dict.yaml')]
    canon = load_variants(collections.Counter(c for w, _ in rows for c in w))

    chars = {}      # char -> (default, other readings, flag as polyphone?)
    for ch in sorted(set(lshk) | set(rime) | set(canon)):
        r = rime.get(ch) or rime.get(canon.get(ch, ''))
        l = lshk.get(ch) or lshk.get(canon.get(ch, ''), [])
        if not r and not l:
            continue
        default = pick_default(ch, r, {ch: l})
        if r:   # rime weights: none = primary, 5% common, 3% uncommon, 0% rare
            weight = {jp: 100 if w is None else w for jp, w in r}
        else:
            weight = {jp: 100 for jp in l}
        others = sorted((jp for jp, w in weight.items() if w >= 3 and jp != default),
                        key=lambda jp: l.index(jp) if jp in l else len(l))
        # A changed tone (人 jan4 -> jan2, 姨 ji4 -> ji1) belongs to words,
        # so it alone does not make a character ambiguous.
        changed = lambda jp: (jp[:-1] == default[:-1] and jp[-1] in '12'
                              and default[-1] not in '12')
        flag = any(weight[jp] >= 5 and not (changed(jp) and weight[jp] < weight.get(default, 100))
                   for jp in others)
        chars[ch] = (default, others, flag)

    # --- words -----------------------------------------------------------
    entries = collections.defaultdict(list)
    usage = collections.defaultdict(collections.Counter)
    for word, syls in rows:
        if (len(word) < 2 or len(syls) != len(word)
                or not all(c in chars for c in word)
                or not all(SYL.match(s) for s in syls)):
            continue
        if syls not in entries[word]:
            entries[word].append(syls)
        for c, s in zip(word, syls):
            usage[c][s] += 1

    def score(word, syls):          # how usual each syllable is for its char
        return sum(math.log(usage[c][s] + 1) for c, s in zip(word, syls))

    words = {w: max(rs, key=lambda s: score(w, s)) for w, rs in entries.items()}
    for w, jp in CURATED_WORDS.items():
        assert len(jp.split()) == len(w) and all(SYL.match(x) for x in jp.split()), w
        words[w] = jp.split()
    # The adverb suffix 地 (慢慢地, 麻麻地) is often written 哋.
    for w, syls in list(words.items()):
        if w.endswith('地') and syls[-1] == 'dei2':
            words.setdefault(w[:-1] + '哋', syls)
    dupes = sum(1 for rs in entries.values() if len(rs) > 1)

    # Aliases spelt with canonical characters, so 因為 finds rime's 因爲.
    aliases, clashes = {}, 0
    for w, syls in words.items():
        cw = ''.join(canon.get(c, c) for c in w)
        if cw == w or cw in words:
            continue
        if cw in aliases and aliases[cw] != syls:
            clashes += 1
            continue
        aliases[cw] = syls
    allwords = {**words, **aliases}

    longest = collections.defaultdict(int)  # final char -> longest word
    for w in allwords:
        longest[w[-1]] = max(longest[w[-1]], len(w))

    # --- output ----------------------------------------------------------
    header = [
        '%% Generated by tools/build-data.py -- do not edit.',
        '%% Sources: LSHK Jyutping table (CC BY 4.0),',
        '%%          rime-cantonese jyut6ping3 dictionaries (CC BY 4.0),',
        '%%          OpenCC HK/TW variant tables (Apache-2.0).',
    ]
    with open(REPO / 'xjyutping-chars.def', 'w', encoding='utf8') as f:
        f.write('\n'.join(header) + '\n')
        f.write('\\ProvidesFile{xjyutping-chars.def}[%s xjyutping character data]\n' % VERSION)
        for ch, (default, others, flag) in chars.items():
            if flag:        # polyphone: default, then the other readings
                f.write('\\xjp@M %s%s %s;\n' % (ch, default, ' '.join(others)))
            else:
                f.write('\\xjp@C %s%s;\n' % (ch, default))
        for v, s in sorted(canon.items()):
            if v in chars:
                f.write('\\xjp@V %s%s;\n' % (v, s))
        for ch, jp in CURATED_FINALS.items():
            f.write('\\xjp@F %s%s;\n' % (ch, jp))
    with open(REPO / 'xjyutping-words.def', 'w', encoding='utf8') as f:
        f.write('\n'.join(header) + '\n')
        f.write('\\ProvidesFile{xjyutping-words.def}[%s xjyutping word data]\n' % VERSION)
        for w in sorted(allwords):
            f.write('\\xjp@W %s=%s;\n' % (w, ' '.join(allwords[w])))
        for c in sorted(longest):
            f.write('\\xjp@E %s%d;\n' % (c, longest[c]))

    # The same tables for the Python package (it derives the longest-word
    # bound from words.tsv itself).
    if py_data:
        py_data.mkdir(parents=True, exist_ok=True)

        def tsv(name, rows):
            with open(py_data / name, 'w', encoding='utf8', newline='\n') as f:
                f.writelines('\t'.join(row) + '\n' for row in rows)
        tsv('chars.tsv', ((ch, d, ' '.join(o), '1' if fl else '0')
                          for ch, (d, o, fl) in chars.items()))
        tsv('finals.tsv', CURATED_FINALS.items())
        tsv('variants.tsv', ((v, s) for v, s in sorted(canon.items()) if v in chars))
        tsv('words.tsv', ((w, ' '.join(allwords[w])) for w in sorted(allwords)))
    else:
        print('Python data skipped: %s not found' % PY_DATA.parent, file=sys.stderr)

    print('chars %d (polyphonic %d), variants %d, words %d (+%d aliases, '
          '%d alias clashes, %d words with several readings)' % (
              len(chars), sum(f for _, _, f in chars.values()), len(canon),
              len(words), len(aliases), clashes, dupes), file=sys.stderr)


if __name__ == '__main__':
    main()
