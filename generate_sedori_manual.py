#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os

# ── フォント登録 ──────────────────────────────────────────
pdfmetrics.registerFont(TTFont('JP', '/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('JP-Bold', '/Library/Fonts/Arial Unicode.ttf'))

# ── カラーパレット ─────────────────────────────────────────
C_DARK    = colors.HexColor('#1A1A2E')   # 濃紺
C_ACCENT  = colors.HexColor('#E94560')   # 赤
C_BLUE    = colors.HexColor('#0F3460')   # 青
C_LIGHT   = colors.HexColor('#16213E')   # 中間紺
C_GOLD    = colors.HexColor('#F5A623')   # ゴールド
C_GREEN   = colors.HexColor('#27AE60')   # 緑
C_GRAY    = colors.HexColor('#BDC3C7')   # グレー
C_BGLIGHT = colors.HexColor('#F8F9FA')   # 薄グレー背景
C_WHITE   = colors.white
C_RED     = colors.HexColor('#E74C3C')
C_ORANGE  = colors.HexColor('#E67E22')

W, H = A4

# ── スタイル定義 ──────────────────────────────────────────
def make_styles():
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='JP', fontSize=28, leading=40,
        textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=8)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='JP', fontSize=14, leading=22,
        textColor=C_GOLD, alignment=TA_CENTER, spaceAfter=6)

    s['cover_desc'] = ParagraphStyle('cover_desc',
        fontName='JP', fontSize=11, leading=18,
        textColor=C_GRAY, alignment=TA_CENTER)

    s['chapter'] = ParagraphStyle('chapter',
        fontName='JP', fontSize=18, leading=28,
        textColor=C_WHITE, alignment=TA_LEFT,
        spaceBefore=4, spaceAfter=4)

    s['section'] = ParagraphStyle('section',
        fontName='JP', fontSize=13, leading=20,
        textColor=C_DARK, alignment=TA_LEFT,
        spaceBefore=10, spaceAfter=4,
        borderPad=4)

    s['body'] = ParagraphStyle('body',
        fontName='JP', fontSize=10, leading=17,
        textColor=C_DARK, alignment=TA_JUSTIFY,
        spaceAfter=4)

    s['body_white'] = ParagraphStyle('body_white',
        fontName='JP', fontSize=10, leading=17,
        textColor=C_WHITE, alignment=TA_LEFT,
        spaceAfter=3)

    s['bullet'] = ParagraphStyle('bullet',
        fontName='JP', fontSize=10, leading=17,
        textColor=C_DARK, leftIndent=12, spaceAfter=3)

    s['bullet_white'] = ParagraphStyle('bullet_white',
        fontName='JP', fontSize=10, leading=17,
        textColor=C_WHITE, leftIndent=12, spaceAfter=3)

    s['highlight'] = ParagraphStyle('highlight',
        fontName='JP', fontSize=11, leading=19,
        textColor=C_DARK, alignment=TA_CENTER,
        spaceBefore=4, spaceAfter=4)

    s['caption'] = ParagraphStyle('caption',
        fontName='JP', fontSize=9, leading=14,
        textColor=colors.HexColor('#7F8C8D'), alignment=TA_CENTER)

    s['tag'] = ParagraphStyle('tag',
        fontName='JP', fontSize=9, leading=14,
        textColor=C_WHITE, alignment=TA_CENTER)

    s['toc_item'] = ParagraphStyle('toc_item',
        fontName='JP', fontSize=11, leading=18,
        textColor=C_DARK, leftIndent=16, spaceAfter=5)

    s['step_num'] = ParagraphStyle('step_num',
        fontName='JP', fontSize=22, leading=28,
        textColor=C_ACCENT, alignment=TA_CENTER)

    s['step_title'] = ParagraphStyle('step_title',
        fontName='JP', fontSize=12, leading=18,
        textColor=C_DARK, alignment=TA_LEFT)

    s['quote'] = ParagraphStyle('quote',
        fontName='JP', fontSize=13, leading=22,
        textColor=C_DARK, alignment=TA_CENTER,
        spaceBefore=6, spaceAfter=6)

    s['small'] = ParagraphStyle('small',
        fontName='JP', fontSize=9, leading=14,
        textColor=colors.HexColor('#555555'), spaceAfter=2)

    return s

# ── カスタムFlowable ──────────────────────────────────────

class ColorRect(Flowable):
    def __init__(self, w, h, fill_color, radius=4):
        super().__init__()
        self.w, self.h, self.fill = w, h, fill_color
        self.radius = radius
    def draw(self):
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.w, self.h, self.radius, fill=1, stroke=0)

class DividerLine(Flowable):
    def __init__(self, color=C_ACCENT, thickness=2, width=None):
        super().__init__()
        self._color = color
        self.thickness = thickness
        self._width = width
    def wrap(self, availW, availH):
        self.availW = self._width or availW
        return (self.availW, self.thickness + 4)
    def draw(self):
        self.canv.setStrokeColor(self._color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness/2, self.availW, self.thickness/2)

# ── ページテンプレート ─────────────────────────────────────

PAGE_NUM = [0]

