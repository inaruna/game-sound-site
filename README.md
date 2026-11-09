# ゲーム音のどうぐ箱 — 公開までの手順

`docs` フォルダの中身が、そのまま公開できるサイトです（記事10本、無料ツール、トップ、運営者情報、プライバシーポリシー、sitemap.xml、robots.txt）。

アフィリエイトリンクが空の枠は自動で非表示になるので、**今の状態でも公開できます**。Amazonアソシエイトの審査には公開済みのサイトが必要なので、先に公開してから申し込む流れになります。

## あなたがやること（最後の一手）

1. **運営者情報を記入する**
   `config.json` の `operator_name`（ハンドルネーム可）、`contact`（メールアドレスやフォームURL）、`itch_url`（効果音ページ）を埋めます。
2. **サイトを公開する**（どちらか）
   - Netlify Drop：`dist` フォルダをブラウザにドラッグするだけで公開されます。
   - GitHub Pages：リポジトリを作り、`dist` の中身をアップロードして Pages を有効にします。
3. **公開URLを記入する**
   `config.json` の `site_url` を公開URLに書き換えます。
4. **再ビルドしてアップロードし直す**
   `python3 build.py` を実行し、新しい `dist` をアップロードします。Pythonを使わない場合は、記入した内容をClaudeに伝えれば再ビルドします。
5. **Google Search Console に登録し、sitemap.xml を送信する**
6. **アフィリエイトに申し込む**
   - Amazonアソシエイト
   - Unity Affiliate Program（Partnerize経由）
7. **発行されたリンクを `links.json` に貼り、手順4をもう一度行う**
   どのキーがどの商品かは、`links.json` のキー名で判別できます（例：`AMAZON_HP_M50X` は ATH-M50x）。Amazonのリンクが1つでも入ると、フッターにAmazonアソシエイトの表記が自動で入ります。

## フォルダ構成

| パス | 中身 |
| --- | --- |
| `config.json` | サイト名、URL、運営者情報、itchのURL |
| `links.json` | アフィリエイトリンク |
| `content/articles/*.md` | 記事（Markdown） |
| `tools/game-audio-calc.html` | 無料ツール |
| `build.py` | サイトを生成するスクリプト（要 `pip install markdown`） |
| `docs/` | 生成されたサイト（これを公開する） |

## 記事の書き方メモ

記事中で使える置き換え記号です。

- `[[tool]]` … 無料ツールへの誘導枠
- `[[itch]]` … 自作の効果音パックへの誘導枠（`itch_url` が空なら非表示）
- `[[aff:キー|商品名|説明]]` … アフィリエイト枠（`links.json` のキーが空なら非表示）
