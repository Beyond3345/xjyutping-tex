-- xjyutping.lua -- the LuaLaTeX side of xjyutping.sty.
--
-- Copyright (C) 2026 by the xjyutping authors.
-- This work may be distributed and/or modified under the conditions of the
-- LaTeX Project Public License, version 1.3c or later.
--
-- Under XeLaTeX the package builds each cell while xeCJK typesets the
-- character.  LuaTeX has no such per-character hook, so the TeX side builds
-- the ruby of each character in advance (xjyutping@lua@store) and tags the
-- character's glyph with an attribute.  After LuaTeX-ja has added its glue
-- and line-break penalties (in pre_linebreak_filter and hpack_filter), the
-- callback below wraps each tagged glyph into its cell:
--
--   \hbox{ \kern<pad> <ruby overlay> <glyph> \kern<pad> }
--
-- The right pad is left out before punctuation that should hug the
-- character; the glue after a cell becomes the stretch of hsep, as under
-- XeLaTeX.  A Chinese character typeset while annotation is on but without
-- a reading from the preprocessor (text from a macro) is annotated here
-- without context, by running TeX code with tex.runtoks.

local M = {}

local cell_attr  = luatexbase.new_attribute('xjyutping@cell')
local scope_attr = luatexbase.new_attribute('xjyutping@scope')
local UNSET = -0x7FFFFFFF

local GLYPH, HLIST, GLUE, PENALTY, KERN, WHATSIT, RULE, DISC, MARK, INS
  = node.id 'glyph', node.id 'hlist', node.id 'glue', node.id 'penalty',
    node.id 'kern', node.id 'whatsit', node.id 'rule', node.id 'disc',
    node.id 'mark', node.id 'ins'
local LOCALPAR, DIR = node.id 'local_par', node.id 'dir'
local has_attribute, set_attribute, unset_attribute
  = node.has_attribute, node.set_attribute, node.unset_attribute

-- LuaTeX-ja tags the glue it inserts; 68 is the glue between two Chinese
-- characters (its KANJI_SKIP).
local function icflag(n)
  local a = luatexbase.attributes['ltj@icflag']
  return a and has_attribute(n, a)
end
local KANJI_SKIP = (luatexja and luatexja.icflag_table
                    and luatexja.icflag_table.KANJI_SKIP) or 68

-- Punctuation, as in xeCJK's classes FullLeft (opening) and FullRight
-- (closing, full stops, colons ...).  The package asks for these too.
M.fullleft = {}
M.fullright = {}
for _, c in ipairs {
  0x2018, 0x201C, 0x3008, 0x300A, 0x300C, 0x300E, 0x3010, 0x3014, 0x3016,
  0x3018, 0x301A, 0x301D, 0xFE17, 0xFE35, 0xFE37, 0xFE39, 0xFE3B, 0xFE3D,
  0xFE3F, 0xFE41, 0xFE43, 0xFE47, 0xFE59, 0xFE5B, 0xFE5D, 0xFF08, 0xFF3B,
  0xFF5B, 0xFF5F, 0xFF62, 0xFE69, 0xFF04, 0xFFE1, 0xFFE5, 0xFFE6 } do
  M.fullleft[c] = true
end
for _, c in ipairs {
  0x00B7, 0x2019, 0x201D, 0x2013, 0x2014, 0x2025, 0x2026, 0x2027, 0x2E3A,
  0x3001, 0x3002, 0x3009, 0x300B, 0x300D, 0x300F, 0x3011, 0x3015, 0x3017,
  0x3019, 0x301B, 0x301E, 0x301F, 0xFE11, 0xFE12, 0xFE18, 0xFE36, 0xFE38,
  0xFE3A, 0xFE3C, 0xFE3E, 0xFE40, 0xFE42, 0xFE44, 0xFE48, 0xFE50, 0xFE52,
  0xFE5A, 0xFE5C, 0xFE5E, 0xFF09, 0xFF0C, 0xFF0E, 0xFF3D, 0xFF5D, 0xFF60,
  0xFF61, 0xFF63, 0xFF64, 0x30FB, 0xFE54, 0xFE55, 0xFF1A, 0xFF1B, 0xFF65,
  0x16FE0, 0xFE15, 0xFE16, 0xFE56, 0xFE57, 0xFF01, 0xFF1F, 0xFE10, 0xFE13,
  0xFE14, 0xFE6A, 0xFF05, 0xFFE0, 0x301C, 0x30A0, 0xFF5E } do
  M.fullright[c] = true
end
-- For the preprocessor: the class of character code c, as a string.
function M.class(c)
  if M.fullright[c] then tex.sprint('FullRight')
  elseif M.fullleft[c] then tex.sprint('FullLeft') end
end
-- Before these the pad is kept (closing brackets and quotes) ...
local closing = {}
for _, c in utf8.codes '」』）】》〉〕］｝”’〗〙〟｠' do closing[c] = true end
-- ... and before these it is kept only where the line breaks.
local long = {}
for _, c in utf8.codes '—…‥⸺' do long[c] = true end

-- The cells built by the TeX side: id -> { box, pad, stretch }.
local cells, last = {}, 0

local function store(settag)
  local b = token.scan_int()
  local pad = token.scan_int()
  local stretch = token.scan_int()
  last = last + 1
  cells[last] = { box = node.copy(tex.getbox(b)), pad = pad, stretch = stretch }
  if settag then tex.setattribute(cell_attr, last) end
  M.last = last
end

local function define(name, fn)
  local id = luatexbase.new_luafunction(name)
  lua.get_functions_table()[id] = fn
  token.set_lua(name, id, 'protected')
