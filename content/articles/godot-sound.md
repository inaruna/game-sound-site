---
title: Godot 4で効果音を鳴らす方法｜AudioStreamPlayerとバスの基本
description: Godot 4で効果音やBGMを鳴らす方法を、GDScriptのコード付きで解説します。AudioStreamPlayer・2D・3Dの使い分け、Max Polyphonyでの同時再生、ピッチのランダム化、バスでの音量管理、鳴らない・遅れるときの対処まで。
slug: godot-sound
order: 8
published: 2026-11-09
updated: 2026-11-09
---

Godot 4では、音を鳴らすのに「AudioStreamPlayer」系のノードを使います。基本は、ノードに音声ファイルを設定して `play()` を呼ぶだけです。

この記事では、3種類のプレイヤーの使い分け、効果音を重ねて鳴らす方法、バスを使った音量管理を順に説明します。

※Godot 4.5の公式ドキュメントで確認した内容です。

## 3種類のAudioStreamPlayer

| ノード | 特徴 | 使う場面 |
| --- | --- | --- |
| AudioStreamPlayer | 位置に関係なく同じ音量で鳴る | BGM、UI音 |
| AudioStreamPlayer2D | 2D空間の位置で音量と左右が変わる | 2Dゲームの効果音 |
| AudioStreamPlayer3D | 3D空間の位置と距離で変わる | 3Dゲームの効果音 |

## 基本の鳴らし方

1. シーンに AudioStreamPlayer を追加します。
2. Inspectorの「Stream」に音声ファイルをドラッグします。
3. スクリプトから `play()` を呼びます。

```gdscript
@onready var se_jump: AudioStreamPlayer = $SeJump

func _physics_process(_delta: float) -> void:
    if Input.is_action_just_pressed("ui_accept"):
        se_jump.play()
```

`ui_accept` は最初から用意されている入力アクション（Enterキーやスペースキーなど）です。独自のアクション名を使う場合は、プロジェクト設定のインプットマップに追加してください。

BGMのように最初から流したい場合は、Inspectorの「Autoplay」をオンにします。

## 同じ効果音を重ねて鳴らす

1つのプレイヤーで `play()` を連続で呼ぶと、前の音が止まって最初から鳴り直します。連射音のように重ねたいときは、「Max Polyphony」を2以上にします。

```gdscript
se_shot.max_polyphony = 8
```

これで、同じプレイヤーから最大8つの音を同時に鳴らせます。

## 毎回少しだけ音を変える

同じ音が何度も鳴ると単調に聞こえます。再生のたびにピッチを少し変えると、自然になります。

```gdscript
func play_footstep():
    se_step.pitch_scale = randf_range(0.92, 1.08)
    se_step.play()
```

ピッチの代わりに、複数の音からランダムに選ぶ「AudioStreamRandomizer」を Stream に設定する方法もあります。

## バスで音量を分けて管理する

画面下部の「オーディオ」パネルで、バスを追加できます。Masterの下に「BGM」と「SE」を作り、各プレイヤーの「Bus」プロパティで振り分けます。

音量の変更は `AudioServer` から行います。バスの音量はdB単位なので、スライダーの0〜1は `linear_to_db()` で変換します。

```gdscript
func set_bus_volume(bus_name: String, value: float) -> void:
    var index := AudioServer.get_bus_index(bus_name)
    if index == -1:
        push_warning("Bus not found: %s" % bus_name)
        return
    AudioServer.set_bus_mute(index, value <= 0.001)
    AudioServer.set_bus_volume_db(index, linear_to_db(maxf(value, 0.0001)))
```

値が0のときは `linear_to_db()` がマイナス無限大を返すので、ミュートで処理し、変換する値にも下限を設けています。バス名が見つからないときは `get_bus_index()` が -1 を返すので、先に確認しています。

## よくあるトラブル

**音が鳴らない。** Streamが空になっている、Volume dB が -80 などの極端に小さい値になっている、のどちらかであることが多いです。

**音量スライダーが効かない。** プレイヤーのBusに指定した名前のバスが見つからないと、音はMasterから鳴ります。バス名を変えたときは、各プレイヤーのBusも確認しましょう。

**音が遅れる。** 効果音ファイルの先頭に無音がないか確認します。公式ドキュメントでも、先頭の無音は遅れの原因になるとされています。たくさん鳴らす効果音は、OGGより再生の負荷が軽いWAVにしておくと安定します。

**BGMのループがつながらない。** インポート設定でループを有効にします。ループ位置の計算は[BGMのループ長とループポイントの計算方法](../bgm-loop-calc/)で説明しています。

[[itch]]
