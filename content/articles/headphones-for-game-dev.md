---
title: ゲーム制作向けヘッドホンの選び方｜効果音・BGMの確認に使うモニターヘッドホン
description: ゲームの効果音やBGMを確認するためのヘッドホンの選び方を、メーカー公式の解説と仕様の比較表で整理します。Godot 4のAudioStreamPlayer3Dで左右の位置と距離の聞こえ方を確かめる手順も紹介します。
slug: headphones-for-game-dev
order: 9
published: 2026-11-09
updated: 2026-11-09
draft: true
---

効果音やBGMの音量をヘッドホンで決めるとき、ヘッドホン自体の音の傾向が判断に影響することがあります。[オーディオテクニカのモニターヘッドホンの解説](https://www.audio-technica.co.jp/headphone/navi/whatis/07.php)では、低音が強調されたリスニング用ヘッドホンで制作すると、低音を下げすぎてしまう例が挙げられています。

この記事では、メーカー公式の解説と仕様をもとに、ヘッドホンを選ぶときに見る点を整理します。後半では、Godot 4 で効果音の左右と距離の聞こえ方を確かめる手順を紹介します。

## 選ぶときの4つのポイント

### 1. 音の傾向がフラットかどうか

上の[モニターヘッドホンの解説](https://www.audio-technica.co.jp/headphone/navi/whatis/07.php)では、低音の例が次のように書かれています。

> 低音などが強調された音質のリスニング用ヘッドホンで楽曲制作を行うと、必要以上に低音が強調されて聴こえるため、楽曲の低音の音量を下げてしまい、結果狙った通りのバランスで楽曲制作ができなくなってしまいます。

同じページでは、モニターヘッドホンには特定の帯域を強調せず、低音域から高音域までフラットな傾向の音質が求められると説明されています。

また、オーディオテクニカの[モニターヘッドホンとリスニングヘッドホンの違いを説明した記事](https://www.audio-technica.co.jp/always-listening/articles/headphone-basics/)によると、モニターヘッドホンは主に録音や放送の現場で、音声信号をできるだけ正確に再現する目的で使われます。リスニングヘッドホンは音楽を心地よく楽しむことを重視していて、音質の傾向はメーカーやブランドによってさまざまです。

効果音の低音の量を決めるときは、こうした傾向の違いを知ったうえでヘッドホンを選ぶとよいでしょう。

### 2. 密閉型か開放型か

オーディオテクニカの解説ページ（出典は表の下）をもとに要約しました。両方の型について記述がある項目だけを載せています。

| | 密閉型 | 開放型 |
| --- | --- | --- |
| 音漏れ | しにくい（外の音も入りにくい） | しやすい |
| 使う場所 | 遮音性が高く、屋外でも使える | 基本は室内向け |
| 用途の例 | 細かい音を聞き取る用途 | 大きな音を出せない環境で、スピーカーでの出音を確かめたいとき |

出典：音漏れの密閉型は[ヘッドホンの基本を説明した記事](https://www.audio-technica.co.jp/always-listening/articles/headphone-basics/)、開放型は[開放型ヘッドホンの記事](https://www.audio-technica.co.jp/always-listening/articles/open-headphone/)。使う場所は[密閉型と開放型の解説](https://www.audio-technica.co.jp/headphone/navi/whatis/02-03.php)。用途の例は[モニターヘッドホンの解説](https://www.audio-technica.co.jp/headphone/navi/whatis/07.php)。

[密閉型と開放型の解説](https://www.audio-technica.co.jp/headphone/navi/whatis/02-03.php)によると、開放型は広い音場が特徴で、密閉型はモニターヘッドホンとして使われることも多いとされています。

周りに人がいる場所で作業するなら、開放型は音漏れしやすいことも考えに入れておきましょう。

### 3. 重さは測定条件をそろえて比べる

メーカーが公表する重さには、ケーブルを含まない値があります。下の比較表の2機種は、どちらもケーブルを除いた値です。別の機種と比べるときは、ケーブルを含むかどうかを公式の仕様で確かめてから比べましょう。

### 4. ケーブルが着脱できるか

[モニターヘッドホンの解説](https://www.audio-technica.co.jp/headphone/navi/whatis/07.php)によると、使い勝手やメンテナンス性を考えて、コードを着脱できるモデルや、伸び縮みするカールコードのモデルもあります。コードは長いものが多く、3.0m程度が一般的とされています。机とPCの距離など、自分の作業環境に合うコードかどうかも見ておきましょう。

## モニターヘッドホン2機種の公式仕様

メーカー公式の製品ページで確認した仕様です。公式ページで記述を確認できなかった項目は「公式ページに記載なし」としています。仕様は変わることがあるので、購入前に公式で最新を確認してください。

| 項目 | SONY MDR-CD900ST | audio-technica ATH-M50x |
| --- | --- | --- |
| 型式 | 密閉ダイナミック型 | 密閉ダイナミック型 |
| 重さ | 約200g（コード含まず） | 285g（コード除く） |
| インピーダンス | 63Ω | 38Ω |
| ケーブル着脱 | 公式ページに記載なし | 着脱式（バヨネット式ロック機構） |
| 付属コード | 2.5m（ステレオ標準プラグ） | カールコード1.2m（伸ばすと約3m）、ストレートコード3.0m、ストレートコード1.2m（φ6.3mm標準／φ3.5mmミニの2ウェイプラグ） |
| 折りたたみ | 公式ページに記載なし | 可 |
| 発売 | 1989年（消費者向けは1990年から） | 2014年2月14日 |
| 公式ページの掲載（2026年11月11日時点） | 製品ページに掲載 | シリーズページのラインナップに掲載 |

### SONY MDR-CD900ST

メーカーは「数多くのレコーディングスタジオで愛用されている音楽業界のハイスタンダード」と紹介しています。製品ページによると、もともとはCBSソニー信濃町スタジオ（現：ソニー・ミュージックスタジオ）で使うために開発されたモデルです。

製品ページでは、業務用のプロフェッショナル仕様のため無償修理期間はなく、修理はすべて有償とされています。修理の条件は変わることがあるので、公式で最新を確認してください。

[[aff:AMAZON_HP_CD900ST|SONY MDR-CD900ST|密閉ダイナミック型、63Ω（メーカー公式仕様）。]]

### audio-technica ATH-M50x

メーカーは「スタジオレコーディングやミキシングに最適」と紹介しています。ATH-M50 をリニューアルしたモデルです。ケーブルは着脱式で、折りたたみ機構でコンパクトになると説明されています。

[[aff:AMAZON_HP_M50X|audio-technica ATH-M50x|密閉ダイナミック型、着脱コード、折りたたみ機構（メーカー公式仕様）。]]

## ゲーム制作ならではの確認手順

ゲームでは、音源と聞き手の位置関係で効果音の聞こえ方を変えられます。Godot の公式ドキュメントによると、AudioStreamPlayer3D は聞き手（audio listener）との位置関係にもとづいて音を鳴らし、距離による減衰、方向、ドップラー効果がかかります。左右の位置と距離による音の変化を、ヘッドホンで確かめてみましょう。

※Godot 4 の公式ドキュメント（stable 版）で確認した内容です。ページに細かい版番号の表示はないため、お使いのバージョンのドキュメントもあわせて確認してください。

### 使うプロパティ

| プロパティ | 公式ドキュメントの説明（要約） | 既定値 |
| --- | --- | --- |
| attenuation_model | 距離に応じて音を小さくする方法を決める。減衰なしも選べる | Inverse |
| max_distance | この距離を超えると、音がまったく聞こえなくなる。0.0 より大きい値のときだけ効く | 0.0（無効） |
| unit_size | 減衰の効き方の係数。大きくするほど、遠くまで聞こえる | 10.0 |
| panning_strength | プロジェクト設定の audio/general/3d_panning_strength に掛ける倍率。掛けた結果が 0.0 だとステレオのパンが無効になる | 1.0 |

attenuation_model の選択肢は、インスペクターでは次の名前で表示されます。

| インスペクターの表示 | 公式の説明での小さくなり方 | スクリプトで使う定数 |
| --- | --- | --- |
| Inverse | 直線的 | ATTENUATION_INVERSE_DISTANCE |
| Inverse Square | 二次的 | ATTENUATION_INVERSE_SQUARE_DISTANCE |
| Logarithmic | 対数的 | ATTENUATION_LOGARITHMIC |
| Disabled | 距離の影響を受けない | ATTENUATION_DISABLED |

### 手順

1. 3Dシーンに AudioStreamPlayer3D を置き、確認したい効果音を Stream に設定します。公式ドキュメントによると、音は既定でカメラの位置で聞こえます（AudioListener3D で変更できます）。シーンには、現在のカメラになっている Camera3D か、AudioListener3D を置いておきます。
2. ヘッドホンをつけて、音源を聞き手の左右に動かしながら鳴らします。左にあるときに左から聞こえるかを確かめます。
3. panning_strength を 0.0 にして、もう一度鳴らします。左右の変化がなくなることを確かめたら、値を戻して聞き比べます。
4. attenuation_model を切り替えて、音源から離れたときの小さくなり方を聞き比べます。公式ドキュメントによると、距離に応じてローパスフィルターもかかります（attenuation_filter_cutoff_hz、既定値 5000 Hz）。離れると音量だけでなく音色も変わるので、そのつもりで聞きましょう。
5. unit_size を変えて、どのくらい離れるまで聞こえるかを確かめます。
6. max_distance を 0 より大きい値（例：30）にします。既定値の 0.0 のままでは、聞こえなくなる境目がありません。境目をまたぐように音源を動かし、聞こえなくなる位置を確かめます。音が途切れる位置がゲームの場面に合っているかも聞いておきましょう。

インスペクターで値を変える代わりに、スクリプトで比べたい値を入れておく方法もあります。

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # 既定値は unit_size 10.0、max_distance 0.0、panning_strength 1.0
    # 比べたい値に書き換えて、ヘッドホンで聞き比べる
    attenuation_model = AudioStreamPlayer3D.ATTENUATION_LOGARITHMIC
    unit_size = 5.0
    max_distance = 30.0
    panning_strength = 0.5
```

数値は聞き比べのための例です。ゲームの縮尺に合わせて変えてください。

2Dのゲームでも、AudioStreamPlayer2D は聞き手との距離に応じて音が小さくなると、公式ドキュメントで説明されています。2Dでも、音源を動かしながらヘッドホンで聞いてみましょう。

### ヘッドホン以外でも鳴らしてみる

ヘッドホンで確かめたあとは、スマートフォンの実機やノートPCのスピーカー、イヤホンなど、手元にあるほかの機器でもゲームを動かして聞いてみることをおすすめします。効果音がBGMに埋もれていないか、聞こえ方が大きく変わらないかを確かめておくと安心です。

Godot で効果音を鳴らす基本は[Godot 4で効果音を鳴らす方法](../godot-sound/)で説明しています。

## まとめ

メーカーの解説では、モニターヘッドホンにはフラットな傾向の音質が求められるとされています。選ぶときは、密閉型か開放型か、重さの測定条件、ケーブルの着脱を公式の仕様で比べましょう。ゲームに組み込んだら、Godot の AudioStreamPlayer3D で左右と距離の聞こえ方をヘッドホンで確かめ、最後にほかの機器でも鳴らしてみてください。

[[itch]]

## 参考（確認日 2026-11-11）

- ソニー MDR-CD900ST 製品ページ：<https://www.sony.jp/headphone/products/MDR-CD900ST/>
- オーディオテクニカ ATH-M50x 製品ページ：<https://www.audio-technica.co.jp/product/ATH-M50x>
- オーディオテクニカ モニターヘッドホン シリーズページ：<https://www.audio-technica.co.jp/series/monitor-headphones/>
- オーディオテクニカ 密閉型と開放型の解説：<https://www.audio-technica.co.jp/headphone/navi/whatis/02-03.php>
- オーディオテクニカ モニターヘッドホンの解説：<https://www.audio-technica.co.jp/headphone/navi/whatis/07.php>
- オーディオテクニカ ヘッドホンの基本を説明した記事：<https://www.audio-technica.co.jp/always-listening/articles/headphone-basics/>
- オーディオテクニカ 開放型ヘッドホンの記事：<https://www.audio-technica.co.jp/always-listening/articles/open-headphone/>
- Godot Engine ドキュメント AudioStreamPlayer3D（stable）：<https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html>
- Godot Engine ドキュメント AudioStreamPlayer2D（stable）：<https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html>
