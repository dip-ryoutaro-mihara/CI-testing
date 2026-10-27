# CI-testing

CI（継続的インテグレーション）とテストを学ぶためのサンプルです。Python + pytest のコードとテストを、GitHub Actions で自動検証します。

## 構成

```
.
├── .github/workflows/ci.yml   # CI の定義
├── pyproject.toml             # パッケージ・pytest・カバレッジ・ruff の設定
├── requirements-dev.txt       # 開発用ツール（バージョン固定）
├── src/ci_sample/             # テスト対象のコード
│   ├── calculator.py          # 四則演算
│   ├── grading.py             # 点数 → 評価
│   ├── cart.py                # 買い物かご
│   └── weather.py             # 外部 API・現在時刻に依存する処理
└── tests/                     # テスト
    ├── conftest.py            # 共有 fixture
    ├── test_calculator.py
    ├── test_grading.py
    ├── test_cart.py
    └── test_weather.py
```

## ローカルで動かす

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt -e .

pytest                   # テスト
pytest --cov             # テスト + カバレッジ
ruff check .             # lint
ruff format .            # 整形
```

CI で実行しているのも、これと同じコマンドです。**CI は「誰の PC でもない、まっさらな環境」で同じコマンドを動かす仕組み**だと考えると分かりやすいです。

## テストの種類

| 種類 | 何を確かめるか | 例 |
|---|---|---|
| 正常系 | 正しい入力で、正しい結果が返る | `test_add_returns_sum` |
| 異常系 | 不正な入力で、決めた例外が出る（`pytest.raises`） | `test_divide_by_zero_raises_value_error` |
| 境界値 | 条件が切り替わる値の両側（79 と 80 など） | `test_grade_boundaries` |
| パラメータ化 | 1 つのテストを入力を変えて回す（`@pytest.mark.parametrize`） | `test_add_various_inputs` |
| 浮動小数点 | 誤差を許して比べる（`pytest.approx`） | `test_divide_float_uses_approx` |
| fixture | テストの準備を共通化し、テストごとに新しく作る | `conftest.py` の `cart` |
| モック | 外部 API・時刻など、毎回変わるものを偽物に差し替える（`unittest.mock.Mock`） | `test_weather.py` |

モックを使えるように、`weather_advice` は API クライアントを、`greeting` は現在時刻を**引数で受け取る**形にしています。中で直接 API を呼んだり `datetime.now()` を呼んだりすると、CI の実行時刻やネットワークの状態でテスト結果が変わってしまいます（フレーキーなテスト）。

## CI（`.github/workflows/ci.yml`）の解説

```
PR を作る / push する
        │
        ├─▶ lint ジョブ ………… ruff check / ruff format --check
        │
        └─▶ test ジョブ ………… Python 3.11 / 3.12 / 3.13 で並列に pytest + カバレッジ
                                 └─ 3.13 のカバレッジレポートを保存
```

| 設定 | 意味 |
|---|---|
| `on: pull_request` / `push: branches: [main]` | PR の作成・更新時と、main へのマージ時に動く |
| `on: workflow_dispatch` | Actions タブの「Run workflow」から手動で動かせる |
| `permissions: contents: read` | CI に渡るトークンの権限を「読むだけ」に絞る（安全のため） |
| `concurrency` + `cancel-in-progress` | 同じブランチに続けて push したら、古い実行を止める |
| `jobs.lint` / `jobs.test` | ジョブは別々のマシンで**並列**に動く |
| `runs-on: ubuntu-latest` | GitHub が用意する Linux マシンで動かす |
| `actions/checkout@v4` | リポジトリのコードを取ってくる（これが無いとマシンは空っぽ） |
| `actions/setup-python@v5` + `cache: pip` | Python を入れ、pip のダウンロードをキャッシュする |
| `strategy.matrix.python-version` | 同じジョブを Python のバージョンごとに複製して動かす |
| `fail-fast: false` | 1 つのバージョンが落ちても、他のバージョンの結果も最後まで見る |
| `--cov` と `fail_under = 90` | カバレッジが 90% を下回ったら CI を失敗にする |
| `actions/upload-artifact@v4` | `coverage.xml` を実行結果に添付し、Actions の画面からダウンロードできる |

### CI が失敗するのはいつか

各 `run:` のコマンドが 0 以外の終了コードを返すと、そのステップが失敗し、ジョブが失敗します。pytest はテストが1件でも落ちると、ruff は違反が1件でもあると、0 以外を返します。

### 試してみる

1. `src/ci_sample/grading.py` の `score >= 80` を `score > 80` に変えて push する
2. `test_grade_boundaries[80-A]` が落ちて、CI が赤くなる（境界値テストがバグを見つけた例）
3. 元に戻して push すると、緑に戻る

### さらに一歩

- **必須チェックにする**: Settings → Branches（Rules）で `lint` と `test` を「Require status checks to pass」に登録すると、CI が通らない PR はマージできなくなります
- **ログを見る**: `gh run list` で実行一覧、`gh run view <id> --log-failed` で失敗したログだけを見られます