end
-- \xjyutping@lua@store <box> <pad> <stretch>: tag what follows
define('xjyutping@lua@store', function () store(true) end)
-- the same for a character already typeset (no context)
define('xjyutping@lua@storeonly', function () store(false) end)
define('xjyutping@lua@on', function () tex.setattribute(scope_attr, 1) end)
define('xjyutping@lua@off', function ()
  tex.setattribute(scope_attr, UNSET)
  tex.setattribute(cell_attr, UNSET)
end)

-- The glyph of a character as LuaTeX-ja leaves it: a glyph, or a glyph
-- packed alone in an hbox (to give it its JFM width).
local function glyph_of(n)
  if n.id == GLYPH then return n end
  -- (a cell of ours is tagged -1; LuaTeX-ja's box copies the glyph's tag)
  if n.id == HLIST and (has_attribute(n, cell_attr) or 0) >= 0 then
    local h = n.head
    if h and h.id == GLYPH and not h.next then return h end
  end
end

-- The next visible object after n (skipping glue, penalties, kerns and
-- invisible nodes).
local function next_object(n)
  while n do
    local id = n.id
    if id == GLUE or id == PENALTY or id == KERN or id == WHATSIT
       or id == MARK or id == INS or id == LOCALPAR or id == DIR
       or (id == RULE and n.width == 0) then
      n = n.next
    else
      return n
    end
  end
end

local function new_kern(w)
  local k = node.new(KERN)
  k.kern = w
  return k
end

-- A character with no cell but typeset in a scope: build one now.
local char_macro = function (c) return token.get_macro('xjp@c@' .. utf8.char(c)) end
local function nocontext(g)
  if not (char_macro(g.char) or token.get_macro('xjp@u@' .. utf8.char(g.char))) then
    return
  end
  M.last = nil
  local size = font.getfont(g.font)
  size = size and size.size or tex.sp('10pt')
  local ok, err = pcall(tex.runtoks, function ()
    tex.sprint(luatexbase.registernumber('catcodetable@atletter'),
      string.format('\\xjyutping@lua@nocontext{%s}{%.4f}',
                    utf8.char(g.char), size / 65536))
  end)
  if not ok then
    texio.write_nl('log', 'xjyutping: ' .. tostring(err))
    return
  end
  return M.last
end

local function discardable(n)
  local id = n.id
  return id == GLUE or id == KERN or id == PENALTY
end

-- Wrap the character object n (glyph g, cell id) into its cell.
local function wrap(head, n, g, id)
  local c = cells[id]
  cells[id] = nil
  unset_attribute(g, cell_attr)
  unset_attribute(g, scope_attr)
  unset_attribute(n, cell_attr)
  unset_attribute(n, scope_attr)
  local right, brk = c.pad, nil
  local o = next_object(n.next)
  local og = o and glyph_of(o)
  if og and M.fullright[og.char] and not closing[og.char] then
    right = 0
    if long[og.char] then
      -- A line may break before a long mark: find that break and move it
      -- into a discretionary whose pre-break text is the pad, so the pad
      -- stays at the end of the line if the line breaks there.
      local p, prev = n.next, n
      while p and p ~= o do
        local nx = p.next
        if p.id == PENALTY and p.penalty < 10000 then
          brk = math.min(brk or 10000, p.penalty)
          p.penalty = 10000
        elseif p.id == GLUE and not discardable(prev) then
          brk = math.min(brk or 10000, 0)
          local pen = node.new(PENALTY)
          pen.penalty = 10000
          head = node.insert_before(head, p, pen)
        end
        prev, p = p, nx
      end
    end
  end
  local after = n.next
  head = node.remove(head, n)
  n.next, n.prev = nil, nil
  local left, box = new_kern(c.pad), c.box
  left.next, box.prev = box, left
  box.next, n.prev = n, box
  if right ~= 0 then
    local k = new_kern(right)
    n.next, k.prev = k, n
  end
  local cell = node.hpack(left)
  set_attribute(cell, cell_attr, -1)
  if after then
    head = node.insert_before(head, after, cell)
  else
    head = node.insert_after(head, node.tail(head), cell)
  end
  if brk then
    local d = node.new(DISC)
    d.pre = new_kern(c.pad)
    d.penalty = brk
    head = node.insert_after(head, cell, d)
  end
  -- the glue to the next character: only the stretch of hsep (its natural
  -- part is inside the cells)
  local p = cell.next
  while p and (p.id == PENALTY or p.id == WHATSIT or p.id == DISC
               or p.id == KERN or p.id == GLUE) do
    if p.id == GLUE and icflag(p) == KANJI_SKIP then
      p.width, p.stretch, p.shrink = 0, c.stretch, 0
      p.stretch_order, p.shrink_order = 0, 0
      break
    end
    p = p.next
  end
  return head, cell
end

local function process(head)
  local n = head
  while n do
    local g = glyph_of(n)
    local id = g and has_attribute(g, cell_attr)
    if not (id and id > 0 and cells[id]) and g
       and (has_attribute(g, scope_attr) or 0) > 0 then
      unset_attribute(g, scope_attr)
      id = nocontext(g)
    end
    if id and id > 0 and cells[id] then
      local cell
      head, cell = wrap(head, n, g, id)
      n = cell.next
    else
      n = n.next
    end
  end
  return head
end

luatexbase.add_to_callback('pre_linebreak_filter', process, 'xjyutping')
luatexbase.add_to_callback('hpack_filter', process, 'xjyutping')

return M
