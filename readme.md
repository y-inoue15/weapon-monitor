# readme

あるゲームの復元武器を記録するやつです。  
なぜか生産したものを記録したくなったので、作成しました。

# ライブラリ

一応 requirements はありますが、opencv と flask くらいです。  
あと、キャプチャーする環境が必要です。

# 使い方

```bash
python run.py
```

を行った後、http://127.0.0.1:5000でいけます。

あとは OBS なりで、あるゲームをキャプチャーしてもらって仮想カメラを起動したら準備完了です。

# 注意点

HD の環境で検証しているため、HD 出ない場合動作しない可能性があります。  
また、複数カメラを接続している場合、キャプチャー対象を変更する必要がでるかもしれません。
