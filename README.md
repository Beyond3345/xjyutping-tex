# xjyutping (LaTeX)

Version 1.1.0 (2026-09-28). Versions follow
[Semantic Versioning 2.0.0](https://semver.org); the history is in
[`../CHANGELOG.md`](../CHANGELOG.md).

A LaTeX package that puts Jyutping (粵拼) above traditional Chinese
characters, choosing each reading from the words around it. It is modelled on
`xpinyin` and works with XeLaTeX and `xeCJK` (including the `ctex` classes).
A Python version with the same readings is in [`../xjyutping-py`](../xjyutping-py).

```latex
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{Songti TC}      % any traditional Chinese font
\usepackage{xjyutping}
\begin{document}
\begin{jyutpingscope}
我哋去銀行，行路返屋企。校長喺學校長大。
\end{jyutpingscope}
\end{document}
```

行 comes out as *hong4* in 銀行 and *haang4* in 行路; 長 as *zoeng2* in 校長
and 長大.

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

## How readings are chosen

1. The text is split into runs of Chinese characters. Punctuation, Latin
   text and most commands end a run; spaces and line breaks between two
   characters do not, and neither do braces or formatting commands
   (`\textbf`, `\emph`, `\color`, `\textcolor`, size commands …), so
   `銀\textbf{行}` is still the word 銀行. The text of a `\footnote` is a run
   of its own, and the text around it carries on.
2. Each run is segmented with a list of about 100 000 words: fewest words
   first, then fewest single characters; on a tie the longer final word wins.
3. A word takes its reading from the list (your `\setjyutping` words first).
4. A character left on its own takes your `\setjyutping` reading if there is
   one, else its default. A few characters read differently at the end of a
   run (呢 is *ni1* in 呢張床 but the particle *ne1* in 你呢？).
5. `\xjyutping{…}{…}` always wins and also splits the run.

Variant shapes are folded together for word lookup, so 為/爲, 裡/裏, 説/說,
衞/衛, 綫/線, 恒/恆 and the like all find the same words.

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
* The underline and emphasis-mark commands of `xeCJKfntef` (`\CJKunderline`,
  `\CJKunderdot` …) do not keep the cell spacing inside a scope; use
  `\underline` or `ulem`'s `\uline` there.
* One scope can hold well over 100 000 characters, but a single paragraph is
  limited to about 15 000 by TeX's memory (each annotated character is a
  small box), about 13 000 with `fancy`; a brace group spanning many
  paragraphs is read in one piece.
* Characters not in the data are typeset in their cell without Jyutping.

## Data

`xjyutping-chars.def` and `xjyutping-words.def` are generated by
`tools/build-data.py` from:

* the LSHK *Cantonese Pronunciation List of Characters for Computers*
  (粵拼表), CC BY 4.0 — `jyutping-table-master/`;
* rime-cantonese `jyut6ping3.chars` and `jyut6ping3.words` (CC BY 4.0) —
  `rime-cantonese/`;
* OpenCC `HKVariants.txt` and `TWVariants.txt` (Apache-2.0) — `opencc/`.

The `fancy` tone marks follow Visual Jyutping by Vincent Tam (MIT) —
`visual-jyutping-master/`. These source folders and `tools/` sit at the root
of the repository, next to this folder.

Default readings come from rime-cantonese's primary reading, falling back to
the LSHK order. The hand-checked tables in `tools/build-data.py`
(`CURATED_DEFAULTS`, `CURATED_FINALS`, `CURATED_VARIANTS`, `CURATED_WORDS`)
correct the sources where they are wrong or undecided; run
`python3 tools/build-data.py` from the repository root after editing them (it
rewrites the data of both the LaTeX and the Python package).

## Installing

Keep `xjyutping.sty`, `xjyutping-chars.def` and `xjyutping-words.def`
together, either next to your document or in your personal tree:

```bash
mkdir -p ~/Library/texmf/tex/latex/xjyutping && cp xjyutping.sty xjyutping-*.def ~/Library/texmf/tex/latex/xjyutping/
```

The manual is `xjyutping-doc.pdf` (source `xjyutping-doc.tex`).

## Testing

`tests/run-tests.sh` compiles `tests/regression.tex` with and without
`fancy` and compares the debug log with `tests/regression.expected`.
`tests/render.sh tests/layout-check.tex` and
`tests/render.sh tests/fancy-check.tex` render the pages to PNG for a visual
check of the spacing and the tone marks.

## Licence

The package code is under the LaTeX Project Public License 1.3c. The
generated data files carry the licences of their sources (CC BY 4.0 for the
readings, Apache-2.0 for the variant map).
