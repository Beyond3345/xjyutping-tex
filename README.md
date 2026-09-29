# xjyutping (LaTeX)

Version 1.2.0 (2026-09-28). Versions follow
[Semantic Versioning 2.0.0](https://semver.org); the history, and handover
notes for maintainers, are in [`CHANGELOG.md`](CHANGELOG.md).

A LaTeX package that puts Jyutping (粵拼) above traditional Chinese
characters, choosing each reading from the words around it. It works with
XeLaTeX (through `xeCJK`) and LuaLaTeX (through LuaTeX-ja), including the
`ctex` package and classes under either engine. A Python version with the
same readings is [xjyutping-py](https://github.com/Beyond3345/xjyutping-py).

```latex
\documentclass{article}
\usepackage[fontset=none]{ctex}  % compile with xelatex or lualatex
\setCJKmainfont{Songti TC}       % any traditional Chinese font
\usepackage{xjyutping}
\begin{document}
\begin{jyutpingscope}
我哋去銀行，行路返屋企。校長喺學校長大。
\end{jyutpingscope}
\end{document}
```

行 comes out as *hong4* in 銀行 and *haang4* in 行路; 長 as *zoeng2* in 校長
and 長大.

Instead of `ctex` you can load `xeCJK` (XeLaTeX, `\setCJKmainfont`) or
`luatexja-fontspec` (LuaLaTeX, `\setmainjfont`); if none of them is loaded,
`xjyutping` loads `xeCJK` or LuaTeX-ja itself.

## Commands

| Command | Effect |
| --- | --- |
| `\begin{jyutpingscope}[opts] … \end{jyutpingscope}` | Annotate every character in the block. The block ends the paragraph; line spacing inside is made even and wide enough that rubies never come near the line above. |
| `\xjyutping*[opts]{text}` | The same for a piece of running text. |
| `\xjyutping[opts]{字}{reading}` | Give one character (or a word, `\xjyutping{銀行}{ngan4 hong4}`) an explicit reading, inside or outside a scope. |
| `\setjyutping{字}{reading}` | Change a character's default reading, used when it is not part of a known word. |
| `\setjyutping{詞}{readings}` | Add or override a word: `\setjyutping{重話}{zung6 waa6}`. Words win over character defaults. |
| `\disablejyutping`, `\enablejyutping` | Switch annotation off and on inside a scope (until the end of the current group or environment). |
| `\xjyutpingsetup{opts}` | Set options (also accepted as package options). |

`\setjyutping` is global and takes effect from where it appears, including in
the middle of a scope. (Inside a scope it is noticed while the text is read,
so one inside `\iffalse … \fi` or an unused macro definition still applies
to the text after it; keep conditional settings outside the scope.)

## Options

| Key | Default | Meaning |
| --- | --- | --- |
| `ratio` | `0.45` | Jyutping size relative to the text size. |
| `vsep` | `1.05em` | Baseline of the Jyutping above the baseline of the character. |
| `hsep` | `0.15em plus 0.4em` | Space between neighbouring cells. The natural part is the least gap between two Jyutping; the stretch lets lines justify. |
| `width` | `auto` | `auto`: every character in a block (a scope or a `\xjyutping*`) gets the same cell width, wide enough for the longest Jyutping in that block. `natural`: each cell only as wide as its own character or Jyutping. A length (`1.8em`): a fixed grid; a longer Jyutping widens its own cell. |
| `font` | `\normalfont` | Font for the Jyutping (font commands only). |
| `format` | empty | Extra formatting, e.g. `\color{gray}` or `\itshape`. |
| `multiple` | empty | Formatting for characters with several common readings whose reading was *guessed* (not settled by a word or by you), e.g. `\color{red}` while proofreading. |
| `fancy` | `false` | Show tones as Visual Jyutping does: a pitch stroke and a small raised or lowered tone number (see below). |
| `linebreak` | `false` | In `jyutpingscope`, keep the lines of the source: each line end becomes a line break, each blank line a paragraph break (see below). |
| `debug` | `false` | Write each segmented run to the log: `xjyutping> 銀ngan4:w行hong4:w \|去heoi3:s \|重cung5:m(zung6 cung4)`. Types: `w` word, `u` your setting, `m` guessed polyphone (other readings in brackets), `s` single-reading character. Characters annotated without context (see below) are logged as `[no context]`. |

## Fancy tones

`\usepackage[fancy]{xjyutping}` (or `fancy` in `\xjyutpingsetup`, or in the
options of one scope) replaces each tone number with a small stroke that
traces the pitch of the tone, followed by a smaller tone number, the way
[Visual Jyutping](https://github.com/VincentTam/visual-jyutping) writes
jyutˍ₆ ping˗₃:

| Tone | Stroke | Number | Example |
| --- | --- | --- | --- |
| 1 | high level (ˉ) | raised | 詩 si1 |
| 2 | rising to high (ˊ) | raised | 史 si2 |
| 3 | mid level (˗) | lowered | 試 si3 |
| 4 | falling to low (ˎ) | lowered | 時 si4 |
| 5 | rising from low (ˏ) | lowered | 市 si5 |
| 6 | low level (ˍ) | lowered | 事 si6 |

The strokes are drawn rather than taken from a font, so any `font` works and
they take the colour of `format` and `multiple`. The spacing follows the new
shape automatically: cells are measured with the strokes and small numbers in
place (with `width=auto` the cells come out a little wider), line spacing
makes room for the raised numbers, and if the lowered numbers reach below the
letters of the chosen font, the Jyutping is lifted by the difference so that
it keeps its distance from the character. A syllable without a tone number
(`\xjyutping{唔}{m}`) is printed as it is. PDF bookmarks and the debug log
keep plain Jyutping with tone numbers.

## Verse and lyrics: `linebreak`

With `\begin{jyutpingscope}[linebreak]` (or `linebreak` in
`\xjyutpingsetup` or the package options) the lines of the source are kept:

```latex
\begin{jyutpingscope}[linebreak]
床前明月光，
疑是地上霜。

舉頭望明月，
低頭思故鄉。
\end{jyutpingscope}
```

Each line end inside the scope becomes a line break, as if it were written
`\\` or `\newline`, and each blank line (one or more) a paragraph break, so
the next stanza starts a new paragraph by the document's usual rules:
indented by default, or with no indent and some space before it with
`\usepackage[parfill]{parskip}`. Line ends at the start and end of the
scope, after a `\\` and before `\begin`, `\end` or a new paragraph add no
break, and a line ending in `%` joins the next one as usual. A line break
also ends a run of characters, so a word is not looked up across two lines.

The option works for the environment only, and only where the line ends
are still in the source when the scope begins: not in `\xjyutping*`, nor in
a scope inside the argument of a command (`\parbox{…}`) or inside a scope
without the option, whose text has been read already. Inside an environment
such as `minipage` or `center` it works.

## How readings are chosen

1. The text is split into runs of Chinese characters. Punctuation, Latin
   text and most commands end a run; spaces and line breaks between two
   characters do not, and neither do braces or formatting commands
   (`\textbf`, `\emph`, `\color`, `\textcolor`, size commands …), so
   `銀\textbf{行}` is still the word 銀行. The text of a `\footnote` is a run
   of its own, and the text around it carries on.
2. Each run is segmented with a list of about 104 000 words: fewest words
   first, then fewest single characters; on a tie the longer final word wins.
3. A word takes its reading from the list (your `\setjyutping` words first).
4. A character left on its own takes your `\setjyutping` reading if there is
   one, else its default. A few characters read differently at the end of a
   run (呢 is *ni1* in 呢張床 but the particle *ne1* in 你呢？).
5. `\xjyutping{…}{…}` always wins and also splits the run.

Variant shapes are folded together for word lookup, so 為/爲, 裡/裏, 説/說,
衞/衛, 綫/線, 恒/恆 and the like all find the same words.

## XeLaTeX and LuaLaTeX

The readings, the options and the layout are the same under both engines;
only the machinery differs. Under XeLaTeX, `xeCJK` hands each Chinese
character to a hook in which the package builds the character's cell. Under
LuaLaTeX the rubies are built as the text is read, and a Lua function (in
`xjyutping.lua`, which must be installed next to `xjyutping.sty`) puts each
cell together after LuaTeX-ja has laid out the line. So under LuaLaTeX:

* LuaTeX-ja's rules for punctuation widths and line breaks apply (for
  example, a line never breaks just before —— or ……);
* a paragraph can be as long as you like (a 40 000-character paragraph
  compiles; XeLaTeX stops at about 15 000);
* compiling takes about 1.6 times as long as with XeLaTeX;
* text that comes from a macro is annotated when its paragraph is finished,
  with the options in force at that point (its size is taken from the
  character itself).

pdfLaTeX is not supported.

## Things to know

* The environment body and the argument of `\xjyutping*` are read in full
  before typesetting, like any macro argument: `\verb` and verbatim
  environments cannot go inside, and in a `\url` or `\href` inside a scope a
  `%` must be written `\%`.
* `\input{file}` inside a scope reads the file as part of the scope, with the
  same restrictions as the body. A file that uses `\endinput`, `\verb`,
  verbatim environments, `\makeatletter` or catcode changes is instead input
  normally and annotated without word context. Text that comes from a macro,
  an `\include`d file or `\maketitle` is also annotated character by
  character without word context (the debug log marks it `[no context]`):
  put `\xjyutping*` inside the macro, or a scope inside the included file.
* Arguments of `\label`, `\ref`, `\cite`, `\index`, `\url`, `\href` (first
  argument), `\hyperref[…]`, `\hyperlink`, `\pdfbookmark`, `\includegraphics`,
  the cleveref commands, environment names and a few more are passed through
  untouched.
* Give other commands their Chinese argument in braces (`\textbf{行}`, not
  `\textbf 行`).
* Section titles, captions and footnotes inside a scope are annotated. The
  table of contents is annotated only if `\tableofcontents` is itself inside
  a scope (an explicit `\xjyutping` in a title is annotated there too);
  running heads and PDF bookmarks are always plain.
* In beamer, a `\frametitle` inside a scope is typeset after the scope has
  ended and stays plain: write `\frametitle{\xjyutping*{…}}`.
* The underline and emphasis-mark commands of `xeCJKfntef` (XeLaTeX only:
  `\CJKunderline`, `\CJKunderdot` …) do not keep the cell spacing inside a
  scope; use `\underline` or `ulem`'s `\uline` there.
* One scope can hold well over 100 000 characters. Under XeLaTeX a single
  paragraph is limited to about 15 000 by TeX's memory (each annotated
  character is a small box), about 13 000 with `fancy`; LuaLaTeX has no such
  limit. A brace group spanning many paragraphs is read in one piece.
* Characters not in the data are typeset in their cell without Jyutping.
* Under LuaLaTeX, text that comes from a macro takes the `\setjyutping`
  readings in force when its paragraph ends (under XeLaTeX, those in force
  where it stands); text written out in the scope is not affected.

## Data

`xjyutping-chars.def` (30 089 characters) and `xjyutping-words.def` (about
104 000 words) are generated by `tools/build-data.py` from third-party
sources that are kept outside the repository, by default in the directory
that contains it; `tools/fetch-sources.sh` fetches all of them at the commits
the data was built from:

| Folder | Source | Used for |
| --- | --- | --- |
| `jyutping-table-master/` | LSHK *Cantonese Pronunciation List of Characters for Computers* (粵拼表) | character readings |
| `rime-cantonese/` | rime-cantonese `jyut6ping3.chars` and `jyut6ping3.words` | default readings, the main word list |
| `opencc/` | OpenCC `HKVariants.txt` and `TWVariants.txt` | variant shapes |
| `jyut-dict/` | Jyut Dictionary's `src/dictionaries/cedict/data`: CC-Canto and the Cantonese readings of CC-CEDICT | 2 291 more words |
| `cantonese-books-data/` | the book data of 粵音資料集叢 | readings of 640 characters the others lack |

rime-cantonese is authoritative: its default readings and word readings are
never replaced by another source. A word from CC-Canto or the CC-CEDICT
readings is added only if the list would read it otherwise and it passes
checks against rime (every reading known for its character, no inner word or
character pair read differently, no sentence-final particle retoned, no
character taken from a neighbouring word); 480 more were excluded after a
check by hand. The hand-checked tables in `tools/build-data.py`
(`CURATED_DEFAULTS`, `CURATED_FINALS`, `CURATED_VARIANTS`, `CURATED_WORDS`,
`EXCLUDED_WORDS`, `BOOKS`) correct the sources where they are wrong or
undecided; run `python3 tools/build-data.py` after editing them (with
`--sources DIR` if the sources are elsewhere). It also rewrites the data of
the Python package when the `xjyutping-py` repository sits next to this one
(or with `--py-data DIR`).

## Installing

Keep `xjyutping.sty`, `xjyutping.lua` (needed by LuaLaTeX),
`xjyutping-chars.def` and `xjyutping-words.def` together, either next to your
document or in your personal tree (`~/Library/texmf` on macOS, `~/texmf` on
Linux):

```bash
d="$(kpsewhich -var-value TEXMFHOME)/tex/latex/xjyutping" && mkdir -p "$d" && cp xjyutping.sty xjyutping.lua xjyutping-*.def "$d"
```

The manual is `xjyutping-doc.pdf` (source `xjyutping-doc.tex`).

## Testing

`tests/run-tests.sh` compiles `tests/regression.tex` with XeLaTeX and with
LuaLaTeX, each with and without `fancy`, and compares every debug log with
`tests/regression.expected`. `tests/render.sh tests/layout-check.tex
[xelatex|lualatex]` and `tests/render.sh tests/fancy-check.tex
[xelatex|lualatex]` render the pages to PNG for a visual check of the spacing
and the tone marks.

## Acknowledgements and attributions

**Inspiration.** This package was inspired by the authors of the LaTeX
package [xpinyin](https://ctan.org/pkg/xpinyin) by Qing Lee (李清), which puts
Hanyu Pinyin above simplified Chinese characters; xjyutping follows its way of
annotating characters through xeCJK's `\CJKsymbol` hook.

**The `fancy` option** was inspired by
[Visual Jyutping](https://github.com/VincentTam/visual-jyutping) by Vincent
Tam, whose tone symbols it draws, and by the Visual Cantonese Fonts
(粵語字體) by Jon Chui / A3I Ltd.: [canto.hk](https://canto.hk), with
documentation at [docs.visual-fonts.com](https://docs.visual-fonts.com)
([source](https://github.com/jkwchui/visual-fonts-starlight-docs)).
Thank you both.

**Readings and vocabulary.** Many thanks to the authors of every source the
data is built from:

* the *Cantonese Pronunciation List of Characters for Computers*
  (電腦用漢字粵語拼音表), maintained by the Jyutping Workgroup of the
  Linguistic Society of Hong Kong
  ([lshk-org/jyutping-table](https://github.com/lshk-org/jyutping-table),
  CC BY 4.0), with the thanks given there to Prof Lu Qin and Dr Cheung Kwan
  Hin of the Hong Kong Polytechnic University and to Nathan Hammond;
* [rime-cantonese](https://github.com/rime/rime-cantonese) (粵語拼音輸入方案)
  by the Cantonese Computational Linguistics Infrastructure Development
  Workgroup (CanCLID) and its contributors (CC BY 4.0), which gives the
  default readings and most of the words;
* 石見田 and the 粵音資料集叢 ([jyut.net](https://jyut.net/about), data at
  [jyutnet/cantonese-books-data](https://github.com/jyutnet/cantonese-books-data)),
  whose digitised dictionaries give the readings of 640 characters: 廣州話正音字典
  (2004), 廣州話標準音字彙 (1988), 粵語同音字典 (1974/1996), 粵語查音識字字典
  (1985), 同音字彙 (1971), 部身字典 (1967), *The Student's Cantonese-English
  Dictionary* (1947), 粵音韻彙 (1941), 道字典 (1941), 道漢字音 (1939),
  民眾識字粵語拼音字彙 (1931), 廣話國語一貫未定稿 (1916) and
  分部分音廣話九聲字宗 (1914); and the authors and editors of those books;
* [Jyut Dictionary](https://github.com/aaronhktan/jyut-dict) (jyut-dict) by
  Aaron Tan, whose `src/dictionaries` distributes the two word lists used
  here: CC-Canto (© 2015–17 Pleco Inc., [cantonese.org](https://cantonese.org),
  CC BY-SA 3.0) and the Cantonese readings for CC-CEDICT (© 2015 Pleco
  Software Inc., CC BY-SA 3.0), which give Cantonese readings to the words of
  [CC-CEDICT](https://cc-cedict.org) by MDBG and its contributors;
* [OpenCC](https://github.com/BYVoid/OpenCC) by Carbo Kuo (BYVoid) and its
  contributors (Apache-2.0), whose Hong Kong and Taiwan variant tables let
  variant shapes find the same words.

## Licence

See [`LICENSE`](LICENSE). The package code (`xjyutping.sty`,
`xjyutping.lua`, `tools/`, `tests/`) is under the LaTeX Project Public
License 1.3c.

The generated data files (`xjyutping-chars.def`, `xjyutping-words.def`) are
distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):
they adapt the CC BY-SA 3.0 word lists of CC-Canto and the CC-CEDICT
Cantonese readings, together with material under CC BY 4.0 (LSHK,
rime-cantonese) and Apache-2.0 (the OpenCC variant map), all credited above.
The readings of the 640 characters taken from 粵音資料集叢 come from data
published without a licence statement and are used with attribution; to
build the data without them, empty `BOOKS` in `tools/build-data.py`.
