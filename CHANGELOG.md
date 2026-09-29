# Changelog

All notable changes to xjyutping, the LaTeX package, are recorded here. The
format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

The Python port is a separate repository,
[xjyutping-py](https://github.com/Beyond3345/xjyutping-py), with its own
version numbers and its own changelog. Both packages use the data that
`tools/build-data.py` in this repository generates. Up to 1.1.0 the two lived
in one folder with a single changelog; its history is kept here, in Part II.

The version is written in four places: `\ProvidesExplPackage` in
`xjyutping.sty`, `VERSION` in `tools/build-data.py` (it goes into the
`\ProvidesFile` lines of the `.def` files), `README.md`, and `\author` in
`xjyutping-doc.tex`. A release bumps all four and gets an entry in Part I.

This file has two parts:

- **Part I, Releases:** what changed in each version.
- **Part II, Handover notes and development history:** how the package was
  built and how it works, every bug found during development with its cause
  and fix, the known open issues, and how to test. It is written for the
  next maintainer, human or agent.

---

# Part I: Releases

## [Unreleased]

Nothing yet. Add entries here under `### Added`, `### Changed`, `### Fixed`
and so on.

## [1.2.0] - 2026-09-28

### Added

- **LuaLaTeX support**, through LuaTeX-ja (loaded if no Chinese support is
  loaded; the `ctex` package and classes work too). A new file
  `xjyutping.lua` must be installed next to `xjyutping.sty`.
  - The preprocessor, the readings and every option are shared with XeLaTeX.
    Each mark builds its ruby in TeX; a Lua callback that runs after
    LuaTeX-ja wraps each tagged character into its cell and leaves out the
    right pad before punctuation that hugs it.
  - The readings are identical to XeLaTeX's and the layout nearly so. Text
    that comes from macros is annotated without context, as under XeLaTeX.
  - Under LuaLaTeX a paragraph has no length limit.
- **The `linebreak` option**, for verse and lyrics:
  `\begin{jyutpingscope}[linebreak]` or `\xjyutpingsetup{linebreak}`. Each
  line end of the source becomes a line break (`\newline`) and each blank
  line a paragraph break, which follows the document's paragraph settings
  (indented, or with `parskip` spaced and not indented). Line ends at the
  start and end of the scope, after `\\`, and before `\begin`, `\end` or a
  new paragraph add nothing, and a line end also ends a run of characters.
  It works in the environment only, not in `\xjyutping*` (Part II,
  section 7.6).
- **More vocabulary** (see Part II, section 7.4):
  - 2,291 words from CC-Canto and the Cantonese readings of CC-CEDICT, as
    distributed with Jyut Dictionary (`src/dictionaries/cedict/data`). A word
    is added only where it changes a reading and passes consistency checks
    against rime-cantonese; 480 more were excluded by hand.
  - 640 characters that LSHK and rime-cantonese lack, with readings from the
    book data of 粵音資料集叢 (jyutnet/cantonese-books-data, by 石見田).
- `tools/build-data.py` is now part of this repository, with `--sources`
  and `--py-data` options, and `tools/fetch-sources.sh` fetches every data
  source at the commit the data was built from.
- Tests: `tests/run-tests.sh` runs XeLaTeX and LuaLaTeX, each with and
  without `fancy`; `tests/render.sh` takes the engine as its second
  argument; the test documents load xeCJK or ctex depending on the engine.
  `tests/regression.tex` also covers a scope opened by a user environment, a
  table made by a macro, a box in math, and `linebreak`.
- `LICENSE`: LPPL 1.3c for the code, CC BY-SA 4.0 for the data, with every
  source of the data and its licence.
- `tools/make-ctan-zip.sh` builds the archive for CTAN (Part II,
  section 7.8).
- README and manual: a section on the two engines, and an Acknowledgements
  and attributions section (xpinyin by Qing Lee, Visual Jyutping, the Visual
  Cantonese Fonts, and every data source).
- `.gitignore`.

### Changed

- **Readings.** The new words change readings where they are more exact,
  for example 機長 zoeng2, 營業額 ngaak2, 自由行 hang4, 研討會 wui2, 消防隊
  deoi2, 冠狀病毒 gun1, 智能卡 kaat1. 化合物 is now faa3 hap6 mat6 and 會否
  wui5 fau2 (hand fixes). No reading from rime-cantonese was replaced.
- **Licence of the generated data:** the `.def` files are now distributed
  under CC BY-SA 4.0 instead of carrying CC BY 4.0, because the added word
  lists are CC BY-SA 3.0 (share-alike). The package code stays under LPPL
  1.3c.
- **`\xjyutping{<text>}{<readings>}`**: the readings go to the Chinese
  characters of the text, one each, also inside braces and commands
  (`\xjyutping{\textbf{行}}{hong4}`, `{\color{red}行}`). Latin letters and
  punctuation take none, and the warning about the number of readings counts
  Chinese characters only. (In 1.1.0 every item of the text, a punctuation
  mark, a letter or a command, took a reading of its own, which XeLaTeX then
  dropped; a reading written for such an item now goes to the next Chinese
  character, with a warning. Under LuaLaTeX a reading for a character in
  braces was lost and a Latin letter got a cell: review findings D4 and D5,
  Part II, section 7.3.)
- `jyutpingscope` reads its body itself instead of as a `+b` argument, so
  that `linebreak` can see the line ends. The body ends where a `+b`
  argument ended: at the first `\end` that does not close a `\begin` of the
  body, so a scope can still be opened and closed by a user environment.
- The `.def` files carry `v1.2.0`.
- The history of the project (this file) now lives in this repository.

## [1.1.0] - 2026-09-28

### Added

- **`fancy` option**, as in `\usepackage[fancy]{xjyutping}`, also accepted by
  `\xjyutpingsetup` and in the options of one scope or `\xjyutping*`. It shows
  tones the way [Visual Jyutping](https://github.com/VincentTam/visual-jyutping)
  does:
  - The tone number is replaced by a small drawn pitch stroke: high, rising
    to high, mid, falling to low, rising from low, low, after its symbols
    ˉ ˊ ˗ ˎ ˏ ˍ.
  - The stroke is followed by a smaller tone number, raised for tones 1–2 and
    lowered for tones 3–6.

  The strokes are PDF drawing commands, so they do not depend on the font
  and they take the text colour.
- **Automatic spacing for `fancy`:**
  - Cell widths (`width=auto`) are measured with the marks in place.
  - The ruby strut includes the raised and lowered numbers, so line spacing
    stays even.
  - If the lowered numbers reach below the letters, the ruby is lifted by the
    difference (`\g__xjyutping_lift_dim`), so its gap to the character stays
    the same.
- `tests/fancy-check.tex`, a visual check of the tone marks at several
  sizes, fonts, colours and widths.
- `tests/run-tests.sh` now also compiles the regression document with
  `fancy`, which must give the same readings.

### Changed

- **Repository layout.** The LaTeX package moved into `xjyutping-tex/`,
  keeping its file names: `xjyutping.sty`, `xjyutping-chars.def`,
  `xjyutping-words.def`, `README.md`, `xjyutping-doc.tex/.pdf` and `tests/`.
  Documents and installation are unaffected. `tools/build-data.py` and the
  data sources stayed at the root of the workspace (in 1.2.0 the tool moved
  into this repository).
- **Readings** (`CURATED_WORDS`):
  - 慢慢行 is now maan6 maan2 haang4 (rime had maan6 maan6 hang4).
  - New entries 屋企住, 都會話 and 生詞表, which were split wrongly by the
    longer-final-word tie-break: 屋|企住, 都|會話, 生|詞表 with 生 sang1.
- The `.def` files carry `v1.1.0` in their `\ProvidesFile` lines.
- `tests/run-tests.sh` writes the extracted debug lines to
  `<job>.readings`. It used to write them to `regression.out`, the file name
  hyperref uses for its bookmarks.
- The manual has a new "Fancy tones" section; the README and the manual
  state the version and the versioning scheme.

### Fixed

- **`\pdfbookmark`** (and `\currentpdfbookmark`, `\subpdfbookmark`,
  `\belowpdfbookmark`) inside a scope: the anchor name was walked as text and
  annotated, so the named destination contained marks and links to it were
  silently broken. Both arguments are now passed through untouched. This was
  open issue 17 at 1.0.0.

## [1.0.0] - 2026-09-28

The file itself says `1.0`, which is read as 1.0.0.

### Added

- **First release** of the XeLaTeX package `xjyutping`, which puts Jyutping
  above traditional Chinese characters.
- **Commands:**
  - the `jyutpingscope` environment;
  - `\xjyutping*[opts]{text}` for running text;
  - `\xjyutping[opts]{字}{reading}` for manual readings;
  - `\setjyutping` for character defaults and words;
  - `\disablejyutping` and `\enablejyutping`;
  - `\xjyutpingsetup`.
- **Options:** `ratio`, `vsep`, `hsep`, `width` (auto, natural or a
  length), `font`, `format`, `multiple` and `debug`.
- **Readings from context.** Each run of Chinese characters is segmented
  with about 101 000 words: fewest words first, then fewest single
  characters, and the longer final word on a tie. Formatting commands and
  braces do not split words. Variant shapes are folded together for word
  lookup, and some characters have run-final readings (呢).
- **Even, collision-free layout:** uniform cells, the right half-pad paid
  by whatever follows, line spacing and clearance.
- **Works with** hyperref, nameref, cleveref, natbib/biblatex, footnotes,
  tables, the ctex classes and beamer.
- **Data** from the LSHK Jyutping table and rime-cantonese (CC BY 4.0) and
  OpenCC (Apache-2.0), generated by `tools/build-data.py` with hand-checked
  correction tables.

### Fixed (during development, before the release)

- 10 issues while writing the first version, then about 81 distinct bugs
  and 88 accepted reading findings over three review rounds. Each is listed
  with its symptom, cause, fix and verification in Part II, section 3.

---

# Part II: Handover notes and development history

## 0. Start here

**Where things are.** This repository holds the LaTeX package:

| Path | What it is |
| --- | --- |
| `xjyutping.sty` | The package (expl3). |
| `xjyutping.lua` | The LuaLaTeX backend: builds the cells after LuaTeX-ja (section 7.3). |
| `xjyutping-chars.def`, `xjyutping-words.def` | Generated data; never edit by hand. |
| `tools/build-data.py` | Generates the data of this package and of xjyutping-py from the sources. |
| `tools/fetch-sources.sh` | Fetches the sources at the pinned commits. |
| `tools/make-ctan-zip.sh` | Builds the archive for CTAN (section 7.8). |
| `tests/` | `run-tests.sh` (readings, both engines, with and without `fancy`), `render.sh`, `regression.tex/.expected`, `layout-check.tex`, `fancy-check.tex`. |
| `README.md`, `xjyutping-doc.tex/.pdf` | User documentation. |
| `LICENSE` | LPPL 1.3c for the code, CC BY-SA 4.0 for the data, and the sources of the data. |
| `CHANGELOG.md` | This file. |

The third-party sources are not in the repository. `tools/build-data.py`
looks for them in the directory that contains the repository (the
"workspace"), which in the original set-up looks like this:

```
xjyutping/                  workspace (not a repository)
  xjyutping-tex/            this repository
  xjyutping-py/             the Python package's repository
  jyutping-table-master/    LSHK Jyutping table (CC BY 4.0)
  rime-cantonese/           rime-cantonese dictionaries (CC BY 4.0)
  opencc/                   OpenCC variant tables (Apache-2.0)
  jyut-dict/                Jyut Dictionary, sparse: src/dictionaries, src/jyut-dict
  cantonese-books-data/     粵音資料集叢 book data (no licence stated)
  visual-jyutping-master/   Visual Jyutping (reference for fancy)
  xpinyin/, xpinyin-master/ the LaTeX and Python xpinyin (reference only)
```

`tools/fetch-sources.sh [DIR]` recreates the five data folders there.

**Invariants to keep:**

1. **The two packages give the same readings.** Any change to the data or
   to segmentation must keep `tests/run-tests.sh` here and the parity test of
   xjyutping-py (`test_parity_with_tex_package`) passing.
   - When readings change on purpose, regenerate `tests/regression.expected`
     and xjyutping-py's `tests/parity_expected.txt` from the TeX logs
     (section 5) and check the diff by hand.
2. **Fix readings in the data, not in code.** Edit only the tables at the top
   of `tools/build-data.py`, then run it; it rewrites both packages' data.
   - rime-cantonese is authoritative. Other sources only add what rime lacks.
   - Test a candidate entry with `\setjyutping` in a few contexts first. The
     longer-final-word tie-break means a new word can capture its
     neighbours (section 5.2).
3. **Both engines produce the same readings and nearly the same layout.**
   Layout logic lives twice: in the XeLaTeX cell code of `xjyutping.sty`
   (`\__xjyutping_cell:nnn` and the pad functions) and in `xjyutping.lua`
   (`wrap`). A change to one needs the matching change to the other.
4. **The two passes of the TeX walker must visit the same Chinese
   characters in the same order** (section 2.4).
5. **Respect TeX's capacity limits under XeLaTeX** (section 2.10). Names are
   created at top level or globally, per-character slots are reused (set to
   `\relax`), and text is analysed paragraph by paragraph. Whatever a cell
   adds is paid for every character, so measure main memory after layout
   changes (the `fancy` marks cost 50 words per character; section 6).
6. **Versioning** follows SemVer:
   - MAJOR: an incompatible change, such as removing or renaming a command
     or option, or changing an argument's meaning;
   - MINOR: a backward-compatible feature (`fancy` in 1.1.0, LuaLaTeX and new
     vocabulary in 1.2.0);
   - PATCH: bug fixes and reading corrections.

**How to test:**

```bash
tests/run-tests.sh
```

This needs XeLaTeX with xeCJK, LuaLaTeX with LuaTeX-ja and ctex, and the
font Songti TC. It must print `readings ok` for four jobs: XeLaTeX and
LuaLaTeX, each with and without `fancy`. For a visual check:

```bash
tests/render.sh tests/fancy-check.tex lualatex
```

**Open issues:** section 4 gives the state at 1.0.0 and says which issues
1.1.0 resolved; section 7.7 gives the state after 1.2.0.

The review artefacts cited below (repro `.tex` files, review JSON) lived in
the session's temporary directory and are not part of the repository. This
file, the README, the code comments and the tests hold everything needed.

## Sources and conventions of the history (sections 1–5)

Sections 1–5 cover how the XeLaTeX package, now this repository, was built and reviewed. All of this happened on 2026-09-28 in one Claude Code session. The package file says version `1.0`, which this changelog treats as **1.0.0** under Semantic Versioning. The data files carry `v1.0` in their `\ProvidesFile` lines.

Sources used for this history:
- the session transcript (`~/.claude/projects/-Users-beyond555-Documents-CodingProjects-xjyutping/7ca57d4a-….jsonl`);
- the three review-workflow results (`tasks/review.json`, `review2.json`, `review3.json` in the session's temporary directory);
- the reviewers' repro files (`scratchpad/review-artifacts/`);
- the code as frozen at 1.0.0 (a snapshot of `xjyutping.sty` and the `.def` files);
- `tools/build-data.py`.

The review artefacts live under `/private/tmp/…` and will not survive a reboot. Everything needed to maintain the package is in this document, the README, the code comments and `tests/`.

Clock times are local (UTC+8, which is what the file timestamps show). They are given only to order events.

Bug identifiers used below:
- **I-n**: bugs found while writing the first version.
- **R1-nn, R2-nn, R3-nn**: findings of review rounds 1–3, numbered in the order of the review JSON files.
- **Mx-n**: regressions or bugs the main agent hit while applying the fixes for round x.

---

## 1. Origin

### 1.1 The request (09:32)

The user described themselves as a Cantonese learner and a LaTeX user. The project folder held two things:
- `xpinyin/`: the CTeX-kit package that puts Hanyu Pinyin over simplified Chinese (`xpinyin.dtx`, README, PDF);
- `jyutping-table-master/`: a character-to-Jyutping list.

The user asked for a similar package that puts **Jyutping above Chinese characters**, with these requirements:
- readings should change with context "if possible";
- the Jyutping must be uniformly and cleanly spaced and must not collide with other text;
- users can give custom readings for specific characters, because pronunciation shifts with context;
- only traditional characters need to be supported.

The user named the source of the list as `https://github.com/lshk-org/bilingual-glossary.git`. The folder actually contains `jyutping-table-master`, the LSHK *Cantonese Pronunciation List of Characters for Computers* (電腦用漢字粵語拼音表, `list.tsv`, CC BY 4.0, 29 144 distinct characters in `list.tsv`). The session treated it as that table throughout. The repository name in the request does not match the folder's contents, and nothing in the folder mentions a bilingual glossary. The `-master` suffix is how GitHub names a branch download, so the folder is probably a download of `lshk-org/jyutping-table` (unverified). This history records the discrepancy and does not resolve it.

### 1.2 Clarifying questions and answers

1. **May rime-cantonese word and character lists be downloaded?** (CC BY 4.0: `jyut6ping3.words.dict.yaml` 2.6 MB, `jyut6ping3.chars.dict.yaml` 0.35 MB.) Answer: *"Yes, use rime-cantonese (Recommended)"*.
2. **Engine?** Answer: *XeLaTeX (xeCJK / ctex)*. LuaLaTeX was not requested and is not supported.
3. **May OpenCC's HK/TW variant tables be downloaded?** These map spellings such as 為/爲, 裡/裏 and 説/說 onto rime's standard forms. Answer: *"Yes, download them. You can download a bigger variant table or rime-cantonese dictionary. Focus on quality and don't worry too much about space right now."*

Downloaded on 2026-09-28:
- **`rime-cantonese/`**:
  - `jyut6ping3.chars.dict.yaml` (header version "2026.08.10");
  - `jyut6ping3.words.dict.yaml` (about 103 000 lines);
  - `LICENSE-CC-BY`;
  - `jyut6ping3.phrase.dict.yaml` was also fetched, found to contain words without readings, and deleted.
- **`opencc/`**:
  - `HKVariants.txt` and `TWVariants.txt`;
  - `HKVariantsRevPhrases.txt` and `TWVariantsRevPhrases.txt`, downloaded but not used by the builder;
  - `LICENSE` (Apache-2.0).

Environment found on the machine:
- TeX Live 2026, xeCJK, ctex;
- the `Songti TC` font (used by every test);
- Ghostscript at `/opt/homebrew/bin/gs` (the only PDF renderer available);
- python3 3.9.6, without PIL.

### 1.3 Design goals derived from the request

- **G1, context readings:** segment runs of Chinese text into words from a large word list (rime-cantonese, about 101 000 words), and let words override per-character defaults.
- **G2, sensible defaults:** choose a per-character default from rime's weights, falling back to LSHK order. Flag characters with several common readings, so they can be highlighted while proofreading (`multiple=`).
- **G3, even spacing with no collisions:** give every character a cell of uniform width, as wide as the widest Jyutping in the block. Keep the ruby clear of neighbouring rubies, of the line above and of the margins. Leave xeCJK in charge of punctuation, line breaking and CJK/Latin spacing (the xpinyin approach of hooking `\CJKsymbol`).
- **G4, user control:** `\xjyutping{字}{reading}` for one spot, `\setjyutping` for words and defaults, and a debug log.
- **G5, variant spellings:** HK and TW input spellings must find rime's words.
- **G6, robustness in real documents:** sections, TOC, hyperref, footnotes, tables, beamer and ctex classes must work, and the TeX capacity limits must hold at book length.

---

## 2. Architecture (for maintainers)

### 2.1 Files at 1.0.0

| File | Role |
| --- | --- |
| `xjyutping-tex/xjyutping.sty` | The package, expl3, about 1850 lines, LPPL 1.3c. `\ProvidesExplPackage{xjyutping}{2026-09-28}{1.0}`. |
| `xjyutping-tex/xjyutping-chars.def` | Generated, about 516 KB. One line per character: `\xjp@C <char><default>;` or `\xjp@M <char><default> <other readings>;` (flagged polyphone). Also `\xjp@V <variant><canonical>;` and `\xjp@F <char><run-final reading>;`. |
| `xjyutping-tex/xjyutping-words.def` | Generated, about 3.4 MB. `\xjp@W <word>=<syllables>;` and `\xjp@E <char><length of the longest word ending in char>;`. |
| `tools/build-data.py` | Generates both `.def` files from `jyutping-table-master/`, `rime-cantonese/` and `opencc/`. |
| `xjyutping-tex/README.md` | User spec. The review agents treated it as the specification: documented behaviour counts as intended. |
| `xjyutping-tex/xjyutping-doc.tex` / `.pdf` | 5-page manual. |
| `xjyutping-tex/tests/` | Tests: `run-tests.sh`, `regression.tex`, `regression.expected`, `render.sh`, `layout-check.tex` (see section 5). |

Data statistics at 1.0.0, as printed by the builder:
- 29 449 characters, 4 349 of them flagged polyphonic;
- 76 variant mappings;
- 101 275 words plus 68 canonical-spelling aliases, with 0 alias clashes. The 101 275 are 101 088 usable rime-cantonese words, 105 curated words that are not among those rime words (the other 30 `CURATED_WORDS` entries replace the reading of an existing rime word) and 82 地→哋 twins (recomputed for this write-up; the builder prints only the total);
- 1 229 rime words that had several readings.

### 2.2 Loading, and why the data is loaded at top level

- The engine is checked first (`\sys_if_engine_xetex:F` → `\msg_critical` `xetex-only`). xeCJK is loaded if it is missing.
- **Keys** (`\keys_define:nn {xjyutping}`; package options via `\ProcessKeyOptions`; later changes via `\xjyutpingsetup`):

  | Key | Default |
  | --- | --- |
  | `ratio` | `0.45` |
  | `vsep` | `1.05em` |
  | `hsep` | `0.15em plus 0.4em` (was `0.15em plus 0.15em` before R1-26) |
  | `width` | `auto`; also `natural` or a length |
  | `font` | `\normalfont` |
  | `format` | empty |
  | `multiple` | empty |
  | `debug` | `false` |

- **Data.** Each line of the `.def` files is a call to one of six loader macros defined in the `.sty`:

  | Loader | Defines |
  | --- | --- |
  | `\xjp@C` | `\xjp@c@<char>`, the default reading |
  | `\xjp@M` | `\xjp@c@<char>`, plus `\xjp@m@<char>` holding the alternatives |
  | `\xjp@F` | `\xjp@f@<char>`, the run-final reading |
  | `\xjp@V` | `\xjp@v@<variant>`, the canonical spelling |
  | `\xjp@W` | `\xjp@w@<word>` |
  | `\xjp@E` | `\xjp@e@<char>`, the longest word ending in that character |

  User settings live in `\xjp@u@<char>` and in `\xjp@w@<word>` plus `\xjp@uw@<word>`.
- The files are read with `\file_input:n`, with the space catcode set to "space" and `\endlinechar=-1`, **at the top level, not inside a group**. Inside a group every newly created control-sequence name costs a save-stack entry. Loading in a group used 140 558 of the 200 000 save-stack slots before any text was processed (M1-2). The loader names also changed then, from `\C \M \V \W \E` to the internal `\xjp@…` forms, so they no longer clash with user macros.
- Loading costs about 2.47–2.48 million of TeX Live's default 5 000 000 words of main memory. That is the base on which all the capacity figures below sit.

### 2.3 Public interface

| Command | Implementation |
| --- | --- |
| `jyutpingscope` | `\NewDocumentEnvironment{jyutpingscope}{O{} +b}`. It sets the keys, calls `\__xjyutping_baselineskip:` and `\__xjyutping_prepare:n{body}`; at the end, `\__xjyutping_typeset:` then `\par`. |
| `\xjyutping*[opts]{text}` | `\__xjyutping_prepare:n` then `\__xjyutping_typeset:`, inside a group. |
| `\xjyutping[opts]{字}{reading}` | `\__xjyutping_manual:nn`. Each character gets `\xjyutping@mark{u<syllable>}`, with a `count-mismatch` warning when the counts differ. `\group_insert_after:N \__xjyutping_clear_mark:` drops a reading left pending on a non-Chinese token (R2-09). |
| `\setjyutping{text}{readings}` | `\__xjyutping_set:nnn {…}{…}{g}`. One character goes into `\xjp@u@<char>`. A word is stored under its raw and its canonical spelling (`\__xjyutping_set_word:nn`), and `\xjp@e@` is updated. |
| `\disablejyutping`, `\enablejyutping` | `\__xjyutping_disable:` and `\__xjyutping_enable:`. `\enablejyutping` does nothing in plain mode. |

`\__xjyutping_prepare:n` runs both walker passes inside a group, so that a `\setjyutping` met while reading only affects segmentation of the text after it; the real, global setting happens at typesetting time, at its own position. It exports the marked text as `\g__xjyutping_result_tl` and then fixes the cell width in `\l__xjyutping_uniform_tl`:
- `auto`: the widest ruby measured in the block, `\g__xjyutping_max_dim`, stored as a multiple of `\f@size`. If nothing was measured (text that only comes from macros), the fallback measures `gwong2`.
- `natural`: empty.
- a length: used as given.

### 2.4 Reading a block: the two-pass walker

`\__xjyutping_preprocess:n`:
1. increments `\g__xjyutping_block_int`;
2. splits the body into paragraphs with `\__xjyutping_split_pars:Nn`;
3. runs `\__xjyutping_pass:n{1}` and `\__xjyutping_pass:n{2}`.

**Paragraph splitting.** `\__xjyutping_split_pars:Nn` replaces top-level `\par` with a delimiter and wraps each paragraph as `{…}`. It uses `\__xjyutping_split:w` with a leading `\prg_do_nothing:`, so a paragraph that is a single brace group keeps its braces; `\seq_set_split` strips them (M1-4). Each paragraph is analysed separately (`\__xjyutping_paragraph:n` → `\__xjyutping_walk:n` → `\tl_analysis_map_inline:nn`), because the analysis needs far more memory than the text itself (section 2.10). The body is kept in `\l__xjyutping_body_tl` and walked through a variable, never inside a mapping function's definition: `#` tokens in the body would otherwise break the definition (M1-1).

**The two passes see the same tokens and must visit the same Chinese characters in the same order.** Every later reading shifts if they disagree; this invariant was the main target of the round-2 walker review.
- **Pass 1** collects runs of Chinese characters, segments each run (section 2.5) and stores the chosen mark for block character *n* in the global `\xjp@s@<n>`.
- **Pass 2** copies the text into per-depth global `\tl_build` buffers (`l__xjyutping_buf_<depth>_tl`, via `\__xjyutping_put:n`). It puts `\xjp@s@<n>`'s mark in front of character *n* and then sets the slot to `\relax`.

**Token dispatch.** `\__xjyutping_token:nnn` → `\__xjyutping_token:nn`:

| Token | Handling |
| --- | --- |
| begin-group / end-group | `\__xjyutping_begin_group:` / `\__xjyutping_end_group:` |
| letters and others | `\__xjyutping_char:n`: a character that has `\xjp@c@<char>` goes to `\__xjyutping_han:`; anything else goes to `\__xjyutping_nonhan:n` |
| control sequences | `\__xjyutping_cs:` |
| catcode 4 (`&`) | `\__xjyutping_tab:` |
| spaces | in pass 2, a space between two Chinese characters is dropped, as xeCJK does. `\__xjyutping_punct_space:n` also drops a space before full-width punctuation (R2-31). |

**Runs and contexts.** A run lives in context `\l__xjyutping_ctx_int`:
- `xjp@len@<ctx>` is its length;
- `xjp@r@<ctx>@<i>` holds the character;
- `xjp@n@<ctx>@<i>` holds its index in the block.

A new context opens for an argument read as separate text (a brace group after a class `a` or `b` command) and for an optional `[…]` after such a command (`\__xjyutping_opt_begin:n`). The enclosing run is not flushed, so text around a `\footnote` carries on. `\__xjyutping_flush:` segments the current run. `\__xjyutping_flush_all:` segments every open run, and is used before a `\setjyutping` (R2-07) and at the end of a pass.

**Command table.** `\g__xjyutping_cmd_prop` is filled with `\__xjyutping_declare:nnnn {commands}{args}{action}{class}`. Unknown commands default to `{0}{}{b}`.

Classes:

| Class | Meaning | Examples |
| --- | --- | --- |
| `t` (transparent) | the run continues | `\textbf`, `\emph`, `\color`, `\textcolor`, size and font switches, `\underline`, the ulem commands, `\label`, `\index`, `\bgroup` (push), `\begingroup` (push), `\egroup` (pop), `\endgroup` (pop), `\alert`, `\structure`, the ctex font switches (`\songti`, `\heiti`, `\kaishu`, `\fangsong`, `\lishu`, `\youyuan`), `\zihao` (1 argument), `\fontsize` (2 arguments), `\footnotemark` (-1) and the xeCJKfntef commands (-1) |
| `a` (aside) | the run continues around the command; its braced arguments are runs of their own | `\footnote`, `\footnotetext`, `\marginpar`, `\setjyutping` |
| `b` (break) | the run ends; braced arguments after it are separate runs | references and citations (arguments copied untouched), `\url`/`\href` (action `url`), `\hyperref` (-1), `\begin` (push), `\end` (pop), `\input` (action `input`), `\xjyutping` (action `manual`), `\xjyutping@mark` (action `mark`), `\disablejyutping` (off), `\enablejyutping` (on) |
| `z` | the run ends, and a following brace group is ordinary text | `\par`, `\item`, `\\` (action `row`), `\tabularnewline`, `\cr`, `\crcr`, `\hline` |

The `args` column:
- *n* > 0: the number of mandatory arguments copied untouched by the skip machine (`\__xjyutping_skip_token:nn`). Optional `[…]`, beamer `<…>` (only when beamer is loaded), `*` and `-` are copied as well.
- `-1`: optional arguments only.
- A single unbraced token counts as an argument (`\__xjyutping_skip_other:nn`, R1-44).
- For `url`, a catcode-6 `#` becomes a catcode-12 `#` (R1-06).
- `\__xjyutping_arg_done:` dispatches the actions when the last argument is complete: `set`, `manual` (measure the syllables), `mark`, `input`, and `push` (detect alignment environments).

**Other walker state:**
- **Owner.** `\l__xjyutping_owner_tl` is the class of the command whose arguments may follow. It is reset to `n` once the arguments are done (R2-21).
- **Brace stack.** `\l__xjyutping_stack_seq` holds `{active}{class}{owner}` per brace group.
- **Semantic stack.** `\l__xjyutping_sem_seq` holds `{active}{is-alignment}` for `\begin`, `\bgroup` and `\begingroup`, and restores `\l__xjyutping_active_bool` (the walker's view of `\disablejyutping`) at `\end`, `\egroup` and `\endgroup` (R1-36). The state goes back to its enclosing value at `&` (`\__xjyutping_tab:`, R2-25), and at `\\`, `\tabularnewline`, `\cr` and `\crcr` only inside environments listed in `\c__xjyutping_align_clist` (`\__xjyutping_row:`, `\__xjyutping_align_env:n`, R3-04/R3-17).
- **Optional-argument stack.** `\l__xjyutping_opt_seq` entries are `{depth}{owner}{closing char}`. `]` is tested before the owner. Optional arguments still open are closed at group end and at paragraph end (`\__xjyutping_opt_close:n`, R3-03).
- **Beamer overlays.** When beamer is loaded, a `<…>` right after a command is copied untouched (`\l__xjyutping_ovl_int`, `\g__xjyutping_beamer_bool`, R3-18).
- **Premarked text.** A control sequence whose name starts with `xjp@R@`, a mark left by an outer pass (nested scope, `\xjyutping*` inside a scope), is copied with the character that follows it (`\__xjyutping_premarked:`, `\l__xjyutping_raw_bool`). Outer word readings therefore survive (R1-01/R1-23/R1-37).
- **`\input{file}` inside a block** (`\__xjyutping_input:n`). The file is read and walked paragraph by paragraph (`\__xjyutping_walk_file:nn`); its first paragraph continues the current one. Before that, `\__xjyutping_input_safe:nTF` reads the file line by line as a string (`\ior_str_map_inline:Nn`), strips `%` comments (`\c__xjyutping_comment_regex`) and matches `\c__xjyutping_unsafe_regex`. That regex covers `\endinput`, `\verb`, `\Verb`, `\lstinline`, `\mintinline`, `\DefineShortVerb`, `\MakeShortVerb`, `\lstMakeShortInline`, `\obeylines`, `\obeyspaces`, `\makeatletter`, `\makeatother`, `\catcode`, `\ExplSyntaxOn`, and `\begin{…}` with a name containing erbatim, alltt, listing, minted or comment. A match makes the file fall back to a real `\input`, with no word context (R2-02, R2-03, R3-05, R3-08).
- **No-pad marker.** Pass 1 records the last Chinese character (`\l__xjyutping_lasthan_int`) and whether only invisible material followed it (`\l__xjyutping_gap_bool`: `t`-class commands, groups). If the next text token is full-width closing punctuation other than a closing bracket, `\__xjyutping_plain:n` sets `\xjp@np@<n>`, and pass 2 emits `\__xjyutping_nopad:` right after that character (R3-12/R3-21).

### 2.5 Segmentation: dynamic programming and its costs

`\__xjyutping_flush:` segments positions 1…*len* of the current run:
- `cost[i] = min(cost[i-1] + 100001, cost[i-k] + 100000)` over every word of length *k*. A segment costs 100 000 and each single character 1 more. The result is the fewest segments first, then the fewest single characters.
- *k* runs from 2 to `min(i, \__xjyutping_longest:n{i})`, the `\xjp@e@` bound for the character at *i*.
- A word test (`\__xjyutping_if_word:nnT`) tries the raw spelling first, then the canonical one (`\__xjyutping_can:n` via `\xjp@v@`).
- The comparison is `<= best` with *k* ascending, so **on a tie the longer final word wins** (a backward-maximum-matching bias). The round-1 polyphone audit pointed at this tie-break for errors such as 呢|張床. It was deliberately not flipped globally; guard words and run-final readings are used instead.
- The back pointers `xjp@back@<i>` are collected linearly into `xjp@seg@<k>` and emitted in order (R2-24). The emission uses `\use:e`, because one-level expansion passed the macro name (M2-1).
- `\__xjyutping_emit:nn` handles a single character through `\__xjyutping_lookup:nn`, using the `f` (final) variant when it is the last character of the run (`\xjp@f@`, for example 呢 → ne1 in 你呢？). A word takes `\xjp@w@` (raw or canonical); its type is `u` if `\xjp@uw@<word>` exists and `w` otherwise.
- `\__xjyutping_result:nnn` stores the mark, measures the reading for `width=auto` (`\__xjyutping_measure:n`, whose seen-cache is `xjp@seen@<reading as string>` holding the block number: R1-39, R1-40) and appends to the debug log line.
- The run's `xjp@r@`/`xjp@n@` slots are set to `\relax` afterwards (section 2.10).

Debug output (`debug=true`) writes one line per run: `xjyutping> 銀ngan4:w行hong4:w |去heoi3:s |重cung5:m(zung6 cung4) |`. Types:
- `w`: from the word list;
- `u`: from the user;
- `m`: a guessed polyphone, alternatives in brackets;
- `s`: a character with a single reading.

Characters typeset without a mark are logged as `xjyutping> [no context] …`, and only if they have a reading (R2-11).

### 2.6 Marks

- For each (type, reading) pair, pass 1 creates one macro on demand: `\xjp@R@<type><reading>` expands to `\xjyutping@mark{<type><reading>}` (`\__xjyutping_combo:nn`, reading passed through `\tl_to_str:n`). Pass 2 puts that single token before each character. This is the memory-saving replacement for the first version's `\xjyutping@mark{<char>}{<reading>}{<type>}`, which was about 15 tokens per character (R1-08). A consequence: the mark no longer names its character (R2-09).
- `\xjyutping@mark #1` is robust. It does nothing unless annotation is enabled (R1-13). When enabled, it leaves vertical mode first, so paragraph-start code (run-in headings, the output routine) runs before the pending mark exists (R2-19). It then stores `\g__xjyutping_mark_tl`, which the next `\CJKsymbol` consumes.
- Written to the `.toc` through `\protected@write`, a combo mark expands to the robust `\xjyutping@mark{…}`, which is inert outside a scope.
- `\xjyutping@mark` takes one argument and is listed in `\l_text_case_exclude_arg_tl`, so `\MakeUppercase` does not touch the reading (R1-24).

### 2.7 Typesetting a cell

`\__xjyutping_enable:` saves and replaces these xeCJK hooks; `\__xjyutping_disable:` restores them:

| xeCJK hook | Replacement |
| --- | --- |
| `\CJKsymbol` | `\__xjyutping_CJKsymbol:n` |
| `\CJKglue` | `\__xjyutping_CJKglue:` |
| `\CJKecglue` | `\__xjyutping_CJKecglue:` |
| `\xeCJK_CJK_and_Boundary:w` | `\__xjyutping_boundary:w` |
| `\xeCJK_CJK_and_FullRight:N` | `\__xjyutping_fullright:N` |
| `\CJKpunctsymbol` | `\__xjyutping_punct:n` |

`\__xjyutping_CJKsymbol:n` takes the reading from the pending mark, or else from `\__xjyutping_lookup:nn` (a "no context" character), and then calls `\__xjyutping_cell:nnn {char}{reading}{type}`:
1. If a colour change sits between two cells, add the hsep stretch glue that xeCJK could not add (R3-10).
2. Measure the character (`\makexeCJKinactive` plus the saved `\CJKsymbol`) and build the ruby (`\__xjyutping_ruby:nn`):
   - the font comes from `\__xjyutping_select_font:`, which caches the font and the whole NFSS state (encoding, family, series, shape, size; R1-19/R1-38) under `xjp@font@<ratio>/<size>/<font>`, and makes `\xeCJK@family` a no-op there (R1-33);
   - a strut gives every ruby the same height and depth;
   - `format` is applied, and `multiple` too for type `m`.
3. Compute the pad: (max(uniform, char width, ruby width) + natural width of hsep − char width) / 2.
4. Emit `\hbox{}`, then `\kern pad`. The empty box keeps the kern at a line start.
5. Emit `\hbox_overlap_right:n{ \__xjyutping_clearance: \box_move_up:nn{vsep}{ruby centred over the character width} }`. The ruby has zero width.
6. Store the same pad as the pending right pad `\g__xjyutping_pad_dim`, and set `\g__xjyutping_cell_bool`.
7. Typeset the character last, with the saved `\CJKsymbol`, where xeCJK's class machinery expects it (I-3).

**Paying the right pad.** The right half of the cell is paid by whatever comes next; `\__xjyutping_pad:` does the paying:
- **Horizontal mode only** (R2-04). If xeCJK's CJK marker node is the last node, the node is removed, the pad kern added, and the node re-made, so xeCJK still inserts `\CJKglue`/`\CJKecglue` after it (R2-12/13/26). After a whatsit (a colour pop) the node is re-made too (R3-10). The pad is always zeroed.
- **Next character.** `\__xjyutping_CJKglue:` pays the pad. Between two cells it then adds only the stretch part of hsep, because the natural part is already inside the cells; that is why a line break never leaves a stray glue at a line start (R1-12/R1-27). Before the first cell it adds xeCJK's own glue.
- **Latin text.** `\__xjyutping_CJKecglue:` pays the pad, then adds xeCJK's glue.
- **Punctuation.** `\__xjyutping_punct:n` zeroes the pad, so punctuation hugs its character (R1-46). `\__xjyutping_fullright:N` → `\__xjyutping_closing:n`:
  - closing brackets and quotes (」』）】》〉〕］｝”’〗〙〟｠) pay the pad, so bracket pairs stay symmetric (R1-29, R2-16);
  - other full-width punctuation drops it;
  - for the long marks —…‥⸺, `\__xjyutping_long_break:` redefines `\xeCJK_allow_break:` once as `\kern pad \penalty0 \kern -pad`. At a break the pad stays at the line end; mid-line the two kerns cancel (R3-11).
- **Anything else** (a command, a box end, a group end): `\__xjyutping_boundary:w` peeks at the next token.
  - **group end** (`}`, `\group_end:`, `\aftergroup`): defer with `\group_insert_after:N \__xjyutping_defer:`. `\__xjyutping_if_defer:` allows deferral only past plain groups (`\currentgrouptype` 1 or 14) and only when `\l__xjyutping_nodefer_bool` is false; TikZ node text sets that flag. Otherwise the pad is paid inside the group (R3-01).
    - After the group, `\__xjyutping_defer_test_aux:` defers again if another group end or `\check@icr` follows (R3-09), and looks past `\maybe@ic` (`\__xjyutping_defer_ic:w`, R2-28).
    - Otherwise `\__xjyutping_decide:` picks: full-width closing punctuation goes to `\__xjyutping_closing:n`; anything else pays.
  - **`\relax`-like token**: if it is `\__xjyutping_nopad:`, the pad is dropped; otherwise it is paid.
  - **otherwise**: pay, and set `\g__xjyutping_paid_bool`.
- **New paragraph.** A `para/begin` hook zeroes the pad (R1-11/R1-28).

### 2.8 Line spacing and clearance

- `\__xjyutping_baselineskip:` runs only in the environment. It computes `\l__xjyutping_bls_fp = (vsep + ruby height + 0.6em) / \f@size`, sets `\l__xjyutping_scope_bool`, raises `\baselineskip` and sets `\emergencystretch` to at least 2em (R1-26).
- `\__xjyutping_raise_baselineskip:` only ever raises `\baselineskip`. It also rebuilds `\strutbox` (height = baselineskip − 0.25em, depth 0.25em), so tabular rows follow the scope's pitch (R3-16).
- It is re-applied in two hooks:
  - `\AddToHook{selectfont}`: inside a scope it runs `\size@update` first, because LaTeX runs that after the hook and would otherwise undo the raise (R2-05/R2-27). While annotation is on, the hook also reinstalls the package's `\CJKglue`/`\CJKecglue`, which ctex replaces on every size change (R1-03). `\DeclareHookRule{selectfont}{xjyutping}{after}{ctex}` orders it after ctex.
  - `\AddToHook{para/end}`: for `minipage`, `\parbox` and `p` columns, which reset `\baselineskip` without a font change (R2-32).
- `\__xjyutping_clearance:` is an invisible rule inside every ruby of height vsep + ruby height + a margin:
  - 0.05em inside a scope when the raised `\baselineskip` is in force, so framed and coloured boxes do not reach the line above (R2-29);
  - 0.35em otherwise: outside scopes, in alignments where `\baselineskip` is 0 (R3-24), and in minipage, `\parbox` and `p` cells, whose paragraphs are built while `\baselineskip` is still the reset value (it is raised only at `para/end`; see section 4, item 13).
- `\lineskiplimit` is left at LaTeX's 0pt. From round 1 to round 2 it was -0.3em; that was removed together with the 0.05em clearance.

### 2.9 Plain mode, output routine, beamer, cross-references

- **Output routine.** `\AddToHook{build/page/reset}` disables annotation, clears the scope flag and sets `\l__xjyutping_plain_bool`. In plain mode `\xjyutping` prints only its text and `\enablejyutping` does nothing. Running heads and feet are therefore plain even when the page is shipped out from inside a scope, or when a heading contains `\xjyutping` (R1-02, R1-41, R2 status for R1-21/R1-42).
- **beamer.** When beamer is loaded, `\AddToHook{cmd/beamer@typesetheadorfoot/before}` does the same, because beamer builds and measures the headline and footline outside the output routine (R3-23).
- **TikZ.** `every text node part/.append code` sets `\l__xjyutping_nodefer_bool` (R3-01).
- **nameref.** At begin document, `\label@hook` is prefixed with `\__xjyutping_unmark:N \@currentlabelname`. It replaces every `\xjp@R@…` token with its one-level expansion `\xjyutping@mark{…}` (l3regex: `\c__xjyutping_mark_regex`, `\regex_extract_all`, `\u{…}` replacement). Without this, nameref's sanitised title would be written to the `.aux` as `\xjp@R@wngan4`, and read back as `\xjp@R@wngan` followed by `4` (R2-01, R3-02).
- **PDF strings.** `\__xjyutping_pdfstring:` fills `\pdfstringdefDisableCommands`:
  - `\xjyutping` becomes `\xjyutping@pdf`, which returns only the text;
  - `\xjyutping@mark` becomes `\use_none:n`;
  - `\setjyutping` becomes `\use_none:nn`;
  - `\disablejyutping` and `\enablejyutping` become nothing.

  It runs at once if hyperref is already loaded (beamer), and otherwise via `\AddToHook{package/hyperref/after}` (R1-05, R1-21, R3-22).

### 2.10 TeX capacity constraints and the design choices they forced

All figures are for TeX Live defaults: `main_memory` 5 000 000 words, save size 200 000, pool size 5 432 815.

- **Main memory.** The data costs about 2.48M words. A 53 060-character single scope measured, per stage: pass 1 up to 3.88M, both passes 4.80M, before any typesetting. Responses:
  - one-token combo marks in place of three-argument marks;
  - analysing one paragraph at a time;
  - freeing per-run data after each run.

  The same scope then needs about 3.3M words.
- **Save stack.** Creating a control-sequence name inside a group (`\csname` of an undefined name) is a local assignment and costs a save-stack slot. Responses:
  - the data is loaded at top level;
  - the per-character slots `xjp@r@`, `xjp@n@` and `xjp@s@` and the `\tl_build` buffers are global;
  - used slots are set to `\relax` instead of being undefined, so the name is reused rather than recreated (M1-2).
- **Hash and pool.** The width cache originally created one name per (block, reading) pair, which exhausted the pool after about 246 000 pairs. It now keeps one name per reading, holding the block number (R1-40).
- **Remaining limits** (documented in the README):
  - one paragraph holds about 15 000 characters, since each cell uses about 125 words of node memory;
  - one scope holds "well over 100 000 characters" (the README's wording); measured in the round-2 recheck: 159k compiled, 212k did not;
  - a brace group spanning many paragraphs is analysed in one piece, because the `\par` split does not act inside braces.

### 2.11 `tools/build-data.py`

- **`load_lshk()`** reads `list.tsv`, the valid syllables in LSHK order. **`load_rime_chars()`** reads (reading, weight) pairs: no weight means primary (treated as 100), otherwise 5%, 3% or 0%. **`rime_rows()`** yields the body rows of a rime dict.yaml.
- **Defaults** (`pick_default`), in order:
  1. `CURATED_DEFAULTS`;
  2. rime's primary reading;
  3. rime's top weight, tie broken by LSHK order;
  4. the first LSHK reading.
- **Other readings** are those with rime weight ≥ 3, sorted in LSHK order.
- **Polyphone flag** (`\xjp@M` rather than `\xjp@C`): some other reading has weight ≥ 5 and is not a weaker *changed tone*. A changed tone has the same syllable with tone 1 or 2 while the default's tone is neither, as in 人 jan4 → jan2. Changed tones belong to words and alone do not make a character ambiguous. The first rule flagged 6 083 characters; the refined rule flagged 4 188, and 4 349 after the round-1 tweak "weaker than the default" (see colloquial #25 in section 3.3).
- **Variants** (`load_variants(freq)`):
  - OpenCC HK and TW tables, reversed to variant → standard;
  - only single-target, single-character mappings, where the variant is not itself a standard form;
  - only where rime uses the standard form at least as often as the variant. This filter stopped 參 being folded into 蔘 and 針 into 鍼 (D-2);
  - plus `CURATED_VARIANTS` (恒 → 恆).
- **Words.** From rime words: at least 2 characters, as many syllables as characters, all characters known, syllables valid. A word with several readings keeps the one with the highest usage score, the sum of log(count+1) of each character's syllable across the word list.
  - `CURATED_WORDS` then overrides or adds entries, with an assert on syllable count and validity.
  - Words ending in 地 read dei2 also get a 哋 alias (麻麻哋).
  - Canonical-spelling aliases are added unless they clash (clashes are counted): a word that rime (or `CURATED_WORDS`) spells with a variant form also gets an entry in the canonical spelling, e.g. 恒生 → 恆生, 群情洶湧 → 羣情洶湧, 為免 → 爲免. The opposite case, text in a variant spelling and rime's word in the canonical one (因為 in the text, 因爲 in rime), needs no alias: the walker's own canonical lookup (`\__xjyutping_can:n`) handles it. The comment above this code in `build-data.py` gives 因為/因爲 as the example for the aliases, which is the wrong direction.
  - `longest[final char]` is emitted as `\xjp@E`.
- **Curated tables** (the place to fix data permanently):

  | Table | Contents |
  | --- | --- |
  | `CURATED_DEFAULTS` | Two blocks. The first settles the characters rime leaves undecided: 會 生 行 畫 料 咪 咯 率 刊 撈 彙 嗎 嘎 咧 (from the initial build) and 量 (round 1). The second overrides defaults found wrong in review round 1: 返 faan1, 呀 aa3, 驚 geng1, 吓 haa5, 爭 zaang1, 划 waa4, 幢 zong6, 呢 ni1. |
  | `CURATED_FINALS` | 呢 → ne1 at the end of a run. |
  | `CURATED_VARIANTS` | 恒 → 恆. |
  | `CURATED_WORDS` | 135 entries (102 from round 1, 行長 while writing the manual, 32 from round 2): rime errors (畀咗 family, 相處, 前人種樹 …); literary guards for changed defaults (返回, 驚聞 …); missing words; guard words that stop a new entry capturing a phrase it should not (集中咗 for 中咗, 絕種咗 for 種咗, 16 guards for 平啲). |

- **Outputs.** At 1.0.0 the builder wrote `xjyutping-chars.def` and `xjyutping-words.def` next to the package. After 1.0.0 the output paths were changed to `xjyutping-tex/`, and the builder now also writes TSV tables for the Python port. See section 6.

---

## 3. Development log

### 3.0 Research and data (09:32–10:04)

- Read `xpinyin.dtx`. The approach is the same: hook xeCJK's `\CJKsymbol`.
- Studied xeCJK's interchar classes and its punctuation code, and the l3kernel's `\tl_analysis_map_inline:nn` and `\tl_build_*`.
- Sampled polyphones in LSHK and rime. Of the characters rime lists with several readings, 60 have no primary reading. The frequent ones among them (生 到 上 行 會 數 長 重 當 …) were given curated defaults where needed.
- Findings and fixes in the data builder:
  - **D-1.** The first variant analysis used a wrong `grep` pattern, so every pair counted 0. It was redone in Python. This was an analysis mistake, not a shipped bug.
  - **D-2. Bad variant folding.**
    - Symptom: the raw OpenCC reversal mapped common characters onto rare ones (參→蔘, 針→鍼); 77 mappings, 272 aliases.
    - Cause: OpenCC maps both directions, and a character can be both a standard form and a variant.
    - Fix: `load_variants(freq)` keeps a mapping only when rime prefers the standard form. The result was 75 mappings and 59 aliases.
    - Verified by listing the `\V` lines.
  - **D-3.** `jyut6ping3.phrase.dict.yaml` has no readings, so it was dropped.
  - **D-4.** A polyphone flag based on "more than one significant reading" flagged 6 083 characters, including changed tones (人 jan2) and rare readings. It was refined into the changed-tone rule, giving 4 188. (This refinement was made at 10:17, after the first compile, not during the research phase.)

### 3.1 First implementation (10:06–10:17)

The first `xjyutping.sty` (27 KB, written at 10:06) was a single-pass preprocessor:
- a skip-list property for reference commands (`\c__xjyutping_skip_prop`, built with `\prop_const_from_keyval:Nn`; the pre-compile patch replaced it with `\g__xjyutping_skip_prop`);
- a three-argument mark `\xjyutping@mark{char}{reading}{type}`;
- the dynamic-programming segmenter;
- a fixed cell: each character centred in an `\hbox_to_wd:nn` of the cell width, with the ruby as an overlay inside it, and `\CJKglue` replaced by plain hsep glue. There was no pending right pad yet; that came with the I-3 restructuring (10:13), where the right half was left pending and paid only by the next `\CJKglue`.

A patch before the first compile (10:08) fixed six problems: an invalid message-function variant (`\msg_warning:nnnenn` → `:nneeee`), the skip-table value format, the `\prop_get` lookup, the boolean restore on the brace stack, the key used to detect user words (`\__xjyutping_word_cs:nnN` replaced by `\__xjyutping_word:nnN` with the `xjp@w@` prefix at the call sites), and width-cache names shared across nested blocks (made per block). The main agent's reasoning at that point says it found these by reading back its own draft. The item numbers in the patch comments ("1/32", "8/48", "2/3/46", "28") are not explained anywhere (unverified: probably the numbering of that self-review). The first compile of `tests/basic.tex` found:

- **I-1. A digit inside a variable name.**
  - Symptom: `! LaTeX Error: Missing \begin{document}` at `\tl_new:N \l__xjyutping_buf_0_tl`.
  - Cause: under expl3 catcodes digits are not letters, so the token was `\l__xjyutping_buf_` followed by the text `0_tl`.
  - Fix: `c`-type variants (`\tl_new:c { l__xjyutping_buf_0_tl }`, `\tl_build_begin:c` and so on).
- **I-2. The font cache stored the `\font` primitive.**
  - Symptom: `! Font \__xjyutping_strut:=ngo5 not loadable`.
  - Cause: `\cs_gset_eq:cN {key} \tex_font:D` saved the primitive, not the current font.
  - Fix: cache the NFSS font name `\curr@fontshape/\f@size`. This was later replaced by the full NFSS-state cache (R1-19).
- **I-3. Boxing the character broke xeCJK.**
  - Symptom: `! Missing number, treated as zero` inside xeCJK's punctuation-width code (`\c__xeCJK_xeCJK/SongtiTC(0)/m/n/10/quanjiao/dim/rule/right…`), isolated to `行，`.
  - Cause: the first cell layout typeset the real character only inside boxes built in the hook (`\hbox_to_wd:nn` around a `\makexeCJKinactive` character box, with the ruby overlay). The main agent's reasoning at 10:10 gives the diagnosis: XeTeX's last-character class tracking is thrown off when the character is boxed inside the hook, which unbalances xeCJK's class groups; xpinyin avoids this by typesetting the real character last, at the outer level. It was checked by reading xeCJK's class-group code (`\xeCJK_class_group_begin:`/`_end:`), not by a separate experiment. (The session's compaction summary calls the error "Missing }"; the log in the transcript shows "Missing number".)
  - Fix: the cell was restructured into the layout of section 2.7: the character typeset last with the saved `\CJKsymbol`, the ruby as a zero-width overlay, the left half-pad as a kern after an empty box, and the right half pending.
- **I-4. No padding before Latin text; lines too close.**
  - Symptom (seen in renders): the right pad was lost before Latin text, and rubies came near the line above.
  - Fix: `\__xjyutping_CJKecglue:` also pays the pad. Line spacing was raised.
- **I-5. Rubies could touch the line above; the environment's `\baselineskip` was not applied.**
  - Fix: `\__xjyutping_clearance:`, an invisible rule 0.35em above the ruby. The baselineskip factor became vsep + ruby + 0.6em, and the environment now ends with `\par` so its `\baselineskip` applies to its last paragraph.
- **I-6. Proofreading needed the alternatives.** The `\M` loader (renamed `\xjp@M` in M1-2) now also stores the alternative readings, and debug lines show `m(alt …)`. Done at 10:16 together with D-4.

The session summary also lists "ExplSyntax spaces in the data" as an early issue. The first version already sets the space catcode and `\endlinechar=-1` around `\file_input:n`, so no separate event can be identified.

Measurement: a random 19 926-character, 52-page document compiled in **4.7 s**. The README was then written; it became the reviewers' specification.

During round 1 the manual `xjyutping-doc.tex` was drafted and trial-compiled in the scratchpad:
- `\marg`/`\oarg` were added;
- `\XeLaTeX{}` was replaced by `Xe\LaTeX{}`;
- examples were changed to 重未 → `\setjyutping{重未}{zung6 mei6}` and `width=2em`. At 11pt, `1.6em` (17.5pt) is narrower than the auto width (20.6pt), so it looked "too narrow"; it was not a bug;
- `\setlength\emergencystretch{3em}` was set in the manual's preamble later, at 11:47 (after the round-1 fixes), for two overfull lines caused by long typewriter words.

### 3.2 Review process (common to all rounds)

Each round was a Claude Code workflow: several finder agents ("lenses") ran in parallel, and each lens's findings went to an **adversarial verifier**.
- The verifier had to reproduce every finding in its own directory and decide `confirmed`, `modified` (real, but with a corrected fix) or `rejected`. It was told to default to rejected when unsure.
- Finders and verifiers could not edit the package; they wrote repro `.tex` files in `tests/<lens>/`, since moved to `scratchpad/review-artifacts/`.
- The main agent then:
  1. implemented the fixes;
  2. recompiled every repro from the round (`repros.py`/`repros2.py`: compile twice, count `^!` errors, overfull boxes and `[no context]` lines);
  3. re-ran the reading-audit corpora and compared each finding with the new reading;
  4. rendered layout cases to PNG, or dumped boxes.
- Round 2 also re-checked every round-1 finding with a separate "recheck" lens per original lens, reporting fixed, partly-fixed, now-documented or not-applicable.

| Round | Time | Agents | Lenses | Verifier outcomes |
| --- | --- | --- | --- | --- |
| 1 | 10:19–11:03 | 14 | 3 reading audits (colloquial, formal, polyphones) + 4 bug lenses (robust-structure, robust-tokens, layout, code-review) | reading: 57 confirmed, 17 modified, 8 rejected; bugs: 27 confirmed, 18 modified, 1 rejected |
| 2 | 11:47–12:33 | 18 | 4 recheck lenses + 3 bug lenses (review2-walker, review2-layout, review2-robust) + 2 reading audits (textbook, mixed) | 39 new bug findings, none rejected; 14 reading findings |
| 3 | 12:49–13:43 | 6 | 3 regression hunts: r3-walker (code paths), r3-layout (visual), r3-user (a learner builds three real documents from the README only) | 24 findings, none rejected |

### 3.3 Review round 1 (findings 10:19–11:03; fixes 11:09–11:48)

#### Reading accuracy audits (before fixes)

| Corpus | Sentences | Characters | Wrong | Accuracy | Findings (conf/mod/rej) |
| --- | --- | --- | --- | --- | --- |
| colloquial HK Cantonese | 60 | 936 | 43 | 95.4% | 26 (17/8/1) |
| formal written Chinese | 60 | 1 369 | 17 | 98.8% | 16 (11/2/3) |
| polyphone stress test | 75 | 1 500 | 50 | 96.7% | 40 (29/7/4) |

Accuracy was **not** re-measured as a percentage after the fixes. Instead, each kept finding's span was looked up in the recompiled corpus and compared with the expected reading.
- Every data-fixable finding passed, except 平啲 (deferred to round 2).
- The checker script could not locate 划算 / 划船, whose span was written with a slash, so the session never checked it. Re-checked for this write-up against the 1.0.0 snapshot with the finding's sentence (呢個價錢好划算，我哋去划船。): both 划 are waa4 (from the new default, type `m`).
- 發佈會 and 揣度 were reported as mismatches only because the expected field contained "(or …)"; their new readings are the expected ones.

**Fixed via `tools/build-data.py`** (applied at 11:11):
- **`CURATED_DEFAULTS`**, second block:
  - 返 faan1: guarded by 返回, 返鄉, 返航, 返程, 返還, 返國, 積重難返 (faan2);
  - 呀 aa3, plus 係呀 hai6 aa3. rime's other aa4 words (咩呀 …) were kept as genuine challenging particles;
  - 驚 geng1: guarded by 驚聞, 驚見, 驚爆, 驚現, 驚叫, 驚傳, 驚變, 驚艷, 驚悉, 大吃一驚;
  - 吓 haa5 (aspect marker). Accepted cost: the interjection 吓？ becomes haa5;
  - 爭 zaang1, 划 waa4, 幢 zong6;
  - 量 loeng6, guarded by 量體溫 and 量血壓 (loeng4);
  - 呢 ni1.
- **`CURATED_FINALS`**, 呢 → ne1 at run end. The verifier had *rejected* simply changing 呢's default to ni1, because the sentence-final particle ne1 (點解呢) would break. The implemented alternative is a new mechanism: a run-final reading (`\xjp@F`, the `f` argument of `\__xjyutping_lookup:nn`). It gives 呢張床 ni1 and 你呢？ ne1 (both are in `regression.expected`).
- **`CURATED_VARIANTS`**: 恒 → 恆 (恒生).
- **`CURATED_WORDS`**, 102 entries:
  - rime errors: 畀咗 and 6 longer forms (rime read 咗 as saai3), 有朋自遠方來, 相處/共處 (cyu5), 前人種樹, 少壯, 少壯不努力, 世上無難事, 屢見不鮮, 會唔會, 幾度 (gei2), 揣度, 間房 (gaan1), 成日 (seng4);
  - missing words: 好正, 好精, 把聲, 好平, 咁平, 最平, 平嘢, 瞓唔到覺, 成個鐘, 成身, 成間, 彈琴 (and 4 other instruments), 張相, 相集, 着咗件, 着衫, 着多件褸/衫, 著住, 訂位, 訂枱, 冇位, 問下 (guards 問下個月 and 問下個禮拜), 今晚會, 聽晚會, 琴晚會, 行車線, 而行, 恒生, 不亦說乎, 中咗 (guard 集中咗), 人話 (guards 講人話, 唔講人話), 發佈會, 發布會, 調高 (guard 強調高), 數吓, 數完, 應聘, 個名, 頂帽, 上咗, 乾隆, 朝住, 種咗 (guard 絕種咗), 畫咗, 屏住, 屏息, 盛飯, and the 量 compounds.
- **Aliases**: every word ending in 地 read dei2 gets a 哋 twin (麻麻哋). The builder does not print how many; recomputed for this write-up, it adds 82 at 1.0.0 (83 in round 1, when 輕輕哋 was still an alias rather than a curated word). The "103" printed in the transcript by `grep -cF "哋="` counts every word ending in 哋, including rime-cantonese's own 20 (我哋, 佢哋 …).
- **Polyphone flag**: a changed tone only exempts the flag when it is *weaker* than the default. 數 is now flagged `m` (colloquial #25: no reading change, but it can be highlighted). 4 188 → 4 349 flagged. The verifier had predicted only 7 newly flagged characters (扒 數 到 桿 嗎 妹 宅). Recomputed for this write-up with the 1.0.0 builder, the rule change accounts for 158 new flags: 8 characters with rime weights and 150 LSHK-only characters, where every reading counts as weight 100, so their changed tones are never "weaker" and now flag the character.

**Builder bug found while doing this (M1-0):** a curated default can be a reading rime does not list (吓 haa5 comes only from LSHK), which raised `KeyError: 'haa5'` in the weight lookup. Fix: `weight.get(default, 100)`.

**Not fixed; genuinely ambiguous**, for a user override:
- 為 wai4/wai6 (旨在為基層);
- 同行 tung4 hong4 versus hang4;
- 當 (我當佢係) dong3;
- 背得 bui6;
- 散晒 saan3 (dispersing) against saan2 (fallen apart); rime has only saan2 saai3.

**Rejected by verifiers** (8):
- *unsafe fixes, although the error was real or plausible:* 個女 neoi2 (the word would capture 我個女朋友 …), 本會 wui6 (the tie-break would give 根|本會, 日|本會 … wui6), and changing 呢's default to ni1 (see above);
- *accepted variants or doublets:* 差強人意 koeng4, 參差 cam1, 劃龍舟 waa4;
- *doublets that duplicate accepted findings:* polyphones #31/#32 asked for 成個鐘/成日 seng4 and were rejected because sing4 is also heard; the same spans from the colloquial audit (#9, #12) were confirmed, so seng4 was added anyway.

**Deferred to round 2:** 平啲 (colloquial #14). The verifier kept the default ping4 and asked for the word entries 好平, 咁平, 最平 and 平嘢 (added in round 1); 平啲 itself stayed ping4 until round 2.

#### Bug findings (46; one rejected)

Unless noted, the fix came with the 11:18–11:22 rewrite of `xjyutping.sty` (27 KB → 46 KB), which introduced:
- the two-pass walker and command table;
- combo marks;
- right-pad payment at CJK/Boundary;
- local `\setjyutping` while reading;
- `\input` reading;
- the NFSS font cache;
- the clearance and line-spacing hooks;
- output-routine disabling;
- PDF-string handling.

The **Recheck** line gives the status reported by the independent round-2 recheck lens.

**robust-structure lens**

- **R1-01 (high) Nested scope loses word context.**
  - Symptom: an inner scope read 銀行 as ngan4 haang4, and every character was logged twice.
  - Cause: `\xjyutping@mark` was not in the skip list, so the inner pass marked the mark's own arguments.
  - Fix: the walker recognises existing marks (`\__xjyutping_premarked:` for `\xjp@R@…` tokens; the `mark` action for `\xjyutping@mark`) and copies each with its character.
  - Recheck: **fixed**.
- **R1-02 (high) Running heads annotated, in UPPERCASE, when a page is shipped from inside a scope.**
  - Cause: the output routine ran inside the scope group with the replaced `\CJKsymbol`, and `\MakeUppercase` changed the readings.
  - Fix: `\AddToHook{build/page/reset}{\__xjyutping_disable: …}`.
  - Recheck: **fixed** (headings and fancyhdr; the `\headheight` warning is gone).
- **R1-03 (high) ctexart size changes removed the cell spacing, so rubies overlapped.**
  - Cause: ctex redefines `\CJKglue` on every size change.
  - Fix, round 1: paying the pad at CJK/Boundary removed the overlap.
  - Recheck: **partly fixed**; the stretch was still ctex's glue (16 underfull boxes).
  - Completed in round 2: the `selectfont` hook reinstalls the package glue, ordered after ctex.
- **R1-04 (medium) `\setjyutping` in a scope changed text *before* it, and acted even in dead code.**
  - Cause: the preprocessor executed `\setjyutping` globally while reading the whole body.
  - Fix: while reading, settings are local to the reading group (`\__xjyutping_set:nnn … {}`); the global setting happens at typeset time at its position.
  - Recheck: **partly fixed**; settings inside `\iffalse` or an unused `\newcommand` still apply to later text in the same scope. Documented in the README in round 2.
- **R1-05 (medium) PDF bookmarks contained the reading or a stray `*`.**
  - Fix: `\xjyutping@pdf` and the other entries in `\pdfstringdefDisableCommands`.
  - Recheck: **fixed** (the `.out` decodes to plain text; 0 warnings).
- **R1-06 (medium) `\url`/`\href` containing `#` broke inside a scope; `%` ended the file.**
  - Cause: the `+b` body is already tokenised.
  - Fix: action `url` turns catcode-6 `#` into catcode-12 `#`. `%` is documented: write `\%`.
  - Recheck: **fixed** for `#`; `%` documented.
- **R1-07 (medium) Text from `\input`, macros or `\maketitle` ignored the word list.**
  - Fix: `\input` inside a scope is read and walked (`\__xjyutping_input:`). Macro and `\maketitle` text is documented and logged as `[no context]`. `\include` is left alone, as the verifier advised.
  - Recheck: **fixed**.
- **R1-08 (medium) One large scope exhausted main memory** (63k per the finder; the repro has 53 060 Han characters).
  - Fix: see M1-2 and M1-3 below, and section 3.7.
  - Recheck: **partly fixed** (53k OK at 3.32M words; 159k OK; 212k fails). Limits documented in round 2.
- **R1-09 (low) TOC annotated when `\tableofcontents` is inside a scope.**
  - The README was corrected: the TOC is annotated only if `\tableofcontents` is itself in a scope.
  - Recheck: **now-documented**.
- **R1-10 (low) The last character's ruby stuck out of `\fbox`, and `c` cells were off-centre.**
  - Cause: the right pad was paid only by a following glue.
  - Fix: pay the pending pad at xeCJK's CJK→Boundary transition (`\__xjyutping_boundary:w` wrapping `\xeCJK_CJK_and_Boundary:w`). The finder's first idea, a kern after the glyph, was shown by the verifier to destroy xeCJK's break points.
  - Recheck: **fixed**.
- **R1-11 (low) The pending pad leaked across paragraphs, items and cells.**
  - Fix: payment at boundary, and the `para/begin` hook zeroes the pad.
  - Recheck: **fixed**.
- **R1-12 (low) A line after a break at full-width punctuation started with stray glue.**
  - Cause: the empty `\hbox` after the pad kern stopped glue being discarded at the break.
  - Fix: `\CJKglue` now adds only stretch; the natural hsep lives inside the cells.
  - Recheck: **fixed** (every line starts `\hbox{} \kern`).
- **R1-13 (low) A stale mark from outside a scope (TOC, heads) set a later macro character's reading.**
  - Fix: `\xjyutping@mark` does nothing unless enabled, and the mark is cleared in `\__xjyutping_enable:`.
  - Recheck: **fixed**.

**robust-tokens lens**

- **R1-14 (high) Chinese label keys in `\hyperref[…]`, `\cpageref`, `\labelcref` gave `Missing \endcsname`.**
  - Fix: the cleveref and hyperref commands were added to the table; `\hyperref` uses `-1` (optional arguments only, so the link text is still annotated).
  - Recheck: **fixed** (78 errors → 0). The recheck also noted a gap outside this finding: natbib `\citeauthor`, `\citeyear`, `\citealp` and the name argument of `\pdfbookmark` were still annotated. The natbib commands were added in round 2 (R2-23); `\pdfbookmark` never was (see section 4, item 17).
- **R1-15 (high) Rubies overlapped at `\color`, `\textcolor`, `\mbox`, `\href` and image boundaries.**
  - Fix: pad paid at CJK/Boundary. The finder's "pay at the next cell" was rejected by the verifier.
  - Recheck: **fixed** (glyph positions measured with Ghostscript `txtwrite`).
- **R1-16 (high) Adjacent `\xjyutping`/`\xjyutping*` outside a scope overlapped.**
  - Cause: `\__xjyutping_enable:` zeroed the previous call's pending pad, and the pad was never paid after the group.
  - Fix: boundary payment inside the group.
  - Recheck: **fixed**.
- **R1-17 (medium) A brace group or formatting command split a word** (銀\textbf{行} → haang4).
  - Fix: the two-pass walker with transparent (`t`) commands and transparent groups.
  - Recheck: **fixed**.
- **R1-18 (medium) Macro or `\input` text had no word context and no `width=auto`.**
  - Same as R1-07/R1-32; `\input` fixed, macros documented.
  - Recheck: **now-documented**.
- **R1-19 (medium) `format=\itshape` or `\bfseries` printed rubies at full text size.**
  - Cause: the cached branch restored only the font, not `\f@size`.
  - Fix: the cache restores font, encoding, family, series, shape and size.
  - Recheck: **fixed** (ruby 4.48pt).
- **R1-20 (medium) Markup in a reading (`zung\textsuperscript{1}`) gave `Missing \endcsname`.**
  - Cause: the reading was used inside `\csname`.
  - Fix: the seen-cache key and the combo names use `\tl_to_str:n`.
  - Recheck: **fixed**.
- **R1-21 (medium) `\xjyutping` in a `\section` title put the reading into bookmarks and rubies into the TOC.**
  - Fix: bookmarks via `\xjyutping@pdf`.
  - Recheck: **partly fixed**; TOC and running heads still annotated.
  - Round 2: running heads plain (plain mode); the TOC behaviour for an explicit `\xjyutping` documented.
- **R1-22 (medium) `\hyperlink`/`\hypertarget` keys were annotated; links silently broken.**
  - Fix: both added to the table with 1 argument.
  - Recheck: **fixed** (the PDF destination matches).
- **R1-23 (medium) Annotated text preprocessed twice lost its context** (`\jp{銀行}` macro, nested scope).
  - Same fix as R1-01. The verifier showed that simply skipping the mark's 3 arguments was not enough.
  - Recheck: **fixed**.
- **R1-24 (low) `\MakeUppercase` uppercased the Jyutping.**
  - Fix: a one-argument mark, excluded from case changing.
  - Recheck: **fixed**.
- **R1-25 (low, REJECTED) `\setjyutping{為}` did not apply to 爲.** The verifier found it consistent with the README: variant folding is for word lookup only.
  - Recheck: **not-applicable**.

**layout lens**

- **R1-26 (high) Overfull lines at narrow widths and large sizes.** 110/315 lines in a width sweep at normal size; 9 of 21 lines in `punct-break.tex`.
  - Cause: rigid cells with only `0.15em plus 0.15em` of stretch, and no `\emergencystretch`.
  - Fix: default `hsep = 0.15em plus 0.4em`, and `\emergencystretch` ≥ 2em in scopes.
  - Verified by the main agent (0 overfull or underfull in `punct-break`, `frame-huge`, `real-a5paper`). The recheck sweep over 21 widths from 5 to 10cm gave 0 overfull lines:
    - normal size, 320 lines (was 110 overfull);
    - `\large`, 389 lines (was 155);
    - `\Huge`, 246 lines (was 93), with 16 underfull;
    - `width=natural` and `width=1.3em`.
  - Recheck: **fixed**.
- **R1-27 (medium) After a break at a closing mark, the next line began with hsep glue.** About 9% of lines.
  - Same fix as R1-12.
  - Recheck: **fixed** (0 of 1 625 lines).
- **R1-28 (medium) A stale right pad widened the first Latin-to-Chinese gap of the next paragraph.**
  - Fix: `para/begin` zeroing, and boundary payment.
  - Recheck: **fixed**.
- **R1-29 (medium) Uneven spacing inside 「…」 and （…）.**
  - Fix: `\__xjyutping_fullright:N` pays the pad only before closing brackets and quotes; other punctuation keeps hugging. The verifier rejected paying before all FullRight marks.
  - Recheck: **partly fixed**; it failed when the character before the bracket ended a group.
  - Completed in round 2 (R2-16/R2-30).
- **R1-30 (medium) Inline `\xjyutping*` had space on the left and none on the right.**
  - Fix: boundary payment restores the right pad.
  - Recheck: **partly fixed**; natural widths symmetric, stretch not (xeCJK's 0.08\baselineskip on entry against the package's 0.4em on exit).
  - Round 2 rewrote the deferred path so that after a group the pad is paid and xeCJK inserts its own glue (node restored). The transcript does not re-measure this.
  - Re-running `inline-asym.tex` against the 1.0.0 snapshot for this write-up shows `去 glue 0 plus 1.44 | pad 銀 … 行 pad | glue 0 plus 1.44 攞`: both sides now carry xeCJK's glue, so this is **resolved at 1.0.0**.
- **R1-31 (low) Line pitch not constant: deep lines, or a size command inside the scope, fell back to `\lineskip`.**
  - Fix, round 1: `\lineskiplimit -0.3em`, and `\baselineskip` re-raised in the `selectfont` hook.
  - Recheck: **partly fixed**; deep lines fixed, but size changes were still undone by `\size@update`.
  - Completed in round 2 (R2-05/R2-27), where `\lineskiplimit` went back to 0pt with a 0.05em clearance (R2-29).
- **R1-32 (medium) Macro or `\input` text lost word context, and `width=auto` fell back to natural widths.**
  - `\input` fixed in round 1. The `width=auto` fallback (measure `gwong2`) was added in round 2.
  - Recheck: **partly fixed**, then completed in round 2.
- **R1-33 (low) `font=\sffamily` raised a spurious xeCJK "Unknown CJK family" warning.**
  - Fix: `\cs_set_eq:NN \xeCJK@family \use_none:n` in `\__xjyutping_select_font:`.
  - Recheck: **fixed**.

**code-review lens**

- **R1-34 (high) The right pad was lost when a space, `~`, `\ ` or `\,` separated two annotated characters, so rubies overlapped.**
  - Fix: boundary payment puts the pad before the separating glue or kern. The verifier's corrected version also moves the penalty of `~`.
  - Recheck: **fixed**.
- **R1-35 (high) Two adjacent manual `\xjyutping` overlapped.**
  - Same fix as R1-16.
  - Recheck: **fixed**.
- **R1-36 (medium) `\disablejyutping` inside an environment or `\begingroup` leaked into the rest of the scope in the preprocessor.**
  - Fix: the semantic stack pushes and pops the walker's active flag on `\begin`/`\end`, `\begingroup`/`\endgroup` and `\bgroup`/`\egroup`.
  - Recheck: **fixed**.
- **R1-37 (medium) A nested `\xjyutping*` or scope re-segmented marked text.**
  - Same fix as R1-01.
  - Recheck: **fixed**.
- **R1-38 (medium) The font cache ignored `\f@size` for `multiple=`/`format=` font switches.**
  - Same fix as R1-19. The verifier noted that restoring only `\f@size` was incomplete, hence the whole NFSS state.
  - Recheck: **fixed**.
- **R1-39 (medium) A reading containing a command was put inside `\csname` during measurement.**
  - Same fix as R1-20.
  - Recheck: **fixed**.
- **R1-40 (medium) Every block permanently added one csname per distinct reading** (201 blocks → +5 600 names; exhaustion at about 420k names).
  - Fix: one `xjp@seen@<reading>` per reading, holding the block number.
  - Recheck: **fixed** (174 040 names for both the 1-block and the 201-block files).
- **R1-41 (medium) Running heads with rubies and uppercased readings.**
  - Same fix as R1-02.
  - Recheck: **fixed**.
- **R1-42 (low) Manual `\xjyutping` in titles: bookmarks and TOC.**
  - Same as R1-21.
  - Recheck: **partly fixed**; completed in round 2 (plain running heads; TOC documented).
- **R1-43 (low) `\hyperref[銀行]{…}` inside a scope gave an error.**
  - Same fix as R1-14.
  - Recheck: **fixed**.
- **R1-44 (low) A one-token unbraced argument received the mark** (`\textbf 行`, `\setjyutping 行{hong4}`).
  - Fix: table commands take a single unbraced token as an argument (`\__xjyutping_skip_other:nn`). For other commands the README says to use braces.
  - Recheck: **fixed**.
- **R1-45 (low) `\input` text annotated without word context.**
  - Same fix as R1-07.
  - Recheck: **fixed**.
- **R1-46 (low) An unspent pad went stale and widened a later gap** (行。ABC字).
  - Fix: the `\CJKpunctsymbol` wrapper zeroes the pad before punctuation and adds no nodes. The verifier showed that the finder's "pay after the punctuation" broke xeCJK's compression of consecutive punctuation.
  - Recheck: **fixed** (equal widths; 。」 compression kept).

Recheck totals for the 46 round-1 findings: 34 fixed, 9 partly fixed, 2 now documented, 1 not applicable.

#### Follow-up changes during round-1 fixing (11:24–11:48)

- **Pad at a group end.** A first attempt recorded `\currentgrouptype` at xeCJK's class-group start. It was replaced the same minute by the after-group peek (`\__xjyutping_defer:` → `\__xjyutping_defer_test:`): the decision to drop or pay the pad is made from the token after the group. This keeps `{\color{red}長}，` hugging while `\mbox{長}` pays inside the box.
- **Class `z`** was added for commands without arguments (`\par`, `\\`, `\item` …), so a brace group after them is ordinary text, not an argument.
- **M1-1. Rewrite regression: `#` in the body.**
  - Symptom: `! Illegal parameter number in definition of \__int_map_1:w` in `repro-url.tex`.
  - Cause: the body was passed straight into a mapping function.
  - Fix: store the body in `\l__xjyutping_body_tl` and walk it via a `:V` variant.
  - Verified by the repro rerun.
- **M1-2. Save-stack overflow** (`! TeX capacity exceeded, sorry [save size=200000]`). It appeared when per-run data began to be freed inside the reading group. Steps, each measured on the 53k repro:
  1. per-character slots made global: still overflowing;
  2. global `\tl_build_gbegin/gend`: still overflowing;
  3. data loaded at top level with internal loader names. A small test's save stack went from 140 558 to 407 entries, but the repro still overflowed;
  4. slots set to `\relax` instead of undefined: compiles, with 54 180 save-stack entries.
- **M1-3. Main memory.** After step 4 the repro used 4.88M words. A stage breakdown on scratch copies gave base 2.48M, pass 1 3.88M, both passes 4.80M. Per-paragraph analysis brought it to **3.32M words** (12.6 s, 140 pages).
- **M1-4. `\seq_set_split` strips braces.** A test showed that the l3 split turns `{\bfseries C}` into `\bfseries C`, so a custom splitter with a `\prg_do_nothing:` guard is used (`\__xjyutping_split:w`).
- **M1-5. Missing word 行長**, found at 11:48 while building the manual (round 2 was already running). 係\textcolor{red}{行}長 read haang4. The walker was correct (one run); the data lacked the word. Added 行長 hong4 zoeng2 to `CURATED_WORDS`.
- **Process note.** A background repro job was started against an older package version and buffered its output. It was killed and rerun (`repros.py`, skipping the multi-minute memory tests).

**Verification of round 1:**
- every repro recompiled with 0 errors; the only non-zero counts were `\showbox` "OK" pseudo-errors;
- layout stress files: 0 overfull or underfull;
- the three audit corpora compiled without errors (129, 158 and 202 runs logged);
- the README was rewritten to match (it is the spec for round 2).

### 3.4 Review round 2 (findings 11:47–12:33; fixes 12:36–12:49)

#### Reading audits

| Corpus | Sentences | Characters | Wrong | Accuracy | Findings |
| --- | --- | --- | --- | --- | --- |
| learner textbook dialogues | 80 | 890 | 6 | 99.3% | 6 (5 confirmed, 1 modified) |
| mixed HK reading material | 77 | 1 438 | 8 | 99.4% | 8 (4 confirmed, 4 modified) |

**Fixed by data** (`CURATED_WORDS`, 12:36; checked by looking up each span in the recompiled corpora, all matching):
- 平啲 peng4 di1, with 16 guard words for X平+啲 (公平啲, 持平啲, 水平啲, 太平啲, 和平啲 …). The verifier showed that without the guards the tie-break turned 13 correct ping4 contexts into peng4;
- 做邊行 hong4;
- 轉咗工 zyun3;
- 一唱一和 wo6;
- 成個人, 成個人生, 成件事 (and 件事), 成頭家 (seng4);
- 小心地滑 (a segmentation fix);
- 輕輕 hing1 hing1, 輕輕地, 輕輕哋 heng1;
- 為配合, 為確保, 為免 (wai6). The verifier: do *not* add 為方便.

**Left for the user, ambiguous:** 彈得 taan4, 種花 zung3, 假 gaa3 in 請咗三日假, 長得 zoeng2, and 為 in other contexts.

#### Recheck-lens findings (new problems found while re-checking round 1; 16)

- **R2-01 (high) nameref broke.** Also reported as R2-06, R2-18 and R2-33.
  - Symptom: `\nameref` to a section or caption inside a scope gave `Undefined control sequence \xjp@R@wngan` and stray tone digits, on every run, before or after the scope.
  - Cause: nameref detokenises the title into the `.aux`; `\xjp@R@wngan4` is read back as `\xjp@R@wngan` followed by `4`. Combo macros are also undefined before the scope that creates them.
  - Fix, round 2: `\cs_if_exist_use:N \GTS@expandtrue` in `\__xjyutping_enable:`, which makes gettitlestring expand titles, turning marks into `\xjyutping@mark{…}`.
  - **This fix caused R3-02** and was replaced in round 3 by `\__xjyutping_unmark:N` in `\label@hook`.
  - Verified: `regression.tex` contains `\nameref{sec:a}` and compiles without errors (from round 2 on).
- **R2-02 (high) `\endinput` in an `\input` file aborted the whole job.** Also reported as R2-08 and R2-17.
  - Cause: the file was inlined with `\file_get:nnN`, and `\endinput` later ran against the main file.
  - Fix: the safe-file check; files containing `\endinput` (and verbatim or catcode changes) fall back to a real `\input`. The verifier noted that cutting at the first `\endinput` is wrong for guards like `\ifdefined…\endinput\fi`.
- **R2-03 (medium) `\input` files could no longer contain `\verb`, verbatim or a `%` in a URL.** This worked before the rewrite.
  - Fix: the same fallback, and the README documents the restrictions.
- **R2-04 (low) A primitive `\setbox0\hbox{銀行}` between paragraphs added a stray empty line.**
  - Cause: the deferred pad was paid (`\kern` plus `\hbox{}`) in vertical mode.
  - Fix: `\__xjyutping_pad:` pays only `\mode_if_horizontal:T`, and always zeroes.
  - This zeroing in math mode later contributed to R3-06/R3-13/R3-20.
- **R2-05 (low) The `selectfont` hook's raise was undone by `\size@update`** (cramped ruby lines in ctexart).
  - Fix: run `\size@update` inside the hook before `\__xjyutping_raise_baselineskip:`.
  - Verified with `vdump.sh` on `r-size-inside.tex`: all interline glue is `\baselineskip`.
- **R2-06** is a duplicate of R2-01.
- **R2-07 (medium) `\setjyutping` in the middle of a run changed text before it and missed text after it.** Duplicate of R2-20.
  - Cause: class `a` kept the run open, and the local setting was applied before the run was segmented.
  - Fix: `\__xjyutping_flush_all:` before the local set. It segments every open run, including the one around a footnote.
  - Verified: `reg-setjyutping-midrun` logs `銀ngan4:w行hong4:w | 行hang4:u`, and the last line of `regression.expected` covers it.
- **R2-08** is a duplicate of R2-02; the `\makeatletter`-in-file part is handled by the same fallback.
- **R2-09 (low) A manual reading on a non-Chinese character leaked to the next unmarked character.**
  - Cause: the new marks no longer name their character.
  - Fix: `\group_insert_after:N \__xjyutping_clear_mark:` in `\__xjyutping_manual:nn`.
- **R2-10 (low) A long `\input` file ran out of memory where the same text inline did not.**
  - Fix: the file is split into paragraphs and walked like the body (`\__xjyutping_split_pars:NV`, `\__xjyutping_walk_file:nn`).
- **R2-11 (low) The debug log showed `[no context]` lines for characters without a reading** (／, Ａ, 𠮷).
  - Fix: log only when a reading exists.
- **R2-12 (medium) A group-final character got no glue before the next character** (no stretch, no break). Also R2-15 and R2-26.
  - Cause: the deferred pad was paid after xeCJK's CJK node, so xeCJK no longer saw a preceding CJK character.
  - Fix: `\__xjyutping_pad:` removes the node, pays, and re-makes the node (`\xeCJK_if_last_node:nTF`, `\xeCJK_remove_node:`, `\xeCJK_make_node:n`).
  - Verified: in the repro rerun, the reviewers' `r-adjacent-manual.tex` (previously overfull by 37.5pt and 60.8pt) and `r05-group-nobreak.tex` recompiled with 0 errors and 0 overfull boxes. `pad2.tex` (now `tests/layout-check.tex`) keeps an 18-call chain of `\xjyutping{…}{…}` as a standing check.
- **R2-13 (low) A group-final character lost `\CJKecglue` and the break point before Latin text.** Same fix as R2-12.
- **R2-14 (low) Footnote marks, `\textsubscript` and `\textsuperscript` were pushed a pad away from their character.**
  - The verifier's fix (wrapping those commands) was **not implemented**, and round 3 raised no finding about it.
  - Status at 1.0.0: **open**. Re-running `recheck-layout/fnmark.tex` against the 1.0.0 snapshot for this write-up still shows `錢 \kern 4.86 \hbox{}` before the footnote-mark box, and the same before `\mathon` of `\textsubscript`. See section 4.
- **R2-15** is a duplicate of R2-12.
- **R2-16 (low) The pad was dropped before a closing bracket after a manual `\xjyutping` outside a block, and for brackets missing from the list** (〗〙〟｠).
  - Fix: the list was extended, and the deferred path (`\__xjyutping_decide:` → `\__xjyutping_closing:n`) pays before closing brackets.

#### New-lens findings (23)

**review2-walker lens**

- **R2-17** is a duplicate of R2-02.
- **R2-18** is a duplicate of R2-01.
- **R2-19 (high) The pending mark was stolen or cleared at a paragraph start** (run-in `\paragraph`, `\xjyutping` in fancyhdr heads).
  - Cause: the mark was stored in vertical mode; `\everypar` or the output routine then ran before the character.
  - Fix: `\mode_leave_vertical:` inside `\xjyutping@mark`.
- **R2-20** is a duplicate of R2-07 (with `\footnote`).
- **R2-21 (medium) A brace group after a table command's complete arguments was still read as its argument** (`\ref{x}{\itshape 長}大`, `\input`, `\begin{quote}`, `\footnote{…}{…}`).
  - Fix: owner reset to `n` in `\__xjyutping_arg_done:` before dispatch, and after a class-`a` argument group.
  - Verified: the `t17-owner-leak` log gives 長zoeng2:w大daai6:w in every case.
- **R2-22 (medium) `*` or `[…]` before a braced argument merged it with the following text** (`\section*`, `\footnote[7]{…}`, `\marginpar[…]`). Also R2-35.
  - Fix: in `\__xjyutping_nonhan:n`, a `*` after an `a`/`b` owner is copied; a `[` opens its own run without flushing the outer one.
  - Verified with the `t04-star-opt-merge` log.
  - Round 3 replaced the single-slot state with a stack (R3-03).
- **R2-23 (low) Reference commands missing from the table** (`\Vref`, `\Nameref`, `\namecrefs` …, natbib and biblatex citations, `\subref`, `\zref`).
  - Fix: all added with `{1}{}{b}`.
  - Verified: `t21-table-gaps.tex` compiles except for `\lcnameCref`, which is not a real command; that is an error in the test.
- **R2-24 (low) Walker time grew quadratically with an unpunctuated run** (20 000 characters: 28 s).
  - Cause: `\seq_put_left:Ne` per segment, and an unconditional log append.
  - Fix: linear collection into `xjp@seg@<k>`, and the log only in debug mode.
  - The fix introduced **M2-1**: segment emission expanded only one level, giving 122 `Missing number` errors in `basic.tex`. Fixed with `\use:e`.
  - The transcript does not re-time the walker. For this write-up the verifier's timing files were re-run against the 1.0.0 snapshot, with typesetting stubbed out:

    | Test | Before | At 1.0.0 |
    | --- | --- | --- |
    | 5 000-character run | 2.43 s | 1.21 s |
    | 20 000-character run | 28.0 s | 5.35 s |
    | 20 000 characters with a comma every 10 | 2.98 s | 3.45 s |

    A second, independent re-run during the fact check gave 1.19 s, 5.24 s and 3.44 s. The time is now about linear in run length; the punctuated case is slightly slower than before, consistent with the per-character checks added in round 3. **Resolved.**
- **R2-25 (low) `\disablejyutping` in a tabular cell stayed off in the walker for later cells.**
  - Fix: `\__xjyutping_tab:` at `&` restores the state saved at the enclosing `\begin`.
  - Extended to `\\` rows in round 3.

**review2-layout lens**

- **R2-26 (high) Adjacent annotated groups got no `\CJKglue`,** so text ran off the page. Same fix as R2-12.
- **R2-27 (medium) Size commands inside a scope lost the raised `\baselineskip`.** Same fix as R2-05.
- **R2-28 (medium) After `\textbf{…}`, `\emph{…}` and `\underline{…}`, the pad was paid before punctuation.**
  - Cause: `\check@icr` expands to `\aftergroup\maybe@ic`, so the boundary saw `\aftergroup`, not a group end; after the group the peek then saw `\maybe@ic`.
  - Fix: defer on `\tex_aftergroup:D` too, and look past `\maybe@ic` (`\__xjyutping_defer_ic:w`).
  - `\underline` (math) was left for round 3.
- **R2-29 (medium) `\fbox` and `\colorbox` in a scope reached into the line above.**
  - Cause: `\lineskiplimit -0.3em` allowed the overlap.
  - Fix: clearance 0.05em inside scopes, with `\lineskiplimit` back to 0pt; a too-tall line now gets `\lineskip`.
  - `vdump` on `r-fbox.tex` after the fix shows one `\lineskip` glue; the transcript does not comment on it. Re-running the dump against the 1.0.0 snapshot for this write-up gives the same glue list and shows where it is: all four interline glues around the `\fbox` and `\colorbox` lines inside the scope are `\baselineskip` (0.39, 0.43, 0.79 and 0.83pt), so the framed lines fit; the single `\lineskip` comes before the file's third paragraph, the control case *outside* the scope (`\fbox{\xjyutping{行}{hang4}}` in a normal-`\baselineskip` paragraph), where TeX falls back to `\lineskip` as usual. **Fixed.**
- **R2-30 (medium) Brackets after a group-final character lost their padding.**
  - Fix: `\__xjyutping_decide:` handles FullRight marks through `\__xjyutping_closing:n`; see R2-16.
- **R2-31 (medium) A space or source line break between a character and punctuation left a gap.**
  - Fix: `\__xjyutping_punct_space:n` drops the space before FullRight/FullLeft in pass 2.
- **R2-32 (low) minipage, `\parbox` and `p` columns reset `\baselineskip`.**
  - Fix: the `para/end` hook re-raises it.
  - The round-2 verifier had already warned that the `para/end` re-raise alone would leave the line after the `\underline` line on `\lineskip`, because `\@arrayparboxrestore` also resets `\lineskiplimit`; it proposed restoring `\lineskiplimit` too, or adopting R2-29's 0pt scheme. The 0pt scheme is what shipped.
  - `vdump` of `r-parbox.tex` after the fix still showed one `\lineskip` glue; the transcript does not comment on it. A deeper dump against the 1.0.0 snapshot (for this write-up) shows:
    - the minipage lines are `\baselineskip` apart (pitch about 19.57pt at 10pt);
    - the line after the one containing `\underline` (depth 3.47pt) gets `\lineskip 1.0`, a pitch of about 21.6pt. Inside the minipage the cells are built while `\baselineskip` is still the reset 12pt, so every ruby gets the 0.35em clearance (line height 17.17pt instead of 14.12pt); the `\baselineskip` raised at `para/end` then leaves only about 2.4pt for the depth of the line above, and `\lineskiplimit` is 0pt since R2-29;
    - the outer `\lineskip` between the minipage and the tabular is normal for two tall boxes. `vdump.sh` prints only the outer vertical list, so this outer glue is the single `\lineskip` the round-2 check saw; the minipage's own lines were not in that dump.

    In ordinary scope text (checked the same way) the `\underline` line is followed by normal `\baselineskip` glue; only a line deeper than about 5.45pt at 10pt (0.55em, e.g. a display-style `\sum` in the line) falls back to `\lineskip`, as in plain LaTeX. The larger clearance inside the minipage comes from the round-3 fix R3-24 (0.05em only when `\baselineskip` is at the scope minimum): a scratch copy of the 1.0.0 package with the round-2 rule (0.05em whenever in a scope) gives the same minipage all-`\baselineskip` glue. So the R2-32 fix works, but since R3-24 the pitch inside minipage, `\parbox` and `p` cells grows after moderately deep lines. See section 4.

**review2-robust lens**

- **R2-33** is a duplicate of R2-01.
- **R2-34 (medium) Punctuation after `\textbf{…}`, `\emph{…}` or nested groups was pushed away.**
  - Fix: R2-28's fix, plus `\__xjyutping_defer_test_aux:` re-arms when another group end follows ("one more group").
  - The nested `\textbf` case was still broken; completed as R3-09.
- **R2-35 (medium) Starred and optional-argument forms merged, and beamer overlays leaked.**
  - `*` and `[…]`: R2-22's fix. Beamer overlays: R3-18.
- **R2-36 (medium) xeCJKfntef commands (`\CJKunderline`, `\CJKsout` …) collapsed the cell grid; `\CJKunderdot` dots were off-centre.**
  - **Not fixed.** The README tells users to use `\underline` or ulem's `\uline` in scopes.
- **R2-37 (low) Underline and emphasis-mark commands ended the run,** so a marked character lost its word.
  - Fix: ulem commands declared `{0}{}{t}`; xeCJKfntef commands declared `{-1}{}{t}`, with `-` copied like `*`.
- **R2-38 (low) A beamer `\frametitle` inside a scope was segmented but typeset plain.**
  - Cause: beamer typesets the title after the scope has ended.
  - **Not fixed; documented** (`\frametitle{\xjyutping*{…}}`).
- **R2-39 (low) Main-memory overflow for one very long paragraph (above about 16k characters), or a long brace group.**
  - **Not fixed; documented** (about 15k per paragraph; a brace group is read in one piece).

Items left partly fixed by the round-2 recheck, and what round 2 did about them:
- **R1-03** (ctex glue): the `selectfont` hook reinstalls the glue, ordered after ctex. **Fixed.**
- **R1-04** (dead-code `\setjyutping`): **documented.**
- **R1-08** (memory): **documented.**
- **R1-21/R1-42** (TOC and running heads): running heads **fixed** by plain mode (`\xjyutping` prints only its text in the output routine); TOC **documented.**
- **R1-29** (group-final bracket): **fixed** (R2-16/R2-30).
- **R1-30** (stretch asymmetry): **resolved** by the round-2 node-restoring pad (confirmed on the 1.0.0 snapshot; see above).
- **R1-31** (size change): **fixed** (R2-05).
- **R1-32** (`width=auto` for macro text): **fixed** by the `gwong2` fallback in `\__xjyutping_prepare:n`.

**Verification of round 2** (12:42–12:48):
- all repros of rounds 1 and 2 recompiled twice: 0 errors, except `t21-table-gaps.tex` (the test's nonexistent `\lcnameCref`);
- `[no context]` lines appear only in files that deliberately test macro text, the `\input` fallback or dead-code settings;
- walker debug logs checked by hand;
- `vdump` checks as noted above;
- the five audit corpora compiled without errors;
- the 53k memory repro: 3.33M words, 13.6 s; the 20k document: 6.19 s.

**`tests/regression.tex` and `tests/run-tests.sh` were created here** (12:48). `regression.expected` was generated from that run's log, after its readings were checked by hand.

### 3.5 Review round 3 (findings 12:49–13:43; fixes 13:44–14:07)

The round-3 lenses hunted regressions in the round-2 code. The r3-user lens built three documents from the README alone:
- a ctexart handout with a vocabulary tabular, fancyhdr and hyperref;
- a beamer deck;
- an article with six `\input` chapters, a TOC and a long story.

It checked about 600 logged runs for machinery errors and found none in plain text. Fixes landed in three patches (parts A, B and C, 13:48–13:51) plus two small corrections.

**r3-walker lens**

- **R3-01 (high) Carrying the right pad past groups with `\aftergroup` broke amsmath `\text`, `align`, TikZ node text, `\discretionary` and `\leaders` inside a scope.** Errors were `Missing { inserted`, `Improper discretionary list` and TikZ "Giving up on this path".
  - Cause: the deferral re-inserted itself after every enclosing group, including groups owned by other code that must be followed by `{` or glue.
  - Fix: `\__xjyutping_if_defer:` defers only past group types 1 and 14 and pays inside other groups; TikZ node text sets `\l__xjyutping_nodefer_bool`. The check sits in `\__xjyutping_defer:` and `\__xjyutping_defer_test_aux:`, not in `\__xjyutping_boundary_aux:` as the finder suggested: the verifier showed that the boundary code always runs inside xeCJK's own class group (type 1), so a test there never fires.
  - Side effect noted by the verifier: the pad of a box's last character is now paid inside the box, so `\hbox{甲行乙}` is three full cells wide (64.5pt at width=2em, against 58.75pt before). This is also what fixed R3-06.
  - Verified: at the time, all r3 repro files recompiled with 0 errors, apart from agent helper fragments that are not complete documents. For this write-up the verifier's files `f0-math`, `f0-align`, `f0-disc`, `f0-leaders` and `f0-tikz` were recompiled against the 1.0.0 snapshot: 0 errors.
  - Process note: a first rerun claimed failures. They were stale logs, because macOS has no `timeout` command and the loop never recompiled anything.
- **R3-02 (high) `\GTS@expandtrue` (the R2-01 fix) made fragile titles fail inside a scope.** `\footnote` in `\section*`, theorem optional titles and description labels gave 2, 4 and 100 errors; with nameref alone there was an `input stack size` overflow.
  - Fix: removed. `\__xjyutping_unmark:N` is prefixed to `\label@hook` and replaces only the `\xjp@R@` marks in `\@currentlabelname` with their expansion.
  - Implementation note (**M3-1**): a capture inside `\c{…}` is not a regex group. The working approach extracts each distinct mark token and replaces it through `\u{…}`.
  - Verified: `f1-thm-in`, `f1-desc-in`, `f1-sec-in` and `f1l-a` compile with 0 errors against the snapshot; `regression.tex` (`\nameref`) still passes.
- **R3-03 (medium) An optional argument left open left stale walker state** (`\left[…\right]` in a footnote, `。[1]`, `\makebox[\width]`, `\section[\mbox{短}]{重}`).
  - Cause: the owner test came before the `]` test, and the state was a single slot.
  - Fix: `]` is tested first; an optional-argument stack (`\l__xjyutping_opt_seq`, `\__xjyutping_opt_begin:n`, `_end:`, `_pop:`, `_close:n`, `_top:`); still-open arguments are closed at group end and at paragraph end.
  - Verified: `f2-01`, `02`, `06` and `21` logs show the expected runs.
- **R3-04 (medium) `\\` in a tabular did not restore the annotation state after `\disablejyutping` in the last cell.** Duplicate of R3-17.
  - Fix: `\\`, `\tabularnewline`, `\cr` and `\crcr` get the action `row`, which restores the state only inside alignment environments (`\c__xjyutping_align_clist`, marked on the semantic stack when the `\begin` name is known).
  - **M3-2:** the first version compared a detokenised environment name with `\clist_if_in`, never matched, and row 2 stayed `[no context]`. Fixed by comparing the raw name.
  - Verified: `t11-tabular-row` and `r1-tabular-row-disable` give 銀行, 行路 and 校長 as words.
- **R3-05 (medium) The `\input` fallback missed verbatim-like commands and catcode changes** (`\lstinline`, `\Verb`, BVerbatim, alltt, `\DefineShortVerb`, `\obeylines`).
  - Fix: the widened `\c__xjyutping_unsafe_regex`.
  - Verified: all six `f4-*-in` files compile with 0 errors against the snapshot.
- **R3-06 (low) `\underline{字}` and other boxes ending in a character inside inline math lost the right pad.**
  - Cause: the decision ran in math mode, where `\__xjyutping_pad:` (R2-04) only zeroes.
  - Fix: R3-01's group-type test; the pad is now paid inside the `\hbox`.
  - Verified: see R3-20.
- **R3-07 (low) `\footnotemark[n]`: the optional argument was read as text and broke the word.**
  - Fix: `\footnotemark` declared `{-1}{}{t}`.
  - Verified: `f6-a` gives 銀ngan4:w行hong4:w.
- **R3-08 (low) A `%` comment mentioning `\verb` or `\makeatletter` sent a whole `\input` file to the fallback.**
  - Fix: the detection reads the file line by line (`\ior_str_map_inline:Nn`) and strips comments with `\c__xjyutping_comment_regex` before matching. The verifier found that `\file_get` with `\c_str_cctab` loses line ends, so this line-by-line read was needed.
  - Verified: `f7` gives word readings.

**r3-layout lens** (measured with `f0346-measure.tex` at width=2em, where plain `銀行，` is 47.25pt)

- **R3-09 (medium) A nested `\textbf`/`\emph` before another closing brace paid the pad before punctuation** (+5.75pt).
  - Fix: `\__xjyutping_if_group_end:` treats `\check@icr` as a group end, and `\__xjyutping_defer_ic_aux:` re-tests.
  - Verified: all ten nested variants measure 47.25pt (re-run against the snapshot for this write-up).
- **R3-10 (medium) Colour groups got no stretch glue,** so justified spacing was uneven around `\textcolor` and `{\color…}`.
  - Cause: the colour push/pop whatsits hide xeCJK's node, and the package's glue carries all of hsep's stretch.
  - Fix: `\__xjyutping_pad:` re-makes the node after a whatsit (`\lastnodetype` = 9), and `\__xjyutping_cell:nnn` adds the stretch glue when the last node is a whatsit after a paid pad (`\g__xjyutping_paid_bool`).
  - Verified: the bold and coloured lines both have glue set 0.65756.
- **R3-11 (medium) At a line break before —— or ……, the character sat flush with the margin and its ruby stuck out.**
  - Cause: the pad was dropped before long punctuation, where xeCJK allows a break.
  - Fix: `\__xjyutping_long_break:` (a kern pair around xeCJK's `\penalty0`).
  - Verified only partly in the session: the render at the tested width did not break before ——, but the lines shown kept their rubies inside the frame.
  - Re-checked for this write-up: the verifier's `f2-dash-eol.tex` compiled against the 1.0.0 snapshot at the widths it listed. At 4.4cm and 6.4cm a line now breaks before —— and ends `章 \kern 4.86244 \penalty 0`, so the pad stays at the line end (the negative kern after the penalty is discarded). At 4.8, 5.2 and 5.6cm the paragraph no longer breaks there. **Fixed.**
- **R3-12 (medium) Invisible commands between a character and ，。** (`\label`, `\index`, `\color`, `{}`, `\relax`, `\nobreak`) gave the punctuation a gap.
  - Fix: the walker's no-pad marker `\__xjyutping_nopad:` (section 2.4).
  - Verified: all six cases measure 47.25pt.
- **R3-13 (medium) `\underline` in a scope lost the right pad** (lopsided underline). Duplicate of R3-06/R3-20.
  - Verified: `ul` 47.25pt before ，; `ulz` (before 中) is plain + 3.33pt, which is xeCJK's usual math/CJK glue.
- **R3-14 (low) Long rubies before a line-final ，。、 crossed the right margin:** about 0.7pt at default settings, about 3pt at ratio=0.6.
  - **Not fixed.** See section 4.
- **R3-15 (low) `\uline{X}，`: the pad was paid inside the underline, so the comma stood off.**
  - Fix: covered by the no-pad marker, since the ulem commands are `t` class.
  - Verified: `uline` measures 47.25pt against the 1.0.0 snapshot, and a box dump of `銀\uline{行}，` shows the underlined box as left pad + glyph (15.75pt at width=2em) with the comma directly after it, so the pad is no longer paid inside the underline.
  - Note: the session's compaction summary (14:09) lists this as a remaining limit, and at 14:02 the main agent wrote that "the comma after an underlined word sits one pad away" after looking at the `f46-underline-uline` render. The measurements and box dump taken for this write-up show `\uline{X}，` fixed; the remark most likely described the render of a case other than the one measured here (unverified).
- **R3-16 (low) Tabular rows: row-to-row pitch 1.85pt tighter than within a `p` cell, and rubies 0.5pt under `\hline`.**
  - Fix: `\__xjyutping_raise_baselineskip:` rebuilds `\strutbox`.
  - Verified by render: rubies clear `\hline`, and the row pitch equals the in-cell pitch.

**r3-user lens**

- **R3-17 (medium)** Tabular row and `\disablejyutping`: see R3-04.
- **R3-18 (medium) beamer `\alert`, `\structure` and overlay forms (`\textbf<2>{}`, `\textcolor<2>{red}{}`) ended the run.**
  - Fix: `\alert` and `\structure` declared `t`. When beamer is loaded, `<…>` after a command is copied untouched, both in normal walking and in skip mode (`\l__xjyutping_skipclose_int` generalises the closing character).
  - Verified: `v-r3-beamer-alert` gives 銀行 and 校長 as words.
- **R3-19 (low) ctex font switches (`\heiti`, `\kaishu` …) and `\zihao` ended the run.**
  - Fix: declared `t` (`\zihao` with 1 argument, `\fontsize` with 2).
  - Verified: `v-r4-ctex-font-commands`.
- **R3-20 (low) `\underline` (which the README recommends) dropped its last cell's right pad.**
  - Fix: R3-01's group-type deferral.
  - Verified: `v-r2-underline-pad` gives PLAIN 123.05pt, ULINE 123.05pt, UNDERLINE 126.38pt (= plain + 3.33pt math glue, the same difference as outside a scope).
- **R3-21 (low) The pad was paid before 。 when `\label`, `\index`, `{}` or an `\href` link end came between character and punctuation.**
  - Fix: the no-pad marker. The verifier showed that the finder's "peek for `\label`" could not work, because macros are expanded before the boundary fires.
  - Verified: `v-r5` — all four variants 76.05pt.
- **R3-22 (low) In beamer, `\title{\xjyutping*{…}}` gave a "Token not allowed" warning and a `/Title` of `*廣東話會話`.**
  - Cause: beamer fills the PDF title before `\AtBeginDocument` code runs.
  - Fix: `\__xjyutping_pdfstring:` runs at once when `\pdfstringdefDisableCommands` exists, otherwise via `package/hyperref/after`.
  - Verified: `v-r6` has 0 warnings.
- **R3-23 (low) beamer measured the headline with rubies but printed it plain,** leaving a 5.5pt band.
  - Fix: the `cmd/beamer@typesetheadorfoot/before` hook turns on plain mode. `\beamer@calculateheadfoot` is not grouped, so it was not used.
  - Verified: `v-r7` `\headheight` 5.79pt, equal to the plain-title control.
- **R3-24 (low) In tabulars inside a scope, rubies sat about 0.5pt under `\hline`.**
  - Cause: the 0.05em clearance assumes the raised `\baselineskip`, but alignments set it to 0.
  - Fix: `\__xjyutping_clearance:` uses 0.05em only when `\baselineskip` ≥ the scope minimum, and 0.35em otherwise.
  - Verified by render.

**Implementation note (M3-3):** `\str_if_in:nn` has no predicate form, so `\__xjyutping_plain:n` uses the protected `\str_if_in:nnF`.

**Final verification** (13:56–14:07):
- all repros of the three rounds compile; the only failure is `t21-table-gaps` (a test error);
- helper fragments left by the agents do not compile on their own, as expected;
- the five audit corpora: 0 errors and 0 `[no context]` lines;
- the 53k memory repro: 3.34M words, **17.2 s**; the 20k document: **7.45 s** (up from 6.2 s; the main agent attributed this to the extra per-character checks of round 3);
- `run-tests.sh`: `readings: ok`;
- the manual was rebuilt: 5 pages, 0 errors, 0 overfull boxes.

### 3.6 Close-out (14:07–14:09)

- `tests/` was reduced to:
  - `regression.tex`, `regression.expected`, `run-tests.sh`, `render.sh`;
  - `layout-check.tex`, a copy of the round-2 `pad2.tex` without `[debug]`.

  About 35 review directories and scratch test files were moved to `scratchpad/review-artifacts/`.
- `xjyutping-doc.pdf` was rebuilt, and the README re-read for accuracy.
- The user received the delivery summary. It proposed LuaLaTeX support and superscript tone numbers as possible next steps; neither was started.

### 3.7 Performance and memory measurements (summary)

| Test | After first version | After round-1 rewrite | After per-paragraph analysis | After round 2 | 1.0.0 |
| --- | --- | --- | --- | --- | --- |
| `long.tex` (19 926 characters, 52 pages) | 4.7 s | 5.7 s | — | 6.2 s | 7.45 s |
| `repro-memory.tex` (53 060 characters, one scope, 140 pages) | fails: main memory > 5M | 4.88M words, 12.2 s | 3.32M words, 12.6 s | 3.33M words, 13.6 s | 3.34M words, 17.2 s |

- Package loaded with no text: about 2.47–2.48M words.
- Largest single scope: 159k characters compiles (4.87M words); 212k fails.
- One paragraph: about 15–18k characters.

### 3.8 After 1.0.0

At 14:19 the user asked for the `fancy` option, this changelog under
Semantic Versioning, and the split into `xjyutping-tex/` and `xjyutping-py/`.
That work is described in section 6.

---

## 4. Known limitations and open issues at 1.0.0

This section gives the state at 1.0.0, with notes on what 1.1.0 resolved; section 7.7 gives the state after 1.2.0.

**Documented in the README** (intended behaviour):
1. **Engine and body reading.**
   - XeLaTeX only; the package stops with a critical error on other engines. LuaLaTeX is not supported.
   - The environment body and the argument of `\xjyutping*` are read as a macro argument. `\verb` and verbatim environments cannot go inside, and `%` in `\url`/`\href` must be written `\%`.
2. **`\input` and other text without word context.**
   - `\input{file}` inside a scope is read with the body's restrictions. A file using `\endinput`, verbatim-like commands, `\makeatletter`, catcode changes or `\obeylines` is `\input` normally, without word context.
   - Macro text, `\include`d files and `\maketitle` are annotated character by character (`[no context]` in the log).
3. **`\setjyutping` in dead code.** Inside a scope, a `\setjyutping` in dead code (`\iffalse`, an unused `\newcommand`) still affects the segmentation of the text after it in the same scope.
4. **Unbraced arguments.** Commands outside the table need their Chinese argument in braces (`\textbf{行}`). (The round-2 recheck of R1-44 also noted a silent side effect not in the README: with `AutoFakeBold` on the CJK font, an unbraced `\textbf 行` inside `\xjyutping*` loses its bold, while the braced form stays bold.)
5. **TOC.** The TOC is annotated only if `\tableofcontents` is itself inside a scope, or if a title contains an explicit `\xjyutping`.
6. **beamer `\frametitle`.** Inside a scope it stays plain; use `\frametitle{\xjyutping*{…}}`.
7. **xeCJKfntef commands** (`\CJKunderline`, `\CJKunderdot`, `\CJKsout` …) do not keep the cell grid, and `\CJKunderdot` dots are off-centre (R2-36). Use `\underline` or `\uline`.
8. **Capacity.** One paragraph holds about 15 000 characters; a brace group spanning many paragraphs is analysed in one piece; one scope holds "well over 100 000" characters (README), measured at between 159k (compiles) and 212k (fails) with default `main_memory`.
9. **Missing data.** Characters not in the data get a cell without Jyutping.
10. **Variant folding** applies to word lookup only. `\setjyutping{為}{…}` does not change 爲 (R1-25, rejected as a defect).

**Not fixed and not in the README:**

11. **R3-14.** Long rubies before a line-final ，。、 can reach into the right margin: about 0.7pt with default settings, about 3pt at ratio=0.6. The verifier's corrected fix was not implemented: a kern pair after xeCJK's trailing trim rule, only at a line end.
12. **R2-14.** Footnote marks, `\textsuperscript` and `\textsubscript` right after an annotated character sit one pad away from it (4.86pt at 10pt in the repro, where `width=auto` gives a 0.49em pad), and punctuation after the mark moves with it. This was confirmed on the 1.0.0 snapshot with the box dump of `fnmark.tex`. The verifier's `fnmark2.tex`, recompiled against the snapshot, also shows that a character right after a footnote mark (`攞錢\footnote{…}大`, `攞錢\footnotemark 大`) follows it with no glue at all, so there is no line-break point and no stretch there.
    - Cause: `\__xjyutping_boundary_aux:` pays the pad because the next token after expansion is not a group end.
    - Suggested fix (from the round-2 verifier, not implemented): while a scope is enabled, wrap `\footnote`, `\footnotemark`, `\textsuperscript` and `\textsubscript` so that the pad is paid after the mark, or dropped if punctuation follows. The walker must still recognise `\footnote`.
13. **Line pitch after deep lines in minipage, `\parbox` and `p` cells** (a side effect of R3-24's clearance rule, on top of R2-29's 0pt `\lineskiplimit` and R2-32's `para/end` re-raise). Inside such a box within a scope, the cells are built with the 0.35em clearance (the reset `\baselineskip` is raised only at `para/end`, so the R3-24 test sees 12pt), so a line deeper than about 0.24em (for example one containing `\underline`) is followed by `\lineskip` instead of `\baselineskip`, and that one gap is about 2pt larger: 19.57pt against 21.6pt in `r-parbox.tex` at 1.0.0. In ordinary scope text the threshold is about 0.55em, so `\underline` does not trigger it and only unusually deep material (display-style math) does, as in plain LaTeX. This is the trade-off for keeping framed and coloured boxes from overlapping the line above and for keeping rubies clear of `\hline` in `p` cells (the R3-24 verifier chose the `\baselineskip` test precisely so that `p` cells get 0.35em); the round-2 verifier foresaw the `\lineskip` fallback, and no review reported it as a defect.
14. **Ambiguous readings.** Readings that need context beyond the word list are left to user overrides: 為 wai4/wai6 outside the curated 為-phrases, 同行 hong4/hang4, 當佢係 dong3, 背得 bui6, 彈得 taan4, 種花 zung3, 假 gaa3 in 請假-type phrases, 長得 zoeng2, 散晒 saan3. The `multiple=` option and the debug log exist to find them.
    - **Seen in round 3 but never reported as findings** (the r3-user lens listed them as "documented algorithm or data" and moved on). Re-checked for this write-up against the 1.0.0 snapshot; all five are still wrong: 我屋企住 splits 屋|企住 (企 kei5); 電車行得 gives 車行 ce1 hong2; 都會話 gives 會話 wui6 waa2; 生詞表 gives 生 sang1 while 生詞 alone is saang1; 慢慢行 gives 行 hang4. Each is a candidate for a `CURATED_WORDS` entry or guard word. **1.1.0:** 慢慢行, 屋企住, 都會話 and 生詞表 are fixed; 車行 is left, because 行得 as a word would break 銀行得… (section 6.4, F-5).
15. **Segmentation tie-break.** On a tie the longer final word wins, so a demonstrative or numeral followed by a classifier can be split wrongly. 呢|張床 and 一|間房 were examples before the round-1 data fixes. This is handled case by case with word entries, guard words and the run-final reading of 呢, not in general.
16. **Test file error.** `t21-table-gaps.tex` (review artefact, not in `tests/`) uses the nonexistent `\lcnameCref`; the error is in the test, not the package. The R2-23 fix nevertheless put `\lcnameCref` into the command table next to the real `\lcnamecref`; the extra entry is harmless.
17. **`\pdfbookmark` anchor names are annotated inside a scope.** `\pdfbookmark` is not in the command table, so its name argument is walked as text. Recompiling the round-2 recheck file `recheck-robust-tokens/chk-keys.tex` against the 1.0.0 snapshot gives 0 errors and 0 warnings, but the named destination is written as `\xjyutping@mark {wmuk6}目\xjyutping@mark {wbiu1}標.1`, while `\hyperlink{目標}` in the same scope points to `目標`: the link is silently broken. Suggested fix: declare `\pdfbookmark`, `\currentpdfbookmark`, `\subpdfbookmark` and `\belowpdfbookmark` as `{2}{}{b}`; both arguments are PDF strings or keys, never typeset text, and the optional level is copied anyway. **Fixed in 1.1.0 this way** (section 6.4, F-4).

---

## 5. How to test, and how to regenerate the data

This section describes the state at 1.2.0; notes in brackets say what was
different before.

### 5.1 Tests (in `tests/`)

Requirements: XeLaTeX with xeCJK, LuaLaTeX with LuaTeX-ja and ctex (TeX Live
2026 has all of them), the font **Songti TC** (macOS), and Ghostscript
(`gs`) for rendering. The scripts put the package directory on both search
paths with `TEXINPUTS=..: LUAINPUTS=..:` (LuaTeX finds `xjyutping.lua`
through `LUAINPUTS`, not `TEXINPUTS`), so they must be run from `tests/` or
called by their path.

- **`./run-tests.sh`** is the regression check. For each of four jobs
  (XeLaTeX and LuaLaTeX, each with and without the `fancy` option) it:
  1. compiles `regression.tex` twice (the document uses hyperref,
     `\section`/`\nameref`, a footnote, `\textbf`/`\color` inside words,
     variant spellings, 呢 final and non-final, `\xjyutping` and a mid-text
     `\setjyutping`; a scope opened by a user environment, with `center`, a
     table made by a macro and `$x\mbox{…}$` in it; and a `linebreak` scope.
     It loads xeCJK under XeLaTeX and ctex under LuaLaTeX);
  2. fails if the log has any `^!` error;
  3. extracts the `xjyutping>` debug lines into `<job>.readings` and diffs
     them against `regression.expected` (26 lines).

  `<job>: readings ok` four times and exit status 0 mean pass. (At 1.0.0 the
  script ran XeLaTeX once and wrote `regression.out`; 1.1.0 added the
  `fancy` job; 1.2.0 the LuaLaTeX jobs.)
- **When a reading changes on purpose** (a data fix), check the diff by hand,
  then run `grep -a '^xjyutping>' regression-xelatex.log > regression.expected`
  and rerun. Do the same for the Python package: compile its
  `tests/parity.tex` (with `TEXINPUTS`/`LUAINPUTS` pointing here and
  `max_print_line=10000`) and copy the `xjyutping>` lines to its
  `tests/parity_expected.txt`.
- **`./render.sh file.tex [engine] [dpi]`** compiles a file that sits in
  `tests/` with `xelatex` (default) or `lualatex` and renders every page to
  `file-N.png` (default 200 dpi). For files elsewhere, compile with absolute
  `TEXINPUTS=<this repository>: LUAINPUTS=<this repository>:` instead.
- **`layout-check.tex`** is the visual layout check. It covers:
  - `\textbf`, `\emph` and `{{…}}` before ，。：;
  - group-final characters before characters and Latin text;
  - brackets around coloured and manual characters;
  - a source line break before punctuation;
  - `\fbox`/`\colorbox`;
  - a long chain of manual `\xjyutping` that must still break lines.
- **`fancy-check.tex`** is the visual check of the tone marks: sizes,
  sans-serif italic in colour, `width=natural` and a fixed width, a large
  ratio, inline `\xjyutping*`, `multiple`, a syllable without a tone, and
  `fancy=false`.
- **Debugging aids:**
  - `\usepackage[debug]{xjyutping}` (or `\xjyutpingsetup{debug=true}`) logs
    segmentation; the log is the same under both engines;
  - `multiple=\color{red}` highlights guessed polyphones;
  - `\showbox` or a `\vbox` dump shows the cell structure. Under XeLaTeX:
    `\hbox{} \kern<pad> <overlap box> <char> \kern<pad> \hbox{}`, and
    interline glue. Under LuaLaTeX each cell is one hbox,
    `[\kern<pad> <overlap box> <char> \kern<pad>]`, between LuaTeX-ja's glue.
- **Checks to repeat after any change to padding, deferral or the Lua
  wrapping** (these regressed before):
  - the 18-call chain of `\xjyutping` in `layout-check.tex` must break lines
    (no overfull boxes);
  - `銀\textbf{行}，`, `銀{\textbf{行}}，`, `銀行\label{x}，` and
    `銀\uline{行}，` must all be as wide as `銀行，`;
  - `$\text{面積}$`, `align` with `\text`, and TikZ node text inside a scope
    must compile;
  - `\nameref` to a section inside a scope must compile on the second run;
  - a scope opened by a user environment must end with it, and the
    `\author` of `\maketitle` and `$\text{\foo}$` in a scope must be
    annotated under both engines (the debug logs must match);
  - `\footnote` inside `\section*` in a scope must compile;
  - the XeLaTeX renders of `regression.tex`, `layout-check.tex` and
    `fancy-check.tex` should stay identical when only the LuaLaTeX path is
    changed (compare the PNGs with `cmp`).

### 5.2 Regenerating the data

From anywhere:

```bash
python3 tools/build-data.py [--sources DIR] [--py-data DIR]
```

By default it reads the sources from the directory that contains this
repository and, if xjyutping-py sits there too, also rewrites
`xjyutping-py/src/xjyutping/data/*.tsv`. `tools/fetch-sources.sh [DIR]`
fetches the sources at the pinned commits. It needs:

- `jyutping-table-master/list.tsv`;
- `rime-cantonese/jyut6ping3.chars.dict.yaml` and
  `rime-cantonese/jyut6ping3.words.dict.yaml`;
- `opencc/HKVariants.txt` and `opencc/TWVariants.txt`;
- `jyut-dict/src/dictionaries/cedict/data/CC-CANTO.txt` and `READINGS.txt`
  (since 1.2.0);
- the book files of `cantonese-books-data/` listed in `BOOKS` (since 1.2.0).

It prints statistics to stderr. At 1.2.0:

```
chars 30089 (polyphonic 4407), variants 76, words 103579 (+133 aliases, 0 alias clashes, 1229 words with several readings)
chars added from cantonese-books-data: 640 (...)
words added from jyut-dict: 2291 (CC-CEDICT readings 1927, CC-Canto 364); not added: ...
```

(At 1.0.0 the first line read `chars 29449 (polyphonic 4349), variants 76,
words 101275 (+68 aliases, ...)`; at 1.1.0 `words 101277`.) A build takes
about 3 seconds, and it is deterministic.

- **Permanent reading fixes** go into the tables at the top of the script:
  `CURATED_DEFAULTS`, `CURATED_FINALS`, `CURATED_VARIANTS`, `CURATED_WORDS`;
  words of CC-Canto or the CC-CEDICT readings that must not be added go into
  `EXCLUDED_WORDS`; `BOOKS` lists the book files, most authoritative first.
- **Test a candidate first.** Before adding a word or changing a default, try
  it with `\setjyutping` in a scratch file against other common contexts.
  Because the longer final word wins ties, a new entry can capture
  neighbouring characters; add guard words where needed (the 平啲 case
  needed 16). The build applies the same reasoning to the added word lists
  automatically (section 7.4).
- **Default changes are riskier than word entries.** Review verifiers
  rejected several default changes: they fix one sentence and break common
  standalone uses.
- **After regenerating**, run `tests/run-tests.sh` and xjyutping-py's tests,
  and update the expected files only for intended changes.
- **Upstream updates.** If a source is updated (change the pinned commit in
  `tools/fetch-sources.sh`), expect changes in defaults, flags and words.
  Compare the statistics and the regression output, and review the new words
  that the build adds.

---

### Appendix: counts

| Round | Bug findings | Reading findings | Other |
| --- | --- | --- | --- |
| Initial development | 6 package bugs (I-1…I-6) and 4 data-builder issues (D-1…D-4) | — | — |
| Round 1 | 46 (45 accepted, 1 rejected), about 32 distinct after duplicates | 82 (74 accepted, 8 rejected), from 110 wrong characters over 3 corpora | 6 issues found by the main agent while fixing (M1-0 builder KeyError, M1-1 `#` in body, M1-2 save stack, M1-3 main memory, M1-4 split strips braces, M1-5 missing 行長) |
| Round 2 | 39 new (16 recheck-lens, 23 new-lens; none rejected), about 29 distinct | 14 | 46 recheck statuses for round 1: 34 fixed, 9 partly, 2 documented, 1 not applicable; 1 main-agent regression (M2-1) |
| Round 3 | 24 (none rejected), 20 distinct | — | 3 main-agent implementation issues (M3-1…M3-3); 1 test-harness issue (no `timeout` on macOS) |

At 1.0.0:
- **not fixed:** R2-14 (confirmed still present), R2-36 (documented), R2-38 (documented), R2-39 (documented), R3-14, and the `\pdfbookmark` gap noted in the R1-14 recheck (confirmed still present; section 4, item 17).
- **Re-measured for this write-up against the 1.0.0 snapshot, all confirmed fixed:** R1-30, R2-24, R2-29, R3-11, R3-15, and the 划算/划船 reading check. The round-3 repros cited as verification (`f0-*`, `f1-*-in`, `f1l-a`, `f2-*`, `f4-*-in`, `f6-a`, `f7`, `f0346-measure`, `v-r1` … `v-r7`) and `tests/regression.tex` were also recompiled against the snapshot: 0 errors and the stated widths and readings.
- **R2-32:** minipage pitch fixed; the remaining deep-line effect (minipage, `\parbox` and `p` cells only) is described in section 4, item 13.
- **Wrong readings seen in round 3 but never reported**, still present at 1.0.0: section 4, item 14.

---

## 6. Version 1.1.0 of the LaTeX package and 1.0.0 of the Python port (2026-09-28, 14:19–)

### 6.1 The request

The user added two reference repositories:

- `visual-jyutping-master/`, the Visual Jyutping page by Vincent Tam (MIT),
  "inspired by Visual Cantonese Fonts";
- `xpinyin-master/`, the Python xpinyin package by lxneng.

They asked for four things:

1. a `fancy` package option, `\usepackage[fancy]{xjyutping}`, that gives
   the Jyutping Visual Jyutping's visual tone indicators, with the automatic
   spacing adapted to it;
2. this `CHANGELOG.md`, usable as a handover file, recording how the project
   was created and every change, bug and fix;
3. versions in the changelog and READMEs that comply with Semantic
   Versioning;
4. a split of the project into `xjyutping-tex/` (the LaTeX package) and
   `xjyutping-py/` (a Python version like xpinyin).

### 6.2 How the work was organised

- **Main agent:** moved the LaTeX files into `xjyutping-tex/` and changed
  the output paths in `tools/build-data.py`, then froze a copy of the 1.0.0
  `.sty` and `.def` files (the "snapshot"). It then implemented `fancy`
  itself.
- **Background workflow**, in parallel (7 agents):
  - one agent built the Python port against the snapshot;
  - three independent reviewers checked the port through different lenses
    (reading parity with TeX; API, packaging and docs; edge cases and tone
    styles);
  - a fixer reproduced each review finding before fixing it;
  - a historian wrote Part II sections 1–5 from the session transcript and
    the review artefacts;
  - a fact-checker verified every claim in that history against the
    transcript, the artefacts and the code, and recompiled about 40 repro
    files against the snapshot.

### 6.3 The `fancy` option: design

**What Visual Jyutping does.** `assets/js/script.js` replaces a syllable's
final tone digit with a spacing modifier letter plus a superscript or
subscript digit:

| Tone | Web map (`webToneMap`) | Discord map (`dcToneMap`) |
| --- | --- | --- |
| 1 | ˉ¹ | ˉ¹ |
| 2 | ˊ² | ⸍² |
| 3 | ˗₃ | -₃ |
| 4 | ˎ₄ | ⸜₄ |
| 5 | ˏ₅ | ⸝₅ |
| 6 | ˍ₆ | ˍ₆ |

**Drawn strokes, not glyphs.** Those code points (U+02C9, U+02CA, U+02D7,
U+02CE, U+02CF, U+02CD and the sub/superscript digits) are missing from
many fonts, including the Latin Modern default of `font=\normalfont`, and
the package lets users choose any `font`. So the TeX package draws the
stroke instead:

- `\special{pdf:content …}` inside a box of fixed width. xdvipdfmx, XeTeX's
  only driver, wraps `pdf:content` in `q 1 0 0 1 x y cm … Q`, which puts
  the origin at the current point. This was checked in an uncompressed PDF
  (`xdvipdfmx -z 0`).
- The stroke takes the colour set by xcolor's colour stack (checked with
  red text), and it follows `\rotatebox`.
- The small tone number is ordinary text in the ruby font at 0.7 of its
  size, selected once through NFSS and then called by its font identifier.

**Shapes.**

- *First attempt:* Chao tone contours (55, 35, 33, 21, 13, 22). At 700 dpi
  the level strokes of tones 3 and 6 were only 0.14em apart at ruby size and
  could not be told apart.
- *Final:* the geometry of the Visual Jyutping symbols. Levels are at pitch
  5, 3 and 1 (ˉ, ˗, ˍ); ˊ rises 3→5, ˎ falls 3→1, ˏ rises 1→3. Pitch 1 is
  the baseline and pitch 5 the height of the digit 6. The stroke is 0.4em
  long and 0.08em thick with round caps, after a 0.07em gap, in a box 0.51em
  plus the stroke width wide.
- Raised numbers for tones 1–2 are lifted by 0.3 × digit height + 0.12em;
  lowered numbers for 3–6 by −0.12em.

**Code in `xjyutping.sty`:**

- `\__xjyutping_syllable:n` (called by `\__xjyutping_ruby:nn`) splits off a
  final tone digit 1–6. A syllable without one is printed unchanged.
- `\__xjyutping_tones:` and `\__xjyutping_tones_build:` build the six marks
  once per font, keyed by `\fontname\font`:
  - `\xjp@tone@<font>@<tone>` holds the box and the number;
  - `\xjp@tones@<font>` holds the largest height and depth among them.
- The drawing itself: `\__xjyutping_contour:n`, `\__xjyutping_stroke:nn`,
  `\__xjyutping_pitch:n`, `\__xjyutping_bp:n`.

**Spacing.**

- Horizontal: `\__xjyutping_measure:n` builds the same ruby as the cell, so
  `width=auto` measures the fancy form.
- Vertical: `\__xjyutping_strut:` includes the marks' height and depth, so
  every fancy ruby has the same box and lines stay evenly spaced.
- Lift: `\g__xjyutping_lift_dim` is the amount the marks reach below the
  letters' descenders. It is 0 for Latin Modern, since −0.12em is less than
  the depth of g. `\__xjyutping_vsep:` (vsep + lift) replaces the raw `vsep`
  in the cell's `\box_move_up:nn`, in `\__xjyutping_clearance:` and in
  `\__xjyutping_baselineskip:`.

**Measurements.**

| Test | Plain | `fancy` |
| --- | --- | --- |
| 29 118-character document | 8.69 s, 58 pages | 11.01 s, 65 pages (wider cells) |
| One 12 000-character paragraph, first version of the marks | 4.06M words | 4.84M words (+65 words per character) |
| One 12 000-character paragraph, final version | 4.06M words | 4.66M words (+50 words per character) |
| One 15 000-character paragraph | 4.45M words | exceeds main memory |

The single-paragraph limit with `fancy` is documented as about 13 000
characters.

**Checks.**

- `tests/run-tests.sh`: both jobs give the same readings as
  `regression.expected`.
- `tests/fancy-check.tex`, rendered at 200 and 600 dpi:
  - it covers `\small`/`\Large` in a scope, `font=\sffamily` with italic
    blue `format` and `width=natural`, `ratio=0.6, vsep=1.3em, width=2.2em`,
    inline `\xjyutping*` in a normal paragraph, `multiple=\color{red}`, a
    syllable without a tone (`\xjyutping{唔}{m}`), and `fancy=false` inside
    a fancy document;
  - no ruby touches the line above or the character below, and there are
    0 overfull or underfull boxes.
- The manual (5 pages) compiles with 0 errors and 0 overfull boxes.

### 6.4 Bugs found and fixed during this work

**TeX package:**

- **F-1. The fancy marks used too much main memory.**
  - Symptom: a 15 000-character paragraph, which compiles without `fancy`,
    exceeded main memory; at 12 000 characters `fancy` used 4.84M words
    against 4.06M.
  - Cause: the text of every `\special` is stored in its whatsit node. The
    first version wrote 5-decimal bp values plus its own `q … Q`.
  - Fix: `\__xjyutping_bp:n` rounds to 0.01bp, and the redundant `q`/`Q`
    was dropped (`pdf:content` adds them itself). This brought it down to
    +50 words per character, and the limit is documented.
- **F-2. Tones 3 and 6 were indistinguishable** with Chao contours at ruby
  size. The strokes were redesigned on the Visual Jyutping symbols
  (section 6.3).
- **F-3. `run-tests.sh` wrote its extracted readings to `regression.out`,**
  which is also hyperref's bookmark file for `regression.tex`. It now writes
  `<job>.readings`.
- **F-4 (open issue 17 at 1.0.0). `\pdfbookmark` names were annotated.**
  - Fix: `\pdfbookmark`, `\currentpdfbookmark`, `\subpdfbookmark` and
    `\belowpdfbookmark` are declared `{2}{}{b}`.
  - Verified: the round-2 file `chk-keys.tex` now writes the destination
    `目標.1` (hex `e79baee6a8992e31` in the uncompressed PDF) with no
    marks, and 書簽 and 目標 no longer appear in the debug log. (hyperref
    itself names the anchor `<name>.<level>`, so `\hyperlink{目標}` in that
    test never matched, with or without the package.)
- **F-5 (open issue 14 at 1.0.0). Four readings corrected** through
  `CURATED_WORDS`: 慢慢行, 屋企住, 都會話, 生詞表.
  - 生詞表 also turned out to be a rime entry with 生 sang1.
  - 車行 in 電車行得 was left alone. Adding the word 行得 would turn
    銀行得… into 銀|行得 through the tie-break, and 車行 "car dealer" is a
    real word.
  - The four phrases were appended to the Python parity corpus, and
    `parity_expected.txt` was regenerated from the 1.1.0 TeX log. The
    earlier 106 lines were unchanged, plus 3 new ones.

**Python port** (found by the three review lenses, then reproduced and fixed
by the fixer; the author's own 35 tests had passed):

- **P-1. CR line ends** (reported by all three lenses). A lone CR was not
  counted as a line end, so `'\r\r'`, a blank line to TeX, did not end a
  run. That changed segmentation and the run-final 呢.
  - Fix: `_runs` counts `\n`, and `\r` not followed by `\n`.
  - Test: `test_runs_cr_line_ends`, with expected values from a TeX log.
- **P-2. The sdist lacked the parity files,** so its own test suite failed
  (2 tests, FileNotFoundError). Fix: `MANIFEST.in` includes `tests/*.txt`
  and `*.tex`.
- **P-3. The README's editable install failed** with the machine's pip
  21.2.4, since editable installs need pip 21.3 or later. The README now
  upgrades pip first.
- **P-4. `license = {text = "MIT"}` in `pyproject.toml`** triggered a
  setuptools deprecation that becomes a build error after 2027-02-18.
  Removed; `License-File` and the classifier remain.
- **P-5. The README's run-final example showed a word-list entry** instead
  of the run-final rule. It was replaced with 呢張床好平，好麻煩呢？
- **P-6. `set_jyutping` on a character missing from the data did nothing.**
  TeX reads such a character without context and with type `u`. It is now
  its own run of type `u`; test `test_set_jyutping_char_not_in_data`.
- **P-7. `set_jyutping` rejected whitespace** that `\setjyutping` ignores.
  It now strips spaces, tabs, CR and LF; test
  `test_set_jyutping_ignores_spaces`.

**Process notes:**

- The permission check stopped the Python agent from running
  `tools/build-data.py` in place, because it rewrites
  `xjyutping-tex/*.def`, which another agent was editing. The agent ran it on
  a scratch copy and confirmed byte-identical `.def` files. The in-place
  run happened later, for 1.1.0.
- The history agents found three things at 1.0.0 that the earlier summary
  had wrong:
  - `\uline{X}，` (R3-15) is fixed, not a remaining limit;
  - the I-3 error was "Missing number", not "Missing }";
  - the 地→哋 alias count is 82, not 103.

### 6.5 The Python port: how it maps to the TeX package

| TeX (`xjyutping.sty`) | Python (`src/xjyutping/__init__.py`) |
| --- | --- |
| a character is Chinese iff `\xjp@c@<char>` exists | `c in self._chars` |
| runs: spaces and single line breaks between characters continue a run; `\par`/blank line ends it | `_runs` (ASCII space, tab, CR, LF; two line ends end the run; U+3000 ends it) |
| `\__xjyutping_flush:` (DP, 100000 per segment + 1 per single, `<=` so longer final word wins; bound `\xjp@e@` raw or canonical) | `_segment_run` (same costs and comparison; bound `_longest`, computed from `words.tsv` at load) |
| `\__xjyutping_emit:nn` word: raw key, else canonical; type `u` if `\xjp@uw@` | same, `self._user_words` |
| `\__xjyutping_lookup:nn` single: user, then `\xjp@f@` at run end, then default; type m/s from `\xjp@m@` | same (`_user_chars`, `_finals`, polyphone flag in `chars.tsv`) |
| `\__xjyutping_set:nnn` / `\__xjyutping_set_word:nn` | `set_jyutping` (raw and canonical keys, longest bound) |
| `debug` log `銀ngan4:w…` | `segment()` |

Differences by design:

- Python has no markup, so it has nothing like the command table, footnote
  runs, `\xjyutping` manual readings or plain mode. The parity corpus
  therefore has TeX's commands resolved into the runs TeX makes of them.
- `chars.tsv` lists the other readings of every character (for
  `get_jyutpings`), not only of flagged polyphones.

### 6.6 Open after this work

Part II, section 4 still applies, except items 14 (partly) and 17, which
1.1.0 resolved. Specific to `fancy`:

- One paragraph holds about 13 000 characters, against about 15 000
  without it.
- The strokes are graphics. Copying text out of the PDF gives the letters
  and the tone number without the stroke.
- A `format` that changes the font size or shape gets marks built for that
  font, but the strut and lift are computed from the base ruby font. This
  matches how `format` already interacts with the strut.

---

## 7. Version 1.2.0: LuaLaTeX, more vocabulary, `linebreak`, two repositories (2026-09-28, from 15:59)

### 7.1 The request

After 1.1.0 the user asked for four things:

1. more vocabulary from two repositories: 石見田's
   [cantonese-books-data](https://github.com/jyutnet/cantonese-books-data)
   (found through [jyut.net/about](https://jyut.net/about)), and
   [jyut-dict](https://github.com/aaronhktan/jyut-dict), from its two
   subdirectories under `src`: `dictionaries` and `jyut-dict`;
2. LuaLaTeX support, and then all documentation updated;
3. attributions in a separate section of the README of both packages:
   - the LaTeX package names the authors of the LaTeX xpinyin (Qing Lee) as
     its inspiration;
   - the Python package names the author of the Python xpinyin (lxneng, Eric
     Lo) as its inspiration;
   - both thank Visual Jyutping and the Visual Cantonese Fonts for inspiring
     `fancy`, and the authors of every other source, OpenCC included;
4. (said in passing) the user had made separate git repositories of the two
   folders, [Beyond3345/xjyutping-tex](https://github.com/Beyond3345/xjyutping-tex)
   and [Beyond3345/xjyutping-py](https://github.com/Beyond3345/xjyutping-py).

### 7.2 Two repositories

The workspace root (with the old single `CHANGELOG.md`, the root
`README.md` and `tools/`) belonged to neither repository, and the READMEs
linked to `../CHANGELOG.md` and `../xjyutping-py`, which break on GitHub.
Changes:

- `tools/build-data.py` moved into this repository. `REPO` is the
  repository and `ROOT` the directory with the sources (default: the parent
  of the repository; `--sources DIR` to change it). The Python data goes to
  `../xjyutping-py/src/xjyutping/data` if that package is there, or to
  `--py-data DIR`; otherwise it is skipped. The output was checked to be
  byte-identical after the move.
- The changelog was split. This file keeps the whole history. xjyutping-py
  has its own `CHANGELOG.md`, with its releases and handover notes for the
  Python side.
- Links now point into the repository or to the other repository on GitHub.
- Both repositories got a `.gitignore`.
  - The user's interim commit had picked up `.DS_Store` and
    `tools/__pycache__/build-data.cpython-313.pyc`. The `.pyc` came from an
    agent that imported the script with importlib, and was deleted in a
    later commit.
  - `.DS_Store` is still tracked; `git rm --cached .DS_Store` would remove
    it.

### 7.3 The LuaLaTeX backend

**Why not the XeLaTeX way.** Under XeLaTeX, xeCJK calls `\CJKsymbol` for
every Chinese character, and the package builds the cell there. LuaTeX-ja
has no such hook: characters become glyph nodes, and LuaTeX-ja inserts its
glue (`kanjiskip`, JFM glue) and line-break penalties in Lua callbacks
(`ltj.main` in `pre_linebreak_filter` and `hpack_filter`). xpinyin, the
model of this package, supports XeTeX and pdfTeX only, so there was no
precedent to follow.

**Design:** the TeX side prepares, and Lua assembles after LuaTeX-ja.

- The preprocessor is unchanged: both engines get the same marks
  `\xjp@R@<type><reading>` → `\xjyutping@mark{<type><reading>}` right before
  each character.
- Under LuaLaTeX `\xjyutping@mark` ends with `\__xjyutping_mark_next:`. It
  peeks at the next token and, if it is a character (catcode 11 or 12), runs
  `\__xjyutping_lua_mark:N`, which does the following:
  1. `\__xjyutping_lua_build:nnnN` measures the character, builds the ruby
     with the shared `\__xjyutping_ruby:nn` (font cache, strut, `format`,
     `multiple`, `fancy`), and computes the pad exactly as the XeLaTeX cell
     does;
  2. it puts the ruby, with `\__xjyutping_clearance:` and raised by
     `\__xjyutping_vsep:`, into a zero-width overlay box as wide as the
     character;
  3. it calls `\xjyutping@lua@store <box> <pad> <stretch>`, a Lua function
     defined with `token.set_lua`, which copies the box into a table and sets
     the attribute `xjyutping@cell` to the new id;
  4. it typesets the character inside a group, so only its glyph carries the
     id.
- `\__xjyutping_enable:` and `\__xjyutping_disable:` set and unset a second
  attribute, `xjyutping@scope` (`\xjyutping@lua@on`, `\xjyutping@lua@off`),
  instead of replacing xeCJK's hooks. Internal boxes (the character measure,
  the ruby, the overlay) switch it off locally (`\__xjyutping_cjk_inactive:`).
- `xjyutping.lua` registers a callback in `pre_linebreak_filter` and
  `hpack_filter`, after LuaTeX-ja's `ltj.main`. For each glyph whose cell id
  is in the table, `wrap` does this:
  - it replaces the glyph (or the one-glyph box LuaTeX-ja packed it into)
    with a cell hbox: `[\kern pad][overlay][glyph][\kern pad]`, tagged -1;
  - it leaves out the right pad when the next visible object is FullRight
    punctuation other than a closing bracket or quote, as under XeLaTeX;
  - before a long mark (—— ……) it would move the line break into a
    discretionary whose pre-break text is the pad. LuaTeX-ja (with ctex's
    JFM) never allows a break there, so this never fires in practice;
  - it turns the LuaTeX-ja glue after a cell (`ltj@icflag` 68, KANJI_SKIP)
    into the stretch of `hsep`, with no natural width and no shrink, which is
    what `\CJKglue` becomes under XeLaTeX.
- **Characters without a mark** typeset while annotation is on (text from
  macros, `\maketitle`, the `\input` fallback) carry the scope attribute
  only. The callback runs TeX with `tex.runtoks`, calling
  `\xjyutping@lua@nocontext{<char>}{<size>}`. That does the lookup, writes
  the `[no context]` debug line and builds the cell data. It is tested inside
  both callbacks; the options are those in force when the paragraph is
  finished, and the size is the glyph's.
- **The walker's punctuation tests** (`\__xjyutping_if_class:nn`) use
  xeCJK's classes under XeLaTeX and, under LuaLaTeX, `xjyutping.class`,
  whose lists are copied from xeCJK: FullLeft = OP + PR, FullRight = CL + NS
  + EX + IS + PO + hyphens.
- **The fancy strokes** go through `\__xjyutping_literal:n`: xdvipdfmx's
  `pdf:content` under XeLaTeX (it adds `q … Q` itself), and
  `\pdfextension literal {q … Q}` under LuaLaTeX. LuaTeX-ja refuses DVI
  output, so there is no DVI path.
- The package loads LuaTeX-ja if it is missing (as it loads xeCJK under
  XeLaTeX), then `require('xjyutping')`.

**Verification:**

- `tests/run-tests.sh`: all four jobs give the same readings.
- A stress document (`\maketitle`, `\section`, a footnote, macro text,
  `\disablejyutping`, a tabular with `p` and `c` cells and `\fbox`, a
  minipage, a TikZ node, —— and …… in a long run): the debug logs of the two
  engines are identical, including the `[no context]` lines; the renders
  match except where LuaTeX-ja spaces punctuation differently.
- The XeLaTeX renders of `regression.tex`, `layout-check.tex`,
  `fancy-check.tex` and that stress document are pixel-identical to 1.1.0.
- Size and speed:

  | Document | XeLaTeX | LuaLaTeX |
  | --- | --- | --- |
  | 29 118 characters, plain | 8.7–9.7 s, 68 pages | 13.3 s, 68 pages |
  | the same, `fancy` | 11 s, 70 pages | 17 s, 70 pages |
  | one paragraph of 20 000 characters, `fancy` | exceeds main memory | 13 s, 48 pages |
  | one paragraph of 40 000 characters, `fancy` | exceeds main memory | 23 s, 96 pages |

  Breakdown of the 29 118-character document (typesetting without the
  package / the preprocessor / building the cells): XeLaTeX 1.2 / 1.9 / 6.6 s;
  LuaLaTeX 2.2 / 2.25 / 8.9 s. Loading the package takes 0.16 s under
  XeLaTeX and 0.33 s under LuaLaTeX.

**Bugs found while building it:**

- **L-1. The module was not found in the tests.**
  - Symptom: `module 'xjyutping' not found` with `TEXINPUTS=..:`.
  - Cause: LuaTeX looks for Lua files through `LUAINPUTS`. The installed
    location (`tex/latex/xjyutping/`) and the document's own folder are on
    that path; a `TEXINPUTS` override is not.
  - Fix: the test scripts set `LUAINPUTS=..:` as well.
- **L-2. Only 3 of about 100 characters got rubies under LuaLaTeX.**
  - Cause: LuaTeX-ja packs most characters into a one-glyph hbox (to give it
    its JFM width) and copies the glyph's attributes onto that box. The
    first `glyph_of` skipped any box carrying the cell attribute, meant to
    skip the package's own cells, so it only found the few glyphs LuaTeX-ja
    had left unpacked (before 。).
  - Found by dumping the node list in a callback placed before the
    package's.
  - Fix: skip only boxes tagged -1 (cells).
- **L-3. Test documents loaded xeCJK unconditionally**, which does not exist
  under LuaLaTeX. `regression.tex`, `layout-check.tex`, `fancy-check.tex` and
  xjyutping-py's `parity.tex` now load xeCJK under XeLaTeX and ctex under
  LuaLaTeX (`iftex`).
- **L-4. A DVI branch** for the stroke literal was removed once it turned
  out that LuaTeX-ja stops with "DVI output is not supported".

**Review.** The backend was then reviewed the way 1.0.0 had been (section
3.2): a regression sweep and a code review, each by an agent, with every
finding reproduced by a small document before it was fixed.

- **The sweep** compiled every complete document among the review artefacts
  of section 3 (1 303 documents in 36 folders) twice with XeLaTeX and twice
  with LuaLaTeX, with xeCJK replaced by `\usepackage[fontset=none]{ctex}`,
  and compared errors, overfull and underfull boxes, pages and every
  `xjyutping>` line. 48 were skipped (24 too large for XeLaTeX's memory, 24
  that patch 1.0.0 internals). Of the 1 255 compared, 1 115 agreed in
  everything, and the other 140 were explained:
  - LuaTeX-ja's punctuation widths and line breaks (64);
  - fonts that luaotfload does not find under the names given (26);
  - documents that exceed XeLaTeX's memory and compile under LuaLaTeX (10);
  - the same fatal error under both engines (9), documents without
    annotation (9), reviewer patch files (5), hyperref errors outside any
    scope (4), xeCJK-only commands (3), soul (2), xpinyin (1), log wrapping
    (1);
  - real defects in 6 documents (D1 and D7 below).
- **The code review** found ten defects, all under LuaLaTeX:
  - **D1 (medium)** Text from a macro was annotated at the end of its
    paragraph, with the settings in force there instead of where it stood.
    Fix: `\xjyutping@lua@on` takes a snapshot of the settings (a token list
    of assignments; one copy of each distinct set is kept) and tags what
    follows with its id. The no-context build puts the settings back
    (`\xjyutping@lua@restore`), and `\xjyutpingsetup` takes a new snapshot.
    The `\setjyutping` readings are not in the snapshot, so macro text still
    takes those in force at the end of its paragraph (documented).
  - **D1b (low)** A no-context cell was built at the size of the glyph's
    font. With a scaled CJK font (luatexja-fontspec's default scale
    0.962216) its ruby came out smaller and lower than its neighbours'. Fix:
    a third attribute, `xjyutping@size`, carries `\f@size`, set in the
    `selectfont` hook while annotation is on.
  - **D2 (medium)** `\__xjyutping_nopad:`, which the walker puts after a
    character followed by invisible material and then ，or 。, did nothing,
    so the comma after `銀\uline{行}` did not hug its character. Fix:
    `\xjyutping@lua@nopad` flags the last cell, and `wrap` leaves out its
    right pad. `銀\uline{行}，` is now 44.53pt wide, as without `\uline`.
  - **D3 (medium)** In a justified line, the glue between a character and
    punctuation that hugs it took hsep's stretch, so the mark drifted away.
    Fix: that glue is now zero, as under XeLaTeX.
  - **D4 (medium)** A manual reading was lost when its character was not
    the token right after the mark (`\xjyutping{\textbf{行}}{hong4}`, a brace
    group, `\color`). **D5 (low)** A reading given for a Latin letter or a
    punctuation mark was typeset as a cell. Fix for both, in the code the
    engines share: `\__xjyutping_manual:nn` walks the text token by token
    and into brace groups, and puts a mark right before each Chinese
    character only. The count warning counts Chinese characters (Part I,
    1.2.0, says how this differs from 1.1.0).
  - **D6 (low)** Cells stored for characters that never reach the callbacks
    (in math, in `\discretionary`) stayed in the Lua table. Fix: no cell is
    built in math mode. `\discretionary` still leaks a few bytes per
    character, with no visible effect.
  - **D7 (medium)** Chinese characters in a `\url`, which url.sty sets in
    math, got no-context rubies. Fix: `\everymath` and `\everydisplay`
    switch annotation off. This turned out to be too broad (see "After the
    review").
  - **D8 (high)** In a box, the TeX code that `tex.runtoks` runs for a
    no-context cell during `hpack_filter` appended LuaTeX-ja whatsits after
    TeX's stale tail pointer: the box's last glyph, which LuaTeX-ja had
    meanwhile packed into a box of its own. The last character of the box
    then got no ruby, even one with its own mark (`\mbox{\foo 大}`). Fix: the
    no-context build runs inside `\hbox_set:Nn \l__xjyutping_nocontext_box`,
    so it adds nothing to the list being packed.
  - **D9 (medium)** Text from a macro in a TikZ node: the node box is packed
    where pgf's `\selectfont` selects `\nullfont`, so the ruby was set in
    `\nullfont` and sat on the character. Fix: the no-context build restores
    `\pgf@selectfontorig` and sets the size itself. The output now matches
    XeLaTeX's.
  - **D10 (low)** Only the finite stretch of hsep reached Lua, as an
    integer, so its shrink and any fil order were lost. Fix: `store` reads
    the whole glue with `token.scan_glue`.
- **Verification.** After three rounds of fixes, every repro gives the same
  debug log under both engines (except D1's `\setjyutping` case), and the
  widths of D2 and the glue of D3 and D10 match XeLaTeX's. The first
  rewrite for D4 lost the braces of a group holding one token
  (`\xjyutping{\textbf{行}}{hong4}` printed `uhong4`); the walk now takes one
  token or one brace group at a time (`\tl_if_head_is_group:nTF`).

**After the review.** The sweep was run once more on the finished code, with
the 1.1.0 data so that only code changes show, over the 393 documents in the
ten folders that exercise the walker, the layout and whole user documents.
It found two regressions, both fixed:

- The body collector of `linebreak` broke a scope opened by a user
  environment and a scope inside braces within a scope (3 documents, both
  engines; section 7.6, LB-3).
- D7's guard also switched annotation off in text inside math: in `\text`,
  in `\mbox`, and in the cells of a tabular, which LaTeX builds inside
  `$…$`. So `\maketitle`'s `\author` (a tabular) lost its rubies under
  LuaLaTeX. Now `\everyhbox` and `\everyvbox` (LuaTeX-ja's registers, which
  it runs from the primitive ones) switch annotation back on in a box inside
  math (`\__xjyutping_unmath:`). That is what XeLaTeX does, since xeCJK sees
  text-mode material inside math. It also lifted a documented limit:
  `$\text{\foo}$` is now annotated under LuaLaTeX too.

After these fixes:

- XeLaTeX is unchanged in all 393 documents: errors, boxes, pages and every
  debug line.
- LuaLaTeX has the same errors and overfull boxes.
  - 3 documents have fewer no-context cells (D7, and soul).
  - 7 documents with narrow columns report more underfull boxes (22 → 37 in
    all), because the glue before punctuation no longer stretches (D3).
    XeLaTeX reports underfull boxes in the same places.
- The debug logs of the two engines differ in 7 documents (8 before), all
  for the reasons listed above.
- One stress test (`code-review/t14-hash-exhaust.tex`) runs over the
  sweep's 300 s limit under both engines, as it did before.

### 7.4 More vocabulary

Built by an agent in the background; the full evaluation files (added words,
rejected candidates, disagreements with rime, the book characters, the test
sentences) were in the session's scratch directory.

**Sources and commits** (`tools/fetch-sources.sh`):

| Folder | Upstream | Commit |
| --- | --- | --- |
| `jyutping-table-master/` | lshk-org/jyutping-table | `dad2dd6d6f02fc51138ecc6818f7b38eba5c2ad3` (2024-01-12) |
| `rime-cantonese/` | rime/rime-cantonese (the files cite CanCLID/rime-cantonese-upstream) | `259f0e48bba840c3a2e0d117539e96937f3d89bc` (dictionaries 2026.08.10) |
| `opencc/` | BYVoid/OpenCC `data/dictionary` and LICENSE | `e02cb540b9f98b2da7868b4e8f7b43f88bacadc5` |
| `cantonese-books-data/` | jyutnet/cantonese-books-data | `02740c7e136e2766d7931a37ed0633aa41009ae1` (2026-09-25) |
| `jyut-dict/` | aaronhktan/jyut-dict, sparse: `src/dictionaries`, `src/jyut-dict` without `vendor/` | `26526015424de3f9c30cd9c7e42b96dadb068b6a` (2026-09-28) |

The local copies of the four older sources match those commits byte for
byte. A fresh fetch into an empty directory rebuilt identical data.

**What jyut-dict contains.**

- `src/jyut-dict` is the Qt application: code, translations, an empty
  user-database template and `audio.zip` (6 145 syllables of speech). It has
  no vocabulary.
- The word data is in `src/dictionaries/cedict/data`:
  - `CC-CANTO.txt`: CC-Canto, Version 2017-02-02, © 2015–17 Pleco Inc.,
    CC BY-SA 3.0;
  - `READINGS.txt`: "CC-CEDICT Cantonese Readings", Version 2015-09-23,
    © 2015 Pleco Software Inc., CC BY-SA 3.0;
  - `FULLREADINGS.txt`: the two combined and lowercased, so it is not read.

  `CC-CEDICT.txt`, `CFDICT.txt` and `HANDEDICT.txt` have no Cantonese and
  are not used. The other folders of `src/dictionaries` hold only scripts
  that download their data elsewhere.

**Words.** The candidates are the headwords of 2 or more characters that
the list lacks under their raw or canonical spelling (52 660).

- Romanisation is normalised: lowercased; changed tones `cin4*2` → cin2 and
  `hang4*haang4` → haang4; of `a / b` the first is taken.
- A candidate is added only if all of these hold:
  1. Each syllable is a reading LSHK, rime or a book gives the character, or
     a changed tone (tone 1 or 2) of one. Rejected: 155.
  2. Every word of the list inside it keeps a reading rime gives it.
     Rejected: 568 (for example 車公廟站 miu6 against rime's 車公廟 miu2).
  3. The same holds for every pair of characters that occurs in rime's
     words. Rejected: 656 (過嚟 lai2, 唔會 wui2, 上個禮拜 soeng5).
  4. It does not change the tone of a sentence-final particle. Rejected: 21
     (你好嗎 maa1, 得喇 laa1).
  5. **The tie rule:** a two-character word AB is refused if some word of the
     list ends in A with another reading, because on a tie the later word
     would steal A. This is the 屋企|住 → 屋|企住 bug. Rejected: 8 908.
     - It prevented regressions from 種花 (呢種花), 長得 (時間長得可怕),
       行好 (品行好), 當上 and 上行.
     - It also blocks some good words (重未, 慢行).
  6. The list, with the shorter new words already added, reads it otherwise.
     Words are processed shortest first; 38 877 candidates already read as
     their source says and are not added.
  7. It is not in `EXCLUDED_WORDS`: 480 words checked by hand. They are
     readings Hong Kong and rime do not use (乙 jyut3, 這 ze5, 陷 haam6,
     購/構 gau3, 擾 jiu5 …), dropped changed tones (慳錢 cin4, 練習簿
     bou6), names read otherwise (柯士甸, 楊千嬅, 許冠傑), wrong readings
     (同學會 wui5, 左行 haang1), and words that would steal characters
     (方法|會 → 方|法會, 中學|到 → 中|學到, 家長會 before modal 會, 照會,
     知會 …).
- Where both sources have a word, CC-Canto wins, then the most usual
  syllables. Only 50 words were in both, and they all agreed.
- **Added: 2 291 words** (CC-CEDICT readings 1 927, CC-Canto 364). For
  example: 基金會/房委會/研討會 wui2, 冠狀病毒 gun1, 智能卡
  kaat1, 機長/理事長 zoeng2, 交換生/侍應生 sang1, 曾蔭權 zang1, 上海話 waa2,
  動畫片/芯片 pin2, 幾位 wai2, 手相 soeng3, 自由行/單行 hang4, 營業額/成交額
  ngaak2.

**Characters.** 640 characters that LSHK and rime lack. Each takes the first
reading not labelled 俗/舊/古/本/原/誤/罕/專名 from the first book in `BOOKS`
that has it:

- modern books: 2004 34, 1988 211, 1974/96 72, 1985 26, 1971 1, 1967 31,
  1947 60, 1941 4;
- four pre-1940 books, through the modern Jyutping their digitiser derived:
  1939 172, 1931 2, 1916 2, 1914 25.

58 of the 640 are flagged as polyphones. Left out:

- compatibility ideographs;
- 1962 廣州音字彙, which the collection itself withdrew as inaccurate;
- books with reconstructed readings only.

**Book example words** (the ～ in glosses) were evaluated and not used:

- only the headword's reading is given;
- many are classical fragments;
- the books contradict each other (龜茲);
- several would impose conservative, non-Hong-Kong readings on common words
  (韌性 ngan6, 餅食 bing2).

**Evaluation**, with the Python package (same readings as TeX), old data
against new:

- **The audited corpora of the earlier rounds** (17 files, 8 349
  characters): 2 readings changed, both neutral: 舊樓 lau2, 成交額 ngaak2.
- **Three files of new test sentences** (1 804 characters, about 30 of them
  traps for the risks above): 27 changes, 24 improvements and 3 neutral.
  Examples: 機長 zoeng2, 消防隊 deoi2, 膠帶 daai2, 雙人房 fong2, 香港公園
  jyun2, 核彈 daan2, 請問幾位 wai2.
- **No regressions.** The first version, with filters 1–3 only, changed 48
  characters in the corpora, most of them for the worse (你好嗎, 得喇, 過嚟,
  唔會, 種花, 長得, 慳錢, 這次, 划船 …); filters 4–5 and the exclusions came
  from those.
- **The TeX side:** `regression.expected` is unchanged. xjyutping-py's
  `parity_expected.txt` changed in one line: 隨着 is now one word, with the
  same readings.

**Hand fixes** added to `CURATED_WORDS`:

- 化合物 faa3 hap6 mat6 (rime has gap3, a 0% reading of 合, though its own
  化合 is hap6);
- 會否 wui5 fau2 (rime has wui2; the modal is wui5).

Not applied, because they are disputed or would change the regression demo:
這個 ze2, 開玩笑/玩笑 waan4, 敏捷 zit6, 分散 saan3, 預訂 ding6, 應允 jing3,
重未 zung6.

**Where CC-Canto and the CC-CEDICT readings disagree with rime:**

- in 1 910 of CC-Canto's 16 929 known words and 1 575 of 53 957 CC-CEDICT
  words;
- mostly they drop Hong Kong changed tones (面 min2, 女 neoi2, 頭 tau2) or
  use standard or Guangzhou readings (券 hyun3, 購 gau3, 擾 jiu5, 嚟 lei4);
- rime was kept in every case.

**Licences.** The word lists are CC BY-SA 3.0, so the generated data (the
`.def` files and the Python TSVs) must be shared alike. It is distributed
under CC BY-SA 4.0, which 3.0 §4(b) allows. The CC BY 4.0 (LSHK, rime) and
Apache-2.0 (OpenCC) material may be part of it, with credit.

cantonese-books-data states no licence. jyut.net says "© 2014-2026
粵音資料集叢" and offers the files for researchers' convenience. Only the
readings of 640 rare characters are used, with credit. Before a wide
release, it would be prudent to ask the author (a GitHub issue or jyut.net);
emptying `BOOKS` builds without them.

**Statistics:**

- characters 29 449 → 30 089 (polyphonic 4 349 → 4 407);
- words 101 277 → 103 579; canonical-spelling aliases 68 → 133;
- `xjyutping-words.def` 3.43 → 3.52 MB, `xjyutping-chars.def` 516 → 527 KB;
- the build takes 0.7 → 3 s;
- `Jyutping()` construction about 5–9 % slower; XeLaTeX times unchanged
  within noise.

**Process notes:**

- The agent was stopped twice by an API usage limit and resumed with its
  context.
- An `importlib` import of the script created a `__pycache__`, which the
  user's interim commit picked up (section 7.2).

### 7.5 Documentation and versions

- README of this package: engines, data sources and their filters, the
  new licence of the data, and a separate "Acknowledgements and
  attributions" section:
  - xpinyin by Qing Lee (李清) as the inspiration;
  - Visual Jyutping (Vincent Tam) and the Visual Cantonese Fonts (Jon Chui /
    A3I Ltd., canto.hk) for `fancy`;
  - the LSHK Jyutping Workgroup, rime-cantonese (CanCLID), 石見田 and the
    books of 粵音資料集叢, Jyut Dictionary (Aaron Tan) with CC-Canto and the
    CC-CEDICT readings (Pleco) and CC-CEDICT (MDBG), and OpenCC.

  Author names were checked against the sources: `xpinyin.dtx`, the Python
  xpinyin `setup.py`, Visual Jyutping's LICENSE, canto.hk's footer, and the
  LSHK README.
- Manual: the "Getting started" example uses ctex for either engine; there
  is a new section "XeLaTeX and LuaLaTeX", and the limits, data and
  acknowledgements are updated.
- Versions: this package 1.2.0 (new features, backward compatible); the
  Python package 1.1.0 (new vocabulary).

### 7.6 The `linebreak` option

**The request.** The user asked for an option like `fancy`, usable as
`\begin{jyutpingscope}[linebreak]`, under which every line end of the source
becomes a line break (`\\` or `\newline`) and a blank line a paragraph break
that follows the usual LaTeX conventions. For example, with
`\usepackage[parfill]{parskip}` the new paragraph has no indent. The user's
example was two lines of a song; the documentation uses 靜夜思 (Li Bai,
public domain) instead.

**Design:**

- The line ends must reach the package as characters, so the catcode of
  ^^M is 12 (other) while the body is read. A `+b` argument is read before
  the begin code runs, that is before the option is known. The environment
  therefore takes only `O{}` and collects its body itself
  (`\__xjyutping_collect:w`); with `linebreak` off, the catcodes stay as
  they are.
- The collector follows ltcmd's `+b`:
  - it grabs the text up to the next `\end` outside braces;
  - it counts the `\begin` tokens outside braces in that text;
  - it stops at the first `\end` that closes none of them, and leaves that
    `\end` to read its own argument, so `\end{lesson}` of a user environment
    ends the scope through the environment's end code;
  - a `\q_nil` in front of each piece keeps the braces of a piece that is
    one group;
  - without `linebreak` the body is trimmed of spaces, as `+b` trims it.
- `\__xjyutping_lines:N` rewrites the body with l3regex:
  - line ends and spaces at both ends are dropped;
  - two or more line ends in a row (a blank line) become `\par`;
  - a line end after `\\` or `\newline` is dropped;
  - any other line end becomes `\__xjyutping_newline:`, which issues
    `\newline` in horizontal mode unless the next token is `\begin`, `\end`
    or `\par`.
- The walker ends a run at `\newline` and `\par`, so no word is looked up
  across two lines. A `%` at a line end removes the line end as usual.

**Bugs found while building it:**

- **LB-1. Under LuaLaTeX the first line break was lost** when the option
  came from `\xjyutpingsetup` and the environment had no optional argument.
  - Cause: LuaTeX-ja's `process_input_buffer` callback appends U+FFFFF, a
    comment character (`\ltjlineendcomment`), to a line that ends in a
    Chinese character while ^^M has catcode 5, so that the line end gives no
    space. Looking for the optional argument reads the first line of the
    body before the begin code runs.
  - A first fix, `!O{}`, stopped the look-ahead but also refused a space
    before `[linebreak]`.
  - Fix kept: inside the scope the catcode of `\ltjlineendcomment` is 9
    (ignored), so the appended character vanishes and the line end
    survives. LuaTeX-ja appends nothing further while ^^M is catcode 12.
- **LB-2. An underfull box** came from a `\newline` right before
  `\begin{center}`. `\__xjyutping_newline:` now does nothing before
  `\begin`, `\end` and `\par`.
- **LB-3. The first collector** stopped only at `\end{jyutpingscope}`, and
  counted nested scopes with a regex, which also sees inside braces.
  - Effect: a scope opened by a user environment ran to the end of the file,
    and so did a scope inside braces within a scope ("File ended while
    scanning use of `\__xjyutping_collect:w`"). The final sweep found it
    (section 7.3, "After the review").
  - Fix: the collector was rewritten to follow `+b`, as described above.

**Tests:**

- Line ends, blank lines, `\\`, `%`, `center` and `parskip`, and the option
  given as `[linebreak]`, as ` [linebreak]` after a space, and through
  `\xjyutpingsetup`, all under both engines: 0 errors, 0 bad boxes, the
  same debug logs. These files were not kept.
- `tests/regression.tex` keeps a `linebreak` scope and a scope opened by a
  user environment.

**Limit:** the option works only where the line ends are still in the
source when the scope begins. It does nothing in `\xjyutping*`, in a scope
inside a command's argument (`\parbox{…}`), or in a scope inside a scope
without the option. Inside environments such as `minipage` or `center` it
works.

### 7.7 Open issues after 1.2.0

Documented in the README and the manual:

1. Under LuaLaTeX, text from a macro takes the `\setjyutping` readings in
   force at the end of its paragraph (D1); its options and size are those
   of the place where it stands. A fix would put the user readings into the
   snapshot, copying them at every change.
2. Under LuaLaTeX, LuaTeX-ja's rules for punctuation and line breaks apply
   (no break before —— or ……), so lines break differently from XeLaTeX.
3. `linebreak` needs the line ends in the source (section 7.6).

Not in the README:

4. Under LuaLaTeX, a cell built for a character in `\discretionary` is
   never used and stays in the Lua table (D6).
5. The long-mark branch of `wrap` (a discretionary holding the pad) never
   fires with ctex's JFMs, which forbid a break before —— and ……. It is kept
   for other JFMs and is untested.
6. **The 640 characters from cantonese-books-data** come from a source
   with no licence statement (section 7.4). CTAN and TeX Live distribute
   only freely licensed material. Before uploading, ask 石見田 for
   permission (a GitHub issue or jyut.net), or empty `BOOKS` in
   `tools/build-data.py` and rebuild the data.
7. `.DS_Store` is still tracked (section 7.2).
8. Items 11–15 of section 4 (R3-14, R2-14, the line pitch after deep lines,
   ambiguous readings, the segmentation tie-break) are unchanged.

### 7.8 Tests and release files at 1.2.0

- `tests/run-tests.sh`: four jobs and 26 expected lines, all `readings ok`.
- **`tools/make-ctan-zip.sh [OUT]`** builds the archive for CTAN, by default
  `../xjyutping.zip`.
  - Contents: one folder, `xjyutping/`, with `README.md`, `LICENSE`,
    `CHANGELOG.md`, the package (`xjyutping.sty`, `xjyutping.lua` and the
    two `.def` files), the manual (`xjyutping-doc.tex` and `.pdf`),
    `tools/`, and the sources in `tests/`.
  - Permissions: files 644; folders and scripts 755.
  - Checks: it stops if a file does not carry the version of
    `xjyutping.sty`, and warns if the manual's PDF is older than its source.
    Rebuild the manual first (`xelatex xjyutping-doc`, twice; it needs the
    font Songti TC) whenever `xjyutping-doc.tex` has changed.
  - The 1.2.0 archive was checked by unpacking it and compiling, from its
    files alone, a sample document with each engine and the manual, and by
    running its `tests/run-tests.sh`.
- **For the CTAN upload form:**
  - licences: `lppl1.3c` for the code and `cc-by-sa-4` for the data;
  - suggested directory: `/macros/unicodetex/latex/xjyutping`;
  - home page and repository: https://github.com/Beyond3345/xjyutping-tex;
  - bug tracker: https://github.com/Beyond3345/xjyutping-tex/issues.
- The Python package is released separately (xjyutping-py 1.1.0, see its
  changelog).
