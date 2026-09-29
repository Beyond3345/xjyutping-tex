#!/usr/bin/env python3
"""Generate the xjyutping data files from the upstream sources.

    python3 tools/build-data.py [--sources DIR] [--py-data DIR]

Run it from anywhere; paths are resolved from this file.  The sources are
third-party data kept outside the repository, by default in the directory
that contains this repository (tools/fetch-sources.sh fetches them):

  jyutping-table-master/list.tsv               LSHK Jyutping table, CC BY 4.0
  rime-cantonese/jyut6ping3.chars.dict.yaml    rime-cantonese, CC BY 4.0
  rime-cantonese/jyut6ping3.words.dict.yaml    rime-cantonese, CC BY 4.0
  opencc/HKVariants.txt, opencc/TWVariants.txt OpenCC, Apache-2.0
  jyut-dict/src/dictionaries/cedict/data/
      CC-CANTO.txt   CC-Canto (Pleco Inc.), CC BY-SA 3.0
      READINGS.txt   Cantonese readings of CC-CEDICT words (Pleco), CC BY-SA 3.0
  cantonese-books-data/<book>/*資料.json        粵音資料集叢 book data (jyut.net,
                                               by 石見田), no licence stated
  ToJyutping-main/src/ToJyutping/trie.txt      ToJyutping (CanCLID), BSD-2-Clause

rime-cantonese is authoritative.  CC-Canto, the CC-CEDICT readings and
ToJyutping only add words that are not in its list and that the list would
read otherwise; ToJyutping also chooses between the readings rime itself gives
a word (see load_tojyutping).  The books only add characters that LSHK and
rime lack (see BOOKS).

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
import json
import math
import pathlib
import re
import sys
import unicodedata

REPO = pathlib.Path(__file__).resolve().parent.parent     # xjyutping-tex
ROOT = REPO.parent                                         # the sources
PY_DATA = ROOT / 'xjyutping-py' / 'src' / 'xjyutping' / 'data'
SYL = re.compile(r'^[a-z]+[1-6]$')
VERSION = '2026/09/29 v1.4.0'

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
    # 1.4.0, after ToJyutping and the Hong Kong Cantonese Corpus: the
    # particles 囖, 嚹 and 㗎 as LSHK lists them first, 嘞 as laak3, and 揾,
    # which Hong Kong writing uses for 搵 (look for; OpenCC already folds it
    # into 搵 for word lookup)
    '囖': 'lo1', '嚹': 'laa3', '㗎': 'gaa3', '嘞': 'laak3', '揾': 'wan2',
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
    # 1.2.0: rime reads 合 gap3 here (its own 化合 is faa3 hap6), and 會否
    # wui2 (the modal is wui5); CC-Canto and the CC-CEDICT readings agree
    '化合物': 'faa3 hap6 mat6', '會否': 'wui5 fau2',
    # 1.4.0: 都會 is far more often 都 + the modal 會 (wui5) than 'metropolis'
    # (大都會, 國際大都會 and 都會大學 keep wui6; rime also gives wui6 to
    # 間中都會 and 係人都會), and rime reads 係呢 hai5.  The particle 呢 before
    # 就, 都 and 又 (佢呢就 ...) is never the demonstrative.
    '都會': 'dou1 wui5', '間中都會': 'gaan3 zung1 dou1 wui5',
    '係人都會': 'hai6 jan4 dou1 wui5', '國際都會': 'gwok3 zai3 dou1 wui6',
    '都會區': 'dou1 wui6 keoi1', '係呢': 'hai6 ne1',
    '呢就': 'ne1 zau6', '呢都': 'ne1 dou1', '呢又': 'ne1 jau6',
}

# Words of CC-Canto and the CC-CEDICT Cantonese readings that are not added
# (every added word was checked by hand).  Most give a character a reading
# that Hong Kong usage and rime do not use (乙 jyut3, 這 ze5, 陷 haam6,
# 寺 zi6, 購 gau3, 擾 jiu5, 噶 gaa1 ...), drop a colloquial changed tone
# (慳錢 cin4, 練習簿 bou6, 黃大仙廟 miu6), read a Hong Kong name otherwise
# (柯士甸 din6, 楊千嬅 waa4, 許冠傑 gun1) or are wrong (同學會 wui5,
# 左行 haang1); others would take characters from their neighbours (方法|會
# would become 方|法會, 中學|到 中|學到, 家長|會擔心 家長會|擔心).
EXCLUDED_WORDS = set('''
一年生 一打 一更 一毛錢 七姊妹 七姊妹星團 七姊妹道 三相 三相點
上甘嶺 上甘嶺區 不勝其擾 不對勁 不擴散核武器條約 不暇 不蒸饅頭爭口氣
丕績 丙烷 乙丑 乙二醇 乙亥 乙型 乙基 乙太 乙巳 乙方 乙未 乙炔
乙烯 乙種 乙肝 乙部 乙酉 乙酰 乙醛 了當 二年生 亞喀巴 交易會
人肉搜索 伊媚兒 併捲機 併系群 侵擾 保有 修會 修道張 偷雞不著蝕把米
傣族 傳幫帶 優惠券 元江哈尼族彞族傣族自治縣 兄弟會 光孝寺 光明頂 全會
八達嶺 公主道 公立醫院 兼並與收購 兼併 出勤率 划船 初生 利什曼病
副將 加勁 努庫阿洛法 勇悍 勘測 勛績 北京烤鴨 區間 十六烷值 半生
南普陀寺 博士買驢 卡洛馳 吃拿卡要 同和站 同學會 含蘊 吳興 周會 咄咄
咄咄稱奇 和勝和 和達清夫 哄抬物價 哲蚌寺 唐招提寺 唐老鴨 商洛 商洛市
商洽 單立文 噶倫 噶哈巫族 噶嗒 噶嘣 噶噶 噶布倫 噶拉 噶爾 噶爾縣
噶瑪蘭 噶瑪蘭族 噶舉派 噶隆 噶霏 國會議員 國會議長 圓明園 坎塔布連
坎塔布連山脈 坎塔布連海 坎大哈 坎大哈省 坎帕拉 坎特伯雷 坎特伯雷大主教
坎貝爾 坎貝爾侏儒倉鼠 坦噶尼喀 坦噶尼喀湖 報告會 塌陷 塔公寺 塔爾寺
塗乙 塗漿檯 塗鴨 多年生 夢到 大慈恩寺 大昭寺 大雅鄉 大麥町 太僕寺
太空探索 奈洛比 女修道張 好奇會吃苦頭的 好心倒做了驢肝肺 好整以暇
好玩兒 媽閣廟 嬌媚 孔乙己 孔雀女 孟連傣族拉祜族佤族自治縣 季會 學到
學舌 宗喀巴 室町 家長會 密會 富蘊 富蘊縣 寬帶 寶達邨 對乙酰氨基酚
小昭寺 小雅 少林寺 尤坎 尼雅 尼雅河 屈指可數 崇洋媚外 崗頂站
嶺上開花 左行 巴伐洛堤 市議會 布坎南 布氏桿菌病 布洛陀 席不暇暖 帳簾
干擾素 平頂山 平頂山市 幹將 幾遠 店錢 庫珀帶 廣雅 張惠妹 强制性
彈盡糧絕 彩擴 待乙妥 德宏傣族景頗族自治州 快刀斷亂麻 情陷夜中環 惠遠寺
慈善機構 慈照寺 慳錢 戎行 戒斷 戛然 戛然而止 手彈 折中 抹去 抹平
捷安特 捷爾任斯克 捷爾梅茲 捷達航空貨運 掏錢 探測器 接待處 掩映 搔擾
撟舌 撤併 擴大化 收購要約 敬上 敵將 數學符號 斯捷潘
新平彞族傣族自治縣 新界地產和富大埔 新紀 新藝綜合體 斷路器 日喀則
日喀則地區 日喀則市 日無暇晷 星光行 星架坡 春試 昨早
景谷傣族彞族自治縣 智力測驗 書會 朗拿甸奴 木柵 木柵線 李斯特氏桿菌
東區走廊 東協 板鴨 林和西站 柯士甸 柯士甸道 校友會 核不擴散 核擴散
桿菌 梳刷 棉襖 楊千嬅 橄欖球 欲取姑予 欺哄 歐洲核研究組織 歪瓜劣棗
氯乙烯 沉陷 沒溜兒 沖涼涼 法會 洛寧縣 洛川縣 洛扎縣 洛江區 洛浦縣
洛溪站 洛隆縣 洛龍區 洪廟村 海幢寺 海底擴張 海底擴張說 淫猥 深不可測
準噶爾 準將 溜之大吉 滇藏川 滬綜指 激忿 灌腸 炭疽桿菌 無暇 煎魚
照會 熱水澡 燈會 爽捷 牙縫刷 狗玩兒的 猥褻 獷悍 玉皇頂 玩兒不轉
玩兒命 玩兒壞 玩兒完 玩兒得轉 玩兒花招 玩失蹤 玩藝兒 甄綜 甲乙 甲亢
甲狀腺功能亢進 申購 登位 百分 目及 直行 瞞哄 知會 知識論 秋試
科舉考試 第二處 筆會 約分 紅寺堡 紅寺堡區 紅寺堡鎮 納什維爾 紛擾
結核桿菌 練習簿 織田信長 繚繞 繞一圈 繞遠兒 纏擾 羊腸小道 老爺嶺
耍錢 耿馬傣族佤族自治縣 聖路易斯 聚乙烯 聚氯乙烯 肉毒桿菌 能說會道
臥位 自愧不如 自愧弗如 興都庫什 船到橋門自會直 苯乙烯 莫洛尼 莰烷
菏蘭 華嚴經 萌渚嶺 萬難 葉蘊儀 蒙娜麗莎 蒙特卡洛法 蕉嶺 蕉嶺縣
蕾哈娜 薩噶達娃節 薩斯喀徹溫 藍妹 蠡測 行衰運 袷襖 製表 複試 西門町
西雙版納傣族自治州 覆蓋面 觥籌交錯 許冠傑 許冠英 調嘴學舌 諂媚 豬舍
貝聿銘 買斷 賞錢 購物券 購物大廈 購物廣場 購物袋 購物車 購買者 贖錢
赤坎區 超高速乙太網路 越演越烈 越陷越深 趙構 跨地區 跨學科 跨海大橋
跨線橋 跨鶴揚州 跨鶴西遊 路易十四 路易威登 路易港 身陷 身陷囹圄
軍團桿菌 軍帽 農會 返券黃牛 送客檯 送返 這刻 這是 這次 達嚕噶齊
那打素醫院 酥酪 醃漬 量販店 金平苗族瑤族傣族自治縣 金平苗瑤傣自治縣
金銀膶 閉塞眼睛捉麻雀 閑暇 關帝廟 關廟 防水表 阿喀琉斯 陜西 院試
陷於癱瘓 階地 雙江拉祜族佤族布朗族傣族自治縣 電位 電玩 震中 霍亂桿菌
靈谷寺 靈雀寺 青年會 非微擾 非誠勿擾 面試會 頤和園 頻帶 首重
香港考試及評核局 馬噶爾尼 馬噶爾尼使團 馬戛爾尼 馬戛爾尼使團 馬拉喀什
馬斯喀特 騎驢找驢 騷擾客蚤 騷驢 驍悍 驢友 驢年馬月 驢脣馬觜 驢駒子
驢騾 高大上 高蹺 鬧哄哄 鬧著玩兒 魂牽夢繞 鮑威爾 鮑德里亞 鮑羅丁
鱖魚 鵠立 黃大仙廟 黎曼面 點將 龍舌蘭酒
'''.split())

# Sentence-final particles: their tone follows the intonation, so a new word
# may not change the default reading of one at its end (你好嗎 maa1).
PARTICLES = '呀啊吖喇啦嘞囉咯喎㗎嘅咩嗎呢噃啫咋嘛喔哦吓啩'

# The character dictionaries of cantonese-books-data used for characters that
# LSHK and rime-cantonese lack, most authoritative first.  The last five
# files are four pre-1940 books, used through the modern Jyutping their
# digitiser derived (粵拼讀音).  Not used: the older books, which carry
# reconstructed readings only (粵拼擬音), and 1962_廣州音字彙, withdrawn from
# the collection as inaccurate.
BOOKS = [
    '2004_廣州話正音字典/B01_資料.json',
    '1992_常用字廣州話讀音表/C01_資料.json',
    '1992_香港中學生中文詞典/B01_資料.json',
    '1988_廣州話標準音字彙/B01_資料.json',
    '1974_1996_粵語同音字典/B01_資料.json',
    '1941_粵音韻彙/B01_資料.json',
    '1985_粵語查音識字字典/B01_資料.json',
    '1971_同音字彙/B01_資料.json',
    '1947_The_Students_Cantonese_English_Dictionary/B01_資料.json',
    '1967_部身字典/B01_資料.json',
    '1941_道字典/B01_資料.json',
    '1939_道漢字音/C01_卷一_道漢字典_資料.json',
    '1939_道漢字音/D01_卷二_粵語音典_資料.json',
    '1931_民眾識字粵語拼音字彙/B01_資料.json',
    '1916_廣話國語一貫未定稿/B01_資料.json',
    '1914_分部分音廣話九聲字宗/B01_資料.json',
]
# Labels (讀音標記) of readings that never become the default: popular but
# incorrect, old, archaic, original, wrong, rare, proper names only.
NOT_DEFAULT = ('俗', '舊', '古', '本', '原', '誤', '罕', '專名')


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


def load_book(path):
    """char -> [(reading, label)] of a cantonese-books-data file, in book
    order; the label (讀音標記) is '' when there is none."""
    def walk(x, out):
        if isinstance(x, dict):
            if isinstance(x.get('粵拼讀音'), str):
                label = x.get('讀音標記', x.get('標記')) or ''
                out.append((x['粵拼讀音'], ''.join(label)))     # a list of labels too
            for v in x.values():
                walk(v, out)
        elif isinstance(x, list):
            for v in x:
                walk(v, out)
        return out
    book = collections.defaultdict(list)
    for entry in json.load(open(path, encoding='utf8')):
        heads = entry.get('字頭')
        for ch in [heads] if isinstance(heads, str) else heads or []:
            if isinstance(ch, str) and len(ch) == 1:
                book[ch] += [r for r in walk(entry, []) if r not in book[ch]]
    return book


def load_cedict(path):
    """word -> readings of a CC-Canto style file (the Jyutping in braces
    after the pinyin).  Of alternatives 'a / b' the first is taken; a changed
    tone, marked cin4*2 or hang4*haang4, is read as the changed form."""
    words = collections.defaultdict(list)
    for line in open(path, encoding='utf8'):
        m = re.match(r'(\S+) \S+ \[[^]]*\] \{([^}]*)\}', line)
        if not m:
            continue
        syls = []
        for s in m.group(2).split('/')[0].lower().split():
            s, _, new = s.partition('*')
            syls.append(s[:-1] + new if new.isdigit() else new or s)
        if syls not in words[m.group(1)]:
            words[m.group(1)].append(syls)
    return words


def load_tojyutping(freq):
    """word -> [readings] of ToJyutping's trie: its words of two or more
    characters, in traditional script only (every character occurs in rime's
    word list, which is traditional; the trie also holds simplified forms)."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / 'ToJyutping-main' / 'src'))
    from ToJyutping import Trie
    out = {}

    def walk(node, key):
        if node.v and len(key) > 1 and all(freq[c] for c in key):
            out[key] = [[str(s.jyutping) for s in node.v[0]]]
        for c, child in node.items():
            walk(child, key + c)
    sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))
    walk(Trie.root, '')
    return out


