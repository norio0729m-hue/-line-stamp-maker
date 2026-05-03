# INUGOYA — Design System

## ブランドコンセプト

**ブランド名案**: `INUGOYA` / `Maison du Chien` / `THE DOG HOUSE`

> 都会の喧騒から離れ、洗練された空間で犬たちと過ごす——  
> 贅沢な静寂と温もりが交差する、大人のための隠れ家カフェ。

**キーワード**: Sophisticated / Serene / Warm Luxury / Timeless / Organic

---

## カラーパレット

### Primary

| 名前 | HEX | 用途 |
|------|-----|------|
| Pure White | `#FAFAF8` | ベース背景（純白より少し温かみのあるオフホワイト）|
| Ivory | `#F2EFE9` | セクション区切り・カード背景 |
| Warm Cream | `#EDE8DF` | アクセント背景・ホバー |

### Secondary（メインカラー）

| 名前 | HEX | 用途 |
|------|-----|------|
| Truffle | `#2C2420` | 見出し・メインテキスト（ほぼ黒・茶みがかる）|
| Espresso | `#4A3728` | サブ見出し・アイコン |
| Caramel | `#8B6248` | アクセント・リンク・ボーダー |

### Accent

| 名前 | HEX | 用途 |
|------|-----|------|
| Sage | `#8A9E8C` | ポイントカラー（自然・穏やかさ）|
| Sand Gold | `#C4A882` | ゴールドアクセント・CTA枠線 |
| Mist | `#D4CEBF` | 区切り線・サブテキスト |

### Functional

| 名前 | HEX | 用途 |
|------|-----|------|
| Text Primary | `#1E1A17` | 本文テキスト |
| Text Secondary | `#7A6E66` | キャプション・補足テキスト |
| Divider | `#E0DAD2` | 区切り線 |

---

## タイポグラフィ

### 日本語
- **見出し**: `Noto Serif JP` / `游明朝` — 明朝体で格調高く
- **本文**: `Noto Sans JP` — ウェイト 300〜400 / 読みやすい細め

### 欧文
- **見出し・ロゴ**: `Cormorant Garamond` — セリフ体、エレガント
- **サブ・ラベル**: `Montserrat` / `Jost` — ウェイト 300〜400 / スリムなサンセリフ
- **装飾テキスト**: `Playfair Display Italic` — 斜体でアクセント

### サイズスケール（rem）

```
Display:  4.0rem / line-height 1.1
H1:       2.8rem / line-height 1.2
H2:       2.0rem / line-height 1.3
H3:       1.4rem / line-height 1.4
Body:     1.0rem / line-height 1.8
Small:    0.85rem / line-height 1.6
Caption:  0.75rem / letter-spacing 0.12em
```

---

## スペーシング

8pxグリッドベース。セクション間は余白を大きめにとり「呼吸感」を演出。

```
xs:  8px
sm:  16px
md:  24px
lg:  48px
xl:  80px
2xl: 120px
3xl: 160px
```

---

## デザイン原則

### 1. White Space First
余白を贅沢に使う。詰め込まず「引き算のデザイン」。

### 2. Texture Over Flat
完全なフラットではなく、微細なテクスチャや紙のような質感を取り入れる。

### 3. Photography Driven
犬と空間の写真を大きく使い、テキストは添える程度に。

### 4. Organic Lines
直線的すぎず、わずかな曲線・有機的な形状（犬の柔らかさを反映）。

### 5. Restrained Animation
動きは最小限。フェードイン・スローなパララックスのみ。高速なアニメは使わない。

---

## UIコンポーネント方針

### ボタン
- Primary: `Sand Gold` ボーダー + `Truffle` テキスト、背景透明（アウトラインボタン）
- Filled: `Truffle` 背景 + `Pure White` テキスト、角丸なし（シャープ）
- フォントは大文字 `letter-spacing: 0.15em`

### カード
- 背景 `Ivory` / シャドウなし / 細い `Caramel` ボーダー or ボーダーレス
- hover時に微細な背景色変化のみ

### ナビゲーション
- 背景透明（スクロール後に `Pure White` + 薄いボーダー）
- ロゴは欧文セリフ体
- リンクは小文字・細め `letter-spacing: 0.1em`

### 区切り
- `<hr>` ではなく細線 `1px solid #E0DAD2` か装飾的な縦線

---

## サイト構成（予定）

1. **Hero** — フルスクリーン写真 + キャッチコピー + 予約CTA
2. **Concept** — ブランドストーリー（テキスト + 写真）
3. **Dogs** — 在籍犬の紹介（グリッドギャラリー）
4. **Menu** — カフェメニュー（エレガントなリスト形式）
5. **Space** — 店内写真ギャラリー
6. **Access** — 住所・地図・営業時間
7. **Reservation** — 予約フォーム or 外部リンク
8. **Footer** — SNS・著作権

---

## ムードボード イメージ参照

参考スタイル:
- 高級ホテルのウェルカムページ
- ジャパニーズミニマリズム + ヨーロピアンラグジュアリー
- Aesop / Maison Margiela のウェブデザイン感
