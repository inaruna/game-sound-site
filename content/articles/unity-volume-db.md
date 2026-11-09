---
title: Unityの音量をdBに変換する方法｜スライダーとAudioMixerをつなぐ
description: UnityのAudioSource.volume（0〜1）とAudioMixerのdBの関係を、変換式と早見表で解説します。スライダー値をdBに変換するC#コード、PlayerPrefsでの保存と復元、ありがちな失敗もまとめました。無料の変換ツール付き。
slug: unity-volume-db
order: 1
published: 2026-11-09
updated: 2026-11-09
---

Unityで音量設定画面を作るとき、スライダーの値（0〜1）をそのままAudioMixerに渡すと、ほとんど音量が変わらなかったり、急に無音になったりします。原因は、**AudioMixerの音量がdB（デシベル）単位**だからです。

この記事では、0〜1の値とdBの関係、変換のコード、つまずきやすい点を順に説明します。

※Unity 6（6000.0系）の公式ドキュメントで確認した内容です。

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

**スライダーの値をそのまま渡している。** 0〜1をそのままdBとして渡すと、0〜+1dBの範囲しか動かないため、ほぼ変化を感じません。

**-80〜0のdBをスライダーで直接動かしている。** -80〜-40dB付近はほとんど聞こえないため、スライダーの左半分を動かしても音がほぼ変わりません。0〜1のスライダーを上の式で変換すると、よく使う-20〜0dBの範囲にスライダーの9割が割り当てられ、操作しやすくなります。

**Awakeで設定を復元している。** AudioMixer.SetFloat は、Awake や OnEnable で呼ぶと反映されないことがあります。保存した音量の復元は Start で行いましょう。

**ExposeしたパラメーターをSnapshotでも動かそうとしている。** Exposeしたパラメーターは、一度 SetFloat で値を設定すると、Snapshotを切り替えても変わらなくなります（ClearFloat で元に戻せます）。Snapshotで音量を変えたいなら、そのパラメーターは SetFloat で操作しないほうが扱いやすくなります。

## 音量の保存と復元

PlayerPrefsにはdBではなく、スライダーの値（0〜1）を保存しておくと、UIの復元とdB変換を同じ処理で済ませられます。上の `VolumeSlider` を、保存と復元まで含めて書き直すと次のようになります。

```csharp
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.UI;

public class VolumeSlider : MonoBehaviour
{
    [SerializeField] AudioMixer mixer;
    [SerializeField] Slider slider;
    [SerializeField] string parameter = "BGMVolume";

    void Start()
    {
        float saved = PlayerPrefs.GetFloat(parameter, 0.8f);
        // 値が同じだと OnValueChanged は呼ばれないため、明示的に適用する
        slider.SetValueWithoutNotify(saved);
        SetVolume(saved);
    }

    // UI Slider の OnValueChanged に登録する
    public void SetVolume(float value)
    {
        mixer.SetFloat(parameter, Mathf.Log10(Mathf.Max(value, 0.0001f)) * 20f);
        PlayerPrefs.SetFloat(parameter, value);
    }
}
```

## まとめ

AudioMixerはdB、スライダーはリニアです。間に `20 × log10` をはさむだけで、自然な音量スライダーになります。具体的な値を確かめたいときは、上の変換ツールを使ってください。

[[itch]]