def with_aliases(words, canon):
    """The word list plus aliases spelt with canonical characters, so 因為
    finds rime's 因爲; also the number of aliases dropped as clashes."""
    aliases, clashes = {}, 0
    for w, syls in words.items():
        cw = ''.join(canon.get(c, c) for c in w)
        if cw == w or cw in words:
            continue
        if cw in aliases and aliases[cw] != syls:
            clashes += 1
            continue
        aliases[cw] = syls
    return {**words, **aliases}, len(aliases), clashes


def reader(chars, canon, lex):
    """The readings of a run of text with the word list lex, segmented as
    xjyutping.sty and xjyutping-py do: the fewest words, then the fewest
    single characters; on a tie the longer final word wins."""
    longest = collections.defaultdict(int)
    for w in lex:
        longest[w[-1]] = max(longest[w[-1]], len(w))

    def read(run):
        cr = ''.join(canon.get(c, c) for c in run)
        cost, back = [0] * (len(run) + 1), [1] * (len(run) + 1)
        for i in range(1, len(run) + 1):
            best = cost[i - 1] + 100001
            for size in range(2, min(i, max(longest[run[i - 1]], longest[cr[i - 1]])) + 1):
                if cost[i - size] + 100000 <= best and (run[i - size:i] in lex or
                                                        cr[i - size:i] in lex):
                    best, back[i] = cost[i - size] + 100000, size
            cost[i] = best
        out, j = [], len(run)
        while j:
            i = j - back[j]
            out[:0] = (lex.get(run[i:j]) or lex[cr[i:j]]) if j - i > 1 else [chars[run[i]][0]]
            j = i
        return out
    return read


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
    freq = collections.Counter(c for w, _ in rows for c in w)
    canon = load_variants(freq)

    chars = {}      # char -> (default, other readings, flag as polyphone?)
    known = {}      # char -> every reading a source gives it
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
        known[ch] = set(weight) | set(l)

    # Characters LSHK and rime lack, from the first book that has them: its
    # first reading not labelled as incorrect, old or rare.  Compatibility
    # ideographs (the same characters as unified ones) are left out.
    from_books = collections.Counter()
    for name in BOOKS:
        for ch, rs in sorted(load_book(ROOT / 'cantonese-books-data' / name).items()):
            rs = [(jp, label) for jp, label in rs if SYL.match(jp)]
            if (ch in chars or not rs or not is_han(ch)
                    or unicodedata.normalize('NFC', ch) != ch):
                continue
            good = [jp for jp, label in rs if not any(x in label for x in NOT_DEFAULT)]
            default = (good or [rs[0][0]])[0]
            others = [jp for jp in dict.fromkeys(good) if jp != default]
            chars[ch] = (default, others, bool(others))
            known[ch] = {jp for jp, _ in rs}
            from_books[name.split('/')[0]] += 1
    chars = dict(sorted(chars.items()))

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

    # Where rime gives a word several readings, ToJyutping's choice wins: it
    # follows Hong Kong usage (公園 gung1 jyun2, 郵局 jau4 guk2, 請假 ceng2).
    # Tested on the Hong Kong Cantonese Corpus (see CHANGELOG.md, Part II,
    # Section 9), taking its other readings too gained nothing.
    tojyutping = load_tojyutping(freq)
    overridden = 0
    for w, (syls,) in tojyutping.items():
        if w in words and w not in CURATED_WORDS and syls != words[w] and syls in entries[w]:
            words[w] = syls
            overridden += 1
    for w, jp in CURATED_WORDS.items():
        assert len(jp.split()) == len(w) and all(SYL.match(x) for x in jp.split()), w
        words[w] = jp.split()
    dupes = sum(1 for rs in entries.values() if len(rs) > 1)

    def adverbs(ws):    # The adverb suffix 地 (慢慢地, 麻麻地) is often written 哋.
        for w, syls in list(ws.items()):
            if w.endswith('地') and syls[-1] == 'dei2':
                words.setdefault(w[:-1] + '哋', syls)
    adverbs(words)

    # Words of CC-Canto, the CC-CEDICT Cantonese readings and ToJyutping that
    # the list (by raw or canonical spelling) does not have.  A reading is
    # taken if
    #  - each syllable is a reading LSHK, rime or the book gives its
    #    character, or a changed tone of one (tone 1 or 2);
    #  - it keeps a reading rime gives to every word and every pair of
    #    characters of the list inside it (rime stays authoritative);
    #  - it does not change the reading of a final particle (你好嗎 maa1);
    #  - for two characters AB: no word of the list ends in A with another
    #    reading, as a tie goes to the later word (屋企|住 -> 屋|企住).
    # CC-Canto, the Cantonese dictionary, wins over the readings of Mandarin
    # words and ToJyutping comes last; then the most usual syllables.
    cedict = ROOT / 'jyut-dict/src/dictionaries/cedict/data'
    sources = {'CC-Canto': load_cedict(cedict / 'CC-CANTO.txt'),
               'CC-CEDICT readings': load_cedict(cedict / 'READINGS.txt')}
    sources['ToJyutping'] = tojyutping
    cw = lambda w: ''.join(canon.get(c, c) for c in w)
    listed = {w: entries[w] if w in entries and w not in CURATED_WORDS else [s]
              for w, s in words.items()}
    listed = {**{cw(w): rs for w, rs in listed.items()}, **listed}
    pairs = collections.defaultdict(set)    # two characters -> readings in the list
    ends = collections.defaultdict(set)     # char -> readings ending a word of the list
    for w, rs in listed.items():
        for s in rs:
            ends[w[-1]].add(s[-1])
            for i in range(len(w) - 1):
                pairs[w[i:i + 2]].add((s[i], s[i + 1]))

    def problem(w, syls):
        """Why the reading syls of the new word w is not taken, or None."""
        if len(syls) != len(w) or not all(
                SYL.match(s) and (s in known[c] or s[-1] in '12' and
                                  any(k[:-1] == s[:-1] for k in known[c]))
                for c, s in zip(w, syls)):
            return 'unknown readings'
        if not all(syls[i:j] in listed.get(w[i:j], listed.get(cw(w[i:j]), [syls[i:j]]))
                   for i in range(len(w)) for j in range(i + 2, len(w) + 1)):
            return 'a word inside read otherwise'
        if not all(tuple(syls[i:i + 2]) in pairs.get(cw(w[i:i + 2]), {tuple(syls[i:i + 2])})
                   for i in range(len(w) - 1)):
            return 'two characters read otherwise'
        if w[-1] in PARTICLES and syls[-1] != chars[w[-1]][0]:
            return 'final particle'
        if len(w) == 2 and ends[cw(w[0])] - {syls[0]}:
            return 'first character ends a word read otherwise'
        return None

    rejected = collections.Counter()
    new = {}        # word -> (reading, source)
    for w in sorted(set().union(*sources.values())):
        if len(w) < 2 or w in listed or cw(w) in listed:
            continue
        if w in EXCLUDED_WORDS:
            rejected['excluded by hand'] += 1
            continue
        if not all(c in chars for c in w):
            rejected['characters outside the table'] += 1
            continue
        why = {(name, tuple(s)): problem(w, s) for name, src in sources.items()
               for s in src.get(w, [])}
        ok = [(name, list(s)) for (name, s), p in why.items() if not p]
        if not ok:
            rejected[next(iter(why.values()))] += 1
            continue
        name = ok[0][0]
        new[w] = (max((s for n, s in ok if n == name), key=lambda s: score(w, s)), name)

    # Only the words that change a reading: shortest first (only shorter
    # words can change how a word is read), add those that the list, with
    # the shorter words added, reads otherwise.
    added = {}
    for size in sorted({len(w) for w in new}):
        read = reader(chars, canon, with_aliases({**words, **added}, canon)[0])
        added.update({w: s for w, (s, _) in new.items() if len(w) == size and read(w) != s})
    rejected['read so already'] = len(new) - len(added)
    words.update(added)
    adverbs(added)
    from_cedict = collections.Counter(new[w][1] for w in added)

    allwords, n_aliases, clashes = with_aliases(words, canon)

    longest = collections.defaultdict(int)  # final char -> longest word
    for w in allwords:
        longest[w[-1]] = max(longest[w[-1]], len(w))

    # --- output ----------------------------------------------------------
    header = [
        '%% Generated by tools/build-data.py -- do not edit.',
        '%% Distributed under CC BY-SA 4.0 (it adapts CC BY-SA material);',
        '%% see README.md for the sources and their authors.',
        '%% Sources: LSHK Jyutping table (CC BY 4.0),',
        '%%          rime-cantonese jyut6ping3 dictionaries (CC BY 4.0),',
        '%%          OpenCC HK/TW variant tables (Apache-2.0),',
        '%%          ToJyutping word list (CanCLID, BSD-2-Clause),',
    ]
    with open(REPO / 'xjyutping-chars.def', 'w', encoding='utf8') as f:
        f.write('\n'.join(header) + '\n%%          cantonese-books-data readings of '
                'characters (no licence stated).\n')
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
        f.write('\n'.join(header) + '\n%%          CC-Canto and CC-CEDICT Cantonese readings '
                '(CC BY-SA 3.0).\n')
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
              len(words), n_aliases, clashes, dupes), file=sys.stderr)
    print('chars added from cantonese-books-data: %d (%s)' % (
        sum(from_books.values()), ', '.join('%s %d' % kv for kv in from_books.items())),
        file=sys.stderr)
    print('ToJyutping readings taken for words of the list: %d' % overridden, file=sys.stderr)
    print('words added from jyut-dict and ToJyutping: %d (%s); not added: %s' % (
        len(added), ', '.join('%s %d' % kv for kv in sorted(from_cedict.items())),
        ', '.join('%d %s' % (n, why) for why, n in rejected.most_common())), file=sys.stderr)


if __name__ == '__main__':
    main()
