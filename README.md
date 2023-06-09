# BGM-Player-Anywhere
![image](https://github.com/tarou-imokenpi/BGM-Player-Anywhere/assets/91922753/069b6ff9-c413-402e-926c-6a49baceda59)
ショートカットキーで音楽を再生できるBGMプレイヤーです。バックグラウンド再生に対応しています。
***
## 使い方

### 実行ファイル形式（exe）の場合
`BGM-PlayerGUI.exe`をクリックするだけでOKです。

### python環境で実行したい場合
> コードを確認したい、変更したい場合はこちらをご利用ください。

`main.py`を実行してください。
`main.py`はexeの元になっているコードです。

## 操作

### 音楽を追加
* 押すとファイル選択するためのエクスプローラーが表示されます。
* 音楽を選択し開くを押すことで音楽が追加されます。

### 再生
* その行の音楽が再生されます。
* もう一度押すと最初から再生されます。

### 停止
* その行の音楽の再生を停止します。

### 音量の調整
* 青いスライダーを移動させると音楽ごとに音量を調整出来ます。
* 真ん中がデフォルトです。

### 削除
* その行の音楽を一覧から削除します。

### ショートカットキーを登録
* その行の音楽を再生するためのショートカットキーを設定出来ます。
* ショートカットキーはこのソフトがアクティブウィンドウでなくても、そのキーが押されたら再生されます。
* 再生中にもう一度押すと最初から再生されます。
* ボタンの右側に現在のショートカットキーが表示されています。
## 設定データの保存機能について

実行ファイルでもpythonファイルでも起動後、保存すると`settings.json`と`window_size.json`が作成されます。

もし、ファイルが読み込みエラーの場合でも設定ファイルを再構成するようになっているので安心してご利用いただけます。
### settings.json
以下のデータが保存されています。
* 音楽ファイルのパス
* その音楽ファイルに設定されていた音量
* ショートカットキー
### window_size.json
終了時にウィンドウサイズを保存し、次回起動時にウィンドウサイズを復元するためのデータが保存されています。

以下のデータが保存されています。
* 横幅、縦幅
## exe化
main.pyのexe化には`Nuitka`を使いexe化してます。