def on_page(canvas, doc):
    PAGE_NUM[0] += 1
    pn = PAGE_NUM[0]
    if pn == 1:
        # カバーページ：背景塗りつぶし
        canvas.setFillColor(C_DARK)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        # アクセントライン上部
        canvas.setFillColor(C_ACCENT)
        canvas.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
        # 底部帯
        canvas.setFillColor(C_BLUE)
        canvas.rect(0, 0, W, 22*mm, fill=1, stroke=0)
        canvas.setFillColor(C_GOLD)
        canvas.setFont('JP', 9)
        canvas.drawCentredString(W/2, 8*mm,
            'リベラルアーツ大学 両学長動画解説  |  2026年版  |  せどり副業完全行動マニュアル')
    else:
        # 通常ページ：ヘッダー帯
        canvas.setFillColor(C_DARK)
        canvas.rect(0, H - 14*mm, W, 14*mm, fill=1, stroke=0)
        canvas.setFillColor(C_ACCENT)
        canvas.rect(0, H - 14*mm, 3*mm, 14*mm, fill=1, stroke=0)
        canvas.setFillColor(C_WHITE)
        canvas.setFont('JP', 9)
        canvas.drawString(8*mm, H - 9*mm, 'せどり副業 完全行動マニュアル 2026年版')
        canvas.drawRightString(W - 8*mm, H - 9*mm, f'p.{pn - 1}')
        # フッター
        canvas.setFillColor(C_BGLIGHT)
        canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
        canvas.setFillColor(C_GRAY)
        canvas.setFont('JP', 8)
        canvas.drawCentredString(W/2, 3*mm,
            'リベラルアーツ大学 両学長  |  第52回・第86回 動画解説マニュアル')

# ── ヘルパー関数 ─────────────────────────────────────────

def chapter_header(title, subtitle='', color=C_DARK):
    """章タイトルブロック"""
    data = [[Paragraph(title, make_styles()['chapter'])]]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ])
    t = Table(data, colWidths=[170*mm])
    t.setStyle(ts)
    items = [Spacer(1, 6*mm), t]
    if subtitle:
        items.append(Spacer(1, 2*mm))
        items.append(Paragraph(subtitle, make_styles()['caption']))
    items.append(Spacer(1, 4*mm))
    return items

def section_box(title, color=C_BLUE):
    """セクションタイトル"""
    st = make_styles()
    data = [[Paragraph(f'  {title}', ParagraphStyle('sh',
        fontName='JP', fontSize=12, leading=18, textColor=C_WHITE))]]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ])
    t = Table(data, colWidths=[170*mm])
    t.setStyle(ts)
    return [Spacer(1, 3*mm), t, Spacer(1, 2*mm)]

def info_box(text, color=C_BGLIGHT, text_color=C_DARK, border_color=C_ACCENT):
    """情報ボックス"""
    data = [[Paragraph(text, ParagraphStyle('ib',
        fontName='JP', fontSize=10, leading=17, textColor=text_color))]]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEAFTER', (0,0), (0,-1), 4, border_color),
    ])
    t = Table(data, colWidths=[170*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 3*mm)]

def two_col_table(left_data, right_data, headers=('', ''),
                  left_bg=C_BGLIGHT, right_bg=colors.HexColor('#EBF5FB')):
    """2列比較テーブル"""
    st = make_styles()
    h_style = ParagraphStyle('th', fontName='JP', fontSize=10,
                              leading=16, textColor=C_WHITE, alignment=TA_CENTER)
    c_style = ParagraphStyle('td', fontName='JP', fontSize=9, leading=15, textColor=C_DARK)

    rows = []
    if headers[0] or headers[1]:
        rows.append([Paragraph(headers[0], h_style), Paragraph(headers[1], h_style)])

    for l, r in zip(left_data, right_data):
        rows.append([Paragraph(l, c_style), Paragraph(r, c_style)])

    ts = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, C_GRAY),
        ('BACKGROUND', (0,0), (0,0), C_ACCENT),
        ('BACKGROUND', (1,0), (1,0), C_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_BGLIGHT, C_WHITE]),
    ])
    t = Table(rows, colWidths=[85*mm, 85*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 4*mm)]

def step_card(num, title, details, color=C_DARK):
    st = make_styles()
    num_p = Paragraph(str(num), ParagraphStyle('sn',
        fontName='JP', fontSize=24, leading=28, textColor=color, alignment=TA_CENTER))
    title_p = Paragraph(title, ParagraphStyle('st',
        fontName='JP', fontSize=11, leading=17, textColor=C_DARK))
    detail_p = Paragraph(details, ParagraphStyle('sd',
        fontName='JP', fontSize=9, leading=14, textColor=colors.HexColor('#555')))
    row = [[num_p, [title_p, detail_p]]]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#F0F3F4')),
        ('BACKGROUND', (1,0), (1,0), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_GRAY),
        ('LINEAFTER', (0,0), (0,-1), 2, color),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,0), 4),
        ('LEFTPADDING', (1,0), (1,0), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    t = Table(row, colWidths=[20*mm, 150*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 2*mm)]

def warning_box(title, content):
    st = make_styles()
    t_style = ParagraphStyle('wt', fontName='JP', fontSize=10, leading=16,
                              textColor=C_WHITE, alignment=TA_LEFT)
    c_style = ParagraphStyle('wc', fontName='JP', fontSize=9, leading=15,
                              textColor=C_DARK)
    rows = [
        [Paragraph(f'  {title}', t_style)],
        [Paragraph(content, c_style)],
    ]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_RED),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor('#FDEDEC')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, C_RED),
    ])
    t = Table(rows, colWidths=[170*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 3*mm)]

