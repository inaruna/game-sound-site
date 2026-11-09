---
title: Unityの音量をdBに変換する方法｜スライダーとAudioMixerを正しくつなぐ
description: UnityのAudioSource.volume（0〜1）とAudioMixerのdBの関係、スライダー値をdBに変換するコード、ありがちな失敗をまとめました。変換ツール付き。
slug: unity-volume-db
order: 1
---

Unityで音量設定画面を作るとき、スライダーの値（0〜1）をそのままAudioMixerに渡すと、ほとんど音量が変わらなかったり、急に無音になったりします。原因は、**AudioMixerの音量がdB（デシベル）単位**だからです。

この記事では、0〜1の値とdBの関係、変換のコード、つまずきやすい点を順に説明します。

[[tool]]

## AudioSourceとAudioMixerで単位が違う

Unityの音量には2つの単位が混在しています。

| 場所 | 単位 | 範囲 |
| --- | --- | --- |
| AudioSource.volume | リニア（倍率） | 0〜1 |
| AudioMixer の Volume | dB | -80〜+20 |

リニアの1.0とdBの0は、どちらも「元の音量のまま」を意味します。違うのはその下の目盛りです。dBは対数なので、リニアで半分（0.5）にするとdBでは約-6になります。

## 変換の式

リニアからdBへの変換は次の式です。

```
dB = 20 × log10(リニア値)
```

逆に、dBからリニアに戻すときはこうなります。

```
リニア値 = 10 ^ (dB ÷ 20)
```

よく使う値を早見表にしました。

| リニア | dB |
| --- | --- |
| 1.0 | 0 |
| 0.7 | 約 -3.1 |
| 0.5 | 約 -6.0 |
| 0.3 | 約 -10.5 |
| 0.1 | -20 |
| 0.01 | -40 |

## スライダーをAudioMixerにつなぐコード

まずAudioMixerで音量パラメーターを外部に公開します。Mixerウィンドウでグループを選び、InspectorのVolumeを右クリックして「Expose」を選びます。Exposed Parametersの一覧で名前を「BGMVolume」などに変えておきます。

そのうえで、スライダーの値を変換して渡します。

```csharp
using UnityEngine;
using UnityEngine.Audio;

public class VolumeSlider : MonoBehaviour
{
    [SerializeField] AudioMixer mixer;
    [SerializeField] string parameter = "BGMVolume";

    // UI Slider の OnValueChanged に登録する
    public void SetVolume(float value)
    {
        float dB = Mathf.Log10(Mathf.Max(value, 0.0001f)) * 20f;
        mixer.SetFloat(parameter, dB);
    }
}
```

`Mathf.Max(value, 0.0001f)` は、log10(0) がマイナス無限大になるのを防ぐためのものです。0.0001はちょうど-80dBにあたり、AudioMixerの最小値と一致します。

## よくある失敗

**スライダーの値をそのまま渡している。** 0〜1をdBとして渡すと、0dB付近の1dBしか動かないので、ほぼ変化を感じません。

**-80〜0をスライダーで直接動かしている。** 数値上は正しくても、体感では右半分でしか音量が変わりません。人の耳は対数的に聞こえるので、リニアのスライダーを上の式で変換するほうが自然な手触りになります。

**Awakeで設定を復元している。** AudioMixer.SetFloat は Awake の時点では反映されないことがあります。保存した音量の復元は Start で行うと確実です。

**Snapshotの切り替えで上書きされる。** Exposeしたパラメーターは、Snapshotの値より SetFloat の値が優先されます。逆に、Snapshotで音量を変えたいなら、そのパラメーターはExposeしないほうが扱いやすくなります。

## 音量の保存と復元

PlayerPrefsにはdBではなく、スライダーの値（0〜1）を保存しておくと、UIの復元とdB変換を同じ処理で済ませられます。

```csharp
void Start()
{
    float saved = PlayerPrefs.GetFloat(parameter, 0.8f);
    slider.value = saved;   // OnValueChanged 経由で SetVolume が呼ばれる
}

public void SetVolume(float value)
{
    mixer.SetFloat(parameter, Mathf.Log10(Mathf.Max(value, 0.0001f)) * 20f);
    PlayerPrefs.SetFloat(parameter, value);
}
```

## まとめ

AudioMixerはdB、スライダーはリニアです。間に `20 × log10` をはさむだけで、自然な音量スライダーになります。具体的な値を確かめたいときは、上の変換ツールを使ってください。

[[aff:UNITY_AUDIO|オーディオ管理アセット|SEやBGMの再生管理、音量設定画面づくりをまとめて楽にできます。]]

[[itch]]
