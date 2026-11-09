---
title: Unity AudioMixerの使い方｜BGM・効果音の音量設定とポーズ時の切り替え
description: UnityのAudioMixerでBGM・効果音・ボイスの音量を分けて管理する方法を、グループの作り方、Exposeしたパラメーターの変更、Snapshotでのポーズ演出、ダッキングの順に解説します。C#のコードと、よくあるトラブルの対処付き。
slug: unity-audiomixer
order: 6
published: 2026-11-09
updated: 2026-11-09
---

AudioMixerを使うと、BGM・効果音・ボイスなどの音量を、種類ごとにまとめて調整できます。オプション画面の音量設定や、ポーズ中にBGMをこもらせる演出も、AudioMixerがあれば簡単に作れます。

※Unity 6（6000.0系）の公式ドキュメントで確認した内容です。

## 1. AudioMixerを作る

1. メニューの Window → Audio → Audio Mixer で、Audio Mixerウィンドウを開きます。
2. 左側の Mixers パネルの「＋」で、新しいAudioMixerを作ります。
3. 最初から「Master」グループがあります。

## 2. グループを分ける

Groupsの「＋」を押して、Masterの下に次のグループを作ります。

```
Master
├─ BGM
├─ SE
└─ Voice
```

各AudioSourceの「Output」に、対応するグループを設定します。これで、BGMを鳴らすAudioSourceはすべてBGMグループの音量に従うようになります。

## 3. 音量をスクリプトから変えられるようにする

1. BGMグループを選び、InspectorのVolumeを右クリックします。
2. 「Expose 'Volume (of BGM)' to script」を選びます。
3. Audio Mixerウィンドウ右上の「Exposed Parameters」を開き、名前を「BGMVolume」に変えます。

スクリプトからは `SetFloat` で変更します。値はdB単位です。

```csharp
mixer.SetFloat("BGMVolume", -10f);
```

スライダーの0〜1をdBに変換する方法は、[Unityの音量をdBに変換する方法](../unity-volume-db/)で詳しく説明しています。

## 4. Snapshotでポーズ中の音を切り替える

Snapshotは、ミキサー全体の状態を保存しておく機能です。

1. 最初からあるSnapshot（名前は「Snapshot」）を「Normal」に改名します。
2. Snapshotsの「＋」で「Paused」を作ります。
3. BGMグループに「Lowpass」エフェクトを追加します。エフェクトはすべてのSnapshotに共通で、Snapshotごとに持つのは値だけです。
4. Normalを選び、Cutoffを22000Hz（音がこもらない値）にします。
5. Pausedを選び、Cutoffを下げます（例：800Hz）。
6. スクリプトから切り替えます。

```csharp
// クラスの中に書く断片です（ファイルの先頭に using UnityEngine.Audio; が必要）
[SerializeField] AudioMixerSnapshot normal;
[SerializeField] AudioMixerSnapshot paused;

public void Pause()  { paused.TransitionTo(0.3f); }
public void Resume() { normal.TransitionTo(0.3f); }
```

`TransitionTo` の引数は切り替えにかける秒数です。`Time.timeScale = 0` でポーズする場合は、AudioMixerの Update Mode を Unscaled Time にしておく必要があります。スクリプトからは `mixer.updateMode = AudioMixerUpdateMode.UnscaledTime;` で設定できます。

**注意：** Exposeしたパラメーターは、一度 SetFloat で値を設定すると、Snapshotを切り替えても変わらなくなります（ClearFloat で元に戻せます）。オプションの音量は SetFloat で、演出用の変化はSnapshotで、と役割を分けると混乱しません。

## 5. ダッキングでボイス中にBGMを下げる

キャラクターのボイスが鳴っている間だけBGMを下げたいときは、ダッキングを使います。

1. Voiceグループに「Send」エフェクトを追加します。
2. BGMグループに「Duck Volume」エフェクトを追加します。
3. VoiceのSendの送り先にBGMのDuck Volumeを選び、Send Levelを0dBにします。
4. Duck Volume の Threshold と Ratio で下げ幅を、Attack Time と Release Time で下げる・戻す速さを調整します。

## よくあるトラブル

**音量が反映されない。** AudioSourceのOutputにグループが設定されているか確認します。Noneのままだとミキサーを通りません。

**起動直後に音量が戻る。** [Unityの音量をdBに変換する方法](../unity-volume-db/)の「よくある失敗」を参照してください。

**効果音が重なって大きくなりすぎる。** SEグループに「Compressor」エフェクトを入れて急な音量の跳ね上がりを抑える、同じ音の同時再生数を制限する、といった対策があります。

[[itch]]