def success_box(title, content):
    t_style = ParagraphStyle('gt', fontName='JP', fontSize=10, leading=16,
                              textColor=C_WHITE)
    c_style = ParagraphStyle('gc', fontName='JP', fontSize=9, leading=15,
                              textColor=C_DARK)
    rows = [
        [Paragraph(f'  {title}', t_style)],
        [Paragraph(content, c_style)],
    ]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_GREEN),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor('#EAFAF1')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, C_GREEN),
    ])
    t = Table(rows, colWidths=[170*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 3*mm)]

def gold_quote(text):
    data = [[Paragraph(text, ParagraphStyle('gq',
        fontName='JP', fontSize=13, leading=22,
        textColor=C_DARK, alignment=TA_CENTER))]]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF9E7')),
        ('LINEABOVE', (0,0), (-1,0), 3, C_GOLD),
        ('LINEBELOW', (0,-1), (-1,-1), 3, C_GOLD),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ])
    t = Table(data, colWidths=[170*mm])
    t.setStyle(ts)
    return [t, Spacer(1, 4*mm)]

# ── コンテンツ生成 ────────────────────────────────────────

def build_content():
    st = make_styles()
    story = []

    # ═══════════════════════════════════
    # PAGE 1: カバーページ
    # ═══════════════════════════════════
    story.append(Spacer(1, 28*mm))
    story.append(Paragraph('せどり副業', st['cover_title']))
    story.append(Paragraph('完全行動マニュアル', ParagraphStyle('ct2',
        fontName='JP', fontSize=32, leading=44,
        textColor=C_ACCENT, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('2026年版', st['cover_sub']))
    story.append(Spacer(1, 6*mm))

    # カバー区切り線
    data_div = [['']]
    ts_div = TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, C_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ])
    t_div = Table(data_div, colWidths=[120*mm])
    t_div.setStyle(ts_div)
    story.append(Table([[t_div]], colWidths=[170*mm],
                        style=[('ALIGN',(0,0),(-1,-1),'CENTER')]))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        'リベラルアーツ大学 両学長',
        st['cover_desc']))
    story.append(Paragraph(
        '第52回「せどりで年収100万円アップ」× 第86回「稼げる人と稼げない人の違い」',
        st['cover_desc']))
    story.append(Spacer(1, 8*mm))

    # バッジ行
    badge_style = ParagraphStyle('badge', fontName='JP', fontSize=10,
                                  leading=16, textColor=C_WHITE, alignment=TA_CENTER)
    badges = [
        [Paragraph('考え方', badge_style), Paragraph('実践ステップ', badge_style),
         Paragraph('ロードマップ', badge_style), Paragraph('失敗対策', badge_style)],
    ]
    ts_b = TableStyle([
        ('BACKGROUND', (0,0), (0,0), C_ACCENT),
        ('BACKGROUND', (1,0), (1,0), C_BLUE),
        ('BACKGROUND', (2,0), (2,0), C_GREEN),
        ('BACKGROUND', (3,0), (3,0), C_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ])
    t_b = Table(badges, colWidths=[40*mm, 44*mm, 44*mm, 42*mm])
    t_b.setStyle(ts_b)
    story.append(Table([[t_b]], colWidths=[170*mm],
                        style=[('ALIGN',(0,0),(-1,-1),'CENTER')]))

    story.append(PageBreak())

    # ═══════════════════════════════════
    # PAGE 2: 目次
    # ═══════════════════════════════════
    story += chapter_header('目  次', color=C_DARK)

    toc_items = [
        ('01', 'この動画がなぜ重要なのか', '動画の本質・他サイトとの違い'),
        ('02', '根本思想：稼げる人と稼げない人の違い', '考え方の転換が最初のステップ'),
        ('03', 'せどり5種類の全体像', '手法の選び方と向き不向き'),
        ('04', 'クロードができること vs あなたがすること', '役割分担で最速で進む'),
        ('05', '実践ロードマップ（全スケジュール）', '週・月別の行動計画'),
        ('06', '初心者が「つまずく」7大ポイントと突破法', '失敗を事前につぶす'),
        ('07', '利益計算・ツール・コスト完全整理', '数字で判断するための基礎'),
        ('08', '行動チェックリスト', '今日から動くための確認表'),
    ]

    for num, title, sub in toc_items:
        row = [
            [Paragraph(num, ParagraphStyle('tn', fontName='JP', fontSize=14,
                                            leading=20, textColor=C_ACCENT, alignment=TA_CENTER)),
             [Paragraph(title, ParagraphStyle('tt', fontName='JP', fontSize=11,
                                              leading=17, textColor=C_DARK)),
              Paragraph(sub, ParagraphStyle('ts', fontName='JP', fontSize=9,
                                            leading=14, textColor=C_GRAY))]
            ]
        ]
        ts_toc = TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#F0F3F4')),
            ('LINEAFTER', (0,0), (0,0), 2, C_ACCENT),
            ('BOX', (0,0), (-1,-1), 0.5, C_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (0,0), 4),
            ('LEFTPADDING', (1,0), (1,0), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
        t_toc = Table(row, colWidths=[18*mm, 152*mm])
        t_toc.setStyle(ts_toc)
        story.append(t_toc)
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 01: なぜこの動画が重要か
    # ═══════════════════════════════════
    story += chapter_header('01  なぜこの動画が重要なのか', color=C_ACCENT)

    story += gold_quote(
        '"手段（せどりの種類）を探す前に、\n稼げる・稼げないを分ける思考の違いを知ることが\n全ての出発点である"'
    )

    story += section_box('この動画2本が必要な理由')
    story.append(Paragraph(
        '多くの副業解説コンテンツは「やり方・手順」だけを教えます。しかし両学長の動画が他と決定的に異なるのは、'
        '「なぜ稼げる人と稼げない人が生まれるのか」という根本の思考から解説している点です。',
        st['body']))
    story.append(Spacer(1, 2*mm))

    diff_rows = [
        ['比較項目', '一般的な副業解説サイト', '両学長の動画（この2本）'],
        ['出発点', '「手順・やり方」から入る', '「思考・価値提供」から入る'],
        ['失敗原因', '手順が間違っていると考える', '思考の向きが逆と指摘する'],
        ['再現性', '同じ商品・手法を真似る', '原則を学ぶので何にでも応用可'],
        ['持続性', 'トレンドが変わると陳腐化', '原則は不変なので長期活用可'],
        ['対象範囲', '特定の副業のみ対応', 'せどり・蕎麦屋・どんな副業にも適用'],
        ['深さ', '表面的なHow-to止まり', 'Why（なぜ）まで掘り下げる'],
    ]
    h_style = ParagraphStyle('dh', fontName='JP', fontSize=9, leading=14,
                              textColor=C_WHITE, alignment=TA_CENTER)
    c_style = ParagraphStyle('dc', fontName='JP', fontSize=9, leading=14, textColor=C_DARK)
    c_red = ParagraphStyle('dcr', fontName='JP', fontSize=9, leading=14,
                            textColor=colors.HexColor('#C0392B'))
    c_green = ParagraphStyle('dcg', fontName='JP', fontSize=9, leading=14,
                              textColor=colors.HexColor('#1E8449'))

    fmt_rows = []
    for i, row in enumerate(diff_rows):
        if i == 0:
            fmt_rows.append([Paragraph(c, h_style) for c in row])
        else:
            fmt_rows.append([
                Paragraph(row[0], c_style),
                Paragraph(row[1], c_red),
                Paragraph(row[2], c_green),
            ])

    ts_diff = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK),
        ('BACKGROUND', (0,1), (-1,-1), C_WHITE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_BGLIGHT, C_WHITE]),
        ('GRID', (0,0), (-1,-1), 0.5, C_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEAFTER', (0,0), (0,-1), 1.5, C_ACCENT),
    ])
    t_diff = Table(fmt_rows, colWidths=[32*mm, 66*mm, 72*mm])
    t_diff.setStyle(ts_diff)
    story.append(t_diff)
    story.append(Spacer(1, 4*mm))

    story += info_box(
        '注意：第52回動画は2020年版のため、一部ツール（モノレート）はすでに終了。'
        '2026年現在は「Keepa（月額約3,000円）」を使用。ただし考え方・原則は現在も完全に有効。',
        color=colors.HexColor('#FEF9E7'), border_color=C_GOLD)

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 02: 根本思想
    # ═══════════════════════════════════
    story += chapter_header('02  根本思想：稼げる人と稼げない人の違い', color=C_BLUE)

    story += gold_quote(
        '"稼げる人は相手に価値を提供することを考える\n稼げない人は自分がどうお金をもらうかを考える"'
    )

    story += section_box('思考の構造比較')
    think_rows = [
        ['思考の向き', '稼げない人', '稼げる人'],
        ['最初の問い', '「この副業は儲かる？」', '「誰の何の悩みを解決できる？」'],
        ['仕入れの基準', '「安いから仕入れよう」', '「誰かが必要としているか？」'],
        ['値決め', '「利益が出る値段」', '「相手が感じる価値に見合う値段」'],
        ['失敗時', '「運が悪かった」', '「データを取って次に活かす」'],
        ['継続性', 'うまくいかないと辞める', 'パターンが出るまで改善を続ける'],
    ]
    fmt2 = []
    h_s = ParagraphStyle('h2', fontName='JP', fontSize=9, leading=14,
                          textColor=C_WHITE, alignment=TA_CENTER)
    c_s = ParagraphStyle('c2', fontName='JP', fontSize=9, leading=14, textColor=C_DARK)
    for i, row in enumerate(think_rows):
        if i == 0:
            fmt2.append([Paragraph(c, h_s) for c in row])
        else:
            fmt2.append([Paragraph(r, c_s) for r in row])
    ts2 = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK),
        ('BACKGROUND', (1,1), (1,-1), colors.HexColor('#FDEDEC')),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor('#EAFAF1')),
        ('GRID', (0,0), (-1,-1), 0.5, C_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ])
    t2 = Table(fmt2, colWidths=[36*mm, 65*mm, 69*mm])
    t2.setStyle(ts2)
    story.append(t2)
    story.append(Spacer(1, 4*mm))

    story += section_box('稼ぐための3つの問い（どんな副業にも共通）')
    q_rows = [
        ('Q1', '誰の（ターゲット）', '例：地方在住で欲しい物が手に入らない人 / 忙しいビジネスマン'),
        ('Q2', '何の悩み・欲求か（ニーズ）', '例：入手困難商品が欲しい / 短時間で食事を済ませたい'),
        ('Q3', 'どう解決するか（差別化）', '例：希少品の専門仕入れ / 5分で提供できる蕎麦メニュー'),
    ]
    for q, title, ex in q_rows:
        row_data = [
            [Paragraph(q, ParagraphStyle('ql', fontName='JP', fontSize=14,
                                          leading=20, textColor=C_ACCENT, alignment=TA_CENTER)),
             [Paragraph(title, ParagraphStyle('qt', fontName='JP', fontSize=11,
                                              leading=17, textColor=C_DARK)),
              Paragraph(ex, ParagraphStyle('qe', fontName='JP', fontSize=9,
                                           leading=14, textColor=C_GRAY))]]
        ]
        ts_q = TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FEF9E7')),
            ('LINEAFTER', (0,0), (0,0), 3, C_GOLD),
            ('BOX', (0,0), (-1,-1), 0.5, C_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (1,0), (1,0), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
        t_q = Table(row_data, colWidths=[16*mm, 154*mm])
        t_q.setStyle(ts_q)
        story.append(t_q)
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 03: せどり5種類
    # ═══════════════════════════════════
    story += chapter_header('03  せどり5種類の全体像', color=C_GREEN)

    types = [
        ('店舗せどり', C_BLUE,
         '難易度:★★☆',
         'ブックオフ・ゲオ・ハードオフ等に行き、バーコードをスキャンして差益のある商品を仕入れる。',
         '体を動かすのが苦にならない人・近所にリサイクルショップがある人',
         'Amazonセラーアプリ（無料）・Keepa（月額約3,000円）'),
        ('電脳せどり', C_GREEN,
         '難易度:★★☆',
         '楽天・Yahoo!・メルカリ・ヤフオクなどネットで仕入れ、Amazonで販売。場所を問わない。',
         'PC作業が得意な人・在宅で副業したい人',
         'Keepa（月額約3,000円）・プライスター等'),
        ('新品せどり', C_ORANGE,
         '難易度:★☆☆',
         'セール品・廃番品を定価以下で仕入れてAmazonで定価以上で売る。初心者に最適。',
         '初心者・少ない資金から始めたい人',
         'Keepa・Amazonセラーアプリ'),
        ('中古せどり', C_ACCENT,
         '難易度:★★★',
         '中古品の状態見極め・真贋判断が必要。利益率が高いが知識とリサーチ力が必要。',
         'せどり経験者・得意ジャンルがある人',
         '鑑定ツール・Keepa・相場サイト'),
        ('輸出せどり', C_DARK,
         '難易度:★★★',
         '日本商品をeBay等で海外販売。円安メリットを活かせる。英語対応が必要。',
         '英語力がある人・大きく稼ぎたい人',
         'eBayアカウント・Payoneer・Keepa'),
    ]

    for name, col, diff, desc, target, tools in types:
        row_data = [
            [Paragraph(f'{name}\n{diff}',
                        ParagraphStyle('tn2', fontName='JP', fontSize=10,
                                       leading=16, textColor=C_WHITE, alignment=TA_CENTER)),
             [Paragraph(desc, ParagraphStyle('td2', fontName='JP', fontSize=9, leading=14, textColor=C_DARK)),
              Paragraph(f'向いてる人: {target}', ParagraphStyle('tg', fontName='JP', fontSize=8, leading=13, textColor=C_BLUE)),
              Paragraph(f'必要ツール: {tools}', ParagraphStyle('tt2', fontName='JP', fontSize=8, leading=13, textColor=C_GRAY))]
            ]
        ]
        ts_type = TableStyle([
            ('BACKGROUND', (0,0), (0,0), col),
            ('BACKGROUND', (1,0), (1,0), C_WHITE),
            ('BOX', (0,0), (-1,-1), 0.5, C_GRAY),
            ('LINEAFTER', (0,0), (0,0), 3, col),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (0,0), 4),
            ('LEFTPADDING', (1,0), (1,0), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
        t_type = Table(row_data, colWidths=[30*mm, 140*mm])
        t_type.setStyle(ts_type)
        story.append(t_type)
        story.append(Spacer(1, 2*mm))

    story += info_box(
        '初心者おすすめ：まず「店舗せどり × 新品 × 1ジャンル絞り込み」でスタート。'
        'ゲームソフト・本・おもちゃがAmazon規制が少なく始めやすい。',
        color=colors.HexColor('#EBF5FB'), border_color=C_BLUE)

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 04: 役割分担
    # ═══════════════════════════════════
    story += chapter_header('04  クロードができること vs あなたがすること', color=C_ACCENT)

    story.append(Paragraph(
        'クロード（AI）を活用することで、学習・分析・計画立案のスピードを大幅に上げられます。'
        '一方で「実際のお金・契約・物理作業」はあなた自身が行う必要があります。',
        st['body']))
    story.append(Spacer(1, 3*mm))

    role_data = [
        ['フェーズ', 'クロードができること（AI）', 'あなたがすること（必須）'],
        ['学習', '仕組み解説・用語説明・戦略相談', 'Amazonアカウント開設・本人確認'],
        ['リサーチ', '商品カテゴリ選定の考え方・競合分析の視点', 'Keepa実操作・実際の商品スキャン'],
        ['計算', '利益計算チェック・仕入れ予算シミュレーション', '実際の資金準備（3〜5万円）'],
        ['文章', '商品説明文・テンプレート作成', '出品ページへの入力・写真撮影'],
        ['改善', '「なぜ売れないか」の仮説・改善案提示', '実際の仕入れ・発送・数字記録'],
        ['計画', 'スケジュール・ロードマップ設計', '実行・継続・諦めない意志'],
        ['規約', 'Amazon規約・禁止カテゴリの確認補助', '最終判断・法的責任'],
    ]
    h_s = ParagraphStyle('rh', fontName='JP', fontSize=9, leading=14,
                          textColor=C_WHITE, alignment=TA_CENTER)
    c_s = ParagraphStyle('rc', fontName='JP', fontSize=9, leading=14, textColor=C_DARK)
    fmt_role = []
    for i, row in enumerate(role_data):
        if i == 0:
            fmt_role.append([Paragraph(c, h_s) for c in row])
        else:
            fmt_role.append([Paragraph(r, c_s) for r in row])
    ts_role = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK),
        ('BACKGROUND', (1,1), (1,-1), colors.HexColor('#EBF5FB')),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor('#EAFAF1')),
        ('ROWBACKGROUNDS', (0,1), (0,-1), [C_BGLIGHT, C_WHITE]),
        ('GRID', (0,0), (-1,-1), 0.5, C_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('LINEAFTER', (0,0), (0,-1), 1.5, C_ACCENT),
    ])
    t_role = Table(fmt_role, colWidths=[22*mm, 74*mm, 74*mm])
    t_role.setStyle(ts_role)
    story.append(t_role)
    story.append(Spacer(1, 4*mm))

    story += success_box(
        'クロードの活用例',
        '「Keepaのグラフが読めない」「この商品は仕入れていいか？」「利益計算を確認して」'
        '「月3万円稼ぐための計画を立てて」など、具体的な質問ほど精度高い回答が得られます。'
    )

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 05: ロードマップ
    # ═══════════════════════════════════
    story += chapter_header('05  実践ロードマップ（全スケジュール）', color=C_BLUE)

    phases = [
        (C_BLUE, 'Phase 1', '基礎準備期', '1〜2週間', [
            'Amazonセラー登録（大口出品：月4,900円）',
            'Keepaアカウント登録（月3,000円）',
            'Amazonセラーアプリをスマホにインストール',
            '扱うジャンル1つ決める（ゲーム・本・おもちゃ等）',
            '仕入れ資金3〜5万円を確保',
            'Keepaの見方・利益計算方法を習得',
        ]),
        (C_GREEN, 'Phase 2', '実験期', '1〜2ヶ月', [
            '週2〜3回 店舗リサーチ（1回2〜3時間）',
            '仕入れ目標：月5〜10点からスタート',
            '出品・梱包・発送を実際に体験',
            '売上・仕入れ・利益をExcelで記録',
            '売れた商品・売れなかった商品の原因分析',
            '1ジャンルで再現性あるパターンを探す',
        ]),
        (C_GOLD, 'Phase 3', '拡大期', '3〜6ヶ月', [
            '仕入れ点数を2〜3倍に増やす',
            '電脳せどり（ネット仕入れ）も並行開始',
            '月利益3〜5万円を目標にする',
            '回転が速い商品ジャンルに資金集中',
            '仕入れルートを複数確保する',
            '月利益8〜10万円（年収100万円ペース）へ',
        ]),
        (C_ACCENT, 'Phase 4', '仕組み化', '6ヶ月〜', [
            '梱包・発送の外注を検討する',
            '電脳せどりの自動化ツール導入',
            '輸出せどりへの展開を検討',
            '労働ではなく仕組みが稼ぐ状態を作る',
        ]),
    ]

    for col, phase, name, period, items in phases:
        h_style = ParagraphStyle('ph', fontName='JP', fontSize=10,
                                  leading=16, textColor=C_WHITE, alignment=TA_CENTER)
        c_style = ParagraphStyle('pc', fontName='JP', fontSize=9, leading=15, textColor=C_DARK)

        items_text = '\n'.join([f'  {i+1}. {item}' for i, item in enumerate(items)])
        row_data = [
            [Paragraph(f'{phase}\n{name}\n({period})', h_style),
             Paragraph(items_text, c_style)]
        ]
        ts_p = TableStyle([
            ('BACKGROUND', (0,0), (0,0), col),
            ('BACKGROUND', (1,0), (1,0), C_WHITE),
            ('BOX', (0,0), (-1,-1), 1, col),
            ('LINEAFTER', (0,0), (0,0), 3, col),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (0,0), 4),
            ('LEFTPADDING', (1,0), (1,0), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
        t_p = Table(row_data, colWidths=[32*mm, 138*mm])
        t_p.setStyle(ts_p)
        story.append(t_p)
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 06: つまずき7大ポイント
    # ═══════════════════════════════════
    story += chapter_header('06  初心者がつまずく7大ポイントと突破法', color=C_RED)

    stumbles = [
        (C_ACCENT, '1', 'リサーチしても利益商品が見つからない',
         '原因：ジャンル絞れていない・Keepaの見方がわからない',
         '突破法：1ジャンルに徹底集中。Keepaで「3ヶ月以上売れ続けている商品」だけを狙う。（←クロードに相談可）'),
        (C_ORANGE, '2', '仕入れたのに売れない（在庫を抱える）',
         '原因：需要確認をせず「安かったから」で仕入れた',
         '突破法：Keepaの売れ行きグラフを必ず確認。月10個以上売れている商品のみ対象にする。'),
        (C_RED, '3', '利益計算を間違える（実は赤字）',
         '原因：Amazon手数料・送料・梱包代を見落とす',
         '突破法：利益 = 売価 - 仕入れ値 - Amazon手数料(約10%) - FBA手数料 - 送料。この計算をクロードと一緒に確認。'),
        (C_BLUE, '4', 'Amazon規制に引っかかる',
         '原因：メーカー規制・真贋調査・カテゴリ制限を知らない',
         '突破法：最初は自由に出品できるカテゴリだけ（本・ゲーム・おもちゃ等）。高額ブランド品・ヘルス系は避ける。'),
        (C_GREEN, '5', '継続できない（3ヶ月で辞める）',
         '原因：最初の1〜2ヶ月で利益が出ないことへの焦り',
         '突破法：最初2ヶ月の目標は「損しないこと」。利益ゼロでも「データが取れた」と考える。月1万でも出たら成功。'),
        (C_DARK, '6', 'ライバルに価格を下げられ利益が消える',
         '原因：競合が多い商品を狙いすぎ',
         '突破法：ライバル出品者が3人以下の商品を狙う。Keepaで「価格が安定している商品」を選ぶ。'),
        (C_GOLD, '7', '確定申告・税金を知らない（無申告）',
         '原因：副業なのに申告義務を知らない',
         '突破法：年間利益20万円超で確定申告義務あり。仕入れ・ツール代・交通費はすべて経費として記録する。'),
    ]

    for col, num, title, cause, solution in stumbles:
        t_s = ParagraphStyle('st_t', fontName='JP', fontSize=10,
                              leading=16, textColor=C_WHITE)
        c_s = ParagraphStyle('st_c', fontName='JP', fontSize=9,
                              leading=14, textColor=C_DARK)
        so_s = ParagraphStyle('st_s', fontName='JP', fontSize=9,
                               leading=14, textColor=colors.HexColor('#1A5276'))

        rows = [
            [Paragraph(num, ParagraphStyle('sn_n', fontName='JP', fontSize=18,
                                            leading=24, textColor=C_WHITE, alignment=TA_CENTER)),
             Paragraph(title, t_s)],
            ['', Paragraph(f'  {cause}', c_s)],
            ['', Paragraph(f'  {solution}', so_s)],
        ]
        ts_s = TableStyle([
            ('BACKGROUND', (0,0), (0,-1), col),
            ('BACKGROUND', (1,0), (1,0), col),
            ('BACKGROUND', (1,1), (1,1), colors.HexColor('#FDFEFE')),
            ('BACKGROUND', (1,2), (1,2), colors.HexColor('#EBF5FB')),
            ('BOX', (0,0), (-1,-1), 0.5, col),
            ('SPAN', (0,0), (0,-1)),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (0,0), 4),
            ('LEFTPADDING', (1,0), (1,0), 8),
            ('VALIGN', (0,0), (0,-1), 'MIDDLE'),
            ('LINEBELOW', (1,0), (1,0), 0.5, C_GRAY),
            ('LINEBELOW', (1,1), (1,1), 0.5, C_GRAY),
        ])
        t_s_obj = Table(rows, colWidths=[14*mm, 156*mm])
        t_s_obj.setStyle(ts_s)
        story.append(t_s_obj)
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 07: 利益計算・ツール
    # ═══════════════════════════════════
    story += chapter_header('07  利益計算・ツール・コスト完全整理', color=C_GOLD)

    story += section_box('利益計算の完全公式', color=C_DARK)

    calc_text = (
        '実際の利益 = 販売価格\n'
        '　　　　　 - 仕入れ値\n'
        '　　　　　 - Amazon販売手数料（カテゴリにより約8〜15%）\n'
        '　　　　　 - FBA手数料（サイズ・重量により異なる）\n'
        '　　　　　 - 梱包材費（約30〜100円/個）\n'
        '　　　　　 - 送料（FBAの場合はFBA手数料に含む）\n'
        '　　　　　= 純利益'
    )
    data_calc = [[Paragraph(calc_text, ParagraphStyle('calc',
        fontName='JP', fontSize=10, leading=18, textColor=C_WHITE))]]
    ts_calc = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_DARK),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEABOVE', (0,0), (-1,0), 3, C_GOLD),
    ])
    t_calc = Table(data_calc, colWidths=[170*mm])
    t_calc.setStyle(ts_calc)
    story.append(t_calc)
    story.append(Spacer(1, 4*mm))

    story += section_box('必要ツール一覧（月額コスト）', color=C_BLUE)

    tool_rows = [
        ['ツール名', '用途', '費用', '優先度'],
        ['Amazonセラーアカウント（大口）', '商品出品・販売', '月4,900円', '必須'],
        ['Keepa', '価格推移・売れ行き分析', '月約3,000円', '必須'],
        ['Amazonセラーアプリ', '店舗でのバーコードスキャン', '無料', '必須'],
        ['プライスター', '価格自動調整・在庫管理', '月3,000円〜', '拡大期から'],
        ['FBAツール（셀러스프라이트等）', '商品リサーチ補助', '月数千円〜', '任意'],
    ]
    h_s = ParagraphStyle('th_t', fontName='JP', fontSize=9, leading=14,
                          textColor=C_WHITE, alignment=TA_CENTER)
    c_s = ParagraphStyle('tc_t', fontName='JP', fontSize=9, leading=14, textColor=C_DARK)
    r_s = ParagraphStyle('tr_t', fontName='JP', fontSize=9, leading=14,
                          textColor=C_ACCENT, alignment=TA_CENTER)
    g_s = ParagraphStyle('tg_t', fontName='JP', fontSize=9, leading=14,
                          textColor=C_GREEN, alignment=TA_CENTER)
    fmt_t = []
    for i, row in enumerate(tool_rows):
        if i == 0:
            fmt_t.append([Paragraph(c, h_s) for c in row])
        else:
            pri_style = r_s if row[3] == '必須' else c_s
            fmt_t.append([
                Paragraph(row[0], c_s),
                Paragraph(row[1], c_s),
                Paragraph(row[2], g_s),
                Paragraph(row[3], pri_style),
            ])
    ts_t = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_BGLIGHT, C_WHITE]),
        ('GRID', (0,0), (-1,-1), 0.5, C_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
    ])
    t_t = Table(fmt_t, colWidths=[62*mm, 48*mm, 28*mm, 32*mm])
    t_t.setStyle(ts_t)
    story.append(t_t)
    story.append(Spacer(1, 3*mm))

    story += info_box(
        '初月コスト目安：Amazonセラー(4,900円) + Keepa(3,000円) = 約7,900円/月が固定費。'
        '仕入れ資金3〜5万円を別途確保。最初の2ヶ月で固定費回収を目標に設定する。',
        color=colors.HexColor('#FEF9E7'), border_color=C_GOLD)

    story.append(PageBreak())

    # ═══════════════════════════════════
    # CHAPTER 08: チェックリスト
    # ═══════════════════════════════════
    story += chapter_header('08  行動チェックリスト', color=C_GREEN)

    story += gold_quote(
        '"考え方を理解したら、完璧な準備より先に動く。\n小さな実験を繰り返すことが、最速で稼げるようになる道。"'
    )

    checklist_sections = [
        ('Week 1 チェックリスト（準備）', C_BLUE, [
            'Amazonセラーアカウントを開設した（大口出品）',
            'Keepaに登録し、基本的なグラフの見方を学んだ',
            'Amazonセラーアプリをスマートフォンにインストールした',
            '扱うジャンルを1つ決めた（ゲーム／本／おもちゃ等）',
            '仕入れ資金3〜5万円を確保した',
            '近所のリサイクルショップ・ゲオ等の場所を確認した',
        ]),
        ('Week 2-4 チェックリスト（初仕入れ）', C_GREEN, [
            '利益計算式を暗記した（売価-仕入-手数料-送料=利益）',
            '実際に店舗でバーコードスキャンを体験した',
            '最初の商品を1〜3点仕入れた',
            '出品ページを作成して出品した',
            '梱包・発送を完了した',
            '売上・仕入れ・利益をExcelに記録した',
        ]),
        ('Month 2-3 チェックリスト（改善）', C_GOLD, [
            '売れた商品と売れなかった商品の理由を分析した',
            '再現性のある「売れるパターン」を1つ発見した',
            '月利益1万円を達成した',
            '電脳せどり（ネット仕入れ）を試した',
            '仕入れ先を2ヶ所以上確保した',
            'Amazon規制カテゴリを確認した',
        ]),
        ('Month 4-6 チェックリスト（拡大）', C_ACCENT, [
            '月利益3〜5万円を達成した',
            '確定申告・経費管理の仕組みを作った',
            '外注・自動化の検討を始めた',
            'せどりの種類を1つ追加した（店舗→電脳 or 新品→中古）',
            '月利益8〜10万円（年収100万円ペース）を達成した',
        ]),
    ]

    for section_title, col, items in checklist_sections:
        story += section_box(section_title, color=col)
        for item in items:
            row_cl = [
                [Paragraph('□', ParagraphStyle('cb', fontName='JP', fontSize=14,
                                                leading=18, textColor=col, alignment=TA_CENTER)),
                 Paragraph(item, ParagraphStyle('ci', fontName='JP', fontSize=10,
                                                leading=16, textColor=C_DARK))]
            ]
            ts_cl = TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
                ('BOX', (0,0), (-1,-1), 0.5, C_GRAY),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (0,0), 6),
                ('LEFTPADDING', (1,0), (1,0), 8),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ])
            t_cl = Table(row_cl, colWidths=[12*mm, 158*mm])
            t_cl.setStyle(ts_cl)
            story.append(t_cl)
            story.append(Spacer(1, 1.5*mm))
        story.append(Spacer(1, 3*mm))

    # 最後のメッセージ
    story.append(Spacer(1, 4*mm))
    story += gold_quote(
        '"稼げる人と稼げない人の違いはたった1つ。\n相手への価値提供を考え続け、行動し続けたかどうか。\n今日から始めた人が、6ヶ月後に稼げるようになっている。"'
    )

    data_end = [[Paragraph(
        '本マニュアルは両学長リベラルアーツ大学 第52回・第86回動画を基に作成。\n'
        '動画URL: https://youtu.be/Sb30bWtUPmI  /  https://www.youtube.com/watch?v=_M1cv_JFqnM',
        ParagraphStyle('footer_note', fontName='JP', fontSize=8, leading=13,
                        textColor=C_GRAY, alignment=TA_CENTER))]]
    ts_end = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ])
    t_end = Table(data_end, colWidths=[170*mm])
    t_end.setStyle(ts_end)
    story.append(t_end)

    return story

# ── メイン ───────────────────────────────────────────────

def main():
    output_path = '/Users/noriomaekawwa/Desktop/【クロード作業用】/コード用仮414/せどり副業完全行動マニュアル2026.pdf'

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=16*mm,
        title='せどり副業完全行動マニュアル2026',
        author='リベラルアーツ大学 両学長動画解説',
    )

    story = build_content()
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'PDF生成完了: {output_path}')

if __name__ == '__main__':
    main()
