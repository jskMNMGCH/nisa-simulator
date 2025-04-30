# つみたてシミュレーション

本リポジトリは、複数の投資信託（ファンド）に対してモンテカルロシミュレーションを行い、つみたて投資の将来資産推移やリスク指標を可視化するStreamlitアプリケーションです。

## 主な機能

- **モンテカルロシミュレーション**：指定した年数・回数で各ファンドの期待リターンとリスク（年率）をもとに乱数シミュレーションを実行
- **総合指標の表示**：シャープレシオ、最終資産の中央値、元本割れ確率などの統計値をダッシュボードで確認
- **資産推移グラフ**：シミュレーション結果の平均・中央値の資産推移をPlotlyで可視化
- **損益ヒストグラム**：一定年後の損益分布をヒストグラムで表示し、平均・中央値・最頻値を強調
- **ファンド設定のカスタマイズ**：初期投資額・月額積立額・期待リターン・リスクをサイドバーから動的に変更
- **相関行列の表示**：資産クラス間の相関係数をテーブルで確認

## デモ

- [ライブデモはこちら](https://nisa-simulator-jskmnmgch.streamlit.app/)

## 環境構築

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/tsumitate-simulation.git
cd tsumitate-simulation

# 必要なパッケージをインストール
pip install -r requirements.txt
```

> **Python バージョン**: 3.8 以上

> **主要依存ライブラリ**:
> - streamlit
> - pandas
> - numpy
> - plotly

## 使い方

```bash
# ローカルでアプリを起動
streamlit run app.py
```

1. サイドバーで「シミュレーション回数」や「運用年数」を設定
2. 各ファンドの「初期投資額」「月額積立額」「期待リターン」「リスク」を入力
3. 「🚀 シミュレーション実行」ボタンをクリック
4. 総合指標・資産推移・ヒストグラム・ファンド一覧のタブで結果を確認

## 設定ファイル

- `app.py`：Streamlit アプリ本体
- `requirements.txt`：必要ライブラリ一覧

## カスタマイズ

- デフォルトのファンド設定（期待リターン・リスク・相関行列）は `app.py` 中の `default_funds` および `correlation_matrix` に定義
- 新たなファンドを追加する場合は、`fund_order` と `default_funds` に追記し、相関行列に行列要素を追加してください

## 貢献

1. Fork リポジトリ
2. ブランチを切る (`git checkout -b feature/your-feature`)
3. 変更をコミット (`git commit -m "Add some feature"`)
4. プッシュ (`git push origin feature/your-feature`)
5. Pull Request を作成

## ライセンス

MIT License

---

*作成者: Josuke MINAMIGUCHI*


