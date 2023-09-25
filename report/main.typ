#import "template.typ": *

#show: project.with(title: "CNNによる画像認識AIの作成実習: 画像認識AIの説明書", authors: ("佐藤 朝陽",))

#show link: underline
#show link: set text(rgb(0, 122, 255))

= はじめに

本稿で説明する画像認識AIは、画像からアルファベット一文字を分類する畳み込みニューラルネットワーク（CNN）である。

ソースコードは以下のGitHubリポジトリにて公開している。

https://github.com/asa1984/cnn-assignment

= 仕様

CNNの仕様は以下の通りである。

- 入力画像は、縦横32ピクセルの正方形にリサイズされている。
- 畳み込み層は2層、全結合層は2層で構成されている。
- 活性化関数はReLUを用いる。

= データセット

学習及び検証に用いるデータセットは、複数種類の異なるフォントのアルファベット一文字の画像である。以下がデータセットの仕様である。

- 画像のフォーマットは、PNGである。
- 画像サイズは、縦横140ピクセルの正方形である。
- 画像は、中央に小文字のアルファベット一文字のみが書かれている。
- 画像は、白黒画像である。
- 訓練用データは、各アルファベットにつき50枚の画像がある。
- 検証用データは、各アルファベットにつき15枚の画像がある。

データセットは以下の手順によって作成される。

+ Google Fonts Developer APIを用いて、フォントの一覧を取得する。
+ 取得したフォントの一覧から、フォントを重複のないよう無作為に選択する。
+ 選択したフォントから、アルファベット一文字の画像を生成する。

データセット作成のためのスクリプトはTypeScriptで記述されており、実行環境は#link("https://deno.com")[Deno]のバージョン1.36.0である。

= 実装

このCNNはPythonの機械学習フレームワークPyTorchを用いて作成されている。学習と検証はGPU（CUDA）を用いてLinux上で行った。実行環境と利用したライブラリは以下の通りである。

- OS: EndeavorOS Cassini Nova
- GPU: NVIDIA GeForce RTX 3090 Ti
- 実行環境: Python 3.11.5
- パッケージマネージャ: #link("https://rye-up.com")[Rye] 0.13.0
- Pythonライブラリ:
  - torch 2.0.1
  - torchvision 0.15.2
  - matplotlib 3.7.3
  - numpy 1.24.4

本稿では、#link("https://github.com/asa1984/cnn-assignment")[ソースコード全体]から一部を抜粋して説明する。

== モデルの定義

ネットワークの構造は以下のように定義している。

#let source_model_py = read("../src/model.py")
#raw(source_model_py, lang: "python")

== データセットの読み込み

データセットの読み込みは`torchvision.datasts.ImageFolder`を用いて行った。

```python
train_dataset = torchvision.datasets.ImageFolder(
    train_data_dir, transform=train_transform
)
validate_dataset = torchvision.datasets.ImageFolder(
    validate_data_dir, transform=validate_transform
)
```

ImageFolderは、データセットのディレクトリ構造を以下のように定義することで、データセットを読み込むことができる。

```
/
├── train
│   ├── class1
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── class2
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── ...
└── validate
    ├── class1
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── class2
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── ...
```

画像が属するディレクトリ名がラベルとなったデータセットが作成される。

== データセットの前処理

データセットの前処理は、以下のように定義している。

```python
train_transform = transforms.Compose(
    [
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ]
)
validate_transform = transforms.Compose(
    [
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ]
)
```

学習用・検証用データセットの前処理は同じである。画像のリサイズとTensorへの変換のみを行っている。

= 実験・結果

以下の条件でモデルの学習を行った。

- バッチサイズ: 32
- エポック数: 10
- 学習率: 0.001
- 損失関数: 交差エントロピー
- 最適化関数: Adam

検証用データに対する正解率はエポック10の時に最も高かった。結果は以下の通りである。

#figure(table(
  columns: (auto, auto),
  inset: 5pt,
  align: (center, center),
  [*ラベル*],
  [*正解率*],
  "a",
  "80.00%",
  "b",
  "53.33%",
  "c",
  "80.00%",
  "d",
  "73.33%",
  "e",
  "73.33%",
  "f",
  "66.67%",
  "g",
  "66.67%",
  "h",
  "66.67%",
  "i",
  "66.67%",
  "j",
  "73.33%",
  "k",
  "73.33%",
  "l",
  "73.33%",
  "m",
  "80.00%",
  "n",
  "80.00%",
  "o",
  "66.67%",
  "p",
  "80.00%",
  "q",
  "66.67%",
  "r",
  "60.00%",
  "s",
  "80.00%",
  "t",
  "73.33%",
  "u",
  "73.33%",
  "v",
  "73.33%",
  "w",
  "86.67%",
  "x",
  "80.00%",
  "y",
  "73.33%",
  "z",
  "66.67%",
), caption: [
  検証用データに対する分類クラスごとの正解率
])

この時の総合正解率は72.56%であった。

学習結果は以下の通りである。 （実行結果より抜粋）

```
====> エポック 1/10, 平均損失: 3.2511191775159136
====> エポック 2/10, 平均損失: 2.5665588000925577
====> エポック 3/10, 平均損失: 1.7992225943542108
====> エポック 4/10, 平均損失: 1.4031684049745885
====> エポック 5/10, 平均損失: 1.0972054455338456
====> エポック 6/10, 平均損失: 0.918772272947358
====> エポック 7/10, 平均損失: 0.7706217256987967
====> エポック 8/10, 平均損失: 0.6575139826390801
====> エポック 9/10, 平均損失: 0.5593940244942177
====> エポック 10/10, 平均損失: 0.4722462954317651
```

Matplotlibを用いて、上記の損失の推移をグラフにしたものが以下の図である。

#figure(image("./loss_plot.png"), caption: [
  損失関数の推移
])
