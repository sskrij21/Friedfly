## 前書き

このページは、最近プログラミング学習としてゲーム作りを始めた知人に向けたものです。
筆者は日常的にプログラミングを行なっていますが、職業プログラマではありません。

この記事を通して伝えたいことは次の通りです。
* アイデアを、とりあえず動くように実装する方法
* とりあえず動くものをより洗練されたプログラムへ発展させていく考え方

この記事ではプログラミング言語としてPython3、ゲーム作りのライブラリとして[pyxel](https://github.com/kitao/pyxel)を用います。

基本的に不定期更新となりますが、進捗次第では連日更新します。

最後に僕から読者の方にメッセージです。

**Done is better than perfect.**

以上です。これから頑張りましょう。

(2021-07-25：公開)

## 開発に関して

あまり本筋ではない話ですが、ソフトウェア開発には多種多様な方法があります。有名なものにはアジャイル開発やウォーターフォール開発などがあり、書店などに行けば参考書なども多く出回っています。

ですが、趣味で行うプログラミングにあまり厳密なものを持ち込んでもしょうがないので、
この記事では最初にざっくりとした設計を行い、筋道を建てた後は拡張性を考えつつもプログラムが動くことを第一に実装していきます。

(2021-07-25：公開)

## どんなゲームを作りたいか考える

いきなりソースコードを編集し始める前に、どんなゲームを作るか考えてみることにします。

今回はゲームのジャンルとしてアクションゲームを作ることにして、
ざっと次のようなコンセプトを考えました。

- コンセプト
  - おやつに迫りよるハエをやっつけろ
- システム
  - マウスクリックでハエを退治
  - 退治したハエが落とすアイテムでパワーアップ
  - 制限時間内にどれだけスコアを稼げるか
  - ある一定スコアを超えるとボスが出現

といった感じで作ってみようと思います。時間に余裕があれば、発展として

* 異なる効果を持つアイテムの追加
* ステージの導入
* コンボシステムの導入
* スコアランキングの導入

などが出来ると思います。

ゲーム画面の模式図をお絵かきしてみると次のような感じです。ここにスコア表示などを追加していくことになります。

![screen_concept](./img/concept.png)

上記のようなゲームを実現するまでの過程を、その試行錯誤も含めて紹介していく予定です。

(2021-07-25：公開)

## 必要な機能を考える

前回はゲームのざっくりとしたシステムを考えました。

今回はこのシステムに沿って、ゲームに必要な機能を考えて行きます。
おさらいすると、

> - システム
>   - マウスクリックでハエを退治
>   - 退治したハエが落とすアイテムでパワーアップ
>   - 制限時間内にどれだけスコアを稼げるか
>   - ある一定スコアを超えるとボスが出現

といった感じです。ここから必要な機能とモノを考えて見ます。

* マウスクリックでハエを退治 -> クリックによる攻撃判定、ハエの当たり判定の定義
* 退治したハエが落とすアイテムでパワーアップ -> アイテムによる強化（攻撃範囲の拡大？）、アイテムの取得判定、アイテムドロップ率
* 制限時間内にどれだけスコアを稼げるか -> スコアの導入、表示
* ある一定スコアを超えるとボスが出現 -> ボスそのもの、ボス用の体力判定

このうち、主役となるのは主人公とハエです。これらの動作について考えてみましょう。

クリックされた際の内部処理はブロック図で表すと次のようになると思います。

![player_concept](./img/player-update.png)

特に、赤枠で囲まれた部分はアイテムやハエ、後で追加するボスハエなどに応じて追加していきます。
上から番号をつけて
1. マウスがクリックされたかどうかの判定
2. マウスカーソルの位置を取得
3. 
    * 攻撃範囲内部にハエがいるか判定
    * ハエの表示を消す。スコアの加算
4. 
    * 攻撃範囲内部にアイテムがあるか判定
    * アイテムを消す。アイテム取得状態の有効化

としておきます。

ハエに関しては

![enemy_concept](./img/enemy-update.png)

5. 画面上部ランダムな位置に出現
6. おやつに向かって移動
7. 攻撃を受けたかを判定
8. 攻撃を受けた場合、表示を消してスコアを加算

といったところでしょうか。

上の二つの図を比べるとクリックされた時のハエに関する処理が重複していますが、
今は実際にどのようにプログラミングするかを考えていないのでこれで良いでしょう。

次回からはこれらを少しづつpyxelに実装していきます。

(2021-07-25：公開)

## 主人公の核を作る

前回までにゲームのメイン要素となるハエタタキ（主人公）とハエのざっくりとした挙動を考えました。この記事ではこれを一つ一つ実装していきます。

以下ではgithubの機能であるブランチを使わずに、
`develop_component.py`と
`friedfly_game.py`
の二つのファイルを使って開発していきます。
`develop_component.py`では実装したい機能の試験を行い、`friedfly_game.py`では実装が終わったものを随時追加していきます。

以下、`update`,`draw`と言った場合には、`develop_component.py`内の`class App()`の`self update(self)`と`self draw(self)`を指します。
なるべく変更点は記事に載せていきますが、`...`と書いてある場合は直前に出てきたものが省略されていると思ってください。

さて、主人公の挙動をおさらいすると、

> 1. マウスがクリックされたかどうかの判定
> 2. マウスカーソルの位置を取得

が必要でした。今回はこの二つに絞って実装を試みます。

### クリックの判定

まず、1.を実装するために[pyxel](https://github.com/kitao/pyxel)のreferenceを読んでみます。

すると、マウスカーソルを表示する関数`mouse(visible)`があったので`update`に追加してみます。

```python
def update(self):
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True) ##### ここです #####
```

実行してみると、ゲーム画面上にマウスカーソルが表示されるようになりました。確認してみてください。
動作が期待通り行われているかを確認するためにも、しばらくはカーソルを表示してままにしておきます。

さて、次にクリックされたかの判定をしてみます。

[ここ](https://github.com/kitao/pyxel/blob/master/pyxel/__init__.py)を見ると、pyxelで使えるkeyの一覧が見られます。
193行目の`MOUSE_LEFT_BUTTON`が怪しいですね。試しに使ってみましょう。

``` python
    def __init__(self):
        self.mouse_pressed = False
        ...

    def update(self):
        ...
        pyxel.mouse(True)
        # check if a mouse is pressed
        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON): ##### ここです #####
            self.mouse_pressed = True

    def draw(self):
        # fill the screen with a black
        pyxel.cls(pyxel.COLOR_BLACK)
        # draw circle when mouse left button is pressed
        if self.mouse_pressed: ##### ここです #####
            pyxel.circ(80, 80, 30, pyxel.COLOR_RED)
```

ここではクリックされたかどうかの情報をdrawに引き継ぐために、`self.mouse_pressed`を導入し、`circ`も使用しました。

プログラムを実行してみると、クリックによって赤い円が表示されました。成功です！！！

しかし、一度クリックすると円が表示されたままになってしまいます。
これだとハエを叩くという動作が一度しかできないですね。

これはif文によってボタンが押されている時だけ、`mouse_pressed`を`True`に
するという書き方になっているためです。

ボタンを押すたび、もしくは押している間だけ円を書くためには、`mouse_pressed`を`False`に戻してやる必要があります。

なので、次の様に変更してみましょう。

``` python
    def update(self):
        ...
        pyxel.mouse(True)
        # check if a mouse is pressed
        self.mouse_pressed =  pyxel.btn(pyxel.MOUSE_LEFT_BUTTON): ##### ここです #####
```
`btn`はこの関数が呼ばれた時に、指定したボタンが押されていれば`True`、そうでなければ`False`を返してくれます
。これでフレーム毎にマウスが押されているかを判定できるようになりました。

### マウス位置の取得

最後に、2.を実装します。
今回はのマウスをクリックした位置に応じて円の場所を変えてみましょう。

変更点は次の通りで
```python
    def update(self):
        ...
        self.mouse_pressed =  pyxel.btn(pyxel.MOUSE_LEFT_BUTTON)
        if self.mouse_pressed: ##### ここです #####
            self.circ_x = pyxel.mouse_x
            self.circ_y = pyxel.mouse_y

    def draw(self):
        ...
        if self.mouse_pressed:
            pyxel.circ(self.circ_x, self.circ_y, 30, pyxel.COLOR_RED) ##### ここです #####
```

実行した結果がこちら。マウス左ボタンは押したまま動かしています。

![circ-move](./img/anime-circ-move.gif)

良さそうですね。

### まとめ

それではこの記事のまとめです。

今回は
* `mouse()`でカーソルを表示する
* マウスがクリックされたかを`btn()`で判断する
* マウスの位置を`mouse_x`、`mouse_y`で取得する
* `circ()`を使って円を書く

ことに挑戦しました。

特に`btn()`の返り値を`draw()`に引き継ぐことで、ボタンが押されている間だけ円を表示しました。

今後`mouse_x`と`mouse_y`を取得した部分に、クリックされた時にだけ必要な処理を追加していきます。

最新版のソースコードのcommit IDは`a3a4e3d`です。

(2021-07-25：公開)

## ハエを叩くモーションを作る

さて、前回はマウスのクリックを認識させ、カーソルの位置に円を描画してみました。

今回はこれを応用して、マウスをクリックした時にだけハエを叩くアニメーションが表示されるようにしてみましょう。

今回は、処理がフレームをまたぐことになるのでなるべく丁寧に解説します。

さて、`pyxeledior`を使って次の様な画像を用意しました。

![item1](./img/anime-item1.png)

今回の目標はこの三つの画像のうち、マウスをクリックしない間は一番左を表示しておき、クリックされた際に右に移り変わっていくようなプログラムを実現します。

まずは、前回の円の表示と何が違うか考えてみましょう。

### フレームについて

ゲームにはフレームという概念があり、一秒あたりのフレーム更新回数をFrame per second (FPS)と呼びます。
FPSが大きくなるほどゲーム画面の更新が頻繁に行われ、見た目には滑らかなゲームになるわけですね。

前回に円を表示した際には、全ての処理を同一フレーム内で完結させていました。
言い換えると一組の`update()`と`draw()`で済んでいたわけです。

単純に考えれば、マウスがクリックされた時に画像を三枚順に表示すれば良いですが、
それだと人間にはあまりに一瞬すぎて良いアニメーションには見えません。

各画像を表示する間にゲームを一時停止するという方法もありますが、その他の処理は継続したいです。
そこで、処理を複数フレームに跨がるようにすることで、ゲームを止めずにアニメーションを表示します。

具体的に実装してみましょう。

まず`__init__()`と`update()`を次のように書き換えます。

```python
    def __init__(self):
        self.mouse_pressed = False
        self.drawing_anime = False ##### ここです #####
        self.frame_anime_init = 0 ##### ここです #####
        self.circ_x = 80
        self.circ_y = 80
        pyxel.init(160, 160, caption="Fried fly", fps=30)
        pyxel.load('friedfly.pyxres') ##### ここです #####
        pyxel.run(self.update, self.draw)

    def update(self):
        ...
        pyxel.mouse(True)
        # check if a mouse is pressed
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        ##### ここから #####
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count
```
`__init__()` には今回の処理で必要な値の初期宣言をいています。

重要な役割を果たすのは`if self.mouse_pressed and not self.drawing_anime:`から始まるif文です。

このif文により、ハエ叩きアニメーション（以下、叩きアニメ）の表示が進行中でない場合かつマウスがクリックされた時にだけ、
叩きアニメを開始するようにしています。
if文の条件に`not self.drawing_anime`があるのは、叩きアニメ表示中に再度`not self.drawing_anime`を書き換えられないようにするためです。

さらに、クリックしていない時でもハエ叩きをカーソルの位置に表示し続けたいので、`circ_x`と`circ_y`はif文の外に出ていることに注意してください。
`self.frame_anime_init`はアニメーション終了のタイミングを決めるため、叩きアニメ開始のタイミングを保存しています。

以上で追加した`self.drawing_anime`と`self.frame_anime_init`を用いて、叩きアニメを描画する処理を実現しましょう。

具体的には

`self.drawing_anime = True`になる -> アニメーションを一定時間表示する -> `self.drawing_anime = False`に戻す

ということができれば良いわけです。加えて、`self.drawing_anime = False`の時には動いていないハエ叩きが表示されるようにしましょう。

これを`draw()`に追加してみると次のようになります。

```python
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        if self.drawing_anime:
            # Count how many frames were passed from the begining
            current_frame = pyxel.frame_count - self.frame_anime_init
            # First four frames
            if current_frame//4 == 0: pyxel.blt(self.circ_x, self.circ_y, 0, 16, 0, 16, 32, pyxel.COLOR_BROWN)
            # Next four frames
            if current_frame//4 == 1: pyxel.blt(self.circ_x, self.circ_y, 0, 32, 0, 16, 32, pyxel.COLOR_BROWN)
            # if the animation lasts more than eight frames, kill it.
            if current_frame >= 8:
                self.drawing_anime = False
        else:
            # nominal state (without a click)
            pyxel.blt(self.circ_x, self.circ_y, 0, 0, 0, 16, 32, pyxel.COLOR_BROWN)

```

ここで重要なのは最初のif文です。
ここでハエ叩きアニメを表示するべき状態なのかを判別し、通常時（`else`）は左端の画像を表示しています。
`else`の中身は通常の状態なんだからif分の前に書いてはいけないの？と思うかもしれませんが、
現在のコードでは毎フレームで画面を黒塗りし（`pyxel.cls(pyxel.COLOR_BLACK)`）、その後に画像を表示しているので画像が重なってしまいます。

そういうわけで叩きアニメを表示する状態とそうでない状態に分ける必要があります。

if文の中身を解説していきましょう。

はじめに`current_frame`を定義しています。ゲームの正解ではフレーム数が時間に相当するので、フレームの数を数えることで時間の経過を取り扱えます。

叩きアニメが始まってからのフレーム数をカウントしたいので、現在のフレーム`pyxel.frame_count`から`self.frame_anime_init`を引くことで
経過時間をカウントしています。

その後二行がアニメーションの核となる部分です。

`//`は代数演算子のひとつで、割り算をしてその小数点以下を切り捨てた値を返します。

ここでは各画像を4フレームづつ表示するとした決めました。すると最初の4フレームは真ん中の画像、後の4フレームは右の画像を表示したいわけです。

そのため0から7フレームまでのうち、0,1,2,3と4,5,6,7で処理を分けたくなります。こんな時に使えるのが`//`なわけです。

4未満の数字は4で割ると1未満になるので、0になり、4から7は1になるので、この条件を使って場合わけができます。

それが`if current_frame//4 == 0:`と`if current_frame//4 == 1:`の部分に相当する訳ですね。

最後に8フレーム以上の時間が経過した際には、`self.drawing_anime`を`False`に戻すことで、通常時の描写に戻します。

これでクリックするたびにハエを叩くアニメーションが表示されるはずです。さて、動かしてみましょう。

![anime-item1](./img/anime-item1.gif)

いい感じですね。だんだんゲームらしくなってきました。

次回はスコアを導入して、敵をクリックするとスコアが増える仕組みを考えてみたいと思います。

最新のコードは`b62e1c2`です。

(2021-07-28：公開)

## スコアを追加する

さて、前回の記事までにクリックしてアニメーションを表示する部分まで完成させることができました。

そろそろゲームとして遊べるようにしていきたいので、今回はスコアシステムを導入してみましょう。

### スコアを画面に表示する。

まずは画面にスコアを表示させてみましょう。`__init__()`と`draw()`に少し処理を追加します。


```python
    def __init__(self):
        ...
        self.frame_anime_init = 0
        self.game_score = 0 ##### ここです #####
        ...
```
```python
    def draw(self):
        # fill the screen with a black
        pyxel.cls(pyxel.COLOR_BLACK)
        ##### ここから #####
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)
        ...
```

合計三行です。しかも`__init__()`の一行は初期化処理なので、実質二行ですね。

この二行では`pyxel.text()`で画面上に文字を表示させています。しかも少しお洒落に緑字の上に赤文字を重ねてみました。

途中`'SCORE: {}'.format()`を使用しましたが、これは`''`内部の`{}`の位置に`format(var)`で与えた変数を代入した文字列を作る関数です。
つまり`self.game_score = 100`の時には`'SCORE: 100'`といった感じにしてくれるわけですね。
pythonの便利な機能のひとつですのでぜひ調べてみてください。

これでスコアの表示は完了です。思ったより簡単でしたね。

### スコアの計算

さて、ここから本題のスコアの計算に入りましょう。

最初のゲームコンセプトではハエをクリックで叩き、倒してスコアを稼ぐ方式にしようということでした。

これを実現するためには以下のような手順が必要です。

1. クリックする
2. カーソルの座標を取得する
3. ある範囲内にハエがいるか確認する
4. ハエがいればスコアをゲット
5. いなければ何もしない

といったところでしょうか。実際のゲームではハエを画面から消す動作が必要になりますが、
今回は一時的なハエもどきで代用することにします。

まず`draw()に`処理を追加して、ハエもどきを画面に表示しましょう。

```python
    def draw(self):
        # fill the screen with a black
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(80,80,0,0,32,16,16,pyxel.COLOR_BROWN)
        ...
```
これで画面中央に"仮"のハエが表示されました。

この仮ハエの近くでクリックした時にだけスコアを増加させたいですね。
こんな時には少し数学を使います。

ある二点の座標A(x_a,y_a)とB(x_b,y_b)があるとき、その距離rは

r = sqrt((x_a - x_b) * (x_a - x_b) + (y_a - y_b) * (y_a - y_b))

これは点Aから点Bまでひいた直線の長さと等しくなります。

この距離がある一定の値より小さい時だけ、スコアを増加させてあげれば良いわけです。

それを`update()`に追加すると

```python
    def update(self):
        ...
            self.frame_anime_init = pyxel.frame_count
        if self.mouse_pressed and dist([self.circ_x,self.circ_y],[80,80]) <= 5: self.game_score += 100
```
ここでは距離が5以下の場合に100点増える様にしました。

ここで`dist`は二つの座標`[x,y]`の配列を引数にとる関数で以下のように実装しました。

```python
def dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
```
少し難しい書き方をしていますが、rの定義と同じことをしています。この関数はクラス内部の情報を使わないのでクラスの外部に定義しています。

正常に動くようにするために`__init__()`にgame_soreの初期化と当たり範囲（ここでは80,80から距離5以内）を
表す円の描画を追加してあげます。

```python
    def __init__(self):
        ...
        self.frame_anime_init = 0
        self.game_score = 0 ##### ここです #####

    def draw(self):
        ...
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(80, 80, 0, 0, 32, 16, 16, pyxel.COLOR_BROWN)
        pyxel.circ(80, 80, 5, pyxel.COLOR_BROWN) ##### ここです #####
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)
```


実行してみると、中心の茶色の円の中をクリックした時にだけ、スコアが増加することが確認できます。

次回はついに敵のモーションを追加していきます。

プログラムがごちゃごちゃしてきたので、一旦整理もしてみようと思います。


(2021-07-28：諸事情により書きかけ)

(2021-08-08：公開)


## 敵の追加

### 複雑化に向けた、プログラムの整理

まずは、敵を実装する前にこれまで作ってきたソースコードを整理することからはじめましょう。

プログラムの処理内容をそのままに改良することをリファクタリングと呼びます。

これから敵の処理が増えるにつれ、コードが煩雑になっていくので一度リファクタリングを行ってみます。

今回は処理の種類を`Player, Score, General`に分けた後に、改良していくこととします。

コメントをつけたコードは`rough`ブランチに残しておいたので、いつでも簡単に確認できます。

コメントをつけたコードを見てみましょう。

```python
def __init__(self):
        ## Player
        self.mouse_pressed = False
        ## Player
        self.drawing_anime = False
        ## Player
        self.frame_anime_init = 0
        ## General
        self.game_score = 0
        ## Player
        self.circ_x = 80
        self.circ_y = 80
        ## General
        pyxel.init(160, 160, caption="Fried fly")
        pyxel.load('friedfly.pyxres')
        pyxel.run(self.update, self.draw)
```
`__init__()`は主に初期化処理の集まりなので今回は手を触れないこととします。
```python

    def update(self):
        ## General
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        ## General
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        ## Player
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count
        ## Score
        if self.mouse_pressed and dist([self.circ_x,self.circ_y],[80,80]) <= 5: self.game_score += 100
```
`update()`はこんな感じです。

`self.mouse_pressed`の代入処理は`Player`ではないのかと悩みましたが、スコアの処理にも使っているので`General`と分類しました。
これからする作業では`Player`と`Score`の間になるべく、依存関係を持たせないようにします。

とりあえず難しいことは抜きにして、簡単に処理をまとめてみましょう。
次のような関数を二つ用意します。
```python
    def update_player(self):

    def update_score(self):

```
この内部に、コメントで区別した`update()`の処理をコピーします。

```python
    def update_player(self):
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count
    def update_score(self):
        if self.mouse_pressed and dist([self.circ_x,self.circ_y],[80,80]) <= 5: self.game_score += 100
```

その後に、`update()`内部の処理をこの二つの関数で置き換えます。

```python
    def update(self):
        ## General
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        ## General
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        ## Player
        self.update_player()
        ## Score
        self.update_score()
```

これで`update()`がすっきりしました。`draw()`も同様にまとめてみるとこれが、

```python
    def draw(self):
        # fill the screen with a black
        ## General
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(80, 80, 0, 0, 32, 16, 16, pyxel.COLOR_BROWN)
        pyxel.circ(80, 80, 5, pyxel.COLOR_BROWN)
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)
        if self.drawing_anime:
            # Count how many frames were passed from the begining
            current_frame = pyxel.frame_count - self.frame_anime_init
            # First four frames
            if current_frame//4 == 0: pyxel.blt(self.circ_x, self.circ_y, 0, 16, 0, 16, 32, pyxel.COLOR_BROWN)
            # Next four frames
            if current_frame//4 == 1: pyxel.blt(self.circ_x, self.circ_y, 0, 32, 0, 16, 32, pyxel.COLOR_BROWN)
            # if the animation lasts more than eight frames, kill it.
            if current_frame >= 8:
                self.drawing_anime = False
        else:
            # nominal state (without a click)
            pyxel.blt(self.circ_x, self.circ_y, 0, 0, 0, 16, 32, pyxel.COLOR_BROWN)

```
こうなります。

```python
    def draw(self):
        # fill the screen with a black
        ## General
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_score()
        self.draw_player()


    def draw_player(self):
        if self.drawing_anime:
            # Count how many frames were passed from the begining
            current_frame = pyxel.frame_count - self.frame_anime_init
            # First four frames
            if current_frame//4 == 0: pyxel.blt(self.circ_x, self.circ_y, 0, 16, 0, 16, 32, pyxel.COLOR_BROWN)
            # Next four frames
            if current_frame//4 == 1: pyxel.blt(self.circ_x, self.circ_y, 0, 32, 0, 16, 32, pyxel.COLOR_BROWN)
            # if the animation lasts more than eight frames, kill it.
            if current_frame >= 8:
                self.drawing_anime = False
        else:
            # nominal state (without a click)
            pyxel.blt(self.circ_x, self.circ_y, 0, 0, 0, 16, 32, pyxel.COLOR_BROWN)

    def draw_score(self):
        ## Score
        pyxel.blt(80, 80, 0, 0, 32, 16, 16, pyxel.COLOR_BROWN)
        pyxel.circ(80, 80, 5, pyxel.COLOR_BROWN)
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)
```

さて、このような作業をしてもプログラムの動作は変わらないはずです。
では、この作業の利点はどこにあるのでしょう。

自分が思う利点は大きく分けて以下の通りです。
1. コードが読みやすくなる。
2. 変更作業が楽になる。
コードの読みやすさに関しては、書き手と読み手のレベルにも依存しますが、例えば主人公の処理に関する部分だけを確認したい時、（バグが明らかにその処理にあるとわかっているとき）
変更前のコードだと、一読して主人公に関する処理を理解してから変更しなければいけないですが、変更後では`update_player`の中身を読めば良いことがわかります。

今はまだ小さなコードですが、今後機能が増えていくとこのありがたみがわかると思います。

次に変更作業についてですが、これは実際に手を動かしてみるのが良いです。
例えば`draw()`の中身の`draw_player()`だけをコメントアウトしてみましょう。draw_playerの中身は処理だけで8行に渡るものですが、`draw_palyer()`の一行をコメントアウトしただけで、ハエ叩きが表示されなくなるのが
わかるかと思います。しかしそれ以外の部分は正常に動作していますね。

このようなことは、プログラムの誤った変更を防ぐことにも繋がります。

あとはこれから敵を導入していくと、複数体の敵を表示したいということになると思います。

そういった時に少し入力の異なる同じ処理を繰り返す時などは関数としてまとめる利点が明らかになるかと思います。乞うご期待。

(2021-08-09：公開)

### 敵の追加と単純なアルゴリズムの実装

さて、ついに敵の実装です。`friedfly.pyxres`にハエの画像を追加しておきました。

今回の記事では、お菓子に向かって真っ直ぐに迫りくるハエを一匹実装してみた後に、プレイヤーを避ける動作を追加してみます。

まずは、敵の実装に必要な変数を`__init__()`に追加しておきます。

ここでは、敵位置のx,y成分と速度のx,y成分に加えて速さを準備しました。
（速度と速さが区別してあるのは、方向と速度の大きさを別々に制御したいからです。）

`__init__()`はこのようになります。

```python
    def __init__(self):
        ...
        self.circ_y = 80
        ## Enemy
        self.pos_ene_x = random.randint(0,160)
        self.pos_ene_y = 0
        self.speed = 1
        self.vel_ene_x = 0
        self.vel_ene_y = 0
        ## Sweet
        self.pos_sweet_x = 80-16/2
        self.pos_sweet_y = 160-16
        ## General
        pyxel.init(160, 160, caption="Fried fly")
        ...
```
`update()`には`update_enemy()`を追加し、詳細な処理は後者の内部に書くこととします。

```python
    def update(self):
        ...
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        self.update_player()
        self.update_enemy() ##### ここです #####
        self.update_score()

```

さて、`update_enemy()`には何を書けば良いでしょうか。

敵は画面上端のランダムな位置から動作を開始します。これは`__init__()`で初期化する際に設定しました。

ここから画面下のお菓子に向かってまっすぐ飛んで欲しい訳です。

しかし敵が生成されるx位置はランダムですから、移動する方向もそれに応じて変化させなければいけません。ここでベクトルの考えかたを使います。

ゲーム画面の原点、敵、そしてお菓子の位置関係をまとめると次のようになります。

![vector](./img/vector_image.png)

図の点線に沿った様な位置の更新ができれば良いわけです。この図の例であれば
位置のy成分は増えていきながら、位置のx成分は減っていきます。

x成分とy成分の変化のしかたは、y成分のほうが大きくなりそうです。これはお菓子に到着するまでに過ぎる時間はxとyに対して等しいためです。これが等しくない場合というのは、まずお菓子の真上まで移動してから近づいていく場合などです。この場合x方向の移動はy方向よりも短時間で終わるので、経過時間は等しくならないですが、生き物の動き方としてはぎこちないですね。

さて問題はこの点線の向きをどうやって計算するかです。図を見ると、赤と青の矢印もあります。点線の方向に動くというのは、赤い矢印を遡って原点まで動き、青い矢印に沿って移動するのと同じことです。

つまり、ベクトルでいうと

敵からお菓子までのベクトル　= 敵から原点までのベクトル　+ 原点からお菓子までのベクトル

となります。ベクトルの性質から始点と終点を入れ替える操作には負符号をかける
ことが伴うので

敵からお菓子までのベクトル　= -1 * 原点から敵までのベクトル + 原点からお菓子までのベクトル

と表せます。ここで注目すべきは、原点からあるモノまでのベクトルはその位置座標を用いて

`vec_from_origin_to_enemy = (x_ene,y_ene)`

と表せます。お菓子に関しても同様に

`vec_from_origin_to_sweet = (x_sweet,y_sweet)`

となるのです。

これを引き算するのは各成分を引き算するのと等しいので

`vec_from_enemy_to_sweet = (x_sweet-x_ene,y_sweet-y_ene)`

と計算できます。

長くなってしまいましたが、ベクトルの概念と計算のしかたは以上のとおりです。

これを使って敵の位置を更新してみましょう。

`update_enemy()`に以下のように記述します。

```python
    def update_enemy(self):
        vec_x = self.pos_sweet_x - self.pos_ene_x
        vec_y = self.pos_sweet_y - self.pos_ene_y
        abs_vec = math.sqrt(vec_x*vec_x+vec_y*vec_y)
        self.pos_ene_x += self.speed * vec_x / abs_vec
        self.pos_ene_y += self.speed * vec_y / abs_vec

```
一行目および二行目はベクトルの各成分を計算しています。三行目ではベクトルの大きさを計算することで、四行目と五行目で位置の更新をする際に、x成分とy成分の大きさの合計が`self.speed`になるよう規格化しています。

さて、この位置を使って敵の描写を追加してみます。

`update`と同様に`draw`にも`draw_enemy`を追加します。

内容は次の通りです。

```python
    def draw_enemy(self):
        if pyxel.frame_count%4 < 2 :
            pyxel.blt(self.pos_ene_x, self.pos_ene_y, 0, 16, 32, 16, 16, pyxel.COLOR_BROWN)
        if pyxel.frame_count%4 >= 2:
            pyxel.blt(self.pos_ene_x, self.pos_ene_y, 0, 32, 32, 16, 16, pyxel.COLOR_BROWN)
```

一見複雑に見えますが、やっていることは2frameごとにハエの画像を入れ替えながら上の計算で更新した位置に表示するということです。

これでランダムな位置に生成されたハエが、お菓子に向かって一直線に飛んでくるような処理ができました。

![bug](./img/bug_coming.gif)

しかし、これではハエらしくありません。ハエ叩きがあったら避けてくれないでしょうか。

今回は長くなったのでこれくらいにしますが、次回はハエ叩きを避けるハエを実現していきます。



(2021-08-09：公開)
