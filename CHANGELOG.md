# Changelog

This file records all notable changes to xjyutping, the LaTeX package. The
format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

The Python port lives in a separate repository,
[xjyutping-py](https://github.com/Beyond3345/xjyutping-py), with its own
version numbers and its own changelog. Both packages use the data that
`tools/build-data.py` in this repository generates. Up to 1.1.0 the two lived
in one folder with a single changelog, and its history is kept here, in
Part II.

The version is written in four places. These are `\ProvidesExplPackage` in
`xjyutping.sty`, `VERSION` in `tools/build-data.py` (which goes into the
`\ProvidesFile` lines of the `.def` files), `README.md` and `\author` in
`xjyutping-doc.tex`. A release bumps all four and gets an entry in Part I.

The file is divided into two parts. Part I (Releases) lists what changed in
each version. Part II (Handover notes and development history) covers how
the package was built and how it works, every bug found during development
with its cause and fix, the known open issues and how to test. This part is
written for the next maintainer, human or agent.

---

# Part I: Releases

## [Unreleased]

There are no unreleased changes yet. Add new entries here under
`### Added`, `### Changed`, `### Fixed` and so on.

## [1.3.0] - 2026-09-29

### Added

- The new `align` option aligns the lines of a scope. Its values are
  `justify` (the default), `left`, `centre` (or `center`) and `right`, and
  they also work on their own, as in
  `\begin{jyutpingscope}[linebreak,fancy,centre]`. An aligned scope starts a
  paragraph of its own (Part II, Section 8).
- `tests/verse-check.tex` is a new visual check of `linebreak` and `align`.

### Changed

- Under `linebreak`, only the paragraph space used to separate stanzas, and
  this space is small next to the line pitch of a scope. A blank line now
  leaves an empty line before the next paragraph, and the document's
  paragraph space (for example from `parskip`) is added to it, so that
  stanzas stand clearly apart.
- The `.def` files carry `v1.3.0`.

### Fixed

- Lines set with `linebreak` were off centre under `\centering` and not
  flush right under `\raggedleft`. This was due to each line end becoming
  `\newline`, which ends the line with an `\hfil` that pulls it to the left,
  the more so the shorter the line. A line end is now `\\`, which follows the
  alignment in force.

## [1.2.0] - 2026-09-28

### Added

- The package now supports LuaLaTeX through LuaTeX-ja, which it loads if the
  document has not loaded any Chinese support (the `ctex` package and
  classes work too). A new file, `xjyutping.lua`, must be installed next to
  `xjyutping.sty`.
  - The preprocessor, the readings and every option are shared with
    XeLaTeX. While each mark builds its ruby in TeX, a Lua callback that
    runs after LuaTeX-ja wraps each tagged character into its cell and
    leaves out the right pad before punctuation that hugs it.
  - The readings are identical to those under XeLaTeX, and the layout is
    nearly identical. As under XeLaTeX, text that comes from macros is
    annotated without context.
  - Under LuaLaTeX a paragraph has no length limit.
- The `linebreak` option, for verse and lyrics, is turned on with
  `\begin{jyutpingscope}[linebreak]` or `\xjyutpingsetup{linebreak}`. Each
  line end of the source becomes a line break (`\newline`) and each blank
  line a paragraph break, which follows the document's paragraph settings
  (indented, or with `parskip` spaced and not indented). Line ends add
  nothing at the start and end of the scope, after `\\` or before `\begin`,
  `\end` or a new paragraph. A line end also ends a run of characters. The
  option works in the environment only, not in `\xjyutping*` (Part II,
  Section 7.6).
- We added more vocabulary (see Part II, Section 7.4).
  - The 2,291 new words come from CC-Canto and the Cantonese readings of
    CC-CEDICT, as distributed with Jyut Dictionary
    (`src/dictionaries/cedict/data`). A word is added only where it changes
    a reading and passes consistency checks against rime-cantonese, and we
    excluded 480 more by hand.
  - The 640 new characters are ones that LSHK and rime-cantonese lack, and
    their readings come from the book data of 粵音資料集叢
    (jyutnet/cantonese-books-data, by 石見田).
- `tools/build-data.py` is now part of this repository, with the options
  `--sources` and `--py-data`, and `tools/fetch-sources.sh` fetches every
  data source at the commit the data was built from.
- In the tests, `tests/run-tests.sh` runs XeLaTeX and LuaLaTeX, each with
  and without `fancy`. `tests/render.sh` takes the engine as its second
  argument, and the test documents load xeCJK or ctex depending on the
  engine. `tests/regression.tex` also covers a scope opened by a user
  environment, a table made by a macro, a box in math and `linebreak`.
- A `LICENSE` file gives LPPL 1.3c for the code and CC BY-SA 4.0 for the
  data, and lists every source of the data with its licence.
- `tools/make-ctan-zip.sh` builds the archive for CTAN (Part II,
  Section 7.8).
- The README and the manual now have a section on the two engines and an
  Acknowledgements and attributions section (xpinyin by Qing Lee, Visual
  Jyutping, the Visual Cantonese Fonts and every data source).
- We added a `.gitignore` file.

### Changed

- The new words change readings where they are more exact, for example
  機長 zoeng2, 營業額 ngaak2, 自由行 hang4, 研討會 wui2, 消防隊 deoi2,
  冠狀病毒 gun1 and 智能卡 kaat1. We corrected 化合物 to faa3 hap6 mat6 and
  會否 to wui5 fau2 by hand. No reading from rime-cantonese was replaced.
- Since the added word lists are CC BY-SA 3.0 (share-alike), the `.def`
  files, which hold the generated data, are now distributed under
  CC BY-SA 4.0 instead of carrying CC BY 4.0. The package code stays under
  LPPL 1.3c.
- The readings of `\xjyutping{<text>}{<readings>}` now go to the Chinese
  characters of the text, one each, also inside braces and commands
  (`\xjyutping{\textbf{行}}{hong4}`, `{\color{red}行}`). Latin letters and
  punctuation take none, and the warning about the number of readings counts
  Chinese characters only. In 1.1.0 every item of the text, whether a
  punctuation mark, a letter or a command, took a reading of its own, which
  XeLaTeX then dropped. A reading written for such an item now goes to the
  next Chinese character, with a warning. Under LuaLaTeX a reading for a
  character in braces was lost and a Latin letter got a cell. These were
  review findings D4 and D5 (Part II, Section 7.3).
- The `jyutpingscope` environment now reads its body itself instead of as a
  `+b` argument, so that `linebreak` can see the line ends. The body ends
  where a `+b` argument ended. Specifically, it ends at the first `\end`
  that does not close a `\begin` of the body. Hence a scope can still be
  opened and closed by a user environment.
- While the manual keeps the details, the README is now shorter, with an
  overview, the command and option tables and the attributions.
- The `.def` files carry `v1.2.0`.
- The history of the project (this file) now lives in this repository.

## [1.1.0] - 2026-09-28

### Added

- The new `fancy` option, given as in `\usepackage[fancy]{xjyutping}`, is
  also accepted by `\xjyutpingsetup` and in the options of one scope or
  `\xjyutping*`. It shows
  tones the way [Visual Jyutping](https://github.com/VincentTam/visual-jyutping)
  does.
  - The tone number is replaced by a small drawn pitch stroke for the six
    tones (high, rising to high, mid, falling to low, rising from low and
    low), modelled on the Visual Jyutping symbols ˉ ˊ ˗ ˎ ˏ ˍ.
  - The stroke is followed by a smaller tone number, raised for tones 1–2
    and lowered for tones 3–6.

  The strokes are PDF drawing commands, so they do not depend on the font
  and they take the text colour.
- Spacing adjusts automatically to `fancy`.
  - Cell widths (`width=auto`) are measured with the marks in place.
  - The ruby strut includes the raised and lowered numbers, so line spacing
    stays even.
  - If the lowered numbers reach below the letters, the ruby is lifted by
    the difference (`\g__xjyutping_lift_dim`), so its gap to the character
    stays the same.
- `tests/fancy-check.tex` is a visual check of the tone marks at several
  sizes, fonts, colours and widths.
- `tests/run-tests.sh` now also compiles the regression document with
  `fancy`, which must give the same readings.

### Changed

- In a new repository layout, the LaTeX package moved into `xjyutping-tex/`
  and kept its file names, `xjyutping.sty`, `xjyutping-chars.def`,
  `xjyutping-words.def`, `README.md`, `xjyutping-doc.tex/.pdf` and
  `tests/`. Documents and installation are unaffected. `tools/build-data.py`
  and the data sources stayed at the root of the workspace (in 1.2.0 the
  tool moved into this repository).
- In `CURATED_WORDS`, 慢慢行 is now maan6 maan2 haang4, where rime had
  maan6 maan6 hang4. We also added the entries 屋企住, 都會話 and 生詞表,
  since the longer-final-word tie-break split them wrongly into 屋|企住,
  都|會話 and 生|詞表 with 生 sang1.
- The `.def` files carry `v1.1.0` in their `\ProvidesFile` lines.
- `tests/run-tests.sh` used to write the extracted debug lines to
  `regression.out`, the file name hyperref uses for its bookmarks. It now
  writes them to `<job>.readings`.
- The manual has a new "Fancy tones" section, and the README and the manual
  state the version and the versioning scheme.

### Fixed

- Inside a scope, links to the named destination of `\pdfbookmark` (and of
  `\currentpdfbookmark`, `\subpdfbookmark` and `\belowpdfbookmark`) were
  silently broken. The cause was that the anchor name was walked as text
  and annotated, so the named destination contained marks. Both arguments
  are now passed through untouched. This was open issue 17 at 1.0.0.

## [1.0.0] - 2026-09-28

The file itself says `1.0`, which is read as 1.0.0.

### Added

- This is the first release of the XeLaTeX package `xjyutping`, which puts
  Jyutping above traditional Chinese characters.
- The commands are,
  - the `jyutpingscope` environment,
  - `\xjyutping*[opts]{text}` for running text,
  - `\xjyutping[opts]{字}{reading}` for manual readings,
  - `\setjyutping` for character defaults and words,
  - the pair `\disablejyutping` and `\enablejyutping` and
  - `\xjyutpingsetup`.
- The options are `ratio`, `vsep`, `hsep`, `width` (auto, natural or a
  length), `font`, `format`, `multiple` and `debug`.
- The package chooses readings from context. It segments each run of
  Chinese characters with about 101 000 words, and the segmentation prefers
  the fewest words first and then the fewest single characters, while a tie
  goes to the longer final word. Formatting commands and braces do not split
  words. Variant shapes are folded together for word lookup, and some
  characters have run-final readings (呢).
- The layout is even and collision-free, with uniform cells, the right
  half-pad paid by whatever follows, line spacing and clearance.
- The package works with hyperref, nameref, cleveref, natbib/biblatex,
  footnotes, tables, the ctex classes and beamer.
- The data comes from the LSHK Jyutping table and rime-cantonese (CC BY 4.0)
  and OpenCC (Apache-2.0), and is generated by `tools/build-data.py` with
  hand-checked correction tables.

### Fixed (during development, before the release)

- We fixed 10 issues while writing the first version, and then about 81
  distinct bugs and 88 accepted reading findings over three review rounds.
  Each is listed with its symptom, cause, fix and verification in Part II,
  Section 3.

---

# Part II: Handover notes and development history

## 0. Start here

This repository holds the LaTeX package, and the table below lists its files.

| Path | What it is |
| --- | --- |
| `xjyutping.sty` | The package (expl3). |
| `xjyutping.lua` | The LuaLaTeX backend: builds the cells after LuaTeX-ja (Section 7.3). |
| `xjyutping-chars.def`, `xjyutping-words.def` | Generated data; never edit by hand. |
| `tools/build-data.py` | Generates the data of this package and of xjyutping-py from the sources. |
| `tools/fetch-sources.sh` | Fetches the sources at the pinned commits. |
| `tools/make-ctan-zip.sh` | Builds the archive for CTAN (Section 7.8). |
| `tests/` | `run-tests.sh` (readings, both engines, with and without `fancy`), `render.sh`, `regression.tex/.expected`, `layout-check.tex`, `fancy-check.tex`, `verse-check.tex`. |
| `README.md`, `xjyutping-doc.tex/.pdf` | User documentation. |
| `LICENSE` | LPPL 1.3c for the code, CC BY-SA 4.0 for the data, and the sources of the data. |
| `CHANGELOG.md` | This file. |

The third-party sources are not part of the repository. Instead,
`tools/build-data.py` looks for them in the directory that contains the
repository (the "workspace"), which in the original set-up is organised as
follows.

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

The script `tools/fetch-sources.sh [DIR]` recreates the five data folders
there.

The following invariants must be kept.

1. The two packages must give the same readings. Any change to the data or
   to the segmentation must therefore keep both `tests/run-tests.sh` in this
   repository and the parity test of xjyutping-py
   (`test_parity_with_tex_package`) passing. When readings change on
   purpose, regenerate `tests/regression.expected` and xjyutping-py's
   `tests/parity_expected.txt` from the TeX logs (Section 5) and check the
   diff by hand.
2. Fix readings in the data rather than in the code. Edit only the tables at
   the top of `tools/build-data.py`, then run it to rewrite the data of both
   packages. Of the sources, rime-cantonese is authoritative, and the others
   only add what rime lacks. A candidate entry should first be tested with
   `\setjyutping` in a few contexts, since the longer-final-word tie-break
   means that a new word can capture its neighbours (Section 5.2).
3. Both engines must produce the same readings and nearly the same layout.
   Since the layout logic is implemented twice, in the XeLaTeX cell code of
   `xjyutping.sty` (`\__xjyutping_cell:nnn` and the pad functions) and in
   `xjyutping.lua` (`wrap`), a change to one needs the matching change to
   the other.
4. The two passes of the TeX walker must visit the same Chinese characters
   in the same order (Section 2.4).
5. Respect TeX's capacity limits under XeLaTeX (Section 2.10). Specifically,
   names are created at the top level or globally, per-character slots are
   reused (set to `\relax`) and text is analysed paragraph by paragraph.
   Since whatever a cell adds is paid for every character, measure main
   memory after layout changes. For example, the `fancy` marks cost 50 words
   per character (Section 6).
6. Versioning follows Semantic Versioning (SemVer). The MAJOR version is
   raised for an incompatible change, such as removing or renaming a command
   or option, or changing an argument's meaning. The MINOR version is raised
   for a backward-compatible feature, such as `fancy` in 1.1.0, or LuaLaTeX
   and the new vocabulary in 1.2.0. The PATCH version is raised for bug
   fixes and reading corrections.

Run the tests with,

```bash
tests/run-tests.sh
```

The script needs XeLaTeX with xeCJK and LuaLaTeX with LuaTeX-ja and ctex, as
well as the font Songti TC. It must print `readings ok` for all four jobs,
which run XeLaTeX and LuaLaTeX, each with and without `fancy`. For a visual
check, run,

```bash
tests/render.sh tests/fancy-check.tex lualatex
```

For the open issues, Section 4 gives the state at 1.0.0 and says which of
them 1.1.0 resolved, while Section 7.7 gives the state after 1.2.0 and
Section 8.5 what 1.3.0 adds.

The review artefacts cited below (the repro `.tex` files and the review
JSON) lived in the session's temporary directory and are not part of the
repository. However, this file, the README, the code comments and the tests
hold everything needed.

## Sources and conventions of the history (Sections 1–5)

Sections 1–5 describe how the XeLaTeX package, which is now this repository, was built and reviewed. All of this happened on 2026-09-28 in a single Claude Code session. While the package file gives the version as `1.0`, this changelog treats it as 1.0.0 under SemVer. The data files carry `v1.0` in their `\ProvidesFile` lines.

This history is based on,
- the session transcript (`~/.claude/projects/-Users-beyond555-Documents-CodingProjects-xjyutping/7ca57d4a-….jsonl`),
- the three review-workflow results (`tasks/review.json`, `review2.json` and `review3.json` in the session's temporary directory),
- the reviewers' repro files (`scratchpad/review-artifacts/`),
- the code as frozen at 1.0.0 (a snapshot of `xjyutping.sty` and the `.def` files) and
- `tools/build-data.py`.

The review artefacts live under `/private/tmp/…` and will not survive a reboot, while everything needed to maintain the package is in this document, the README, the code comments and `tests/`.

Clock times are in local time (UTC+8), which is what the file timestamps show. They are given only to put the events in order.

Bug identifiers follow three schemes. I-n numbers the bugs found while writing the first version. R1-nn, R2-nn and R3-nn number the findings of review rounds 1–3, in the order of the review JSON files. Mx-n numbers the regressions or bugs that the main agent hit while applying the fixes for round x.

---

## 1. Origin

### 1.1 The request (09:32)

The request came from the author of the package, a Cantonese learner and LaTeX user. At that point the project folder held two things. The first was `xpinyin/`, the CTeX-kit package that puts Hanyu Pinyin over simplified Chinese (`xpinyin.dtx`, README and PDF), and the second was `jyutping-table-master/`, a character-to-Jyutping list.

We asked for a similar package that puts Jyutping above Chinese characters. Its readings should change with context "if possible", and its Jyutping must be uniformly and cleanly spaced and must not collide with other text. Since pronunciation shifts with context, users should also be able to give custom readings for specific characters. Only traditional characters need to be supported.

We gave `https://github.com/lshk-org/bilingual-glossary.git` as the source of the list. However, the folder contains `jyutping-table-master`, which is the LSHK *Cantonese Pronunciation List of Characters for Computers* (電腦用漢字粵語拼音表). This table is licensed under CC BY 4.0 and is stored in `list.tsv`, which has 29 144 distinct characters. The session treated the folder as that table throughout. The repository name in the request does not match the folder's contents, and nothing in the folder mentions a bilingual glossary. Since the `-master` suffix is how GitHub names a branch download, the folder is probably a download of `lshk-org/jyutping-table`, although this has not been verified. This history records the discrepancy and does not resolve it.

### 1.2 Clarifying questions and answers

1. The session asked whether the rime-cantonese word and character lists could be downloaded. Both are licensed under CC BY 4.0, and their files are `jyut6ping3.words.dict.yaml` (2.6 MB) and `jyut6ping3.chars.dict.yaml` (0.35 MB). We answered *"Yes, use rime-cantonese (Recommended)"*.
2. It then asked which engine the package should support, and we answered *XeLaTeX (xeCJK / ctex)*. LuaLaTeX was neither requested nor supported.
3. Lastly, it asked whether OpenCC's HK and TW variant tables could be downloaded. These tables map spellings such as 為/爲, 裡/裏 and 説/說 onto rime's standard forms. We answered *"Yes, download them. You can download a bigger variant table or rime-cantonese dictionary. Focus on quality and don't worry too much about space right now."*

On 2026-09-28 we downloaded `jyut6ping3.chars.dict.yaml` (header version "2026.08.10"), `jyut6ping3.words.dict.yaml` (about 103 000 lines) and `LICENSE-CC-BY` into `rime-cantonese/`. The file `jyut6ping3.phrase.dict.yaml` was also fetched, but it was deleted after it was found to contain words without readings. Into `opencc/` we downloaded `HKVariants.txt`, `TWVariants.txt` and `LICENSE` (Apache-2.0), as well as `HKVariantsRevPhrases.txt` and `TWVariantsRevPhrases.txt`, which the builder does not use.

The environment found on the machine was,
- TeX Live 2026 with xeCJK and ctex,
- the `Songti TC` font (used by every test),
- Ghostscript at `/opt/homebrew/bin/gs` (the only PDF renderer available) and
- python3 3.9.6 without PIL.

### 1.3 Design goals derived from the request

- G1 (context readings). The package should segment runs of Chinese text into words from a large word list (rime-cantonese, about 101 000 words) and let words override the per-character defaults.
- G2 (sensible defaults). The per-character default should come from rime's weights, with LSHK order as the fallback. Characters with several common readings should be flagged, so that they can be highlighted while proofreading (`multiple=`).
- G3 (even spacing with no collisions). Every character should get a cell of uniform width, as wide as the widest Jyutping in the block, and the ruby should stay clear of neighbouring rubies, of the line above and of the margins. Punctuation, line breaking and CJK/Latin spacing should be left to xeCJK, using the xpinyin approach of hooking `\CJKsymbol`.
- G4 (user control). The package should provide `\xjyutping{字}{reading}` for one spot and `\setjyutping` for words and defaults, together with a debug log.
- G5 (variant spellings). HK and TW input spellings must find rime's words.
- G6 (working in real documents). Sections, the table of contents (TOC), hyperref, footnotes, tables, beamer and ctex classes must work, and the TeX capacity limits must hold at book length.

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
| `xjyutping-tex/tests/` | Tests: `run-tests.sh`, `regression.tex`, `regression.expected`, `render.sh`, `layout-check.tex` (see Section 5). |

At 1.0.0 the builder printed these data statistics,
- 29 449 characters with 4 349 of them flagged polyphonic,
- 76 variant mappings,
- 101 275 words plus 68 canonical-spelling aliases (with 0 alias clashes) and
- 1 229 rime words that had several readings.

Since the builder prints only the total, we recomputed the breakdown of the 101 275 words for this write-up. They are 101 088 usable rime-cantonese words, 105 curated words that are not among those rime words and 82 地→哋 twins. The other 30 `CURATED_WORDS` entries replace the reading of an existing rime word.

### 2.2 Loading, and why the data is loaded at top level

- The engine is checked first: on any engine other than XeTeX, `\sys_if_engine_xetex:F` calls `\msg_critical` with `xetex-only`. xeCJK is loaded if it is missing.
- The keys are defined with `\keys_define:nn {xjyutping}`. Package options are processed through `\ProcessKeyOptions`, and later changes go through `\xjyutpingsetup`. The keys and their defaults are,

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

- Each line of the `.def` files is a call to one of six loader macros defined in the `.sty`. The loaders and the macros they define are,

  | Loader | Defines |
  | --- | --- |
  | `\xjp@C` | `\xjp@c@<char>`, the default reading |
  | `\xjp@M` | `\xjp@c@<char>`, plus `\xjp@m@<char>` holding the alternatives |
  | `\xjp@F` | `\xjp@f@<char>`, the run-final reading |
  | `\xjp@V` | `\xjp@v@<variant>`, the canonical spelling |
  | `\xjp@W` | `\xjp@w@<word>` |
  | `\xjp@E` | `\xjp@e@<char>`, the longest word ending in that character |

  User settings are kept in `\xjp@u@<char>` and in `\xjp@w@<word>` plus `\xjp@uw@<word>`.
- The files are read with `\file_input:n`, with the space catcode set to "space" and `\endlinechar=-1`, at the top level rather than inside a group. Inside a group, every newly created control-sequence name costs a save-stack entry, and loading in a group used 140 558 of the 200 000 save-stack slots before any text was processed (M1-2). When we fixed this, we also changed the loader names from `\C \M \V \W \E` to the internal `\xjp@…` forms, so that they no longer clash with user macros.
- Loading costs about 2.47–2.48 million of TeX Live's default 5 000 000 words of main memory, and all the capacity figures below sit on this base.

### 2.3 Public interface

| Command | Implementation |
| --- | --- |
| `jyutpingscope` | `\NewDocumentEnvironment{jyutpingscope}{O{} +b}`. It sets the keys, calls `\__xjyutping_baselineskip:` and `\__xjyutping_prepare:n{body}`; at the end, `\__xjyutping_typeset:` then `\par`. |
| `\xjyutping*[opts]{text}` | `\__xjyutping_prepare:n` then `\__xjyutping_typeset:`, inside a group. |
| `\xjyutping[opts]{字}{reading}` | `\__xjyutping_manual:nn`. Each character gets `\xjyutping@mark{u<syllable>}`, with a `count-mismatch` warning when the counts differ. `\group_insert_after:N \__xjyutping_clear_mark:` drops a reading left pending on a non-Chinese token (R2-09). |
| `\setjyutping{text}{readings}` | `\__xjyutping_set:nnn {…}{…}{g}`. One character goes into `\xjp@u@<char>`. A word is stored under its raw and its canonical spelling (`\__xjyutping_set_word:nn`), and `\xjp@e@` is updated. |
| `\disablejyutping`, `\enablejyutping` | `\__xjyutping_disable:` and `\__xjyutping_enable:`. `\enablejyutping` does nothing in plain mode. |

`\__xjyutping_prepare:n` runs both walker passes inside a group, so that a `\setjyutping` met while reading affects only the segmentation of the text after it. The real, global setting happens at typesetting time, at the position of the `\setjyutping` itself. `\__xjyutping_prepare:n` exports the marked text as `\g__xjyutping_result_tl` and then fixes the cell width in `\l__xjyutping_uniform_tl`, which depends on the `width` key,
- `auto` gives the widest ruby measured in the block, `\g__xjyutping_max_dim`, stored as a multiple of `\f@size`,
- `natural` leaves it empty and
- a length is used as given.

If nothing was measured under `auto`, as with text that only comes from macros, the fallback measures `gwong2`.

### 2.4 Reading a block: the two-pass walker

`\__xjyutping_preprocess:n` first increments `\g__xjyutping_block_int`. It then splits the body into paragraphs with `\__xjyutping_split_pars:Nn` and lastly runs `\__xjyutping_pass:n{1}` and `\__xjyutping_pass:n{2}`.

To split the paragraphs, `\__xjyutping_split_pars:Nn` replaces each top-level `\par` with a delimiter and wraps each paragraph as `{…}`. It uses `\__xjyutping_split:w` with a leading `\prg_do_nothing:`, so a paragraph that is a single brace group keeps its braces, whereas `\seq_set_split` strips them (M1-4). Each paragraph is analysed separately (`\__xjyutping_paragraph:n` → `\__xjyutping_walk:n` → `\tl_analysis_map_inline:nn`), since the analysis needs far more memory than the text itself (Section 2.10). The body is kept in `\l__xjyutping_body_tl` and walked through that variable, never inside the definition of a mapping function, because `#` tokens in the body would otherwise break the definition (M1-1).

The two passes see the same tokens and must visit the same Chinese characters in the same order, since every later reading shifts if they disagree. This invariant was the main target of the round-2 walker review. Pass 1 collects runs of Chinese characters, segments each run (Section 2.5) and stores the chosen mark for block character *n* in the global `\xjp@s@<n>`. Pass 2 copies the text into per-depth global `\tl_build` buffers (`l__xjyutping_buf_<depth>_tl`, via `\__xjyutping_put:n`), puts the mark from `\xjp@s@<n>` in front of character *n* and then sets the slot to `\relax`.

Each token passes through `\__xjyutping_token:nnn` to `\__xjyutping_token:nn`, which dispatches it according to its type,

| Token | Handling |
| --- | --- |
| begin-group / end-group | `\__xjyutping_begin_group:` / `\__xjyutping_end_group:` |
| letters and others | `\__xjyutping_char:n`: a character that has `\xjp@c@<char>` goes to `\__xjyutping_han:`; anything else goes to `\__xjyutping_nonhan:n` |
| control sequences | `\__xjyutping_cs:` |
| catcode 4 (`&`) | `\__xjyutping_tab:` |
| spaces | in pass 2, a space between two Chinese characters is dropped, as xeCJK does. `\__xjyutping_punct_space:n` also drops a space before full-width punctuation (R2-31). |

A run lives in context `\l__xjyutping_ctx_int`, where
- `xjp@len@<ctx>` is its length,
- `xjp@r@<ctx>@<i>` holds the character and
- `xjp@n@<ctx>@<i>` holds its index in the block.

A new context opens for an argument read as separate text (a brace group after a class `a` or `b` command) and for an optional `[…]` after such a command (`\__xjyutping_opt_begin:n`). The enclosing run is not flushed, so the text around a `\footnote` carries on in the same run. While `\__xjyutping_flush:` segments the current run, `\__xjyutping_flush_all:` segments every open run, and it is used before a `\setjyutping` (R2-07) and at the end of a pass.

The command table `\g__xjyutping_cmd_prop` is filled with `\__xjyutping_declare:nnnn {commands}{args}{action}{class}`, and unknown commands default to `{0}{}{b}`. The classes are,

| Class | Meaning | Examples |
| --- | --- | --- |
| `t` (transparent) | the run continues | `\textbf`, `\emph`, `\color`, `\textcolor`, size and font switches, `\underline`, the ulem commands, `\label`, `\index`, `\bgroup` (push), `\begingroup` (push), `\egroup` (pop), `\endgroup` (pop), `\alert`, `\structure`, the ctex font switches (`\songti`, `\heiti`, `\kaishu`, `\fangsong`, `\lishu`, `\youyuan`), `\zihao` (1 argument), `\fontsize` (2 arguments), `\footnotemark` (-1) and the xeCJKfntef commands (-1) |
| `a` (aside) | the run continues around the command; its braced arguments are runs of their own | `\footnote`, `\footnotetext`, `\marginpar`, `\setjyutping` |
| `b` (break) | the run ends; braced arguments after it are separate runs | references and citations (arguments copied untouched), `\url`/`\href` (action `url`), `\hyperref` (-1), `\begin` (push), `\end` (pop), `\input` (action `input`), `\xjyutping` (action `manual`), `\xjyutping@mark` (action `mark`), `\disablejyutping` (off), `\enablejyutping` (on) |
| `z` | the run ends, and a following brace group is ordinary text | `\par`, `\item`, `\\` (action `row`), `\tabularnewline`, `\cr`, `\crcr`, `\hline` |

In the command table's `args` column, a value *n* > 0 is the number of mandatory arguments that the skip machine (`\__xjyutping_skip_token:nn`) copies untouched. Optional `[…]`, beamer `<…>` (only when beamer is loaded), `*` and `-` are copied as well. A value of `-1` means optional arguments only. A single unbraced token counts as an argument (`\__xjyutping_skip_other:nn`, R1-44), and for the `url` action a catcode-6 `#` becomes a catcode-12 `#` (R1-06). When the last argument is complete, `\__xjyutping_arg_done:` dispatches the actions `set`, `manual` (measure the syllables), `mark`, `input` and `push` (detect alignment environments).

Beyond this, the walker keeps some further state.
- The owner, `\l__xjyutping_owner_tl`, is the class of the command whose arguments may follow. It is reset to `n` once the arguments are done (R2-21).
- The brace stack `\l__xjyutping_stack_seq` holds `{active}{class}{owner}` for each brace group.
- The semantic stack `\l__xjyutping_sem_seq` holds `{active}{is-alignment}` for `\begin`, `\bgroup` and `\begingroup`, and restores `\l__xjyutping_active_bool` (the walker's view of `\disablejyutping`) at `\end`, `\egroup` and `\endgroup` (R1-36). The state goes back to its enclosing value at `&` (`\__xjyutping_tab:`, R2-25), and at `\\`, `\tabularnewline`, `\cr` and `\crcr` only inside environments listed in `\c__xjyutping_align_clist` (`\__xjyutping_row:`, `\__xjyutping_align_env:n`, R3-04/R3-17).
- The optional-argument stack `\l__xjyutping_opt_seq` has entries of the form `{depth}{owner}{closing char}`. A `]` is tested before the owner, and optional arguments that are still open are closed at group end and at paragraph end (`\__xjyutping_opt_close:n`, R3-03).
- When beamer is loaded, a beamer overlay `<…>` right after a command is copied untouched (`\l__xjyutping_ovl_int`, `\g__xjyutping_beamer_bool`, R3-18).
- A control sequence whose name starts with `xjp@R@` is a mark left by an outer pass (a nested scope, or `\xjyutping*` inside a scope). Such premarked text is copied together with the character that follows it (`\__xjyutping_premarked:`, `\l__xjyutping_raw_bool`), so outer word readings survive (R1-01/R1-23/R1-37).
- `\__xjyutping_input:n` handles an `\input{file}` inside a block. The file is read and walked paragraph by paragraph (`\__xjyutping_walk_file:nn`), and its first paragraph continues the current one. Before that, `\__xjyutping_input_safe:nTF` reads the file line by line as a string (`\ior_str_map_inline:Nn`), strips `%` comments (`\c__xjyutping_comment_regex`) and matches `\c__xjyutping_unsafe_regex`. That regex covers `\endinput`, `\verb`, `\Verb`, `\lstinline`, `\mintinline`, `\DefineShortVerb`, `\MakeShortVerb`, `\lstMakeShortInline`, `\obeylines`, `\obeyspaces`, `\makeatletter`, `\makeatother`, `\catcode`, `\ExplSyntaxOn` and `\begin{…}` with a name containing erbatim, alltt, listing, minted or comment. A match makes the file fall back to a real `\input`, with no word context (R2-02, R2-03, R3-05, R3-08).
- For the no-pad marker, pass 1 records the last Chinese character in `\l__xjyutping_lasthan_int`, and in `\l__xjyutping_gap_bool` whether only invisible material (`t`-class commands, groups) followed it. If the next text token is full-width closing punctuation other than a closing bracket, `\__xjyutping_plain:n` sets `\xjp@np@<n>`, and pass 2 emits `\__xjyutping_nopad:` right after that character (R3-12/R3-21).

### 2.5 Segmentation: dynamic programming and its costs

`\__xjyutping_flush:` segments positions 1…*len* of the current run using `cost[i] = min(cost[i-1] + 100001, cost[i-k] + 100000)` over every word of length *k*. Specifically, a segment costs 100 000 and each single character 1 more. Hence the result has the fewest segments first and then the fewest single characters. The length *k* runs from 2 to `min(i, \__xjyutping_longest:n{i})`, the `\xjp@e@` bound for the character at *i*. A word test (`\__xjyutping_if_word:nnT`) tries the raw spelling first and then the canonical one (`\__xjyutping_can:n` via `\xjp@v@`).

The comparison is `<= best` with *k* ascending, so on a tie the longer final word wins, which gives a backward-maximum-matching bias. The round-1 polyphone audit pointed at this tie-break for errors such as 呢|張床. However, we deliberately did not flip it globally, and we use guard words and run-final readings instead.

The back pointers `xjp@back@<i>` are collected linearly into `xjp@seg@<k>` and emitted in order (R2-24). The emission uses `\use:e`, because one-level expansion passed the macro name (M2-1). `\__xjyutping_emit:nn` handles a single character through `\__xjyutping_lookup:nn` and uses the `f` (final) variant (`\xjp@f@`) when it is the last character of the run. For example, in 你呢？ the 呢 is read ne1. A word takes `\xjp@w@` under its raw or canonical spelling, and its type is `u` if `\xjp@uw@<word>` exists and `w` otherwise.

`\__xjyutping_result:nnn` stores the mark, measures the reading for `width=auto` and appends to the debug log line. `\__xjyutping_measure:n` does the measuring, and its seen-cache `xjp@seen@<reading as string>` holds the block number (R1-39, R1-40). Afterwards the run's `xjp@r@`/`xjp@n@` slots are set to `\relax` (Section 2.10).

With `debug=true` the package writes one line per run, such as `xjyutping> 銀ngan4:w行hong4:w |去heoi3:s |重cung5:m(zung6 cung4) |`. The types are `w` for a reading from the word list, `u` for one from the user, `m` for a guessed polyphone (alternatives in brackets) and `s` for a character with a single reading. Characters typeset without a mark are logged as `xjyutping> [no context] …`, but only if they have a reading (R2-11).

### 2.6 Marks

For each (type, reading) pair, pass 1 creates one macro on demand with `\__xjyutping_combo:nn`, passing the reading through `\tl_to_str:n`. The macro `\xjp@R@<type><reading>` expands to `\xjyutping@mark{<type><reading>}`, and pass 2 puts this single token before each character. This combo mark is the memory-saving replacement for the first version's `\xjyutping@mark{<char>}{<reading>}{<type>}`, which took about 15 tokens per character (R1-08). As a consequence, the mark no longer names its character (R2-09).

`\xjyutping@mark #1` is robust, and it does nothing unless annotation is enabled (R1-13). When annotation is enabled, it first leaves vertical mode, so paragraph-start code (run-in headings, the output routine) runs before the pending mark exists (R2-19). It then stores the mark in `\g__xjyutping_mark_tl`, which the next `\CJKsymbol` consumes.

When a combo mark is written to the `.toc` through `\protected@write`, it expands to the robust `\xjyutping@mark{…}`, which is inert outside a scope. Moreover, `\xjyutping@mark` takes one argument and is listed in `\l_text_case_exclude_arg_tl`, so `\MakeUppercase` does not touch the reading (R1-24).

### 2.7 Typesetting a cell

`\__xjyutping_enable:` saves and replaces these xeCJK hooks, and `\__xjyutping_disable:` restores them,

| xeCJK hook | Replacement |
| --- | --- |
| `\CJKsymbol` | `\__xjyutping_CJKsymbol:n` |
| `\CJKglue` | `\__xjyutping_CJKglue:` |
| `\CJKecglue` | `\__xjyutping_CJKecglue:` |
| `\xeCJK_CJK_and_Boundary:w` | `\__xjyutping_boundary:w` |
| `\xeCJK_CJK_and_FullRight:N` | `\__xjyutping_fullright:N` |
| `\CJKpunctsymbol` | `\__xjyutping_punct:n` |

`\__xjyutping_CJKsymbol:n` takes the reading from the pending mark, or else from `\__xjyutping_lookup:nn` (a "no context" character). It then calls `\__xjyutping_cell:nnn {char}{reading}{type}`, which builds the cell in these steps,
1. If a colour change sits between two cells, add the hsep stretch glue that xeCJK could not add (R3-10)
2. Measure the character (`\makexeCJKinactive` plus the saved `\CJKsymbol`) and build the ruby (`\__xjyutping_ruby:nn`), where
   - the font comes from `\__xjyutping_select_font:`, which caches the font and the whole NFSS state (encoding, family, series, shape and size; R1-19/R1-38) under `xjp@font@<ratio>/<size>/<font>` and makes `\xeCJK@family` a no-op there (R1-33),
   - a strut gives every ruby the same height and depth and
   - `format` is applied, with `multiple` as well for type `m`
3. Compute the pad as (max(uniform, char width, ruby width) + natural width of hsep − char width) / 2
4. Emit `\hbox{}`, which keeps the kern at a line start, and then `\kern pad`
5. Emit `\hbox_overlap_right:n{ \__xjyutping_clearance: \box_move_up:nn{vsep}{ruby centred over the character width} }`, so the ruby has zero width
6. Store the same pad as the pending right pad `\g__xjyutping_pad_dim` and set `\g__xjyutping_cell_bool`
7. Typeset the character last with the saved `\CJKsymbol`, where xeCJK's class machinery expects it (I-3)

The right half of the cell is paid by whatever comes next, and `\__xjyutping_pad:` does the paying. It acts in horizontal mode only (R2-04). If xeCJK's CJK marker node is the last node, the node is removed, the pad kern is added and the node is re-made, so that xeCJK still inserts `\CJKglue`/`\CJKecglue` after it (R2-12/13/26). After a whatsit (a colour pop) the node is re-made too (R3-10). The pad is always zeroed.

How the pad is paid depends on what comes next.
- Before the next character, `\__xjyutping_CJKglue:` pays the pad. Between two cells it then adds only the stretch part of hsep, since the natural part is already inside the cells. This is why a line break never leaves a stray glue at a line start (R1-12/R1-27). Before the first cell, on the other hand, it adds xeCJK's own glue.
- Before Latin text, `\__xjyutping_CJKecglue:` pays the pad and then adds xeCJK's glue.
- Before punctuation, `\__xjyutping_punct:n` zeroes the pad, so punctuation hugs its character (R1-46). `\__xjyutping_fullright:N` calls `\__xjyutping_closing:n`, where
  - closing brackets and quotes (」』）】》〉〕］｝”’〗〙〟｠) pay the pad, which keeps bracket pairs symmetric (R1-29, R2-16),
  - other full-width punctuation drops it and
  - for the long marks —…‥⸺, `\__xjyutping_long_break:` redefines `\xeCJK_allow_break:` once as `\kern pad \penalty0 \kern -pad`. At a break the pad stays at the line end, while mid-line the two kerns cancel (R3-11).
- Before anything else (a command, a box end, a group end), `\__xjyutping_boundary:w` peeks at the next token.
  - At a group end (`}`, `\group_end:`, `\aftergroup`), the payment is deferred with `\group_insert_after:N \__xjyutping_defer:`. However, `\__xjyutping_if_defer:` allows deferral only past plain groups (`\currentgrouptype` 1 or 14) and only when `\l__xjyutping_nodefer_bool` is false, a flag that TikZ node text sets. Otherwise the pad is paid inside the group (R3-01).
    - After the group, `\__xjyutping_defer_test_aux:` defers again if another group end or `\check@icr` follows (R3-09), and looks past `\maybe@ic` (`\__xjyutping_defer_ic:w`, R2-28).
    - Otherwise `\__xjyutping_decide:` sends full-width closing punctuation to `\__xjyutping_closing:n` and pays the pad before anything else.
  - At a `\relax`-like token, the pad is dropped if the token is `\__xjyutping_nopad:` and paid otherwise.
  - At any other token, the pad is paid and `\g__xjyutping_paid_bool` is set.
- At a new paragraph, a `para/begin` hook zeroes the pad (R1-11/R1-28).

### 2.8 Line spacing and clearance

`\__xjyutping_baselineskip:` runs only in the environment. It computes `\l__xjyutping_bls_fp = (vsep + ruby height + 0.6em) / \f@size`, sets `\l__xjyutping_scope_bool`, raises `\baselineskip` and sets `\emergencystretch` to at least 2em (R1-26).

`\__xjyutping_raise_baselineskip:` only ever raises `\baselineskip`. It also rebuilds `\strutbox` (height = baselineskip − 0.25em, depth 0.25em), so tabular rows follow the scope's pitch (R3-16). It is re-applied in two hooks. The first is `\AddToHook{selectfont}`: inside a scope the hook runs `\size@update` first, because LaTeX runs that after the hook and would otherwise undo the raise (R2-05/R2-27). While annotation is on, the hook also reinstalls the package's `\CJKglue`/`\CJKecglue`, which ctex replaces on every size change (R1-03), and `\DeclareHookRule{selectfont}{xjyutping}{after}{ctex}` orders it after ctex. The second is `\AddToHook{para/end}`, for `minipage`, `\parbox` and `p` columns, which reset `\baselineskip` without a font change (R2-32).

`\__xjyutping_clearance:` is an invisible rule inside every ruby, of height vsep + ruby height + a margin. The margin is 0.05em inside a scope when the raised `\baselineskip` is in force, so that framed and coloured boxes do not reach the line above (R2-29). Otherwise it is 0.35em, which applies outside scopes, in alignments where `\baselineskip` is 0 (R3-24) and in minipage, `\parbox` and `p` cells. The paragraphs of these cells are built while `\baselineskip` is still the reset value, since it is raised only at `para/end` (see Section 4, item 13).

`\lineskiplimit` is left at LaTeX's 0pt. From round 1 to round 2 it was -0.3em, and that setting was removed together with the 0.05em clearance.

### 2.9 Plain mode, the output routine, beamer and cross-references

For the output routine, `\AddToHook{build/page/reset}` disables annotation, clears the scope flag and sets `\l__xjyutping_plain_bool`. In plain mode `\xjyutping` prints only its text and `\enablejyutping` does nothing. Running heads and feet are therefore plain even when the page is shipped out from inside a scope, or when a heading contains `\xjyutping` (R1-02, R1-41, R2 status for R1-21/R1-42).

When beamer is loaded, `\AddToHook{cmd/beamer@typesetheadorfoot/before}` does the same. This is due to beamer building and measuring the headline and footline outside the output routine (R3-23). For TikZ, `every text node part/.append code` sets `\l__xjyutping_nodefer_bool` (R3-01).

For nameref, `\label@hook` is prefixed at begin document with `\__xjyutping_unmark:N \@currentlabelname`. This replaces every `\xjp@R@…` token with its one-level expansion `\xjyutping@mark{…}`, using l3regex (`\c__xjyutping_mark_regex`, `\regex_extract_all` and a `\u{…}` replacement). Without it, nameref's sanitised title would be written to the `.aux` as `\xjp@R@wngan4` and read back as `\xjp@R@wngan` followed by `4` (R2-01, R3-02).

For PDF strings, `\__xjyutping_pdfstring:` fills `\pdfstringdefDisableCommands`, where
- `\xjyutping` becomes `\xjyutping@pdf`, which returns only the text,
- `\xjyutping@mark` becomes `\use_none:n`,
- `\setjyutping` becomes `\use_none:nn` and
- `\disablejyutping` and `\enablejyutping` become nothing.

`\__xjyutping_pdfstring:` runs at once if hyperref is already loaded, as with beamer, and otherwise through `\AddToHook{package/hyperref/after}` (R1-05, R1-21, R3-22).

### 2.10 TeX capacity constraints and the design choices they forced

All figures are for the TeX Live defaults, which are a `main_memory` of 5 000 000 words, a save size of 200 000 and a pool size of 5 432 815.

Looking at main memory, the data costs about 2.48M words. Measured per stage, a single scope of 53 060 characters reached up to 3.88M in pass 1 and 4.80M after both passes, before any typesetting. Our responses were,
- one-token combo marks in place of three-argument marks,
- analysing one paragraph at a time and
- freeing per-run data after each run.

After these changes the same scope needs about 3.3M words.

For the save stack, the problem is that creating a control-sequence name inside a group (`\csname` of an undefined name) is a local assignment and costs a save-stack slot. We responded by
- loading the data at top level,
- making the per-character slots `xjp@r@`, `xjp@n@` and `xjp@s@` and the `\tl_build` buffers global and
- setting used slots to `\relax` instead of undefining them, so the name is reused rather than recreated (M1-2).

For the hash and the pool, the problem was the width cache. It originally created one name per (block, reading) pair, which exhausted the pool after about 246 000 pairs, and it now keeps one name per reading, holding the block number (R1-40).

The remaining limits, which are documented in the README, are that
- one paragraph holds about 15 000 characters, since each cell uses about 125 words of node memory,
- one scope holds "well over 100 000 characters" in the README's wording (in the round-2 recheck, 159k compiled while 212k did not) and
- a brace group spanning many paragraphs is analysed in one piece, because the `\par` split does not act inside braces.

### 2.11 `tools/build-data.py`

- `load_lshk()` reads `list.tsv`, the valid syllables in LSHK order. `load_rime_chars()` reads (reading, weight) pairs, where no weight means primary (treated as 100) and otherwise the weight is 5%, 3% or 0%. `rime_rows()` yields the body rows of a rime dict.yaml.
- `pick_default` picks the default reading from these sources, in order,
  1. `CURATED_DEFAULTS`,
  2. rime's primary reading,
  3. rime's top weight (tie broken by LSHK order) and
  4. the first LSHK reading.
- The other readings are those with rime weight ≥ 3, sorted in LSHK order.
- A character is flagged as a polyphone (`\xjp@M` rather than `\xjp@C`) when some other reading has weight ≥ 5 and is not a weaker *changed tone*. A changed tone has the same syllable with tone 1 or 2 while the default's tone is neither, as in 人 jan4 → jan2. Since changed tones belong to words, they alone do not make a character ambiguous. The first rule flagged 6 083 characters and the refined rule 4 188, which rose to 4 349 after the round-1 tweak "weaker than the default" (see colloquial #25 in Section 3.3).
- `load_variants(freq)` builds the variants from the OpenCC HK and TW tables, reversed to variant → standard. It keeps only single-target, single-character mappings where the variant is not itself a standard form, and only those where rime uses the standard form at least as often as the variant. This last filter stopped 參 being folded into 蔘 and 針 into 鍼 (D-2). `CURATED_VARIANTS` (恒 → 恆) is added on top.
- The word list is built from rime's words. A rime word is used if it has at least 2 characters, as many syllables as characters, only known characters and only valid syllables. A word with several readings keeps the one with the highest usage score, which is the sum of log(count+1) of each character's syllable across the word list.
  - `CURATED_WORDS` then overrides or adds entries, with an assert on syllable count and validity.
  - Words ending in 地 read dei2 also get a 哋 alias (麻麻哋).
  - Canonical-spelling aliases are added unless they clash, and the clashes are counted. A word that rime (or `CURATED_WORDS`) spells with a variant form also gets an entry in the canonical spelling, for example 恒生 → 恆生, 群情洶湧 → 羣情洶湧 and 為免 → 爲免. The opposite case, text in a variant spelling with rime's word in the canonical one (因為 in the text, 因爲 in rime), needs no alias, since the walker's own canonical lookup (`\__xjyutping_can:n`) handles it. However, the comment above this code in `build-data.py` gives 因為/因爲 as the example for the aliases, which is the wrong direction.
  - `longest[final char]` is emitted as `\xjp@E`.
- The curated tables are the place to fix data permanently,

  | Table | Contents |
  | --- | --- |
  | `CURATED_DEFAULTS` | Two blocks. The first settles the characters rime leaves undecided: 會 生 行 畫 料 咪 咯 率 刊 撈 彙 嗎 嘎 咧 (from the initial build) and 量 (round 1). The second overrides defaults found wrong in review round 1: 返 faan1, 呀 aa3, 驚 geng1, 吓 haa5, 爭 zaang1, 划 waa4, 幢 zong6, 呢 ni1. |
  | `CURATED_FINALS` | 呢 → ne1 at the end of a run. |
  | `CURATED_VARIANTS` | 恒 → 恆. |
  | `CURATED_WORDS` | 135 entries (102 from round 1, 行長 while writing the manual, 32 from round 2): rime errors (畀咗 family, 相處, 前人種樹 …); literary guards for changed defaults (返回, 驚聞 …); missing words; guard words that stop a new entry capturing a phrase it should not (集中咗 for 中咗, 絕種咗 for 種咗, 16 guards for 平啲). |

- At 1.0.0 the builder wrote `xjyutping-chars.def` and `xjyutping-words.def` next to the package. After 1.0.0 we changed the output paths to `xjyutping-tex/`, and the builder now also writes TSV tables for the Python port (see Section 6).

---

## 3. Development log

### 3.0 Research and data (09:32–10:04)

We read `xpinyin.dtx`. Its approach is the same as ours, which is to hook xeCJK's `\CJKsymbol`. We also studied xeCJK's interchar classes and its punctuation code, as well as the l3kernel's `\tl_analysis_map_inline:nn` and `\tl_build_*`. Furthermore, we sampled polyphones in LSHK and rime. Of the characters that rime lists with several readings, 60 have no primary reading, and the frequent ones among them (生 到 上 行 會 數 長 重 當 …) were given curated defaults where needed.

The findings and fixes in the data builder were as follows.

D-1. The first variant analysis used a wrong `grep` pattern, so every pair counted 0. We redid the analysis in Python. This was an analysis mistake rather than a shipped bug.

D-2. The variant folding was wrong. The raw OpenCC reversal mapped common characters onto rare ones (參→蔘, 針→鍼), which gave 77 mappings and 272 aliases. This was because OpenCC maps both directions and a character can be both a standard form and a variant. We fixed it with `load_variants(freq)`, which keeps a mapping only when rime prefers the standard form. The result was 75 mappings and 59 aliases, which we verified by listing the `\V` lines.

D-3. Since `jyut6ping3.phrase.dict.yaml` has no readings, we dropped it.

D-4. A polyphone flag based on "more than one significant reading" flagged 6 083 characters, including changed tones (人 jan2) and rare readings. We refined it into the changed-tone rule, which gave 4 188. This refinement was made at 10:17, after the first compile, rather than during the research phase.

### 3.1 First implementation (10:06–10:17)

The first `xjyutping.sty` (27 KB, written at 10:06) was a single-pass preprocessor. Its parts were,
- a skip-list property for reference commands, `\c__xjyutping_skip_prop`, built with `\prop_const_from_keyval:Nn` (the pre-compile patch replaced this property with `\g__xjyutping_skip_prop`),
- a three-argument mark `\xjyutping@mark{char}{reading}{type}`,
- the dynamic-programming segmenter and
- a fixed cell, in which each character was centred in an `\hbox_to_wd:nn` of the cell width with the ruby as an overlay inside it, and `\CJKglue` was replaced by plain hsep glue.

There was no pending right pad yet. It came with the I-3 restructuring (10:13), where the right half was left pending and paid only by the next `\CJKglue`.

Before the first compile, a patch (10:08) fixed these six problems,
- an invalid message-function variant (`\msg_warning:nnnenn` → `:nneeee`),
- the skip-table value format,
- the `\prop_get` lookup,
- the boolean restore on the brace stack,
- the key used to detect user words (`\__xjyutping_word_cs:nnN` replaced by `\__xjyutping_word:nnN`, with the `xjp@w@` prefix at the call sites) and
- width-cache names shared across nested blocks (made per block).

The main agent's reasoning at that point says it found these by reading back its own draft. The item numbers in the patch comments ("1/32", "8/48", "2/3/46", "28") are not explained anywhere. They are probably the numbering of that self-review, although this is unverified.

The first compile of `tests/basic.tex` found the following problems.

I-1. A digit inside a variable name gave `! LaTeX Error: Missing \begin{document}` at `\tl_new:N \l__xjyutping_buf_0_tl`. This was because digits are not letters under expl3 catcodes, so the token was `\l__xjyutping_buf_` followed by the text `0_tl`. We fixed it with `c`-type variants (`\tl_new:c { l__xjyutping_buf_0_tl }`, `\tl_build_begin:c` and so on).

I-2. The compile gave `! Font \__xjyutping_strut:=ngo5 not loadable`. This was because the font cache stored the `\font` primitive, as `\cs_gset_eq:cN {key} \tex_font:D` saved the primitive rather than the current font. We fixed it by caching the NFSS font name `\curr@fontshape/\f@size`, and this was later replaced by the full NFSS-state cache (R1-19).

I-3. Boxing the character broke xeCJK, giving `! Missing number, treated as zero` inside xeCJK's punctuation-width code (`\c__xeCJK_xeCJK/SongtiTC(0)/m/n/10/quanjiao/dim/rule/right…`), which was isolated to `行，`. The session's compaction summary calls the error "Missing }", while the log in the transcript shows "Missing number". The cause was that the first cell layout typeset the real character only inside boxes built in the hook (`\hbox_to_wd:nn` around a `\makexeCJKinactive` character box, with the ruby overlay). The main agent's reasoning at 10:10 gives the diagnosis. Specifically, XeTeX's last-character class tracking is thrown off when the character is boxed inside the hook, which unbalances xeCJK's class groups, and xpinyin avoids this by typesetting the real character last, at the outer level. The diagnosis was checked by reading xeCJK's class-group code (`\xeCJK_class_group_begin:`/`_end:`), not by a separate experiment. We fixed it by restructuring the cell into the layout of Section 2.7, in which the character is typeset last with the saved `\CJKsymbol`, the ruby is a zero-width overlay, the left half-pad is a kern after an empty box and the right half is left pending.

I-4. The renders showed that the right pad was lost before Latin text and that rubies came near the line above. We made `\__xjyutping_CJKecglue:` pay the pad as well and raised the line spacing.

I-5. Rubies could touch the line above, and the environment's `\baselineskip` was not applied. We added `\__xjyutping_clearance:`, an invisible rule 0.35em above the ruby, and the baselineskip factor became vsep + ruby + 0.6em. The environment now ends with `\par`, so its `\baselineskip` applies to its last paragraph.

I-6. Proofreading needed the alternative readings. The `\M` loader (renamed `\xjp@M` in M1-2) now also stores them, and debug lines show `m(alt …)`. This was done at 10:16 together with D-4.

The session summary also lists "ExplSyntax spaces in the data" as an early issue. However, since the first version already set the space catcode and `\endlinechar=-1` around `\file_input:n`, no separate event can be identified.

We measured a random 19 926-character, 52-page document, which compiled in 4.7 s. We then wrote the README, which became the reviewers' specification.

During round 1 we drafted the manual `xjyutping-doc.tex` and trial-compiled it in the scratchpad. We added `\marg`/`\oarg`, replaced `\XeLaTeX{}` by `Xe\LaTeX{}` and changed the examples to 重未 → `\setjyutping{重未}{zung6 mei6}` and `width=2em`. At 11pt, `1.6em` (17.5pt) is narrower than the auto width (20.6pt), so it looked "too narrow", but this was not a bug. Later, at 11:47 (after the round-1 fixes), we set `\setlength\emergencystretch{3em}` in the manual's preamble for two overfull lines caused by long typewriter words.

### 3.2 Review process (common to all rounds)

Each round was a Claude Code workflow in which several finder agents ("lenses") ran in parallel, and the findings of each lens went to an adversarial verifier. Specifically, the verifier had to reproduce every finding in its own directory and decide `confirmed`, `modified` (real, but with a corrected fix) or `rejected`, and it was told to default to rejected when unsure. The finders and verifiers could not edit the package. Instead, they wrote repro `.tex` files in `tests/<lens>/`, which have since been moved to `scratchpad/review-artifacts/`.

The main agent then went through these steps,
1. Implement the fixes
2. Recompile every repro from the round (`repros.py`/`repros2.py` compile twice and count `^!` errors, overfull boxes and `[no context]` lines)
3. Re-run the reading-audit corpora and compare each finding with the new reading
4. Render layout cases to PNG, or dump boxes

Round 2 also re-checked every round-1 finding with a separate "recheck" lens per original lens, which reported each finding as fixed, partly-fixed, now-documented or not-applicable.

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

We did not re-measure the accuracy as a percentage after the fixes. Instead, we looked up each kept finding's span in the recompiled corpus and compared it with the expected reading. Every data-fixable finding passed except 平啲, which was deferred to round 2. The checker script could not locate 划算 / 划船, whose span was written with a slash, so the session never checked it. For this write-up we re-checked it against the 1.0.0 snapshot with the finding's sentence (呢個價錢好划算，我哋去划船。), and both 划 are waa4, from the new default (type `m`). 發佈會 and 揣度 were reported as mismatches only because the expected field contained "(or …)", and their new readings are the expected ones.

The data fixes were made in `tools/build-data.py` and applied at 11:11.
- The second block of `CURATED_DEFAULTS` sets,
  - 返 faan1, guarded by 返回, 返鄉, 返航, 返程, 返還, 返國, 積重難返 (faan2),
  - 呀 aa3, plus 係呀 hai6 aa3, while the other aa4 words in rime (咩呀 …) were kept as genuine challenging particles,
  - 驚 geng1, guarded by 驚聞, 驚見, 驚爆, 驚現, 驚叫, 驚傳, 驚變, 驚艷, 驚悉 and 大吃一驚,
  - 吓 haa5 (aspect marker), with the accepted cost that the interjection 吓？ becomes haa5,
  - 爭 zaang1, 划 waa4 and 幢 zong6,
  - 量 loeng6, guarded by 量體溫 and 量血壓 (loeng4) and
  - 呢 ni1.
- `CURATED_FINALS` makes 呢 read ne1 at the end of a run. The verifier had rejected simply changing 呢's default to ni1, because the sentence-final particle ne1 (點解呢) would break. The implemented alternative is a new mechanism, a run-final reading (`\xjp@F`, the `f` argument of `\__xjyutping_lookup:nn`). It gives 呢張床 ni1 and 你呢？ ne1, and both are in `regression.expected`.
- `CURATED_VARIANTS` maps 恒 to 恆 (恒生).
- `CURATED_WORDS` (102 entries) corrects rime errors and adds missing words. The rime errors are 畀咗 and 6 longer forms (rime read 咗 as saai3), 有朋自遠方來, 相處/共處 (cyu5), 前人種樹, 少壯, 少壯不努力, 世上無難事, 屢見不鮮, 會唔會, 幾度 (gei2), 揣度, 間房 (gaan1) and 成日 (seng4). The missing words are 好正, 好精, 把聲, 好平, 咁平, 最平, 平嘢, 瞓唔到覺, 成個鐘, 成身, 成間, 彈琴 (and 4 other instruments), 張相, 相集, 着咗件, 着衫, 着多件褸/衫, 著住, 訂位, 訂枱, 冇位, 問下 (guards 問下個月 and 問下個禮拜), 今晚會, 聽晚會, 琴晚會, 行車線, 而行, 恒生, 不亦說乎, 中咗 (guard 集中咗), 人話 (guards 講人話, 唔講人話), 發佈會, 發布會, 調高 (guard 強調高), 數吓, 數完, 應聘, 個名, 頂帽, 上咗, 乾隆, 朝住, 種咗 (guard 絕種咗), 畫咗, 屏住, 屏息, 盛飯 and the 量 compounds.
- The aliases give every word ending in 地 read dei2 a 哋 twin (麻麻哋). The builder does not print how many there are. When we recomputed the count for this write-up, it came to 82 at 1.0.0 (83 in round 1, when 輕輕哋 was still an alias rather than a curated word). The "103" printed in the transcript by `grep -cF "哋="` counts every word ending in 哋, including rime-cantonese's own 20 (我哋, 佢哋 …).
- The polyphone flag rule now lets a changed tone exempt a character from the flag only when that tone is weaker than the default. 數 is now flagged `m` (colloquial #25, where there is no reading change but it can be highlighted), and the number of flagged characters went from 4 188 to 4 349. While the verifier had predicted only 7 newly flagged characters (扒 數 到 桿 嗎 妹 宅), our recomputation for this write-up with the 1.0.0 builder shows that the rule change accounts for 158 new flags. These are 8 characters with rime weights and 150 LSHK-only characters, where every reading counts as weight 100, so their changed tones are never "weaker" and now flag the character.

M1-0. While making these changes we found a builder bug. The weight lookup raised `KeyError: 'haa5'`, since a curated default can be a reading that rime does not list (吓 haa5 comes only from LSHK). We fixed it with `weight.get(default, 100)`.

We left these genuinely ambiguous cases unfixed, for a user override,
- 為 wai4/wai6 (旨在為基層),
- 同行 tung4 hong4 versus hang4,
- 當 (我當佢係) dong3,
- 背得 bui6 and
- 散晒 saan3 (dispersing) against saan2 (fallen apart), where rime has only saan2 saai3.

The verifiers rejected 8 findings.
- 個女 neoi2, 本會 wui6 and changing 呢's default to ni1 were unsafe fixes, although the error was real or plausible. The word 個女 would capture 我個女朋友 …, and for 本會 the tie-break would give 根|本會, 日|本會 … wui6. The 呢 change is discussed above.
- 差強人意 koeng4, 參差 cam1 and 劃龍舟 waa4 were accepted variants or doublets.
- Polyphones #31/#32 were doublets that duplicate accepted findings. They asked for 成個鐘/成日 seng4 and were rejected because sing4 is also heard. However, the same spans from the colloquial audit (#9, #12) were confirmed, so seng4 was added anyway.

We deferred 平啲 (colloquial #14) to round 2. The verifier kept the default ping4 and asked for the word entries 好平, 咁平, 最平 and 平嘢, which were added in round 1, while 平啲 itself stayed ping4 until round 2.

#### Bug findings (46; one rejected)

Unless noted, each fix came with the 11:18–11:22 rewrite of `xjyutping.sty`, which grew the file from 27 KB to 46 KB. The rewrite introduced,
- the two-pass walker and command table,
- combo marks,
- right-pad payment at CJK/Boundary,
- local `\setjyutping` while reading,
- `\input` reading,
- the NFSS font cache,
- the clearance and line-spacing hooks,
- output-routine disabling and
- PDF-string handling.

For each finding, the recheck status is the one reported by the independent round-2 recheck lens.

Findings R1-01 to R1-13 came from the robust-structure lens.

R1-01 (high). A nested scope lost the word context. An inner scope read 銀行 as ngan4 haang4, and every character was logged twice. This was because `\xjyutping@mark` was not in the skip list, so the inner pass marked the mark's own arguments. The fix makes the walker recognise existing marks (`\__xjyutping_premarked:` for `\xjp@R@…` tokens and the `mark` action for `\xjyutping@mark`) and copy each with its character. The recheck reported it fixed.

R1-02 (high). When a page was shipped from inside a scope, the running heads were annotated, in uppercase. This was because the output routine ran inside the scope group with the replaced `\CJKsymbol`, and `\MakeUppercase` changed the readings. The fix is `\AddToHook{build/page/reset}{\__xjyutping_disable: …}`. The recheck reported it fixed (headings and fancyhdr), and the `\headheight` warning is gone.

R1-03 (high). Size changes in ctexart removed the cell spacing, so rubies overlapped. This is due to ctex redefining `\CJKglue` on every size change. In round 1, paying the pad at CJK/Boundary removed the overlap. The recheck reported it partly fixed, since the stretch was still ctex's glue (16 underfull boxes). It was completed in round 2, where the `selectfont` hook reinstalls the package glue, ordered after ctex.

R1-04 (medium). A `\setjyutping` in a scope changed the text before it, and it acted even in dead code. This was because the preprocessor executed `\setjyutping` globally while reading the whole body. With the fix, settings made while reading are local to the reading group (`\__xjyutping_set:nnn … {}`), and the global setting happens at typeset time, at its position. The recheck reported it partly fixed, since settings inside `\iffalse` or an unused `\newcommand` still apply to later text in the same scope. This was documented in the README in round 2.

R1-05 (medium). PDF bookmarks contained the reading or a stray `*`. We fixed this with `\xjyutping@pdf` and the other entries in `\pdfstringdefDisableCommands`. The recheck reported it fixed (the `.out` decodes to plain text, with 0 warnings).

R1-06 (medium). Inside a scope, a `\url`/`\href` containing `#` broke, and `%` ended the file. This is due to the `+b` body being already tokenised. The action `url` now turns catcode-6 `#` into catcode-12 `#`, while for `%` the documentation says to write `\%`. The recheck reported it fixed for `#`, with `%` documented.

R1-07 (medium). Text from `\input`, macros or `\maketitle` ignored the word list. An `\input` inside a scope is now read and walked (`\__xjyutping_input:`), while macro and `\maketitle` text is documented and logged as `[no context]`. As the verifier advised, `\include` is left alone. The recheck reported it fixed.

R1-08 (medium). One large scope exhausted main memory (63k per the finder, while the repro has 53 060 Han characters). For the fix, see M1-2 and M1-3 below and Section 3.7. The recheck reported it partly fixed (53k OK at 3.32M words, 159k OK, 212k fails), and the limits were documented in round 2.

R1-09 (low). The TOC was annotated when `\tableofcontents` was inside a scope. We corrected the README, which now says that the TOC is annotated only if `\tableofcontents` is itself in a scope. The recheck reported it as now-documented.

R1-10 (low). The last character's ruby stuck out of `\fbox`, and `c` cells were off-centre. This was because the right pad was paid only by a following glue. The fix pays the pending pad at xeCJK's CJK→Boundary transition (`\__xjyutping_boundary:w` wrapping `\xeCJK_CJK_and_Boundary:w`). The finder's first idea, a kern after the glyph, was shown by the verifier to destroy xeCJK's break points. The recheck reported it fixed.

R1-11 (low). The pending pad leaked across paragraphs, items and cells. It is now paid at the boundary, and the `para/begin` hook zeroes it. The recheck reported it fixed.

R1-12 (low). After a break at full-width punctuation, the next line started with stray glue. This was because the empty `\hbox` after the pad kern stopped the glue from being discarded at the break. We changed `\CJKglue` so that it adds only stretch, while the natural hsep lives inside the cells. The recheck reported it fixed (every line starts `\hbox{} \kern`).

R1-13 (low). A stale mark from outside a scope (TOC, heads) set the reading of a later macro character. Now `\xjyutping@mark` does nothing unless enabled, and the mark is cleared in `\__xjyutping_enable:`. The recheck reported it fixed.

Findings R1-14 to R1-25 came from the robust-tokens lens.

R1-14 (high). Chinese label keys in `\hyperref[…]`, `\cpageref` and `\labelcref` gave `Missing \endcsname`. We added the cleveref and hyperref commands to the table, where `\hyperref` uses `-1` (optional arguments only), so the link text is still annotated. The recheck reported it fixed (the errors went from 78 to 0). It also noted a gap outside this finding, as natbib `\citeauthor`, `\citeyear`, `\citealp` and the name argument of `\pdfbookmark` were still annotated. The natbib commands were added in round 2 (R2-23), but `\pdfbookmark` never was (see Section 4, item 17).

R1-15 (high). Rubies overlapped at `\color`, `\textcolor`, `\mbox`, `\href` and image boundaries. The pad is now paid at CJK/Boundary, while the finder's "pay at the next cell" was rejected by the verifier. The recheck reported it fixed (glyph positions measured with Ghostscript `txtwrite`).

R1-16 (high). Adjacent `\xjyutping`/`\xjyutping*` outside a scope overlapped. This was because `\__xjyutping_enable:` zeroed the previous call's pending pad, and the pad was never paid after the group. The fix is boundary payment inside the group. The recheck reported it fixed.

R1-17 (medium). A brace group or formatting command split a word (銀\textbf{行} → haang4). The two-pass walker fixed this with transparent (`t`) commands and transparent groups. The recheck reported it fixed.

R1-18 (medium). Macro or `\input` text had no word context and no `width=auto`. As with R1-07/R1-32, `\input` was fixed and macros were documented. The recheck reported it as now-documented.

R1-19 (medium). With `format=\itshape` or `\bfseries`, rubies were printed at full text size. This was because the cached branch restored only the font, not `\f@size`. The cache now restores the font, encoding, family, series, shape and size. The recheck reported it fixed (ruby 4.48pt).

R1-20 (medium). Markup in a reading (`zung\textsuperscript{1}`) gave `Missing \endcsname`. This was because the reading was used inside `\csname`. The seen-cache key and the combo names now use `\tl_to_str:n`. The recheck reported it fixed.

R1-21 (medium). An `\xjyutping` in a `\section` title put the reading into bookmarks and rubies into the TOC. The bookmarks were fixed via `\xjyutping@pdf`. The recheck reported it partly fixed, since the TOC and running heads were still annotated. In round 2 the running heads became plain (plain mode), and the TOC behaviour for an explicit `\xjyutping` was documented.

R1-22 (medium). The keys of `\hyperlink`/`\hypertarget` were annotated, so links were silently broken. We added both to the table with 1 argument. The recheck reported it fixed (the PDF destination matches).

R1-23 (medium). Annotated text that was preprocessed twice lost its context (`\jp{銀行}` macro, nested scope). It had the same fix as R1-01. The verifier showed that simply skipping the mark's 3 arguments was not enough. The recheck reported it fixed.

R1-24 (low). `\MakeUppercase` uppercased the Jyutping. We fixed it with a one-argument mark that is excluded from case changing. The recheck reported it fixed.

R1-25 (low, REJECTED). `\setjyutping{為}` did not apply to 爲. The verifier found this consistent with the README, since variant folding is for word lookup only. The recheck marked it not-applicable.

Findings R1-26 to R1-33 came from the layout lens.

R1-26 (high). Lines were overfull at narrow widths and large sizes, with 110/315 lines in a width sweep at normal size and 9 of 21 lines in `punct-break.tex`. This was due to rigid cells with only `0.15em plus 0.15em` of stretch and no `\emergencystretch`. The fix sets the default `hsep = 0.15em plus 0.4em` and `\emergencystretch` ≥ 2em in scopes. The main agent verified it with 0 overfull or underfull boxes in `punct-break`, `frame-huge` and `real-a5paper`. The recheck sweep over 21 widths from 5 to 10cm gave 0 overfull lines for,
- normal size, 320 lines (was 110 overfull),
- `\large`, 389 lines (was 155),
- `\Huge`, 246 lines (was 93) with 16 underfull and
- `width=natural` and `width=1.3em`.

The recheck reported it fixed.

R1-27 (medium). After a break at a closing mark, the next line began with hsep glue, in about 9% of lines. It had the same fix as R1-12. The recheck reported it fixed (0 of 1 625 lines).

R1-28 (medium). A stale right pad widened the first Latin-to-Chinese gap of the next paragraph. The fix is the zeroing in `para/begin` together with boundary payment. The recheck reported it fixed.

R1-29 (medium). The spacing inside 「…」 and （…） was uneven. `\__xjyutping_fullright:N` now pays the pad only before closing brackets and quotes, while other punctuation keeps hugging. The verifier rejected paying before all FullRight marks. The recheck reported it partly fixed, since it failed when the character before the bracket ended a group. It was completed in round 2 (R2-16/R2-30).

R1-30 (medium). An inline `\xjyutping*` had space on the left and none on the right. Boundary payment restores the right pad. The recheck reported it partly fixed. While the natural widths were symmetric, the stretch was not (xeCJK's 0.08\baselineskip on entry against the package's 0.4em on exit). Round 2 rewrote the deferred path so that after a group the pad is paid and xeCJK inserts its own glue (node restored), but the transcript does not re-measure this. Re-running `inline-asym.tex` against the 1.0.0 snapshot for this write-up shows `去 glue 0 plus 1.44 | pad 銀 … 行 pad | glue 0 plus 1.44 攞`. Both sides now carry xeCJK's glue, so this is resolved at 1.0.0.

R1-31 (low). The line pitch was not constant, since after a deep line or a size command inside the scope the spacing fell back to `\lineskip`. The round-1 fix set `\lineskiplimit -0.3em` and re-raised `\baselineskip` in the `selectfont` hook. The recheck reported it partly fixed, since deep lines were fixed but size changes were still undone by `\size@update`. It was completed in round 2 (R2-05/R2-27), where `\lineskiplimit` went back to 0pt with a 0.05em clearance (R2-29).

R1-32 (medium). Macro or `\input` text lost its word context, and `width=auto` fell back to natural widths. We fixed `\input` in round 1 and added the `width=auto` fallback (measure `gwong2`) in round 2. The recheck reported it partly fixed, and it was then completed in round 2.

R1-33 (low). `font=\sffamily` raised a spurious xeCJK "Unknown CJK family" warning. We fixed it with `\cs_set_eq:NN \xeCJK@family \use_none:n` in `\__xjyutping_select_font:`. The recheck reported it fixed.

Findings R1-34 to R1-46 came from the code-review lens.

R1-34 (high). When a space, `~`, `\ ` or `\,` separated two annotated characters, the right pad was lost, so rubies overlapped. Boundary payment now puts the pad before the separating glue or kern, and the verifier's corrected version also moves the penalty of `~`. The recheck reported it fixed.

R1-35 (high). Two adjacent manual `\xjyutping` overlapped. It had the same fix as R1-16, and the recheck reported it fixed.

R1-36 (medium). In the preprocessor, a `\disablejyutping` inside an environment or `\begingroup` leaked into the rest of the scope. The semantic stack now pushes and pops the walker's active flag on `\begin`/`\end`, `\begingroup`/`\endgroup` and `\bgroup`/`\egroup`. The recheck reported it fixed.

R1-37 (medium). A nested `\xjyutping*` or scope re-segmented marked text. It had the same fix as R1-01, and the recheck reported it fixed.

R1-38 (medium). The font cache ignored `\f@size` for `multiple=`/`format=` font switches. It had the same fix as R1-19. The verifier noted that restoring only `\f@size` was incomplete, hence the whole NFSS state is restored. The recheck reported it fixed.

R1-39 (medium). During measurement, a reading containing a command was put inside `\csname`. It had the same fix as R1-20, and the recheck reported it fixed.

R1-40 (medium). Every block permanently added one csname per distinct reading (201 blocks added 5 600 names, with exhaustion at about 420k names). The fix keeps one `xjp@seen@<reading>` per reading, which holds the block number. The recheck reported it fixed (174 040 names for both the 1-block and the 201-block files).

R1-41 (medium). Running heads had rubies and uppercased readings. It had the same fix as R1-02, and the recheck reported it fixed.

R1-42 (low). A manual `\xjyutping` in titles affected the bookmarks and the TOC. This is the same as R1-21. The recheck reported it partly fixed, and it was completed in round 2 (plain running heads, TOC documented).

R1-43 (low). `\hyperref[銀行]{…}` inside a scope gave an error. It had the same fix as R1-14, and the recheck reported it fixed.

R1-44 (low). A one-token unbraced argument received the mark (`\textbf 行`, `\setjyutping 行{hong4}`). Table commands now take a single unbraced token as an argument (`\__xjyutping_skip_other:nn`), while for other commands the README says to use braces. The recheck reported it fixed.

R1-45 (low). `\input` text was annotated without word context. It had the same fix as R1-07, and the recheck reported it fixed.

R1-46 (low). An unspent pad went stale and widened a later gap (行。ABC字). The `\CJKpunctsymbol` wrapper now zeroes the pad before punctuation and adds no nodes. The verifier showed that the finder's "pay after the punctuation" broke xeCJK's compression of consecutive punctuation. The recheck reported it fixed (equal widths, with the 。」 compression kept).

Over the 46 round-1 findings, the recheck totals were 34 fixed, 9 partly fixed, 2 now documented and 1 not applicable.

#### Follow-up changes during round-1 fixing (11:24–11:48)

A first attempt at handling the pad at a group end recorded `\currentgrouptype` at xeCJK's class-group start. It was replaced the same minute by the after-group peek (`\__xjyutping_defer:` → `\__xjyutping_defer_test:`), in which the decision to drop or pay the pad is made from the token after the group. This keeps `{\color{red}長}，` hugging while `\mbox{長}` pays inside the box.

We added class `z` for commands without arguments (`\par`, `\\`, `\item` …), so that a brace group after them is ordinary text rather than an argument.

M1-1. The rewrite brought a regression with `#` in the body, which gave `! Illegal parameter number in definition of \__int_map_1:w` in `repro-url.tex`. This was because the body was passed straight into a mapping function. We fixed it by storing the body in `\l__xjyutping_body_tl` and walking it via a `:V` variant. Rerunning the repro verified the fix.

M1-2. The save stack overflowed (`! TeX capacity exceeded, sorry [save size=200000]`). The overflow appeared when per-run data began to be freed inside the reading group. Each of the following steps was measured on the 53k repro,
1. Make the per-character slots global (still overflowing)
2. Use global `\tl_build_gbegin/gend` (still overflowing)
3. Load the data at top level with internal loader names (a small test's save stack went from 140 558 to 407 entries, but the repro still overflowed)
4. Set the slots to `\relax` instead of leaving them undefined (compiles, with 54 180 save-stack entries)

M1-3. After step 4 the repro used 4.88M words of main memory. A stage breakdown on scratch copies gave 2.48M for the base, 3.88M with pass 1 and 4.80M with both passes. Per-paragraph analysis brought it down to 3.32M words (12.6 s, 140 pages).

M1-4. `\seq_set_split` strips braces. A test showed that the l3 split turns `{\bfseries C}` into `\bfseries C`, so we use a custom splitter with a `\prg_do_nothing:` guard (`\__xjyutping_split:w`).

M1-5. At 11:48, while building the manual (round 2 was already running), we found that 係\textcolor{red}{行}長 read haang4. The walker was correct (one run), but the data lacked the word 行長, so we added 行長 hong4 zoeng2 to `CURATED_WORDS`.

A background repro job was also started against an older package version and buffered its output. It was killed and rerun (`repros.py`, skipping the multi-minute memory tests).

In the verification of round 1,
- every repro recompiled with 0 errors, and the only non-zero counts were `\showbox` "OK" pseudo-errors,
- the layout stress files had 0 overfull or underfull boxes,
- the three audit corpora compiled without errors (129, 158 and 202 runs logged) and
- the README was rewritten to match, since it is the spec for round 2.

### 3.4 Review round 2 (findings 11:47–12:33; fixes 12:36–12:49)

#### Reading audits

| Corpus | Sentences | Characters | Wrong | Accuracy | Findings |
| --- | --- | --- | --- | --- | --- |
| learner textbook dialogues | 80 | 890 | 6 | 99.3% | 6 (5 confirmed, 1 modified) |
| mixed HK reading material | 77 | 1 438 | 8 | 99.4% | 8 (4 confirmed, 4 modified) |

The fixes by data, in `CURATED_WORDS`, were made at 12:36, and we checked them by looking up each span in the recompiled corpora, where all of them matched. They are,
- 平啲 peng4 di1, with 16 guard words for X平+啲 (公平啲, 持平啲, 水平啲, 太平啲, 和平啲 …), since the verifier showed that without the guards the tie-break turned 13 correct ping4 contexts into peng4;
- 做邊行 hong4;
- 轉咗工 zyun3;
- 一唱一和 wo6;
- 成個人, 成個人生, 成件事 (and 件事), 成頭家 (seng4);
- 小心地滑 (a segmentation fix);
- 輕輕 hing1 hing1, 輕輕地, 輕輕哋 heng1; and
- 為配合, 為確保, 為免 (wai6), for which the verifier advised against adding 為方便.

The ambiguous cases, 彈得 taan4, 種花 zung3, 假 gaa3 in 請咗三日假, 長得 zoeng2 and 為 in other contexts, were left for us to decide.

#### Recheck-lens findings (16 new problems found while re-checking round 1)

- R2-01 (high). `\nameref` broke for sections and captions inside a scope, a problem that was also reported as R2-06, R2-18 and R2-33. Such a reference gave `Undefined control sequence \xjp@R@wngan` and stray tone digits on every run, whether it stood before or after the scope. This is due to nameref detokenising the title into the `.aux`, so that `\xjp@R@wngan4` is read back as `\xjp@R@wngan` followed by `4`, and the combo macros are also undefined before the scope that creates them. The round-2 fix put `\cs_if_exist_use:N \GTS@expandtrue` in `\__xjyutping_enable:`, which makes gettitlestring expand titles and so turns the marks into `\xjyutping@mark{…}`. However, this fix caused R3-02, and in round 3 we replaced it with `\__xjyutping_unmark:N` in `\label@hook`. `regression.tex` contains `\nameref{sec:a}` and has compiled without errors from round 2 on.

- R2-02 (high). An `\endinput` in an `\input` file aborted the whole job, which was also reported as R2-08 and R2-17. The cause was that the file was inlined with `\file_get:nnN`, so the `\endinput` later ran against the main file. The fix is the safe-file check, under which files containing `\endinput`, verbatim or catcode changes fall back to a real `\input`. The verifier noted that cutting the file at the first `\endinput` is wrong for guards such as `\ifdefined…\endinput\fi`.

- R2-03 (medium). `\input` files could no longer contain `\verb`, verbatim or a `%` in a URL, although this had worked before the rewrite. The same fallback fixed it, and the README documents the restrictions.

- R2-04 (low). A primitive `\setbox0\hbox{銀行}` between paragraphs added a stray empty line. This was due to the deferred pad (`\kern` plus `\hbox{}`) being paid in vertical mode. After the fix, `\__xjyutping_pad:` pays the pad only in horizontal mode (`\mode_if_horizontal:T`) but always zeroes it. This zeroing in math mode later contributed to R3-06/R3-13/R3-20.

- R2-05 (low). `\size@update` undid the raise from the `selectfont` hook, which left the ruby lines cramped in ctexart. We fixed this by running `\size@update` inside the hook before `\__xjyutping_raise_baselineskip:`, and a check with `vdump.sh` on `r-size-inside.tex` showed that all interline glue is `\baselineskip`.

- R2-06 is a duplicate of R2-01.

- R2-07 (medium). A `\setjyutping` in the middle of a run changed the text before it and missed the text after it, and it is a duplicate of R2-20. This was because class `a` kept the run open, and the local setting was applied before the run was segmented. The fix calls `\__xjyutping_flush_all:` before the local set, which segments every open run, including the one around a footnote. `reg-setjyutping-midrun` now logs `銀ngan4:w行hong4:w | 行hang4:u`, and the last line of `regression.expected` covers it.

- R2-08 is a duplicate of R2-02, and the same fallback handles its `\makeatletter`-in-file part.

- R2-09 (low). A manual reading on a non-Chinese character leaked to the next unmarked character. The cause is that the new marks no longer name their character, and we fixed it with `\group_insert_after:N \__xjyutping_clear_mark:` in `\__xjyutping_manual:nn`.

- R2-10 (low). A long `\input` file ran out of memory where the same text inline did not. The fix splits the file into paragraphs and walks it like the body (`\__xjyutping_split_pars:NV` and `\__xjyutping_walk_file:nn`).

- R2-11 (low). The debug log showed `[no context]` lines for characters without a reading (／, Ａ, 𠮷). The log now records a line only when a reading exists.

- R2-12 (medium). A group-final character got no glue before the next character, so there was no stretch and no break there, and the same problem was also reported as R2-15 and R2-26. The cause was that the deferred pad was paid after xeCJK's CJK node, so xeCJK no longer saw a preceding CJK character. The fix makes `\__xjyutping_pad:` remove the node, pay the pad and re-make the node (`\xeCJK_if_last_node:nTF`, `\xeCJK_remove_node:` and `\xeCJK_make_node:n`). In the repro rerun, the reviewers' `r-adjacent-manual.tex`, which had been overfull by 37.5pt and 60.8pt, and `r05-group-nobreak.tex` recompiled with 0 errors and 0 overfull boxes. `pad2.tex` (now `tests/layout-check.tex`) keeps an 18-call chain of `\xjyutping{…}{…}` as a standing check.

- R2-13 (low). A group-final character lost `\CJKecglue` and the break point before Latin text, and the R2-12 fix covers it as well.

- R2-14 (low). Footnote marks, `\textsubscript` and `\textsuperscript` were pushed a pad away from their character. While the verifier proposed a fix that wraps those commands, it was not implemented, and round 3 raised no finding about it. Its status at 1.0.0 is therefore open. Re-running `recheck-layout/fnmark.tex` against the 1.0.0 snapshot for this write-up still shows `錢 \kern 4.86 \hbox{}` before the footnote-mark box, and the same before the `\mathon` of `\textsubscript` (see Section 4).

- R2-15 is a duplicate of R2-12.

- R2-16 (low). The pad was dropped before a closing bracket after a manual `\xjyutping` outside a block, and also for brackets missing from the list (〗〙〟｠). We extended the list, and the deferred path (`\__xjyutping_decide:` → `\__xjyutping_closing:n`) now pays the pad before closing brackets.

#### New-lens findings (23)

Findings R2-17 to R2-25 came from the review2-walker lens.

- R2-17 is a duplicate of R2-02.

- R2-18 is a duplicate of R2-01.

- R2-19 (high). The pending mark was stolen or cleared at the start of a paragraph, such as with a run-in `\paragraph` or with `\xjyutping` in fancyhdr heads. This was because the mark was stored in vertical mode, and `\everypar` or the output routine then ran before the character. The fix calls `\mode_leave_vertical:` inside `\xjyutping@mark`.

- R2-20 is a duplicate of R2-07, found with `\footnote`.

- R2-21 (medium). A brace group after the complete arguments of a table command was still read as an argument of that command (`\ref{x}{\itshape 長}大`, `\input`, `\begin{quote}` and `\footnote{…}{…}`). We fixed it by resetting the owner to `n` in `\__xjyutping_arg_done:` before dispatch, and after a class-`a` argument group. The `t17-owner-leak` log gives 長zoeng2:w大daai6:w in every case.

- R2-22 (medium). A `*` or `[…]` before a braced argument merged that argument with the following text (`\section*`, `\footnote[7]{…}` and `\marginpar[…]`), which was also reported as R2-35. Now `\__xjyutping_nonhan:n` copies a `*` after an `a`/`b` owner, and a `[` opens its own run without flushing the outer one. The `t04-star-opt-merge` log verified this, and round 3 later replaced the single-slot state with a stack (R3-03).

- R2-23 (low). Reference commands were missing from the table, such as `\Vref`, `\Nameref`, `\namecrefs` …, natbib and biblatex citations, `\subref` and `\zref`. We added all of them with `{1}{}{b}`. `t21-table-gaps.tex` compiles except for `\lcnameCref`, which is not a real command, so that failure is an error in the test.

- R2-24 (low). The walker's time grew quadratically with the length of an unpunctuated run, so that 20 000 characters took 28 s. This was due to a `\seq_put_left:Ne` per segment and an unconditional log append. The fix collects the segments linearly into `xjp@seg@<k>` and writes the log only in debug mode. This change itself introduced M2-1, in which segment emission expanded only one level and gave 122 `Missing number` errors in `basic.tex`, and we fixed M2-1 with `\use:e`.

  The transcript does not re-time the walker, so for this write-up we re-ran the verifier's timing files against the 1.0.0 snapshot with typesetting stubbed out, and the times were,

    | Test | Before | At 1.0.0 |
    | --- | --- | --- |
    | 5 000-character run | 2.43 s | 1.21 s |
    | 20 000-character run | 28.0 s | 5.35 s |
    | 20 000 characters with a comma every 10 | 2.98 s | 3.45 s |

  A second, independent re-run during the fact check gave 1.19 s, 5.24 s and 3.44 s. While the time is now about linear in run length, the punctuated case is slightly slower than before, which is consistent with the per-character checks added in round 3. R2-24 is resolved.

- R2-25 (low). A `\disablejyutping` in a tabular cell left annotation off in the walker for the later cells. Now `\__xjyutping_tab:` restores, at each `&`, the state saved at the enclosing `\begin`, and round 3 extended this to `\\` rows.

Findings R2-26 to R2-32 came from the review2-layout lens.

- R2-26 (high). Adjacent annotated groups got no `\CJKglue`, so text ran off the page. The same fix as for R2-12 applies.

- R2-27 (medium). Size commands inside a scope lost the raised `\baselineskip`, and the R2-05 fix also resolved this.

- R2-28 (medium). After `\textbf{…}`, `\emph{…}` and `\underline{…}`, the pad was paid before punctuation. This is due to `\check@icr` expanding to `\aftergroup\maybe@ic`, so the boundary saw `\aftergroup` rather than a group end, and after the group the peek then saw `\maybe@ic`. We fixed it by deferring on `\tex_aftergroup:D` as well and by looking past `\maybe@ic` (`\__xjyutping_defer_ic:w`). The `\underline` case (math) was left for round 3.

- R2-29 (medium). `\fbox` and `\colorbox` in a scope reached into the line above, because `\lineskiplimit -0.3em` allowed the overlap. The fix uses a clearance of 0.05em inside scopes, with `\lineskiplimit` back to 0pt, so a line that is too tall now gets `\lineskip`.

  After the fix, `vdump` on `r-fbox.tex` showed one `\lineskip` glue, and the transcript does not comment on it. Re-running the dump against the 1.0.0 snapshot for this write-up gives the same glue list and shows where that glue is. Specifically, all four interline glues around the `\fbox` and `\colorbox` lines inside the scope are `\baselineskip` (0.39, 0.43, 0.79 and 0.83pt), so the framed lines fit, while the single `\lineskip` comes before the file's third paragraph. That paragraph is the control case outside the scope (`\fbox{\xjyutping{行}{hang4}}` in a paragraph with normal `\baselineskip`), where TeX falls back to `\lineskip` as usual. R2-29 is fixed.

- R2-30 (medium). Brackets after a group-final character lost their padding. We fixed it by letting `\__xjyutping_decide:` handle FullRight marks through `\__xjyutping_closing:n` (see R2-16).

- R2-31 (medium). A space or source line break between a character and punctuation left a gap. `\__xjyutping_punct_space:n` now drops the space before FullRight/FullLeft in pass 2.

- R2-32 (low). The minipage environment, `\parbox` and `p` columns reset `\baselineskip`, and we fixed this by having the `para/end` hook raise it again. The round-2 verifier had already warned that the `para/end` re-raise alone would leave the line after the `\underline` line on `\lineskip`, since `\@arrayparboxrestore` also resets `\lineskiplimit`, and it proposed either restoring `\lineskiplimit` as well or adopting the 0pt scheme of R2-29. The 0pt scheme is what shipped.

  After the fix, `vdump` of `r-parbox.tex` still showed one `\lineskip` glue, and the transcript does not comment on it. A deeper dump against the 1.0.0 snapshot, made for this write-up, shows that
  - the minipage lines are `\baselineskip` apart (a pitch of about 19.57pt at 10pt);
  - the line after the one containing `\underline` (depth 3.47pt) gets `\lineskip 1.0`, a pitch of about 21.6pt; and
  - the outer `\lineskip` between the minipage and the tabular is normal for two tall boxes.

  This `\lineskip 1.0` is due to the cells inside the minipage being built while `\baselineskip` is still the reset 12pt, so every ruby gets the 0.35em clearance (a line height of 17.17pt instead of 14.12pt). The `\baselineskip` raised at `para/end` then leaves only about 2.4pt for the depth of the line above, and `\lineskiplimit` has been 0pt since R2-29. Since `vdump.sh` prints only the outer vertical list, the outer glue is the single `\lineskip` that the round-2 check saw, and the minipage's own lines were not in that dump.

  In ordinary scope text, checked the same way, the `\underline` line is followed by normal `\baselineskip` glue, and only a line deeper than about 5.45pt at 10pt (0.55em), for example one with a display-style `\sum`, falls back to `\lineskip`, as in plain LaTeX. The larger clearance inside the minipage comes from the round-3 fix R3-24, which uses 0.05em only when `\baselineskip` is at the scope minimum. A scratch copy of the 1.0.0 package with the round-2 rule (0.05em whenever in a scope) gives the same minipage all-`\baselineskip` glue. Hence the R2-32 fix works, but since R3-24 the pitch inside minipage, `\parbox` and `p` cells grows after moderately deep lines (see Section 4).

Findings R2-33 to R2-39 came from the review2-robust lens.

- R2-33 is a duplicate of R2-01.

- R2-34 (medium). Punctuation after `\textbf{…}`, `\emph{…}` or nested groups was pushed away. The R2-28 fix handled it, together with a change under which `\__xjyutping_defer_test_aux:` re-arms when another group end follows ("one more group"). The nested `\textbf` case was still broken, and we completed it as R3-09.

- R2-35 (medium). Starred and optional-argument forms merged, and beamer overlays leaked. The fix for R2-22 covers `*` and `[…]`, while the beamer overlays were fixed as R3-18.

- R2-36 (medium). The xeCJKfntef commands (`\CJKunderline`, `\CJKsout` …) collapsed the cell grid, and the `\CJKunderdot` dots were off-centre. This was not fixed, and the README tells users to use `\underline` or ulem's `\uline` in scopes instead.

- R2-37 (low). Underline and emphasis-mark commands ended the run, so a marked character lost its word. We declared the ulem commands as `{0}{}{t}` and the xeCJKfntef commands as `{-1}{}{t}`, with `-` copied like `*`.

- R2-38 (low). A beamer `\frametitle` inside a scope was segmented but typeset plain. The reason is that beamer typesets the title after the scope has ended. It was not fixed but documented (`\frametitle{\xjyutping*{…}}`).

- R2-39 (low). Main memory overflowed for one very long paragraph (above about 16k characters) or a long brace group. This was not fixed but documented (about 15k per paragraph, and a brace group is read in one piece).

Of the round-1 items that the round-2 recheck found only partly fixed,
- R1-03 (ctex glue) was fixed, since the `selectfont` hook, ordered after ctex, reinstalls the glue;
- R1-04 (dead-code `\setjyutping`) was documented;
- R1-08 (memory) was documented;
- R1-21/R1-42 (TOC and running heads) were fixed for the running heads by plain mode, in which `\xjyutping` prints only its text in the output routine, and documented for the TOC;
- R1-29 (group-final bracket) was fixed (R2-16/R2-30);
- R1-30 (stretch asymmetry) was resolved by the round-2 node-restoring pad, as confirmed on the 1.0.0 snapshot (see above);
- R1-31 (size change) was fixed (R2-05); and
- R1-32 (`width=auto` for macro text) was fixed by the `gwong2` fallback in `\__xjyutping_prepare:n`.

In the verification of round 2 (12:42–12:48),
- all repros of rounds 1 and 2 recompiled twice with 0 errors, except `t21-table-gaps.tex` (the test's nonexistent `\lcnameCref`);
- `[no context]` lines appeared only in files that deliberately test macro text, the `\input` fallback or dead-code settings;
- the walker debug logs were checked by hand;
- the `vdump` checks gave the results noted above;
- the five audit corpora compiled without errors; and
- the 53k memory repro used 3.33M words and took 13.6 s, while the 20k document took 6.19 s.

We created `tests/regression.tex` and `tests/run-tests.sh` at this point (12:48), and generated `regression.expected` from that run's log after checking its readings by hand.

### 3.5 Review round 3 (findings 12:49–13:43; fixes 13:44–14:07)

The round-3 lenses looked for regressions in the round-2 code. The r3-user lens built three documents from the README alone, namely
- a ctexart handout with a vocabulary tabular, fancyhdr and hyperref;
- a beamer deck; and
- an article with six `\input` chapters, a TOC and a long story.

The lens checked about 600 logged runs for machinery errors and found none in plain text. The fixes landed in three patches (parts A, B and C, 13:48–13:51) plus two small corrections.

Findings R3-01 to R3-08 came from the r3-walker lens.

- R3-01 (high). Carrying the right pad past groups with `\aftergroup` broke amsmath `\text`, `align`, TikZ node text, `\discretionary` and `\leaders` inside a scope, with the errors `Missing { inserted`, `Improper discretionary list` and TikZ "Giving up on this path". This was due to the deferral re-inserting itself after every enclosing group, including groups owned by other code that must be followed by `{` or glue. In the fix, `\__xjyutping_if_defer:` defers only past group types 1 and 14 and pays inside other groups, and TikZ node text sets `\l__xjyutping_nodefer_bool`. The finder suggested placing the check in `\__xjyutping_boundary_aux:`, but the verifier showed that the boundary code always runs inside xeCJK's own class group (type 1), so a test there never fires. The check therefore sits in `\__xjyutping_defer:` and `\__xjyutping_defer_test_aux:`.

  As a side effect, noted by the verifier, the pad of a box's last character is now paid inside the box, so `\hbox{甲行乙}` is three full cells wide (64.5pt at width=2em, against 58.75pt before). This is also what fixed R3-06.

  At the time, all r3 repro files recompiled with 0 errors, apart from agent helper fragments that are not complete documents. For this write-up we recompiled the verifier's files `f0-math`, `f0-align`, `f0-disc`, `f0-leaders` and `f0-tikz` against the 1.0.0 snapshot, with 0 errors. As a note on the process, a first rerun claimed failures, but they were stale logs, because macOS has no `timeout` command and the loop never recompiled anything.

- R3-02 (high). `\GTS@expandtrue`, the R2-01 fix, made fragile titles fail inside a scope. `\footnote` in `\section*`, theorem optional titles and description labels gave 2, 4 and 100 errors, and with nameref alone there was an `input stack size` overflow. We removed it, and `\__xjyutping_unmark:N` is now prefixed to `\label@hook`, where it replaces only the `\xjp@R@` marks in `\@currentlabelname` with their expansion. M3-1, an implementation note from this fix, records that a capture inside `\c{…}` is not a regex group, so the working approach extracts each distinct mark token and replaces it through `\u{…}`. `f1-thm-in`, `f1-desc-in`, `f1-sec-in` and `f1l-a` compile with 0 errors against the snapshot, and `regression.tex` (`\nameref`) still passes.

- R3-03 (medium). An optional argument that stayed open left stale walker state behind, as with `\left[…\right]` in a footnote, `。[1]`, `\makebox[\width]` and `\section[\mbox{短}]{重}`. This was because the owner test came before the `]` test and the state was a single slot. The fix tests `]` first and turns the state into an optional-argument stack (`\l__xjyutping_opt_seq`, `\__xjyutping_opt_begin:n`, `_end:`, `_pop:`, `_close:n` and `_top:`). Arguments that are still open are now closed at group end and at paragraph end. The `f2-01`, `02`, `06` and `21` logs show the expected runs.

- R3-04 (medium). `\\` in a tabular did not restore the annotation state after a `\disablejyutping` in the last cell, and it is a duplicate of R3-17. We gave `\\`, `\tabularnewline`, `\cr` and `\crcr` the action `row`, which restores the state only inside alignment environments (`\c__xjyutping_align_clist`, marked on the semantic stack when the `\begin` name is known). M3-2 records that the first version compared a detokenised environment name with `\clist_if_in`, which never matched, so row 2 stayed `[no context]`; comparing the raw name fixed it. `t11-tabular-row` and `r1-tabular-row-disable` give 銀行, 行路 and 校長 as words.

- R3-05 (medium). The `\input` fallback missed verbatim-like commands and catcode changes (`\lstinline`, `\Verb`, BVerbatim, alltt, `\DefineShortVerb` and `\obeylines`). The fix widened `\c__xjyutping_unsafe_regex`, and all six `f4-*-in` files compile with 0 errors against the snapshot.

- R3-06 (low). `\underline{字}` and other boxes ending in a character inside inline math lost the right pad. The cause was that the decision ran in math mode, where `\__xjyutping_pad:` (R2-04) only zeroes. The group-type test of R3-01 fixed it, as the pad is now paid inside the `\hbox`, and R3-20 gives the verification.

- R3-07 (low). In `\footnotemark[n]` the optional argument was read as text and broke the word. We declared `\footnotemark` as `{-1}{}{t}`, and `f6-a` now gives 銀ngan4:w行hong4:w.

- R3-08 (low). A `%` comment mentioning `\verb` or `\makeatletter` sent a whole `\input` file to the fallback. The detection now reads the file line by line (`\ior_str_map_inline:Nn`) and strips comments with `\c__xjyutping_comment_regex` before matching. This line-by-line read was needed because, as the verifier found, `\file_get` with `\c_str_cctab` loses line ends. `f7` gives word readings.

Findings R3-09 to R3-16 came from the r3-layout lens, which measured with `f0346-measure.tex` at width=2em, where plain `銀行，` is 47.25pt.

- R3-09 (medium). A nested `\textbf`/`\emph` before another closing brace paid the pad before punctuation (+5.75pt). We made `\__xjyutping_if_group_end:` treat `\check@icr` as a group end and `\__xjyutping_defer_ic_aux:` re-test. All ten nested variants measure 47.25pt when re-run against the snapshot for this write-up.

- R3-10 (medium). Colour groups got no stretch glue, so justified spacing was uneven around `\textcolor` and `{\color…}`. This is due to the colour push/pop whatsits hiding xeCJK's node, while the package's glue carries all of hsep's stretch. To fix this, `\__xjyutping_pad:` now re-makes the node after a whatsit (`\lastnodetype` = 9), and `\__xjyutping_cell:nnn` adds the stretch glue when the last node is a whatsit after a paid pad (`\g__xjyutping_paid_bool`). The bold and coloured lines both have glue set 0.65756.

- R3-11 (medium). At a line break before —— or ……, the character sat flush with the margin and its ruby stuck out. This happened because the pad was dropped before long punctuation, where xeCJK allows a break. The fix is `\__xjyutping_long_break:`, a kern pair around xeCJK's `\penalty0`. The session verified this only partly, since the render at the tested width did not break before ——, although the lines shown kept their rubies inside the frame.

  For this write-up we compiled the verifier's `f2-dash-eol.tex` against the 1.0.0 snapshot at the widths it listed. At 4.4cm and 6.4cm a line now breaks before —— and ends `章 \kern 4.86244 \penalty 0`, so the pad stays at the line end (the negative kern after the penalty is discarded). At 4.8, 5.2 and 5.6cm the paragraph no longer breaks there. R3-11 is fixed.

- R3-12 (medium). Invisible commands between a character and ，。 (`\label`, `\index`, `\color`, `{}`, `\relax` and `\nobreak`) gave the punctuation a gap. The fix is the walker's no-pad marker `\__xjyutping_nopad:` (Section 2.4), and all six cases measure 47.25pt.

- R3-13 (medium). `\underline` in a scope lost the right pad, which made the underline lopsided, and it duplicates R3-06/R3-20. The `ul` case measures 47.25pt before ，; `ulz` (before 中) is plain + 3.33pt, which is xeCJK's usual math/CJK glue.

- R3-14 (low). Long rubies before a line-final ，。、 crossed the right margin, by about 0.7pt at default settings and about 3pt at ratio=0.6. This is not fixed (see Section 4).

- R3-15 (low). In `\uline{X}，` the pad was paid inside the underline, so the comma stood off. The no-pad marker covers this, since the ulem commands are `t` class. `uline` measures 47.25pt against the 1.0.0 snapshot, and a box dump of `銀\uline{行}，` shows the underlined box as left pad + glyph (15.75pt at width=2em) with the comma directly after it, so the pad is no longer paid inside the underline.

  However, the session's compaction summary (14:09) lists this as a remaining limit, and at 14:02 the main agent wrote that "the comma after an underlined word sits one pad away" after looking at the `f46-underline-uline` render. The measurements and box dump taken for this write-up show `\uline{X}，` fixed, so the remark most likely described the render of a case other than the one measured here, although this is unverified.

- R3-16 (low). In tabular rows the row-to-row pitch was 1.85pt tighter than within a `p` cell, and the rubies sat 0.5pt under `\hline`. We fixed it by having `\__xjyutping_raise_baselineskip:` rebuild `\strutbox`, and a render confirmed that the rubies clear `\hline` and that the row pitch equals the in-cell pitch.

Findings R3-17 to R3-24 came from the r3-user lens.

- R3-17 (medium). This finding, on the tabular row and `\disablejyutping`, is described under R3-04.

- R3-18 (medium). In beamer, `\alert`, `\structure` and the overlay forms (`\textbf<2>{}` and `\textcolor<2>{red}{}`) ended the run. We declared `\alert` and `\structure` as `t`. When beamer is loaded, `<…>` after a command is now copied untouched, both in normal walking and in skip mode, where `\l__xjyutping_skipclose_int` generalises the closing character. `v-r3-beamer-alert` gives 銀行 and 校長 as words.

- R3-19 (low). The ctex font switches (`\heiti`, `\kaishu` …) and `\zihao` ended the run. We declared them `t`, with `\zihao` taking 1 argument and `\fontsize` 2, and `v-r4-ctex-font-commands` verified the fix.

- R3-20 (low). `\underline`, which the README recommends, dropped the right pad of its last cell. The group-type deferral of R3-01 fixed it. `v-r2-underline-pad` gives PLAIN 123.05pt, ULINE 123.05pt and UNDERLINE 126.38pt (= plain + 3.33pt math glue, the same difference as outside a scope).

- R3-21 (low). The pad was paid before 。 when `\label`, `\index`, `{}` or the end of an `\href` link came between the character and the punctuation. The no-pad marker fixed it; the verifier showed that the finder's "peek for `\label`" could not work, because macros are expanded before the boundary fires. In `v-r5` all four variants measure 76.05pt.

- R3-22 (low). In beamer, `\title{\xjyutping*{…}}` gave a "Token not allowed" warning and a `/Title` of `*廣東話會話`. This is due to beamer filling the PDF title before `\AtBeginDocument` code runs. `\__xjyutping_pdfstring:` now runs at once when `\pdfstringdefDisableCommands` exists, and otherwise through `package/hyperref/after`. `v-r6` has 0 warnings.

- R3-23 (low). The beamer class measured the headline with rubies but printed it plain, which left a 5.5pt band. The fix turns on plain mode in the `cmd/beamer@typesetheadorfoot/before` hook. We did not use `\beamer@calculateheadfoot` for this, since it is not grouped. In `v-r7`, `\headheight` is 5.79pt, equal to the plain-title control.

- R3-24 (low). In tabulars inside a scope, the rubies sat about 0.5pt under `\hline`. This was due to the 0.05em clearance assuming the raised `\baselineskip`, while alignments set it to 0. `\__xjyutping_clearance:` now uses 0.05em only when `\baselineskip` ≥ the scope minimum and 0.35em otherwise. A render verified the fix.

M3-3, an implementation note, records that `\str_if_in:nn` has no predicate form, so `\__xjyutping_plain:n` uses the protected `\str_if_in:nnF`.

In the final verification (13:56–14:07),
- all repros of the three rounds compiled, the only failure being `t21-table-gaps` (a test error);
- the helper fragments left by the agents did not compile on their own, as expected;
- the five audit corpora gave 0 errors and 0 `[no context]` lines;
- the 53k memory repro used 3.34M words and took 17.2 s, while the 20k document took 7.45 s (up from 6.2 s), which the main agent attributed to the extra per-character checks of round 3;
- `run-tests.sh` gave `readings: ok`; and
- the manual was rebuilt with 5 pages, 0 errors and 0 overfull boxes.

### 3.6 Close-out (14:07–14:09)

We reduced `tests/` to `regression.tex`, `regression.expected`, `run-tests.sh` and `render.sh`, together with `layout-check.tex`, which is a copy of the round-2 `pad2.tex` without `[debug]`. About 35 review directories and scratch test files were moved to `scratchpad/review-artifacts/`. We rebuilt `xjyutping-doc.pdf` and re-read the README for accuracy. The delivery summary we received proposed LuaLaTeX support and superscript tone numbers as possible next steps, and neither was started.

### 3.7 Performance and memory measurements (summary)

| Test | After first version | After round-1 rewrite | After per-paragraph analysis | After round 2 | 1.0.0 |
| --- | --- | --- | --- | --- | --- |
| `long.tex` (19 926 characters, 52 pages) | 4.7 s | 5.7 s | — | 6.2 s | 7.45 s |
| `repro-memory.tex` (53 060 characters, one scope, 140 pages) | fails: main memory > 5M | 4.88M words, 12.2 s | 3.32M words, 12.6 s | 3.33M words, 13.6 s | 3.34M words, 17.2 s |

Loading the package with no text takes about 2.47–2.48M words. The largest single scope that compiles has 159k characters (4.87M words), while one of 212k fails, and for one paragraph the limit is about 15–18k characters.

### 3.8 After 1.0.0

At 14:19 we asked for the `fancy` option, this changelog under Semantic Versioning and the split into `xjyutping-tex/` and `xjyutping-py/`. Section 6 describes that work.

---

## 4. Known limitations and open issues at 1.0.0

This section gives the state at 1.0.0, with notes on what 1.1.0 resolved, while Section 7.7 gives the state after 1.2.0.

Items 1–10 are intended behaviour and are documented in the README.

1. The package runs under XeLaTeX only and stops with a critical error on other engines, so LuaLaTeX is not supported. The environment body and the argument of `\xjyutping*` are read as a macro argument. Hence `\verb` and verbatim environments cannot go inside, and `%` in `\url`/`\href` must be written `\%`.
2. `\input{file}` inside a scope is read with the body's restrictions, while a file using `\endinput`, verbatim-like commands, `\makeatletter`, catcode changes or `\obeylines` is `\input` normally, without word context. Macro text, `\include`d files and `\maketitle` also get no word context and are annotated character by character (`[no context]` in the log).
3. Inside a scope, a `\setjyutping` in dead code (`\iffalse`, an unused `\newcommand`) still affects the segmentation of the text after it in the same scope.
4. Commands outside the command table need their Chinese argument in braces (`\textbf{行}`). The round-2 recheck of R1-44 also noted a silent side effect of unbraced arguments that is not in the README. Specifically, with `AutoFakeBold` on the CJK font, an unbraced `\textbf 行` inside `\xjyutping*` loses its bold, while the braced form stays bold.
5. The table of contents (TOC) is annotated only if `\tableofcontents` is itself inside a scope, or if a title contains an explicit `\xjyutping`.
6. Inside a scope, beamer's `\frametitle` stays plain, so use `\frametitle{\xjyutping*{…}}` instead.
7. The xeCJKfntef commands (`\CJKunderline`, `\CJKunderdot`, `\CJKsout` …) do not keep the cell grid, and the dots of `\CJKunderdot` are off-centre (R2-36). Use `\underline` or `\uline` instead.
8. Looking at capacity, one paragraph holds about 15 000 characters, and a brace group spanning many paragraphs is analysed in one piece. One scope holds "well over 100 000" characters according to the README, and the limit was measured at between 159k (compiles) and 212k (fails) with the default `main_memory`.
9. Characters that are missing from the data get a cell without Jyutping.
10. Variant folding applies to word lookup only, so `\setjyutping{為}{…}` does not change 爲 (R1-25, rejected as a defect).

Items 11–17 are not fixed and are not in the README.

11. R3-14. Long rubies before a line-final ，。、 can reach into the right margin, by about 0.7pt with default settings and about 3pt at ratio=0.6. The verifier's corrected fix, which would add a kern pair after xeCJK's trailing trim rule only at a line end, was not implemented.
12. R2-14. Footnote marks, `\textsuperscript` and `\textsubscript` right after an annotated character sit one pad away from it, and punctuation after the mark moves with it. In the repro, at 10pt with `width=auto` giving a 0.49em pad, the distance is 4.86pt. This was confirmed on the 1.0.0 snapshot with the box dump of `fnmark.tex`. Moreover, the verifier's `fnmark2.tex`, recompiled against the snapshot, shows that a character right after a footnote mark (`攞錢\footnote{…}大`, `攞錢\footnotemark 大`) follows it with no glue at all, so there is no line-break point and no stretch there. This is due to `\__xjyutping_boundary_aux:`, which pays the pad because the next token after expansion is not a group end. The round-2 verifier suggested a fix, which was not implemented. While a scope is enabled, the fix would wrap `\footnote`, `\footnotemark`, `\textsuperscript` and `\textsubscript` so that the pad is paid after the mark, or dropped if punctuation follows. The walker must still recognise `\footnote`.
13. The line pitch after deep lines in minipage, `\parbox` and `p` cells is uneven. This is a side effect of R3-24's clearance rule, on top of R2-29's 0pt `\lineskiplimit` and R2-32's `para/end` re-raise. Inside such a box within a scope, the cells are built with the 0.35em clearance, because the reset `\baselineskip` is raised only at `para/end` and the R3-24 test therefore sees 12pt. Hence a line deeper than about 0.24em, for example one containing `\underline`, is followed by `\lineskip` instead of `\baselineskip`, and that one gap is about 2pt larger (19.57pt against 21.6pt in `r-parbox.tex` at 1.0.0). In ordinary scope text, on the other hand, the threshold is about 0.55em, so `\underline` does not trigger it and only unusually deep material such as display-style math does, as in plain LaTeX. This is the trade-off for keeping framed and coloured boxes from overlapping the line above and for keeping rubies clear of `\hline` in `p` cells, and the R3-24 verifier chose the `\baselineskip` test precisely so that `p` cells get 0.35em. The round-2 verifier foresaw the `\lineskip` fallback, and no review reported it as a defect.
14. Ambiguous readings, which need context beyond the word list, are left to user overrides. This applies to 為 wai4/wai6 outside the curated 為-phrases, 同行 hong4/hang4, 當佢係 dong3, 背得 bui6, 彈得 taan4, 種花 zung3, 假 gaa3 in 請假-type phrases, 長得 zoeng2 and 散晒 saan3. The `multiple=` option and the debug log exist to find them.
    - Five further wrong readings were seen in round 3 but never reported as findings, since the r3-user lens listed them as "documented algorithm or data" and moved on. We re-checked them against the 1.0.0 snapshot for this write-up, and all five are still wrong there. Specifically, 我屋企住 splits 屋|企住 (企 kei5); 電車行得 gives 車行 ce1 hong2; 都會話 gives 會話 wui6 waa2; 生詞表 gives 生 sang1 while 生詞 alone is saang1; and 慢慢行 gives 行 hang4. Each is a candidate for a `CURATED_WORDS` entry or guard word. In 1.1.0, 慢慢行, 屋企住, 都會話 and 生詞表 were fixed, while 車行 was left, because 行得 as a word would break 銀行得… (Section 6.4, F-5).
15. The segmentation tie-break can split a demonstrative or numeral followed by a classifier wrongly, since on a tie the longer final word wins. For example, 呢|張床 and 一|間房 were split this way before the round-1 data fixes. This is handled case by case with word entries, guard words and the run-final reading of 呢, not in general.
16. The review artefact `t21-table-gaps.tex`, which is not in `tests/`, uses the nonexistent `\lcnameCref`, so the error lies in the test file rather than in the package. The R2-23 fix nevertheless put `\lcnameCref` into the command table next to the real `\lcnamecref`, but the extra entry is harmless.
17. Inside a scope, `\pdfbookmark` anchor names are annotated. Since `\pdfbookmark` is not in the command table, its name argument is walked as text. Recompiling the round-2 recheck file `recheck-robust-tokens/chk-keys.tex` against the 1.0.0 snapshot gives 0 errors and 0 warnings. However, the named destination is written as `\xjyutping@mark {wmuk6}目\xjyutping@mark {wbiu1}標.1`, while `\hyperlink{目標}` in the same scope points to `目標`, so the link is silently broken. The suggested fix is to declare `\pdfbookmark`, `\currentpdfbookmark`, `\subpdfbookmark` and `\belowpdfbookmark` as `{2}{}{b}`, since both arguments are PDF strings or keys, never typeset text, and the optional level is copied anyway. Version 1.1.0 fixed it this way (Section 6.4, F-4).

---

## 5. How to test, and how to regenerate the data

This section describes the state at 1.2.0, and the notes in brackets say what
was different before.

### 5.1 Tests (in `tests/`)

The tests need XeLaTeX with xeCJK, LuaLaTeX with LuaTeX-ja and ctex (TeX Live
2026 has all of them), the font Songti TC (macOS) and Ghostscript (`gs`) for
rendering. The scripts put the package directory on both search paths with
`TEXINPUTS=..: LUAINPUTS=..:`, so they must be run from `tests/` or called by
their path. Both paths are set because LuaTeX finds `xjyutping.lua` through
`LUAINPUTS`, not `TEXINPUTS`.

`./run-tests.sh` is the regression check. For each of four jobs (XeLaTeX and
LuaLaTeX, each with and without the `fancy` option), the script,

1. compiles `regression.tex` twice;
2. fails if the log has any `^!` error; and
3. extracts the `xjyutping>` debug lines into `<job>.readings` and diffs
   them against `regression.expected` (26 lines).

`regression.tex` uses hyperref, `\section`/`\nameref`, a footnote,
`\textbf`/`\color` inside words, variant spellings, 呢 final and non-final,
`\xjyutping` and a mid-text `\setjyutping`. It also contains a `linebreak`
scope and a scope opened by a user environment, which holds `center`, a
table made by a macro and `$x\mbox{…}$`. The document loads xeCJK under
XeLaTeX and ctex under LuaLaTeX. The run passes when `<job>: readings ok`
appears four times and the exit status is 0. (At 1.0.0 the script ran
XeLaTeX once and wrote `regression.out`. Version 1.1.0 added the `fancy` job
and 1.2.0 the LuaLaTeX jobs.)

When a reading changes on purpose, as with a data fix, the steps are,

1. Check the diff by hand
2. Run `grep -a '^xjyutping>' regression-xelatex.log > regression.expected`
3. Rerun the tests
4. Compile the Python package's `tests/parity.tex`, with
   `TEXINPUTS`/`LUAINPUTS` pointing here and `max_print_line=10000`
5. Copy the `xjyutping>` lines to the Python package's
   `tests/parity_expected.txt`

`./render.sh file.tex [engine] [dpi]` compiles a file that sits in `tests/`
with `xelatex` (the default) or `lualatex` and renders every page to
`file-N.png`, at 200 dpi by default. For files elsewhere, compile with the
absolute search paths
`TEXINPUTS=<this repository>: LUAINPUTS=<this repository>:` instead.

`layout-check.tex` is the visual layout check. It covers,

- `\textbf`, `\emph` and `{{…}}` before ，。：;
- group-final characters before characters and Latin text;
- brackets around coloured and manual characters;
- a source line break before punctuation;
- `\fbox`/`\colorbox`; and
- a long chain of manual `\xjyutping` that must still break lines.

`fancy-check.tex` is the visual check of the tone marks. It covers sizes,
sans-serif italic in colour, `width=natural` and a fixed width, a large
ratio, inline `\xjyutping*`, `multiple`, a syllable without a tone and
`fancy=false`.

`verse-check.tex` (1.3.0) is the visual check of `linebreak` and `align`. It
sets two stanzas with lines of different lengths under `parskip`, centred,
flush left, flush right and with `\centering` in the scope. Line centres (or
edges) must be the same within each scope, and the gap between stanzas must
be one line plus the paragraph space. To measure the result rather than look
at it, use `gs -sDEVICE=txtwrite -dTextFormat=0`, which gives the bounding
box of each text span.

The debugging aids are,

- `\usepackage[debug]{xjyutping}` (or `\xjyutpingsetup{debug=true}`), which
  logs segmentation, with the same log under both engines;
- `multiple=\color{red}`, which highlights guessed polyphones; and
- `\showbox` or a `\vbox` dump, which shows the cell structure.

Under XeLaTeX the cell structure is
`\hbox{} \kern<pad> <overlap box> <char> \kern<pad> \hbox{}`, and the dump
also shows interline glue, while under LuaLaTeX each cell is one hbox,
`[\kern<pad> <overlap box> <char> \kern<pad>]`, between LuaTeX-ja's glue.

Repeat the following checks after any change to padding, deferral or the Lua
wrapping, since these behaviours regressed before,

- the 18-call chain of `\xjyutping` in `layout-check.tex` must break lines
  (no overfull boxes);
- `銀\textbf{行}，`, `銀{\textbf{行}}，`, `銀行\label{x}，` and
  `銀\uline{行}，` must all be as wide as `銀行，`;
- `$\text{面積}$`, TikZ node text and `align` with `\text` inside a scope
  must compile;
- `\nameref` to a section inside a scope must compile on the second run;
- a scope opened by a user environment must end with it, and the `\author`
  of `\maketitle` and `$\text{\foo}$` in a scope must be annotated under both
  engines (the debug logs must match);
- `\footnote` inside `\section*` in a scope must compile; and
- the XeLaTeX renders of `regression.tex`, `layout-check.tex` and
  `fancy-check.tex` should stay identical when only the LuaLaTeX path is
  changed (compare the PNGs with `cmp`).

### 5.2 Regenerating the data

The command below regenerates the data and can be run from any directory,

```bash
python3 tools/build-data.py [--sources DIR] [--py-data DIR]
```

By default the script reads the sources from the directory that contains
this repository, and if xjyutping-py sits there too, it also rewrites
`xjyutping-py/src/xjyutping/data/*.tsv`. `tools/fetch-sources.sh [DIR]`
fetches the sources at the pinned commits. The files that
`tools/build-data.py` needs are,

- `jyutping-table-master/list.tsv`;
- `rime-cantonese/jyut6ping3.chars.dict.yaml` and
  `rime-cantonese/jyut6ping3.words.dict.yaml`;
- `opencc/HKVariants.txt` and `opencc/TWVariants.txt`;
- `jyut-dict/src/dictionaries/cedict/data/CC-CANTO.txt` and `READINGS.txt`
  (since 1.2.0); and
- the book files of `cantonese-books-data/` listed in `BOOKS` (since 1.2.0).

The build prints statistics to stderr, which at 1.2.0 were,

```
chars 30089 (polyphonic 4407), variants 76, words 103579 (+133 aliases, 0 alias clashes, 1229 words with several readings)
chars added from cantonese-books-data: 640 (...)
words added from jyut-dict: 2291 (CC-CEDICT readings 1927, CC-Canto 364); not added: ...
```

(At 1.0.0 the first line read `chars 29449 (polyphonic 4349), variants 76,
words 101275 (+68 aliases, ...)`, and at 1.1.0 it had `words 101277`.) A
build takes about 3 seconds and is deterministic.

Permanent reading fixes go into the tables at the top of the script, which
are `CURATED_DEFAULTS`, `CURATED_FINALS`, `CURATED_VARIANTS` and
`CURATED_WORDS`. Words of CC-Canto or of the CC-CEDICT readings that must not
be added go into `EXCLUDED_WORDS`, and `BOOKS` lists the book files, most
authoritative first.

Before adding a word or changing a default, test the candidate with
`\setjyutping` in a scratch file against other common contexts. Since the
longer final word wins ties, a new entry can capture neighbouring characters,
so add guard words where needed (the 平啲 case needed 16). The build applies
the same reasoning to the added word lists automatically (Section 7.4).
Changes to defaults are riskier than word entries, and review verifiers
rejected several of them, since they fix one sentence but break common
standalone uses.

After regenerating, run `tests/run-tests.sh` and xjyutping-py's tests, and
update the expected files only for intended changes.

To take an upstream update of a source, change the pinned commit in
`tools/fetch-sources.sh` and expect changes in defaults, flags and words.
Then compare the statistics and the regression output, and review the new
words that the build adds.

---

### Appendix: counts

| Round | Bug findings | Reading findings | Other |
| --- | --- | --- | --- |
| Initial development | 6 package bugs (I-1…I-6) and 4 data-builder issues (D-1…D-4) | — | — |
| Round 1 | 46 (45 accepted, 1 rejected), about 32 distinct after duplicates | 82 (74 accepted, 8 rejected), from 110 wrong characters over 3 corpora | 6 issues found by the main agent while fixing (M1-0 builder KeyError, M1-1 `#` in body, M1-2 save stack, M1-3 main memory, M1-4 split strips braces, M1-5 missing 行長) |
| Round 2 | 39 new (16 recheck-lens, 23 new-lens; none rejected), about 29 distinct | 14 | 46 recheck statuses for round 1: 34 fixed, 9 partly, 2 documented, 1 not applicable; 1 main-agent regression (M2-1) |
| Round 3 | 24 (none rejected), 20 distinct | — | 3 main-agent implementation issues (M3-1…M3-3); 1 test-harness issue (no `timeout` on macOS) |

At 1.0.0, R2-14 (confirmed still present), R2-36 (documented), R2-38
(documented), R2-39 (documented), R3-14 and the `\pdfbookmark` gap noted in
the R1-14 recheck (confirmed still present; Section 4, item 17) were not
fixed.

For this write-up we re-measured R1-30, R2-24, R2-29, R3-11, R3-15 and the
划算/划船 reading check against the 1.0.0 snapshot, and all of them were
confirmed fixed. The round-3 repros cited as verification (`f0-*`,
`f1-*-in`, `f1l-a`, `f2-*`, `f4-*-in`, `f6-a`, `f7`, `f0346-measure`,
`v-r1` … `v-r7`) and `tests/regression.tex` were also recompiled against the
snapshot, and they gave 0 errors and the stated widths and readings.

R2-32 (the minipage pitch) was fixed, while the remaining deep-line effect,
which affects minipage, `\parbox` and `p` cells only, is described in
Section 4, item 13. The wrong readings seen in round 3 but never reported
were still present at 1.0.0 (Section 4, item 14).

---

## 6. Version 1.1.0 of the LaTeX package and 1.0.0 of the Python port (2026-09-28, 14:19–)

### 6.1 The request

We added two reference repositories,

- `visual-jyutping-master/`, the Visual Jyutping page by Vincent Tam (MIT),
  "inspired by Visual Cantonese Fonts"; and
- `xpinyin-master/`, the Python xpinyin package by lxneng.

We wanted four things,

1. a `fancy` package option, `\usepackage[fancy]{xjyutping}`, that gives
   the Jyutping the visual tone indicators of Visual Jyutping, with the
   automatic spacing adapted to it;
2. this `CHANGELOG.md`, usable as a handover file, recording how the project
   was created and every change, bug and fix;
3. versions in the changelog and READMEs that comply with Semantic
   Versioning; and
4. a split of the project into `xjyutping-tex/` (the LaTeX package) and
   `xjyutping-py/` (a Python version like xpinyin).

### 6.2 How the work was organised

The work was divided between the main agent and a background workflow of 7
agents running in parallel. The main agent moved the LaTeX files into
`xjyutping-tex/` and changed the output paths in `tools/build-data.py`, then
froze a copy of the 1.0.0 `.sty` and `.def` files (the "snapshot"). It then
implemented `fancy` itself. In the background workflow,

- one agent built the Python port against the snapshot;
- three independent reviewers checked the port through different lenses
  (reading parity with TeX; API, packaging and docs; edge cases and tone
  styles);
- a fixer reproduced each review finding before fixing it;
- a historian wrote Part II, Sections 1–5 from the session transcript and
  the review artefacts; and
- a fact-checker verified every claim in that history against the
  transcript, the artefacts and the code, and recompiled about 40 repro
  files against the snapshot.

### 6.3 The `fancy` option: design

In Visual Jyutping, `assets/js/script.js` replaces a syllable's final tone
digit with a spacing modifier letter plus a superscript or subscript digit.
Its two maps are,

| Tone | Web map (`webToneMap`) | Discord map (`dcToneMap`) |
| --- | --- | --- |
| 1 | ˉ¹ | ˉ¹ |
| 2 | ˊ² | ⸍² |
| 3 | ˗₃ | -₃ |
| 4 | ˎ₄ | ⸜₄ |
| 5 | ˏ₅ | ⸝₅ |
| 6 | ˍ₆ | ˍ₆ |

Those code points (U+02C9, U+02CA, U+02D7, U+02CE, U+02CF, U+02CD and the
sub/superscript digits) are missing from many fonts, including the Latin
Modern default of `font=\normalfont`, and the package lets users choose any
`font`. Therefore the TeX package draws the stroke instead of using a glyph.

The stroke is a `\special{pdf:content …}` inside a box of fixed width.
xdvipdfmx, XeTeX's only driver, wraps `pdf:content` in `q 1 0 0 1 x y cm … Q`,
which puts the origin at the current point, and this was checked in an
uncompressed PDF (`xdvipdfmx -z 0`). The stroke takes the colour set by
xcolor's colour stack (checked with red text), and it follows `\rotatebox`.
The small tone number, on the other hand, is ordinary text in the ruby font
at 0.7 of its size, selected once through NFSS and then called by its font
identifier.

For the shapes, we first tried Chao tone contours (55, 35, 33, 21, 13, 22).
However, at 700 dpi the level strokes of tones 3 and 6 were only 0.14em
apart at ruby size and could not be told apart. The final shapes therefore
use the geometry of the Visual Jyutping symbols. Levels are at pitch 5, 3
and 1 (ˉ, ˗, ˍ), while ˊ rises 3→5, ˎ falls 3→1 and ˏ rises 1→3. Pitch 1 is
the baseline and pitch 5 the height of the digit 6. The stroke is 0.4em long
and 0.08em thick with round caps, after a 0.07em gap, in a box 0.51em plus
the stroke width wide. Raised numbers for tones 1–2 are lifted by 0.3 ×
digit height + 0.12em, and lowered numbers for 3–6 by −0.12em.

In `xjyutping.sty`, `\__xjyutping_syllable:n` (called by
`\__xjyutping_ruby:nn`) splits off a final tone digit 1–6, and a syllable
without one is printed unchanged. `\__xjyutping_tones:` and
`\__xjyutping_tones_build:` build the six marks once per font, keyed by
`\fontname\font`. Specifically, `\xjp@tone@<font>@<tone>` holds the box and
the number, while `\xjp@tones@<font>` holds the largest height and depth
among them. The drawing itself is done by `\__xjyutping_contour:n`,
`\__xjyutping_stroke:nn`, `\__xjyutping_pitch:n` and `\__xjyutping_bp:n`.

The spacing is adapted to the marks in both directions. Horizontally,
`\__xjyutping_measure:n` builds the same ruby as the cell, so `width=auto`
measures the fancy form. Vertically, `\__xjyutping_strut:` includes the
marks' height and depth, so every fancy ruby has the same box and lines stay
evenly spaced. The lift, `\g__xjyutping_lift_dim`, is the amount the marks
reach below the letters' descenders. It is 0 for Latin Modern, since −0.12em
is less than the depth of g. `\__xjyutping_vsep:` (vsep + lift) replaces the
raw `vsep` in the cell's `\box_move_up:nn`, in `\__xjyutping_clearance:` and
in `\__xjyutping_baselineskip:`.

The table below compares the cost of plain and `fancy` rubies.

| Test | Plain | `fancy` |
| --- | --- | --- |
| 29 118-character document | 8.69 s, 58 pages | 11.01 s, 65 pages (wider cells) |
| One 12 000-character paragraph, first version of the marks | 4.06M words | 4.84M words (+65 words per character) |
| One 12 000-character paragraph, final version | 4.06M words | 4.66M words (+50 words per character) |
| One 15 000-character paragraph | 4.45M words | exceeds main memory |

The single-paragraph limit with `fancy` is documented as about 13 000
characters.

We checked the option with `tests/run-tests.sh`, in which both jobs gave the
same readings as `regression.expected`, and with `tests/fancy-check.tex`,
rendered at 200 and 600 dpi. The check file covers `\small`/`\Large` in a
scope, `font=\sffamily` with italic blue `format` and `width=natural`,
`ratio=0.6, vsep=1.3em, width=2.2em`, inline `\xjyutping*` in a normal
paragraph, `multiple=\color{red}`, a syllable without a tone
(`\xjyutping{唔}{m}`) and `fancy=false` inside a fancy document. In the
renders no ruby touched the line above or the character below, and there
were 0 overfull or underfull boxes. The manual (5 pages) also compiled with
0 errors and 0 overfull boxes.

### 6.4 Bugs found and fixed during this work

#### TeX package

- F-1. The fancy marks used too much main memory. A 15 000-character
  paragraph, which compiles without `fancy`, exceeded main memory, and at
  12 000 characters `fancy` used 4.84M words against 4.06M. The cause was
  that the text of every `\special` is stored in its whatsit node, and the
  first version wrote 5-decimal bp values plus its own `q … Q`. The fix
  makes `\__xjyutping_bp:n` round to 0.01bp and drops the redundant
  `q`/`Q`, since `pdf:content` adds them itself. This brought the cost down
  to +50 words per character, and the limit is documented.
- F-2. Tones 3 and 6 were indistinguishable with Chao contours at ruby size.
  The strokes were therefore redesigned on the Visual Jyutping symbols
  (Section 6.3).
- F-3. `run-tests.sh` wrote its extracted readings to `regression.out`,
  which is also hyperref's bookmark file for `regression.tex`. It now writes
  them to `<job>.readings`.
- F-4 (open issue 17 at 1.0.0). `\pdfbookmark` names were annotated. The fix
  declares `\pdfbookmark`, `\currentpdfbookmark`, `\subpdfbookmark` and
  `\belowpdfbookmark` as `{2}{}{b}`. We verified that the round-2 file
  `chk-keys.tex` now writes the destination `目標.1` (hex `e79baee6a8992e31`
  in the uncompressed PDF) with no marks, and that 書簽 and 目標 no longer
  appear in the debug log. However, hyperref itself names the anchor
  `<name>.<level>`, so `\hyperlink{目標}` in that test never matched, with
  or without the package.
- F-5 (open issue 14 at 1.0.0). Four readings, those of 慢慢行, 屋企住,
  都會話 and 生詞表, were corrected through `CURATED_WORDS`. 生詞表 also
  turned out to be a rime entry with 生 sang1. We left 車行 in 電車行得
  alone, since adding the word 行得 would turn 銀行得… into 銀|行得 through
  the tie-break, and 車行 "car dealer" is a real word. The four phrases were
  appended to the Python parity corpus, and `parity_expected.txt` was
  regenerated from the 1.1.0 TeX log. The earlier 106 lines were unchanged,
  and there were 3 new ones.

#### Python port

While the port author's own 35 tests had passed, the three review lenses
found the following bugs, which the fixer then reproduced and fixed.

- P-1 (reported by all three lenses). A lone carriage return (CR) was not
  counted as a line end, so `'\r\r'`, a blank line to TeX, did not end a
  run, which changed segmentation and the run-final 呢. The fix makes
  `_runs` count `\n` as a line end, and also `\r` when it is not followed by
  `\n`. The test `test_runs_cr_line_ends` takes its expected values from a
  TeX log.
- P-2. The source distribution (sdist) lacked the parity files, so its own
  test suite failed (2 tests, FileNotFoundError). `MANIFEST.in` now
  includes `tests/*.txt` and `*.tex`.
- P-3. The editable install in the README failed with the machine's pip
  21.2.4, since editable installs need pip 21.3 or later. The README now
  upgrades pip first.
- P-4. `license = {text = "MIT"}` in `pyproject.toml` triggered a
  setuptools deprecation that becomes a build error after 2027-02-18. The
  line was removed, while `License-File` and the classifier remain.
- P-5. The run-final example in the README showed a word-list entry instead
  of the run-final rule. It was replaced with 呢張床好平，好麻煩呢？
- P-6. `set_jyutping` on a character missing from the data did nothing,
  whereas TeX reads such a character without context and with type `u`.
  Such a character is now its own run of type `u`, and the test
  `test_set_jyutping_char_not_in_data` covers it.
- P-7. `set_jyutping` rejected whitespace that `\setjyutping` ignores. It
  now strips spaces, tabs, CR and LF, and the test
  `test_set_jyutping_ignores_spaces` covers this.

#### Process notes

The permission check stopped the Python agent from running
`tools/build-data.py` in place, because the script rewrites
`xjyutping-tex/*.def`, which another agent was editing. The agent therefore
ran it on a scratch copy and confirmed that the `.def` files were
byte-identical. The in-place run happened later, for 1.1.0.

The history agents also found three things at 1.0.0 that the earlier summary
had wrong,

- `\uline{X}，` (R3-15) is fixed and is not a remaining limit;
- the I-3 error was "Missing number", not "Missing }"; and
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

Some differences are by design. Since Python has no markup, the port has
nothing like the command table, footnote runs, `\xjyutping` manual readings
or plain mode. Therefore the parity corpus has TeX's commands resolved into
the runs TeX makes of them. Moreover, `chars.tsv` lists the other readings
of every character (for `get_jyutpings`), not only of flagged polyphones.

### 6.6 Open after this work

Part II, Section 4 still applies, except for items 14 (partly) and 17, which
1.1.0 resolved. The open issues specific to `fancy` are,

- one paragraph holds about 13 000 characters, against about 15 000 without
  it;
- the strokes are graphics, so copying text out of the PDF gives the letters
  and the tone number without the stroke; and
- a `format` that changes the font size or shape gets marks built for that
  font, but the strut and lift are computed from the base ruby font, which
  matches how `format` already interacts with the strut.

---

## 7. Version 1.2.0: LuaLaTeX, more vocabulary, `linebreak`, two repositories (2026-09-28, from 15:59)

### 7.1 The request

The request after 1.1.0 had four parts,

1. more vocabulary from two repositories, 石見田's
   [cantonese-books-data](https://github.com/jyutnet/cantonese-books-data)
   (found through [jyut.net/about](https://jyut.net/about)) and
   [jyut-dict](https://github.com/aaronhktan/jyut-dict), the latter from its
   two subdirectories `dictionaries` and `jyut-dict` under `src`,
2. LuaLaTeX support, followed by an update of all the documentation,
3. attributions in a separate section of the README of both packages, where
   - the LaTeX package names the authors of the LaTeX xpinyin (Qing Lee) as
     its inspiration,
   - the Python package names the author of the Python xpinyin (lxneng, Eric
     Lo) as its inspiration and
   - both thank Visual Jyutping and the Visual Cantonese Fonts for
     inspiring `fancy`, as well as the authors of every other source, OpenCC
     included
4. and a remark in passing that we had made separate git repositories of the
   two folders,
   [Beyond3345/xjyutping-tex](https://github.com/Beyond3345/xjyutping-tex)
   and [Beyond3345/xjyutping-py](https://github.com/Beyond3345/xjyutping-py).

### 7.2 Two repositories

The workspace root, which held the old single `CHANGELOG.md`, the root
`README.md` and `tools/`, belonged to neither repository. Moreover, the
READMEs linked to `../CHANGELOG.md` and `../xjyutping-py`, links that break
on GitHub. We therefore made the following changes.

- We moved `tools/build-data.py` into this repository. In the script, `REPO`
  is the repository and `ROOT` is the directory with the sources, which
  defaults to the parent of the repository and can be changed with
  `--sources DIR`. The Python data goes to
  `../xjyutping-py/src/xjyutping/data` if that package is there, or to
  `--py-data DIR`, and is skipped otherwise. We checked that the output was
  byte-identical after the move.
- We split the changelog. While this file keeps the whole history,
  xjyutping-py has its own `CHANGELOG.md` with its releases and handover
  notes for the Python side.
- Links now point into the repository or to the other repository on GitHub.
- Both repositories got a `.gitignore`. Our interim commit had picked up
  `.DS_Store` and `tools/__pycache__/build-data.cpython-313.pyc`. The `.pyc`
  came from an agent that imported the script with importlib, and both files
  were deleted in later commits.

### 7.3 The LuaLaTeX backend

We could not reuse the XeLaTeX approach. Under XeLaTeX, xeCJK calls
`\CJKsymbol` for every Chinese character, and the package builds the cell
there. LuaTeX-ja, on the other hand, has no such hook. Instead, characters
become glyph nodes, and LuaTeX-ja inserts its glue (`kanjiskip` and JFM
glue) and line-break penalties in Lua callbacks, specifically `ltj.main` in
`pre_linebreak_filter` and `hpack_filter`. Further, xpinyin, the model for
this package, supports XeTeX and pdfTeX only, so there was no precedent to
follow.

#### Design

The TeX side prepares the parts of each cell, and Lua assembles them after
LuaTeX-ja has run.

- The preprocessor is unchanged, and both engines get the same marks,
  `\xjp@R@<type><reading>` → `\xjyutping@mark{<type><reading>}`, right
  before each character.
- Under LuaLaTeX, `\xjyutping@mark` ends with `\__xjyutping_mark_next:`.
  This peeks at the next token and, if it is a character (catcode 11 or 12),
  runs `\__xjyutping_lua_mark:N`, whose steps are,
  1. Measure the character, build the ruby with the shared
     `\__xjyutping_ruby:nn` (font cache, strut, `format`, `multiple` and
     `fancy`) and compute the pad exactly as the XeLaTeX cell does, all in
     `\__xjyutping_lua_build:nnnN`
  2. Put the ruby, with `\__xjyutping_clearance:` and raised by
     `\__xjyutping_vsep:`, into a zero-width overlay box as wide as the
     character
  3. Call `\xjyutping@lua@store <box> <pad> <stretch>`, a Lua function
     defined with `token.set_lua` that copies the box into a table and sets
     the attribute `xjyutping@cell` to the new id
  4. Typeset the character inside a group, so that only its glyph carries
     the id
- Instead of replacing xeCJK's hooks, `\__xjyutping_enable:` and
  `\__xjyutping_disable:` set and unset a second attribute,
  `xjyutping@scope`, through `\xjyutping@lua@on` and `\xjyutping@lua@off`.
  The internal boxes (the character measure, the ruby and the overlay)
  switch it off locally with `\__xjyutping_cjk_inactive:`.
- `xjyutping.lua` registers a callback in `pre_linebreak_filter` and
  `hpack_filter`, after LuaTeX-ja's `ltj.main`. For each glyph whose cell id
  is in the table, `wrap`
  - replaces the glyph, or the one-glyph box that LuaTeX-ja packed it into,
    with a cell hbox, `[\kern pad][overlay][glyph][\kern pad]`, tagged -1,
  - leaves out the right pad when the next visible object is FullRight
    punctuation other than a closing bracket or quote, as under XeLaTeX,
  - would move the line break before a long mark (—— ……) into a
    discretionary whose pre-break text is the pad, although this never fires
    in practice, since LuaTeX-ja (with ctex's JFM) never allows a break
    there and
  - turns the LuaTeX-ja glue after a cell (`ltj@icflag` 68, KANJI_SKIP)
    into the stretch of `hsep`, with no natural width and no shrink, which
    is what `\CJKglue` becomes under XeLaTeX.
- Characters without a mark that are typeset while annotation is on (text
  from macros, `\maketitle` and the `\input` fallback) carry only the scope
  attribute. For these, the callback runs TeX with `tex.runtoks`, calling
  `\xjyutping@lua@nocontext{<char>}{<size>}`, which does the lookup, writes
  the `[no context]` debug line and builds the cell data. This path is
  tested inside both callbacks. The options it uses are those in force when
  the paragraph is finished, while the size is the glyph's.
- The walker's punctuation tests (`\__xjyutping_if_class:nn`) use xeCJK's
  classes under XeLaTeX. Under LuaLaTeX they use `xjyutping.class`, whose
  lists are copied from xeCJK, with FullLeft = OP + PR and
  FullRight = CL + NS + EX + IS + PO + hyphens.
- The fancy strokes go through `\__xjyutping_literal:n`, which uses
  xdvipdfmx's `pdf:content` under XeLaTeX (this adds `q … Q` itself) and
  `\pdfextension literal {q … Q}` under LuaLaTeX. Since LuaTeX-ja refuses
  DVI output, there is no DVI path.
- The package loads LuaTeX-ja if it is missing, as it loads xeCJK under
  XeLaTeX, and then runs `require('xjyutping')`.

#### Verification

- All four jobs of `tests/run-tests.sh` give the same readings.
- A stress document (with `\maketitle`, `\section`, a footnote, macro text,
  `\disablejyutping`, a tabular with `p` and `c` cells and `\fbox`, a
  minipage, a TikZ node and, in a long run, —— and ……) gives identical
  debug logs under the two engines, including the `[no context]` lines. The
  renders match except where LuaTeX-ja spaces punctuation differently.
- The XeLaTeX renders of `regression.tex`, `layout-check.tex`,
  `fancy-check.tex` and that stress document are pixel-identical to 1.1.0.
- For size and speed, the results are,

  | Document | XeLaTeX | LuaLaTeX |
  | --- | --- | --- |
  | 29 118 characters, plain | 8.7–9.7 s, 68 pages | 13.3 s, 68 pages |
  | the same, `fancy` | 11 s, 70 pages | 17 s, 70 pages |
  | one paragraph of 20 000 characters, `fancy` | exceeds main memory | 13 s, 48 pages |
  | one paragraph of 40 000 characters, `fancy` | exceeds main memory | 23 s, 96 pages |

  Looking at the 29 118-character document, its time breaks down into
  typesetting without the package, running the preprocessor and building
  the cells, which take 1.2, 1.9 and 6.6 s under XeLaTeX and 2.2, 2.25 and
  8.9 s under LuaLaTeX. Loading the package takes 0.16 s under XeLaTeX and
  0.33 s under LuaLaTeX.

#### Bugs found while building the backend

L-1. The module was not found in the tests. With `TEXINPUTS=..:`, they
reported `module 'xjyutping' not found`. This is due to LuaTeX looking for
Lua files through `LUAINPUTS`. While the installed location
(`tex/latex/xjyutping/`) and the document's own folder are on that path, a
`TEXINPUTS` override is not. The fix was to set `LUAINPUTS=..:` in the test
scripts as well.

L-2. Only 3 of about 100 characters got rubies under LuaLaTeX. LuaTeX-ja
packs most characters into a one-glyph hbox, to give it its JFM width, and
copies the glyph's attributes onto that box. However, the first version of
`glyph_of` skipped any box carrying the cell attribute, a test meant to skip
the package's own cells, so it only found the few glyphs that LuaTeX-ja had
left unpacked (before 。). We found this by dumping the node list in a
callback placed before the package's. The fix was to skip only boxes
tagged -1, which are the cells.

L-3. The test documents loaded xeCJK unconditionally, although xeCJK does
not exist under LuaLaTeX. Now `regression.tex`, `layout-check.tex`,
`fancy-check.tex` and xjyutping-py's `parity.tex` use `iftex` to load xeCJK
under XeLaTeX and ctex under LuaLaTeX.

L-4. We removed a DVI branch for the stroke literal once it turned out that
LuaTeX-ja stops with "DVI output is not supported".

#### Review

We then had the backend reviewed the way 1.0.0 had been (Section 3.2), with
a regression sweep and a code review, each done by an agent. Every finding
was reproduced by a small document before it was fixed.

The sweep compiled every complete document among the review artefacts of
Section 3 (1 303 documents in 36 folders) twice with XeLaTeX and twice with
LuaLaTeX, with xeCJK replaced by `\usepackage[fontset=none]{ctex}`. It then
compared the errors, the overfull and underfull boxes, the pages and every
`xjyutping>` line. Of these documents, 48 were skipped, 24 because they are
too large for XeLaTeX's memory and 24 because they patch 1.0.0 internals.
Of the 1 255 compared, 1 115 agreed in everything, while the other 140 were
explained by,

- LuaTeX-ja's punctuation widths and line breaks (64),
- fonts that luaotfload does not find under the names given (26),
- documents that exceed XeLaTeX's memory and compile under LuaLaTeX (10),
- the same fatal error under both engines (9), documents without annotation
  (9), reviewer patch files (5), hyperref errors outside any scope (4),
  xeCJK-only commands (3), soul (2), xpinyin (1), log wrapping (1) and
- real defects in 6 documents (D1 and D7 below).

The code review found ten defects, all under LuaLaTeX.

D1 (medium). Text from a macro was annotated at the end of its paragraph, so
it took the settings in force there instead of those where it stood. To fix
this, `\xjyutping@lua@on` now takes a snapshot of the settings and tags what
follows with the snapshot's id. The snapshot is a token list of assignments,
and one copy of each distinct set is kept. The no-context build puts the
settings back (`\xjyutping@lua@restore`), and `\xjyutpingsetup` takes a new
snapshot. However, the `\setjyutping` readings are not in the snapshot, so
macro text still takes the readings in force at the end of its paragraph.
This limit is documented.

D1b (low). With a scaled CJK font, such as one at luatexja-fontspec's
default scale of 0.962216, the ruby of a no-context cell came out smaller and
lower than its neighbours'. This was due to the cell being built at the size
of the glyph's font. The fix is a third attribute, `xjyutping@size`, which
carries `\f@size` and is set in the `selectfont` hook while annotation is
on.

D2 (medium). The comma after `銀\uline{行}` did not hug its character. The
walker puts `\__xjyutping_nopad:` after a character that is followed by
invisible material and then ，or 。, but this macro did nothing. Now
`\xjyutping@lua@nopad` flags the last cell and `wrap` leaves out its right
pad, so `銀\uline{行}，` is 44.53pt wide, the same as without `\uline`.

D3 (medium). In a justified line, punctuation that hugs its character
drifted away from it. The cause was the glue between the character and the
punctuation, which took hsep's stretch. That glue is now zero, as under
XeLaTeX.

D4 (medium). A manual reading was lost when its character was not the token
right after the mark (`\xjyutping{\textbf{行}}{hong4}`, a brace group or
`\color`).

D5 (low). A reading given for a Latin letter or a punctuation mark was
typeset as a cell. We fixed D4 and D5 together in the code the engines
share, where `\__xjyutping_manual:nn` now walks the text token by token and
into brace groups, and puts a mark right before each Chinese character only.
The count warning counts Chinese characters (Part I, 1.2.0, says how this
differs from 1.1.0).

D6 (low). Cells stored for characters that never reach the callbacks (in
math and in `\discretionary`) stayed in the Lua table. Now no cell is built
in math mode, while `\discretionary` still leaks a few bytes per character,
with no visible effect.

D7 (medium). Chinese characters in a `\url` got no-context rubies, since
url.sty sets a `\url` in math. The fix was to have `\everymath` and
`\everydisplay` switch annotation off, which turned out to be too broad (see
"After the review" below).

D8 (high). The last character of a box got no ruby, even when it had its own
mark (`\mbox{\foo 大}`). This was due to the TeX code that `tex.runtoks` runs
for a no-context cell during `hpack_filter`. In a box, this code appended
LuaTeX-ja whatsits after TeX's stale tail pointer, the box's last glyph,
which LuaTeX-ja had meanwhile packed into a box of its own. The no-context
build now runs inside `\hbox_set:Nn \l__xjyutping_nocontext_box`, so it adds
nothing to the list being packed.

D9 (medium). For text from a macro in a TikZ node, the ruby was set in
`\nullfont` and sat on the character. This was because the node box is
packed where pgf's `\selectfont` selects `\nullfont`. The no-context build
now restores `\pgf@selectfontorig` and sets the size itself, and the output
matches XeLaTeX's.

D10 (low). The shrink of hsep and any fil order were lost, since only its
finite stretch reached Lua, as an integer. Now `store` reads the whole glue
with `token.scan_glue`.

After three rounds of fixes, every reproduction document gives the same
debug log under both engines (except D1's `\setjyutping` case), and the
widths of D2 and the glue of D3 and D10 match XeLaTeX's. The first rewrite
for D4 lost the braces of a group holding one token, so that
`\xjyutping{\textbf{行}}{hong4}` printed `uhong4`. The walk now takes one
token or one brace group at a time (`\tl_if_head_is_group:nTF`).

#### After the review

We ran the sweep once more on the finished code, over the 393 documents in
the ten folders that exercise the walker, the layout and whole user
documents. This run used the 1.1.0 data, so that only code changes show. It
found two regressions, both of which were fixed.

- The body collector of `linebreak` broke a scope opened by a user
  environment and a scope inside braces within a scope. This affected
  3 documents under both engines (Section 7.6, LB-3).
- D7's guard also switched annotation off in text inside math. Specifically,
  it did so in `\text`, in `\mbox` and in the cells of a tabular, which LaTeX
  builds inside `$…$`. Hence `\maketitle`'s `\author`, which is a tabular,
  lost its rubies under LuaLaTeX. Now `\everyhbox` and `\everyvbox`
  (LuaTeX-ja's registers, which it runs from the primitive ones) switch
  annotation back on in a box inside math (`\__xjyutping_unmath:`). This is
  what XeLaTeX does, since xeCJK sees text-mode material inside math. The
  change also lifted a documented limit, as `$\text{\foo}$` is now annotated
  under LuaLaTeX too.

After these fixes, XeLaTeX is unchanged in all 393 documents, in its errors,
boxes, pages and every debug line. While LuaLaTeX has the same errors and
overfull boxes, it gives fewer no-context cells in 3 documents (D7 and soul)
and reports more underfull boxes in 7 documents with narrow columns, from 22
to 37 in all. This is due to the glue before punctuation, which no longer
stretches (D3). XeLaTeX reports underfull boxes in the same places. The debug
logs of the two engines differ in 7 documents (8 before), all for the
reasons listed above. One stress test (`code-review/t14-hash-exhaust.tex`)
runs over the sweep's 300 s limit under both engines, as it did before.

### 7.4 More vocabulary

An agent built the new vocabulary in the background. Its full evaluation
files (the added words, the rejected candidates, the disagreements with rime,
the book characters and the test sentences) were in the session's scratch
directory.

The script `tools/fetch-sources.sh` fetches each source at the commit given
below.

| Folder | Upstream | Commit |
| --- | --- | --- |
| `jyutping-table-master/` | lshk-org/jyutping-table | `dad2dd6d6f02fc51138ecc6818f7b38eba5c2ad3` (2024-01-12) |
| `rime-cantonese/` | rime/rime-cantonese (the files cite CanCLID/rime-cantonese-upstream) | `259f0e48bba840c3a2e0d117539e96937f3d89bc` (dictionaries 2026.08.10) |
| `opencc/` | BYVoid/OpenCC `data/dictionary` and LICENSE | `e02cb540b9f98b2da7868b4e8f7b43f88bacadc5` |
| `cantonese-books-data/` | jyutnet/cantonese-books-data | `02740c7e136e2766d7931a37ed0633aa41009ae1` (2026-09-25) |
| `jyut-dict/` | aaronhktan/jyut-dict, sparse: `src/dictionaries`, `src/jyut-dict` without `vendor/` | `26526015424de3f9c30cd9c7e42b96dadb068b6a` (2026-09-28) |

The local copies of the four older sources match those commits byte for
byte, and a fresh fetch into an empty directory rebuilt identical data.

Inspecting jyut-dict shows that `src/jyut-dict` is the Qt application, with
its code, translations, an empty user-database template and `audio.zip`
(6 145 syllables of speech), and that it has no vocabulary. The word data is
in `src/dictionaries/cedict/data`. There, `CC-CANTO.txt` is CC-Canto
(Version 2017-02-02, © 2015–17 Pleco Inc., CC BY-SA 3.0) and `READINGS.txt`
is "CC-CEDICT Cantonese Readings" (Version 2015-09-23, © 2015 Pleco Software
Inc., CC BY-SA 3.0). `FULLREADINGS.txt` holds the two combined and
lowercased, so it is not read. `CC-CEDICT.txt`, `CFDICT.txt` and
`HANDEDICT.txt` have no Cantonese and are not used. The other folders of
`src/dictionaries` hold only scripts that download their data elsewhere.

The candidate words are the headwords of 2 or more characters that the list
lacks under their raw or canonical spelling, 52 660 in all. Their
romanisation is normalised, meaning that it is lowercased, only the first of
`a / b` is kept and the changed tones `cin4*2` and `hang4*haang4` become cin2
and haang4. A candidate is added only if all of the following hold,

1. Each syllable is a reading that LSHK, rime or a book gives the character,
   or a changed tone (tone 1 or 2) of such a reading. This rejected 155
   candidates.
2. Every word of the list inside the candidate keeps a reading that rime
   gives that word. This rejected 568 (for example, 車公廟站 miu6 against
   rime's 車公廟 miu2).
3. The same holds for every pair of characters that occurs in rime's words.
   This rejected 656 (過嚟 lai2, 唔會 wui2, 上個禮拜 soeng5).
4. It does not change the tone of a sentence-final particle. This rejected
   21 (你好嗎 maa1, 得喇 laa1).
5. It passes the tie rule, under which a two-character word AB is refused if
   some word of the list ends in A with another reading, because on a tie
   the later word would steal A. This is the 屋企|住 → 屋|企住 bug. The rule
   rejected 8 908 candidates. While it prevented regressions from 種花
   (呢種花), 長得 (時間長得可怕), 行好 (品行好), 當上 and 上行, it also blocks
   some good words (重未, 慢行).
6. The list, with the shorter new words already added, reads it otherwise.
   Words are processed shortest first, and this condition left out 38 877
   candidates that already read as their source says.
7. It is not in `EXCLUDED_WORDS`, which holds 480 words checked by hand. They
   are readings that Hong Kong and rime do not use (乙 jyut3, 這 ze5, 陷 haam6,
   購/構 gau3, 擾 jiu5 …), dropped changed tones (慳錢 cin4, 練習簿 bou6),
   names read otherwise (柯士甸, 楊千嬅, 許冠傑), wrong readings (同學會 wui5,
   左行 haang1) and words that would steal characters (方法|會 → 方|法會,
   中學|到 → 中|學到, 家長會 before modal 會, 照會, 知會 …).

Where both sources have a word, CC-Canto wins, then the most usual
syllables. Only 50 words were in both, and they all agreed. In all, 2 291
words were added, 1 927 from the CC-CEDICT readings and 364 from CC-Canto.
They include 基金會/房委會/研討會 wui2, 冠狀病毒 gun1, 智能卡 kaat1,
機長/理事長 zoeng2, 交換生/侍應生 sang1, 曾蔭權 zang1, 上海話 waa2,
動畫片/芯片 pin2, 幾位 wai2, 手相 soeng3, 自由行/單行 hang4 and
營業額/成交額 ngaak2.

We also added 640 characters that LSHK and rime lack. Each takes the first
reading not labelled 俗/舊/古/本/原/誤/罕/專名 from the first book in `BOOKS`
that has it. In the counts that follow, each book is named by its year and
followed by the number of characters taken from it. The modern books give
2004 34, 1988 211, 1974/96 72, 1985 26, 1971 1, 1967 31, 1947 60 and 1941 4.
Four pre-1940 books, used through the modern Jyutping their digitiser
derived, give 1939 172, 1931 2, 1916 2 and 1914 25. Of the 640, 58 are
flagged as polyphones. We left out compatibility ideographs, books with
reconstructed readings only and the 1962 廣州音字彙, which the collection
itself withdrew as inaccurate.

The example words in the books (the ～ in glosses) were evaluated and not
used, since only the headword's reading is given, many are classical
fragments, the books contradict each other (龜茲) and several would impose
conservative, non-Hong-Kong readings on common words (韌性 ngan6, 餅食 bing2).

We evaluated the result with the Python package, which gives the same
readings as TeX, by comparing the old data against the new. In the audited
corpora of the earlier rounds (17 files, 8 349 characters), 2 readings
changed, both neutral: 舊樓 lau2 and 成交額 ngaak2. In three files of new
test sentences (1 804 characters, with about 30 traps for the risks above),
there were 27 changes, of which 24 were improvements and 3 neutral. Examples
are 機長 zoeng2, 消防隊 deoi2, 膠帶 daai2, 雙人房 fong2, 香港公園 jyun2,
核彈 daan2 and 請問幾位 wai2.

There were no regressions. The first version, with filters 1–3 only, changed
48 characters in the corpora, most of them for the worse (你好嗎, 得喇, 過嚟,
唔會, 種花, 長得, 慳錢, 這次, 划船 …). Filters 4–5 and the exclusions came
from those cases. On the TeX side, while `regression.expected` is unchanged,
xjyutping-py's `parity_expected.txt` changed in one line: 隨着 is now one
word, with the same readings.

Two hand fixes were added to `CURATED_WORDS`. The first is 化合物 faa3 hap6
mat6, where rime has gap3, a 0% reading of 合, although its own 化合 is hap6.
The second is 會否 wui5 fau2, where rime has wui2 but the modal is wui5. We
did not apply 這個 ze2, 開玩笑/玩笑 waan4, 敏捷 zit6, 分散 saan3, 預訂 ding6,
應允 jing3 or 重未 zung6, because they are disputed or would change the
regression demo.

CC-Canto disagrees with rime in 1 910 of its 16 929 known words, and the
CC-CEDICT readings in 1 575 of 53 957 CC-CEDICT words. Mostly, the two
sources drop Hong Kong changed tones (面 min2, 女 neoi2, 頭 tau2) or use
standard or Guangzhou readings (券 hyun3, 購 gau3, 擾 jiu5, 嚟 lei4). In every
case, rime was kept.

Since the word lists are CC BY-SA 3.0, the generated data (the `.def` files
and the Python TSVs) must be shared alike. It is distributed under CC BY-SA
4.0, which 3.0 §4(b) allows, and the CC BY 4.0 (LSHK, rime) and Apache-2.0
(OpenCC) material may be part of it, with credit.

The cantonese-books-data repository states no licence. The site jyut.net
says "© 2014-2026 粵音資料集叢" and offers the files for researchers'
convenience. Only the readings of 640 rare characters are used, with credit.
Before a wide release, it would be prudent to ask the author (through a
GitHub issue or jyut.net). Emptying `BOOKS` builds the data without them.

The figures, old against new, are,

- characters 29 449 → 30 089 (polyphonic 4 349 → 4 407),
- words 101 277 → 103 579 and canonical-spelling aliases 68 → 133,
- `xjyutping-words.def` 3.43 → 3.52 MB and `xjyutping-chars.def` 516 → 527 KB,
- the build time 0.7 → 3 s and
- `Jyutping()` construction about 5–9 % slower, with XeLaTeX times unchanged
  within noise.

The agent was stopped twice by an API usage limit and resumed with its
context. An `importlib` import of the script also created a `__pycache__`,
which our interim commit picked up (Section 7.2).

### 7.5 Documentation and versions

The README of this package now covers the engines, the new licence of the
data and the data sources with their filters. It also has a separate
"Acknowledgements and attributions" section, which names xpinyin by Qing Lee
(李清) as the inspiration and credits Visual Jyutping (Vincent Tam) and the
Visual Cantonese Fonts (Jon Chui / A3I Ltd., canto.hk) for `fancy`. Beyond
these, the section credits the data sources,

- the LSHK Jyutping Workgroup,
- rime-cantonese (CanCLID),
- 石見田 and the books of 粵音資料集叢,
- Jyut Dictionary (Aaron Tan) with CC-Canto and the CC-CEDICT readings
  (Pleco) and CC-CEDICT (MDBG) and
- OpenCC.

We checked the author names against `xpinyin.dtx`, the Python xpinyin
`setup.py`, Visual Jyutping's LICENSE, canto.hk's footer and the LSHK README.

In the manual, the "Getting started" example uses ctex for either engine, and
there is a new section, "XeLaTeX and LuaLaTeX". The limits, the data and the
acknowledgements in the manual are updated as well.

This package is now at version 1.2.0 (new features, backward compatible), and
the Python package at 1.1.0 (new vocabulary).

### 7.6 The `linebreak` option

We wanted an option like `fancy`, usable as
`\begin{jyutpingscope}[linebreak]`, under which every line end of the source
becomes a line break (`\\` or `\newline`) and a blank line becomes a
paragraph break that follows the usual LaTeX conventions. For example, with
`\usepackage[parfill]{parskip}` the new paragraph has no indent. While our
request gave two lines of a song as its example, the documentation uses 靜夜思
(Li Bai, public domain) instead.

Since the line ends must reach the package as characters, the catcode of ^^M
is 12 (other) while the body is read. However, a `+b` argument is read before
the begin code runs, that is, before the option is known. The environment
therefore takes only `O{}` and collects its body itself
(`\__xjyutping_collect:w`), and with `linebreak` off the catcodes stay as they
are.

The collector follows ltcmd's `+b`. It grabs the text up to the next `\end`
outside braces, counts the `\begin` tokens outside braces in that text and
stops at the first `\end` that closes none of them. It leaves that `\end` to
read its own argument, so `\end{lesson}` of a user environment ends the scope
through the environment's end code. A `\q_nil` in front of each piece keeps
the braces of a piece that is one group, and without `linebreak` the body is
trimmed of spaces, as `+b` trims it.

`\__xjyutping_lines:N` then rewrites the body with l3regex. It drops line
ends and spaces at both ends, turns two or more line ends in a row (a blank
line) into `\par` and drops a line end after `\\` or `\newline`. Any other
line end becomes `\__xjyutping_newline:`, which issues `\newline` in
horizontal mode unless the next token is `\begin`, `\end` or `\par`. The
walker ends a run at `\newline` and `\par`, so no word is looked up across
two lines. A `%` at a line end removes the line end as usual.

We found three bugs while building the option.

- LB-1. Under LuaLaTeX, the first line break was lost when the option came
  from `\xjyutpingsetup` and the environment had no optional argument. This
  is due to LuaTeX-ja's `process_input_buffer` callback, which appends
  U+FFFFF, a comment character (`\ltjlineendcomment`), to a line that ends in
  a Chinese character while ^^M has catcode 5, so that the line end gives no
  space. Moreover, looking for the optional argument reads the first line of
  the body before the begin code runs. A first fix, `!O{}`, stopped the
  look-ahead but also refused a space before `[linebreak]`. In the fix we
  kept, the catcode of `\ltjlineendcomment` is 9 (ignored) inside the scope,
  so the appended character vanishes and the line end survives. LuaTeX-ja
  appends nothing further while ^^M is catcode 12.
- LB-2. A `\newline` right before `\begin{center}` gave an underfull box. To
  fix this, `\__xjyutping_newline:` now does nothing before `\begin`, `\end`
  and `\par`.
- LB-3. A scope opened by a user environment ran to the end of the file, and
  so did a scope inside braces within a scope ("File ended while scanning use
  of `\__xjyutping_collect:w`"). The final sweep found the bug (Section 7.3,
  "After the review"). This was due to the first collector, which stopped
  only at `\end{jyutpingscope}` and counted nested scopes with a regex that
  also sees inside braces. We rewrote the collector to follow `+b`, as
  described above.

We tested line ends, blank lines, `\\`, `%`, `center` and `parskip`, as well
as the option given as `[linebreak]`, as ` [linebreak]` after a space and
through `\xjyutpingsetup`, all under both engines. This gave 0 errors, 0 bad
boxes and the same debug logs. The test files were not kept, although
`tests/regression.tex` keeps a `linebreak` scope and a scope opened by a user
environment.

The option has one limit. It works only where the line ends are still in the
source when the scope begins, so it does nothing in `\xjyutping*`, in a scope
inside a command's argument (`\parbox{…}`) or in a scope inside a scope
without the option. Inside environments such as `minipage` or `center`, on
the other hand, it works.

### 7.7 Open issues after 1.2.0

The README and the manual document the first three issues.

1. Under LuaLaTeX, text from a macro takes the `\setjyutping` readings in
   force at the end of its paragraph (D1), while its options and size are
   those of the place where it stands. A fix would put the user readings into
   the snapshot, copying them at every change.
2. Under LuaLaTeX, LuaTeX-ja's rules for punctuation and line breaks apply
   (no break before —— or ……), so lines break differently from XeLaTeX.
3. `linebreak` needs the line ends in the source (Section 7.6).

The README does not mention the other four.

4. Under LuaLaTeX, a cell built for a character in `\discretionary` is never
   used and stays in the Lua table (D6).
5. The long-mark branch of `wrap` (a discretionary holding the pad) never
   fires with ctex's JFMs, which forbid a break before —— and ……. It is kept
   for other JFMs but is untested.
6. The 640 characters from cantonese-books-data come from a source with no
   licence statement (Section 7.4). However, CTAN and TeX Live distribute
   only freely licensed material. Before uploading, we need either to ask
   石見田 for permission (through a GitHub issue or jyut.net) or to empty
   `BOOKS` in `tools/build-data.py` and rebuild the data.
7. Items 11–15 of Section 4 (R3-14, R2-14, the line pitch after deep lines,
   ambiguous readings and the segmentation tie-break) are unchanged.

### 7.8 Tests and release files at 1.2.0

`tests/run-tests.sh` has four jobs and 26 expected lines, and all give
`readings ok`.

`tools/make-ctan-zip.sh [OUT]` builds the archive for CTAN, by default
`../xjyutping.zip`. The archive holds one folder, `xjyutping/`, with
`README.md`, `LICENSE`, `CHANGELOG.md`, the package (`xjyutping.sty`,
`xjyutping.lua` and the two `.def` files), the manual (`xjyutping-doc.tex`
and `.pdf`), `tools/` and the sources in `tests/`. Files get permissions 644,
and folders and scripts 755. The script stops if a file does not carry
the version of `xjyutping.sty` and warns if the manual's PDF is older than
its source. Whenever `xjyutping-doc.tex` has changed, rebuild the manual
first by running `xelatex xjyutping-doc` twice, which needs the font Songti
TC.

We checked the 1.2.0 archive by unpacking it and compiling, from its files
alone, a sample document with each engine and the manual, and by running its
`tests/run-tests.sh`.

The CTAN upload form takes these values,

- the licences `lppl1.3c` for the code and `cc-by-sa-4` for the data,
- the suggested directory `/macros/unicodetex/latex/xjyutping`,
- the home page and repository https://github.com/Beyond3345/xjyutping-tex
  and
- the bug tracker https://github.com/Beyond3345/xjyutping-tex/issues.

The Python package is released separately as xjyutping-py 1.1.0 (see its
changelog).

## 8. Version 1.3.0: alignment, and `linebreak` fixed (2026-09-29)

### 8.1 The report

We tested a lyric sheet (a song text, not reproduced here) with
`\usepackage[fancy]{xjyutping}`, `\usepackage[parfill]{parskip}` and
`\begin{jyutpingscope}[linebreak]` with `\centering` as the first line of
the body. Our report also included two reference PDFs of the same text, made
without the package's help, one with the lines centred and one with the
stanzas spaced. In the package's output, the lines drifted left of centre,
the more so the shorter they were, and the stanzas nearly touched.

We wanted an alignment option, as in `[linebreak,fancy,centre]`.

### 8.2 Causes

The lines were off centre because line ends became `\newline`.
Specifically, LaTeX's `\newline` is always the normal `\\` (`\hfil\break`),
while `\centering` redefines only `\\`. Since `\centering` sets both
`\leftskip` and `\rightskip` to 0pt plus 1fil, the extra `\hfil` makes 2fil
on the right against 1fil on the left. Hence each line sits a third of the
way across its free space. Measured on the lyric sheet with
`gs -sDEVICE=txtwrite`, the line centres ranged from 267 to 305.5pt, against
305.5pt for every line in the reference.

The stanza gaps were invisible because the gap was only `\parskip`, that is,
6pt (parskip's `.5\baselineskip` at 10pt) on a line pitch of 20pt in the
scope, where the pitch is raised for the rubies. The reference had 30pt
between stanzas against 12pt between lines. That gap is an empty line plus
the paragraph space, which is what LaTeX gives for `\\` before a blank line.

### 8.3 Changes

`\__xjyutping_newline:` now issues `\\ \scan_stop:`, where the `\scan_stop:`
keeps a line that starts with `[` or `*` from being read as an argument of
`\\`. Under `\centering`, `\raggedright` and `\raggedleft`, `\\` is
`\@centercr`, so each line becomes a paragraph and the paragraph space
between lines is cancelled.

A blank line now gives `\par` followed by `\__xjyutping_stanza:`, which adds
`\addvspace{\baselineskip}` (one line of the scope) in vertical mode. The
next paragraph then adds `\parskip` and its indent as usual.
`\__xjyutping_stanza:` is declared in the command table as class `z`, so it
ends a run. The `\par` in front of it keeps the walker's split into
paragraphs, which matters for TeX's memory under XeLaTeX (Section 2.10).

We added an `align` key, which is a `.choices:nn` key with the values
`justify`, `left`, `centre`, `center` and `right`. Meta keys of the same
names set it. `\__xjyutping_align:` applies `\raggedright`, `\centering` or
`\raggedleft` in the environment's begin code. When the alignment is not
`justify`, a `\par` comes first, so text before the scope keeps its own
alignment. `\l__xjyutping_align_tl` is declared before `\keys_define:nn`,
since the defaults are set right after it and a `\tl_new:N` after a
`\tl_set_eq:NN` would fail.

Since 1.2.0 had been pushed, the version is now 1.3.0, a MINOR release for a
new option. The Python package does not change.

### 8.4 Verification

We compiled a copy of the lyric sheet with the fixed package. The output with
`\centering` in the body and with `[linebreak,centre]` is the same, and every
line's centre is at 305.5pt, as in the reference, except one line with Latin
text, which is at 302.5pt in both. The stanza gaps are 45–46pt against a line
pitch of 20pt (in the reference, 30pt against 12pt).

`tests/verse-check.tex` (靜夜思 and 春曉, both public domain) gives 0 errors
and 0 bad boxes under both engines. Within each scope, the line centres, left
edges or right edges are constant, and the stanza gaps are 46pt under XeLaTeX
and 50pt under LuaLaTeX, where ctex's line spacing is larger.

In `tests/run-tests.sh`, the regression document's `linebreak` scope now has
`centre`, and all four jobs give `readings ok` with no bad boxes.

The renders of `layout-check.tex` and `fancy-check.tex` are pixel-identical
to 1.2.0 under both engines. The 1.2.0 regression document differs only where
the second stanza of its `linebreak` scope now sits one line lower.

### 8.5 Open issues after 1.3.0

1. With `left`, the first cell's left pad keeps the characters slightly in
   from the margin (the pad makes room for a ruby wider than its character).
   The same holds at the right margin with `right`. This is part of the cell
   design rather than a defect.
2. The empty line at a stanza break is one `\baselineskip` of the scope.
   There is no key to change it, and a `stanzaskip` key would be the place
   for one.
3. `align` has no effect in `\xjyutping*`, which is running text.
