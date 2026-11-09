---
title: Unity AudioMixerの使い方｜BGM・SE別の音量設定とポーズ時の切り替え
description: UnityのAudioMixerでBGMと効果音の音量を分けて管理する方法を、グループの作り方、パラメーターの公開、Snapshot、ダッキングの順に解説します。
slug: unity-audiomixer
order: 6
---

AudioMixerを使うと、BGM・効果音・ボイスなどの音量を、種類ごとにまとめて調整できます。オプション画面の音量設定や、ポーズ中にBGMをこもらせる演出も、AudioMixerがあれば簡単に作れます。

## 1. AudioMixerを作る

1. Projectウィンドウで右クリックし、Create → Audio Mixer を選びます。
2. ダブルクリックでAudio Mixerウィンドウを開きます。
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

1. Snapshotsの「＋」で「Paused」を作ります。
2. Pausedを選んだ状態で、BGMグループに「Lowpass」エフェクトを追加し、Cutoffを下げます。
3. スクリプトから切り替えます。

```csharp
[SerializeField] AudioMixerSnapshot normal;
[SerializeField] AudioMixerSnapshot paused;

public void Pause()  { paused.TransitionTo(0.3f); }
public void Resume() { normal.TransitionTo(0.3f); }
```

`TransitionTo` の引数は切り替えにかける秒数です。`Time.timeScale = 0` でポーズする場合は、AudioMixerのInspectorで Update Mode を「Unscaled Time」にしておかないと、切り替えが進みません。

**注意：** スクリプトに公開したパラメーターは、Snapshotでは変わらなくなります。オプションの音量はExposeして SetFloat で、演出用の変化はSnapshotで、と役割を分けると混乱しません。

## 5. ダッキングでボイス中にBGMを下げる

キャラクターのボイスが鳴っている間だけBGMを下げたいときは、ダッキングを使います。

1. Voiceグループに「Send」エフェクトを追加します。
2. BGMグループに「Duck Volume」エフェクトを追加します。
3. VoiceのSendの送り先にBGMのDuck Volumeを選び、Send Levelを0dBにします。
4. Duck VolumeのThresholdやRatioで、下げ幅と反応の速さを調整します。

## よくあるトラブル

**音量が反映されない。** AudioSourceのOutputにグループが設定されているか確認します。Noneのままだとミキサーを通りません。

**起動直後に音量が戻る。** 保存した音量の復元を Awake で行うと反映されないことがあります。Start で行いましょう。

**効果音が重なって大きくなりすぎる。** SEグループに「Compressor」エフェクトを入れて急な音量の跳ね上がりを抑える、同じ音の同時再生数を制限する、といった対策があります。

[[aff:UNITY_AUDIO|オーディオ管理アセット|再生数の制限やカテゴリ別の音量管理を、標準機能より手軽に組めます。]]

[[itch]]
