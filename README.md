# ゲーム音のどうぐ箱

ゲーム開発者向けの、効果音・BGMの解説記事と無料計算ツールのサイトです。

- 公開URL：https://inaruna.github.io/game-sound-site/
- 公開方法：GitHub Pages（`main` ブランチの `/docs` フォルダ）

## 仕組み

`python3 build.py`（要 `pip install markdown`）を実行すると、原稿と設定から `docs/` にサイトが生成されます。`docs/` はビルドのたびに作り直されるため、直接編集しません。

| パス | 中身 |
| --- | --- |
| `config.json` | サイト名、URL、運営者名、連絡先、itch.ioのURL |
| `links.json` | アフィリエイトリンク（空の枠はページに表示されません） |
| `content/articles/*.md` | 記事の原稿。`draft: true` の記事は公開されません |
| `tools/game-audio-calc.html` | 無料の計算ツール |
| `EDITORIAL.md` | 編集体制と公開の基準 |
| `docs/` | 生成されたサイト（GitHub Pages が公開） |

## 記事の原稿で使える記号

- `[[tool]]` … 計算ツールへの誘導枠
- `[[itch]]` … 運営者の効果音素材への誘導枠（`itch_url` が空なら非表示）
- `[[aff:キー|商品名|説明]]` … アフィリエイト枠（`links.json` のキーが空なら非表示）

アフィリエイト枠や運営者の素材の枠があるページには、ページ冒頭に「【PR】」の表示が自動で入ります。
