# xjyutping (LaTeX)

Version 1.2.0 (2026-09-28). Versions follow
[Semantic Versioning](https://semver.org), and the history is in
[`CHANGELOG.md`](CHANGELOG.md).

xjyutping is a LaTeX package that adds Cantonese Jyutping (粵拼) above
Traditional Chinese characters. Pronunciation is determined by looking at the
context and cross-referencing it with a list of about 104 000 words. The
package supports XeLaTeX and LuaLaTeX. It was inspired by xpinyin, which adds
Mandarin pinyin to Simplified Chinese characters. A Python version with the
same readings is [xjyutping-py](https://github.com/Beyond3345/xjyutping-py).

```latex
\documentclass{article}
\usepackage[fontset=none]{ctex}  % compile with xelatex or lualatex
\setCJKmainfont{Songti TC}       % any Traditional Chinese font
\usepackage{xjyutping}
\begin{document}
\begin{jyutpingscope}
我哋去銀行，行路返屋企。校長喺學校長大。
\end{jyutpingscope}
\end{document}
```

Here 行 is read *hong4* in 銀行 and *haang4* in 行路, and 長 is *zoeng2* in
校長 and 長大.

You can load `xeCJK` (XeLaTeX) or `luatexja-fontspec` (LuaLaTeX) instead of
`ctex`. If none of them is loaded, xjyutping loads `xeCJK` or LuaTeX-ja
itself. The manual, [`xjyutping-doc.pdf`](xjyutping-doc.pdf), has the details.

## Commands

| Command | Effect |
| --- | --- |
| `\begin{jyutpingscope}[opts] … \end{jyutpingscope}` | Annotate every character in the block. |
| `\xjyutping*[opts]{text}` | Annotate a piece of running text. |
| `\xjyutping[opts]{字}{reading}` | Give a character or word your own reading: `\xjyutping{銀行}{ngan4 hong4}`. |
| `\setjyutping{字}{reading}` | Change a character's default reading. |
| `\setjyutping{詞}{readings}` | Add or change a word: `\setjyutping{重話}{zung6 waa6}`. |
| `\disablejyutping`, `\enablejyutping` | Turn annotation off and on inside a scope. |
| `\xjyutpingsetup{opts}` | Set options. They also work as package options. |

A scope ends the paragraph, and its lines are spaced so that the Jyutping
never touches the line above. `\setjyutping` is global and applies from where
it appears, also in the middle of a scope. Inside a scope it applies even in
`\iffalse … \fi`, so keep conditional settings outside the scope.

## Options

| Key | Default | Meaning |
| --- | --- | --- |
| `ratio` | `0.45` | Size of the Jyutping relative to the text. |
| `vsep` | `1.05em` | Height of the Jyutping's baseline above the character's. |
| `hsep` | `0.15em plus 0.4em` | Space between characters. The stretch lets lines justify. |
| `width` | `auto` | Cell width. `auto`: the same for the whole block, wide enough for its longest Jyutping. `natural`: each cell as wide as it needs. A length (`1.8em`): a fixed grid. |
| `font` | `\normalfont` | Font of the Jyutping. |
| `format` | empty | Extra formatting, e.g. `\color{gray}`. |
| `multiple` | empty | Formatting for guessed readings of characters with several readings, e.g. `\color{red}` for proofreading. |
| `fancy` | `false` | Show tones the way Visual Jyutping does (see below). |
| `linebreak` | `false` | Keep the lines of the source (see below). |
| `debug` | `false` | Log how each run of text was read. |

In the debug log, `w` marks a word, `u` your own setting, `m` a guessed
reading (the other readings follow in brackets) and `s` a character with one
reading.

## Fancy tones

`fancy` replaces each tone number with a small stroke that shows the pitch of
the tone, followed by a small tone number, the way
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

The strokes are drawn, not taken from a font, so they work with any `font`
and colour, and the spacing adjusts to them. PDF bookmarks and the debug log
keep plain tone numbers.

## Verse and lyrics: `linebreak`

With `linebreak`, each line of the source stays a line in the output:

```latex
\begin{jyutpingscope}[linebreak]
床前明月光，
疑是地上霜。

舉頭望明月，
低頭思故鄉。
\end{jyutpingscope}
```

A line end becomes a line break (`\\`), and a blank line starts a new
paragraph that follows the document's settings: indented by default, not
indented with `\usepackage[parfill]{parskip}`. A word is never looked up
across two lines. The option works in the environment only. It does nothing
in `\xjyutping*`, in a scope inside a command's argument such as
`\parbox{…}`, or in a scope nested in one without it.

## How readings are chosen

The text is split into runs of Chinese characters. Punctuation, Latin text
and most commands end a run, but formatting such as `\textbf` or `\color`
does not, so `銀\textbf{行}` is still the word 銀行. Each run is split into
the fewest words from the word list, and each word takes its reading from the
list. A character on its own takes your `\setjyutping` reading, or else its
default. `\xjyutping{…}{…}` always wins. Variant shapes such as 為/爲 and
裡/裏 find the same words.

## XeLaTeX and LuaLaTeX

The readings and options are the same under both engines. LuaLaTeX also
needs `xjyutping.lua`, installed next to `xjyutping.sty`. Under LuaLaTeX:

* punctuation and line breaks follow LuaTeX-ja's rules, so lines can break
  differently;
* a paragraph can be any length (under XeLaTeX, about 15 000 characters);
* compiling takes about 1.6 times as long;
* text that comes from a macro takes the `\setjyutping` readings in force at
  the end of its paragraph.

pdfLaTeX is not supported.

## Things to know

* The body of a scope is read in full before it is typeset, so `\verb` and
  verbatim environments can't go inside, and a `%` in `\url` or `\href` must
  be written `\%`.
* Text from a macro, `\maketitle` or an `\include`d file is annotated one
  character at a time, without word context. Put `\xjyutping*` in the macro,
  or a scope in the file.
* Arguments of `\label`, `\ref`, `\cite`, `\url`, `\includegraphics` and
  similar commands are left alone. Give other commands their Chinese argument
  in braces: `\textbf{行}`, not `\textbf 行`.
* Section titles, captions and footnotes in a scope are annotated. The table
  of contents is annotated only if `\tableofcontents` is in a scope. Running
  heads and PDF bookmarks stay plain.
* In beamer, write `\frametitle{\xjyutping*{…}}`.
* Use `\underline` or `\uline` rather than xeCJKfntef's `\CJKunderline`.
* Characters missing from the data get no Jyutping.

## Data

The readings are in `xjyutping-chars.def` (30 089 characters) and
`xjyutping-words.def` (about 104 000 words). `tools/build-data.py` builds
them from these sources, which `tools/fetch-sources.sh` downloads:

* the LSHK Jyutping table (character readings);
* rime-cantonese (default readings and the main word list);
* CC-Canto and the Cantonese readings of CC-CEDICT, from Jyut Dictionary
  (2 291 more words);
* OpenCC (variant shapes);
* 粵音資料集叢 (readings of 640 rare characters).

rime-cantonese is authoritative, and the other sources only add what it
lacks. To fix a reading, edit the hand-checked tables at the top of
`tools/build-data.py` and run `python3 tools/build-data.py`. It looks for the
sources in the folder that contains this repository (or `--sources DIR`), and
it also updates the data of xjyutping-py when that repository is next to this
one.

## Installing

Keep `xjyutping.sty`, `xjyutping.lua`, `xjyutping-chars.def` and
`xjyutping-words.def` together, next to your document or in your personal
tree (`~/Library/texmf` on macOS, `~/texmf` on Linux):

```bash
d="$(kpsewhich -var-value TEXMFHOME)/tex/latex/xjyutping" && mkdir -p "$d" && cp xjyutping.sty xjyutping.lua xjyutping-*.def "$d"
```

## Testing

`tests/run-tests.sh` checks the readings under both engines, with and
without `fancy`. `tests/render.sh` renders a test file to PNG for a visual
check.

## Acknowledgements and attributions

xjyutping was inspired by the LaTeX package
[xpinyin](https://ctan.org/pkg/xpinyin) by Qing Lee (李清), which adds pinyin
to Simplified Chinese characters.

The `fancy` option was inspired by
[Visual Jyutping](https://github.com/VincentTam/visual-jyutping) by Vincent
Tam, whose tone symbols it draws, and by the Visual Cantonese Fonts (粵語字體)
by Jon Chui / A3I Ltd. ([canto.hk](https://canto.hk),
[documentation](https://docs.visual-fonts.com),
[source](https://github.com/jkwchui/visual-fonts-starlight-docs)). Thank you
both.

Thanks also to the authors of the data sources:

* the Jyutping Workgroup of the Linguistic Society of Hong Kong, for the
  *Cantonese Pronunciation List of Characters for Computers*
  (電腦用漢字粵語拼音表,
  [lshk-org/jyutping-table](https://github.com/lshk-org/jyutping-table),
  CC BY 4.0), and to Prof Lu Qin and Dr Cheung Kwan Hin of the Hong Kong
  Polytechnic University and Nathan Hammond, who are thanked there;
* the Cantonese Computational Linguistics Infrastructure Development
  Workgroup (CanCLID) and contributors, for
  [rime-cantonese](https://github.com/rime/rime-cantonese) (粵語拼音輸入方案,
  CC BY 4.0), which gives the default readings and most of the words;
* 石見田, for 粵音資料集叢 ([jyut.net](https://jyut.net/about), data at
  [jyutnet/cantonese-books-data](https://github.com/jyutnet/cantonese-books-data)),
  and the authors and editors of the dictionaries it digitises: 廣州話正音字典
  (2004), 廣州話標準音字彙 (1988), 粵語同音字典 (1974/1996), 粵語查音識字字典
  (1985), 同音字彙 (1971), 部身字典 (1967), *The Student's Cantonese-English
  Dictionary* (1947), 粵音韻彙 (1941), 道字典 (1941), 道漢字音 (1939),
  民眾識字粵語拼音字彙 (1931), 廣話國語一貫未定稿 (1916) and
  分部分音廣話九聲字宗 (1914);
* Aaron Tan, for [Jyut Dictionary](https://github.com/aaronhktan/jyut-dict),
  which distributes CC-Canto (© 2015–17 Pleco Inc.,
  [cantonese.org](https://cantonese.org), CC BY-SA 3.0) and the Cantonese
  readings for CC-CEDICT (© 2015 Pleco Software Inc., CC BY-SA 3.0), and MDBG
  and the contributors of [CC-CEDICT](https://cc-cedict.org);
* Carbo Kuo (BYVoid) and contributors, for
  [OpenCC](https://github.com/BYVoid/OpenCC) (Apache-2.0), whose variant
  tables let variant shapes find the same words.

## Licence

The code (`xjyutping.sty`, `xjyutping.lua`, `tools/`, `tests/`) is under the
LaTeX Project Public License 1.3c. The data files (`xjyutping-chars.def`,
`xjyutping-words.def`) are under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), because they
adapt the CC BY-SA 3.0 word lists above. The readings of the 640 characters
from 粵音資料集叢 come from data published without a licence and are used with
attribution; to build the data without them, empty `BOOKS` in
`tools/build-data.py`. See [`LICENSE`](LICENSE).
