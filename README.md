# xjyutping (LaTeX)

Version 1.5.1 (2026-10-02). Versions follow
[Semantic Versioning](https://semver.org), and the history of the project is
kept in [`CHANGELOG.md`](CHANGELOG.md).

## Overview

This project is a LaTeX package that adds Cantonese Jyutping (粵拼) above
Traditional Chinese characters. It is aimed at anyone preparing Cantonese
material in LaTeX, such as teaching notes, lyrics or poetry, where the
pronunciation of each character should be shown above it.

Pronunciation is determined by looking at the context and cross-referencing
it with a list of about 104 000 words. The package supports XeLaTeX and
LuaLaTeX, and it was inspired by xpinyin, which adds Mandarin pinyin to
Simplified Chinese characters. A Python version that gives the same readings
is available as [xjyutping-py](https://github.com/Beyond3345/xjyutping-py).

A minimal document is,

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

Looking at the output, 行 is read *hong4* in 銀行 but *haang4* in 行路, while
長 is read *zoeng2* in both 校長 and 長大.

Instead of `ctex`, a document can load `xeCJK` (XeLaTeX) or
`luatexja-fontspec` (LuaLaTeX). If none of them is loaded, the package loads
`xeCJK` or LuaTeX-ja itself. The manual,
[`xjyutping-doc.pdf`](xjyutping-doc.pdf), describes every command and option
in detail.

## Installing

The package needs four files, `xjyutping.sty`, `xjyutping.lua` (used by
LuaLaTeX), `xjyutping-chars.def` and `xjyutping-words.def`. Keep them
together, either next to your document or in your personal tree
(`~/Library/texmf` on macOS, `~/texmf` on Linux). To copy them into the
personal tree, run,

```bash
d="$(kpsewhich -var-value TEXMFHOME)/tex/latex/xjyutping" && mkdir -p "$d" && cp xjyutping.sty xjyutping.lua xjyutping-*.def "$d"
```

## Commands

| Command | Effect |
| --- | --- |
| `\begin{jyutpingscope}[opts] … \end{jyutpingscope}` | Annotate every character in the block. |
| `\xjyutping*[opts]{text}` | Annotate a piece of running text. |
| `\xjyutping[opts]{字}{reading}` | Give a character or word your own reading, as in `\xjyutping{銀行}{ngan4 hong4}`. |
| `\setjyutping{字}{reading}` | Change a character's default reading. |
| `\setjyutping{詞}{readings}` | Add or change a word, as in `\setjyutping{當我}{dong3 ngo5}`. |
| `\disablejyutping`, `\enablejyutping` | Turn annotation off and on inside a scope. |
| `\xjyutpingsetup{opts}` | Set options. They also work as package options. |

A scope always ends the paragraph, and its lines are spaced so that the
Jyutping never touches the line above. The `\setjyutping` command is global
and applies from the point where it appears, including the middle of a
scope. However, since a scope is read in full before it is typeset, a
`\setjyutping` inside a scope applies even within `\iffalse … \fi`. Hence
conditional settings should be kept outside the scope.

## Options

| Key | Default | Meaning |
| --- | --- | --- |
| `ratio` | `0.45` | Size of the Jyutping relative to the text. |
| `vsep` | `1.05em` | Height of the Jyutping's baseline above the character's. |
| `hsep` | `0.15em plus 0.4em` | Space between characters. The stretch lets lines justify. |
| `width` | `auto` | Cell width. With `auto` the width is the same for the whole block and fits its longest Jyutping, with `natural` each cell is as wide as it needs and a length such as `1.8em` gives a fixed grid. |
| `font` | `\normalfont` | Font of the Jyutping. |
| `format` | empty | Extra formatting, such as `\color{gray}`. |
| `multiple` | empty | Formatting for guessed readings of characters with several readings, such as `\color{red}` for proofreading. |
| `fancy` | `false` | Show tones in the style of Visual Jyutping (Section "Fancy tones"). |
| `linebreak` | `false` | Keep the lines of the source (Section "Verse and lyrics"). |
| `align` | `justify` | Alignment of the lines of a scope, which is `justify`, `left`, `centre` (or `center`) or `right`. The values also work on their own, as in `[linebreak,centre]`. |
| `debug` | `false` | Log how each run of text was read. |

In the debug log, `w` marks a word, `u` a reading you set, `m` a guessed
reading (with the other readings in brackets) and `s` a character with only
one reading.

## Fancy tones

The `fancy` option replaces each tone number with a small stroke showing the
pitch of the tone, followed by a smaller tone number, in the same way as
[Visual Jyutping](https://github.com/VincentTam/visual-jyutping) writes
jyutˍ₆ ping˗₃. The six tones are drawn as,

| Tone | Stroke | Number | Example |
| --- | --- | --- | --- |
| 1 | high level (ˉ) | raised | 詩 si1 |
| 2 | rising to high (ˊ) | raised | 史 si2 |
| 3 | mid level (˗) | lowered | 試 si3 |
| 4 | falling to low (ˎ) | lowered | 時 si4 |
| 5 | rising from low (ˏ) | lowered | 市 si5 |
| 6 | low level (ˍ) | lowered | 事 si6 |

Since the strokes are drawn rather than taken from a font, they work with any
`font` and colour, and the spacing is adjusted to fit them. PDF bookmarks and
the debug log keep the plain tone numbers.

## Verse and lyrics

The `linebreak` option keeps the lines of the source, which suits verse and
lyrics, while the `align` option sets the lines flush left, centred or flush
right. For example,

```latex
\begin{jyutpingscope}[linebreak,centre]
床前明月光，
疑是地上霜。

舉頭望明月，
低頭思故鄉。
\end{jyutpingscope}
```

Specifically, each line end becomes a line break (`\\`), while a blank line
leaves an empty line and starts a new paragraph. The new paragraph follows
the settings of the document, so it is indented by default and not indented
with `\usepackage[parfill]{parskip}`, whose paragraph space is added to the
empty line. A `\centering` inside the scope also works, and an aligned scope
starts a paragraph of its own. Since a line end also ends a run of
characters, a word is never looked up across two lines.

However, `linebreak` only works in the environment. It has no effect in
`\xjyutping*`, in a scope inside the argument of a command such as
`\parbox{…}` or in a scope nested inside one without the option.

## How readings are chosen

The reading of each character is chosen in three steps.

1. First, the text is split into runs of Chinese characters. Punctuation,
   Latin text and most commands end a run, while formatting such as
   `\textbf` or `\color` does not, so `銀\textbf{行}` is still read as the
   word 銀行.
2. Then each run is split into the fewest words from the word list, and each
   word takes its reading from the list. Where two splits have as many words
   and single characters, the one of the more common words wins, as counted
   in the word-frequency list of rime-cantonese and in the transcripts of
   WenetSpeech-Yue (步行|街 rather than 步|行街).
3. Lastly, a character left on its own takes the reading set with
   `\setjyutping`, or otherwise the reading given by the one or two
   characters after it, its reading at the end of a run or its default
   reading. For example, 呢 is the demonstrative *ni1* before a classifier
   (呢張床) and the particle *ne1* otherwise (你呢？, 佢呢就走).

A reading given with `\xjyutping{…}{…}` always takes priority, and a word set
with `\setjyutping` wins a tie of step 2. Variant shapes such as 為/爲 and
裡/裏 find the same words.

## XeLaTeX and LuaLaTeX

While the readings and options are the same under both engines, LuaLaTeX
also needs `xjyutping.lua`, installed next to `xjyutping.sty`. Under LuaLaTeX,

- punctuation and line breaks follow the rules of LuaTeX-ja, so lines can
  break differently,
- a paragraph can be any length, while XeLaTeX stops at about 15 000
  characters,
- compiling takes about 1.6 times as long and
- text that comes from a macro takes the `\setjyutping` readings in force at
  the end of its paragraph.

pdfLaTeX is not supported.

## Troubleshooting

### `\verb` inside a scope gives an error

The body of a scope is read in full before it is typeset, in the same way as
the argument of a command. Hence `\verb` and verbatim environments cannot go
inside a scope, and a `%` in `\url` or `\href` must be written `\%`. Put
verbatim material outside the scope.

### Text from a macro is read one character at a time

Since the package only sees the name of a macro when it reads a scope, text
that comes from a macro, from `\maketitle` or from an `\include`d file is
annotated one character at a time, without word context. Put `\xjyutping*`
inside the macro, or a scope inside the included file.

### A command's argument is annotated or left plain

The arguments of `\label`, `\ref`, `\cite`, `\url`, `\includegraphics` and
similar commands are left alone. Other commands need their Chinese argument
in braces, so write `\textbf{行}` rather than `\textbf 行`.

### The table of contents has no Jyutping

Section titles, captions and footnotes inside a scope are annotated, while
the table of contents is only annotated if `\tableofcontents` is itself
inside a scope. Running heads and PDF bookmarks always stay plain.

### A beamer frame title has no Jyutping

In beamer, a `\frametitle` inside a scope is typeset after the scope has
ended. Write `\frametitle{\xjyutping*{…}}` instead.

### Underlines break the spacing

The commands of xeCJKfntef, such as `\CJKunderline`, do not keep the spacing
of the cells. Use `\underline` or `\uline` from ulem instead.

### A character has no Jyutping

The character is missing from the data. Give it a reading with
`\setjyutping` or `\xjyutping`, which both work for characters outside the
data.

## Data

The readings are stored in `xjyutping-chars.def` (30 089 characters) and
`xjyutping-words.def` (about 104 000 words, with how often each is used). They
are built by `tools/build-data.py` from six sources, which
`tools/fetch-sources.sh` downloads,

- the Jyutping table of the Linguistic Society of Hong Kong (LSHK), for the
  character readings,
- rime-cantonese, for the default readings, the main word list and the word
  frequencies,
- ToJyutping, for the choice between the readings rime gives a word and for
  512 more words,
- CC-Canto and the Cantonese readings of CC-CEDICT from Jyut Dictionary, for
  2 531 more words,
- OpenCC, for variant shapes and
- 粵音資料集叢, for the readings of 640 rare characters.

The build also reads `tools/wenetspeech-yue-counts.tsv`, which counts how
often each word is used in the 6.8 million transcribed utterances of
WenetSpeech-Yue. Since rime-cantonese is treated as authoritative, the other
sources only add what it lacks. The exceptions are ToJyutping, which may
choose a different one of the readings that rime gives a word, since its
choices follow Hong Kong usage (for example 公園 *gung1 jyun2* and 郵局 *jau4
guk2*), and the hand-checked tables at the top of `tools/build-data.py`, which
correct readings found wrong against the corpora below. To fix a reading,

1. Edit the hand-checked tables at the top of `tools/build-data.py`
2. Run `python3 tools/build-data.py`

The script looks for the sources in the folder `jyutData` next to this
repository (or in `--sources DIR`), and it also updates the data of
xjyutping-py when that repository is next to this one.

### Accuracy

We measured the accuracy on seven corpora. The Hong Kong Cantonese Corpus
(HKCanCor) is a corpus of conversation recorded in the 1990s whose 161 045
characters were annotated with Jyutping by hand. On the half of its files
that was kept out of the tuning, the package reads 95.6% of the characters
correctly (94.0% in 1.4.0) and 97.9% of the characters outside
sentence-final particles and interjections, while ToJyutping 3.2.0 reads
92.6% and 96.1%. On the particles of CantoMap, which were transcribed by ear,
it reads 97.5% (79.0% in 1.4.0, 83.0% for ToJyutping). On fresh sentences of
SpiCE, MagicHub and WenetSpeech-Yue, where the systems disagree, the reading
of xjyutping was judged right in 95.3% of the cases (94.9% in 1.5.0), against
60.7% for ToJyutping. Part II, Sections 10 and 11 of `CHANGELOG.md` describe the tests.

## Testing

`tests/run-tests.sh` checks the readings under both engines, with and without
`fancy`, while `tests/render.sh` renders a test file to PNG for a visual
check, for example `tests/verse-check.tex` for `linebreak` and `align`.

## Acknowledgements and attributions

This project was inspired by the LaTeX package
[xpinyin](https://ctan.org/pkg/xpinyin) by Qing Lee (李清), which adds pinyin
to Simplified Chinese characters.

The `fancy` option was inspired by
[Visual Jyutping](https://github.com/VincentTam/visual-jyutping) by Vincent
Tam, whose tone symbols it draws, and by the Visual Cantonese Fonts (粵語字體)
by Jon Chui / A3I Ltd. ([canto.hk](https://canto.hk),
[documentation](https://docs.visual-fonts.com),
[source](https://github.com/jkwchui/visual-fonts-starlight-docs)). We would
like to thank both of them.

We also thank the authors of the data sources,

- the Jyutping Workgroup of the Linguistic Society of Hong Kong (LSHK), for
  the *Cantonese Pronunciation List of Characters for Computers*
  (電腦用漢字粵語拼音表,
  [lshk-org/jyutping-table](https://github.com/lshk-org/jyutping-table),
  CC BY 4.0), together with Prof Lu Qin and Dr Cheung Kwan Hin of the Hong
  Kong Polytechnic University and Nathan Hammond, who are thanked there,
- the Cantonese Computational Linguistics Infrastructure Development
  Workgroup (CanCLID) and its contributors, for
  [rime-cantonese](https://github.com/rime/rime-cantonese) (粵語拼音輸入方案,
  CC BY 4.0), which gives the default readings and most of the words, and
  for [ToJyutping](https://github.com/CanCLID/ToJyutping) (BSD-2-Clause),
  whose word list chooses between rime's readings of a word and adds 512
  words,
- 石見田, for 粵音資料集叢 ([jyut.net](https://jyut.net/about), data at
  [jyutnet/cantonese-books-data](https://github.com/jyutnet/cantonese-books-data)),
  together with the authors and editors of the thirteen dictionaries it
  digitises, namely 廣州話正音字典 (2004), 廣州話標準音字彙 (1988), 粵語同音字典 (1974/1996),
  粵語查音識字字典 (1985), 同音字彙 (1971), 部身字典 (1967), *The Student's
  Cantonese-English Dictionary* (1947), 粵音韻彙 (1941), 道字典 (1941),
  道漢字音 (1939), 民眾識字粵語拼音字彙 (1931), 廣話國語一貫未定稿 (1916) and
  分部分音廣話九聲字宗 (1914),
- Aaron Tan, for [Jyut Dictionary](https://github.com/aaronhktan/jyut-dict),
  which distributes CC-Canto (© 2015–17 Pleco Inc.,
  [cantonese.org](https://cantonese.org), CC BY-SA 3.0) and the Cantonese
  readings for CC-CEDICT (© 2015 Pleco Software Inc., CC BY-SA 3.0), together
  with MDBG and the contributors of [CC-CEDICT](https://cc-cedict.org) and
- Carbo Kuo (BYVoid) and the contributors of OpenCC, for
  [OpenCC](https://github.com/BYVoid/OpenCC) (Apache-2.0), whose variant
  tables let variant shapes find the same words.

Lastly, we thank the authors of the corpora that we used to tune the package
and to measure its accuracy,

- Kang Kwong Luke, for the Hong Kong Cantonese Corpus (HKCanCor, CC BY 4.0),
  as distributed with [PyCantonese](https://github.com/jacksonllee/pycantonese),
- Grégoire Winterstein, Carmen Tang and Regine Lai, for
  [CantoMap](https://github.com/gwinterstein/CantoMap) (GPL-3.0),
- Khia A. Johnson, Molly Babel, Ivan Fong and Nancy Yiu, for SpiCE
  ([doi:10.5683/SP2/MJOXP3](https://doi.org/10.5683/SP2/MJOXP3), CC BY 4.0),
- the ASLP-lab, for [WenetSpeech-Yue](https://github.com/ASLP-lab/WenetSpeech-Yue)
  (CC BY-NC 4.0), whose transcripts also give the word frequencies of
  `tools/wenetspeech-yue-counts.tsv`,
- Beijing Magic Data Technology, for the Guangzhou Cantonese Conversational
  Speech Corpus of [MagicHub](https://magichub.com) and
- the contributors of the Cantonese Wikipedia.

## Licence

The code (`xjyutping.sty`, `xjyutping.lua`, `tools/` and `tests/`) is
released under the LaTeX Project Public License (LPPL) 1.3c, while the data
files (`xjyutping-chars.def` and `xjyutping-words.def`) are released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), since they
adapt the CC BY-SA 3.0 word lists above. The word list of ToJyutping is
used under the BSD 2-Clause License, whose notice is reproduced in
`LICENSE`. The readings of the 640 characters from 粵音資料集叢 come from
data published without a licence and are used with attribution. To build the
data without them, empty `BOOKS` in `tools/build-data.py`. The word counts in
`tools/wenetspeech-yue-counts.tsv` are counted from the transcripts of
WenetSpeech-Yue (CC BY-NC 4.0); no text of any corpus is included. The full
terms are given in [`LICENSE`](LICENSE).
