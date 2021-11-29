# Project 2
contributed by < `robertlin0401` >

###### tags: `資料探勘`

> [GitHub](https://github.com/robertlin0401/Data-Mining-Project2)
---

## 作業要求
- [X] 自定義情境與分類規則
- [X] 根據分類規則生成 positve 與 negative 資料
- [X] 使用生成的資料訓練分類器模型（decision tree）
- [X] 觀察訓練出來的模型，比較其分類規則與最初設定的差別

## 說明
### 檔案結構
* attributes.json：記錄屬性相關資訊，內含兩個項目
    1. attributes - 屬性列表
    2. options - 各個屬性的選項列表
* rules.csv：記錄所有 'absolutely right' 規則
    * 規則的屬性順序與 attributes.json 中屬性列表的順序需一致
    * 使用 '\*' 表示 don't care
* rules.png：根據 'absolutely right' 規則繪製而成，呈現預先設定的分類判斷流程圖
* <text>generator.py</text>：根據執行指令之 flag 不同，會執行不同的功能，詳見[執行](#執行)說明
    1. 生成 dictionary.csv
    2. 生成 data.csv
* <span id="dictionary_csv">dictionary.csv</span>：內含所有可能的屬性組合，以及其對應的分類結果
    * 由 <text>generator.py</text> 依以下步驟生成
        1. 讀取 attributes.json，根據各個屬性的選項列表生成所有可能的屬性組合
        2. 讀取 rules.csv，將每個屬性組合根據規則求出分類結果
    * 用以提供 data.csv 參考，作為其生成資料時所使用的資料庫
* data.csv：自 dictionary.csv 選中資料，組合成 <text>classifier.py</text> 所需的訓練資料集
    * 現有的 data.csv 長度為 200
* <text>classifier.py</text>：根據 data.csv 訓練出分類模型，並生成該模型的分類規則
    * 分別會在終端機印出文字版的決策樹，以及在同一目錄下儲存一份名為 decision_tree.png 的圖像版決策樹
* <text>README.md</text>：即為[本文件](https://hackmd.io/@robertlin0401/Data-Mining-Project2)

### 執行
* <text>generator.py</text>
    * 用法：`python generator.py -m <mode> [-n <number>]`
        * mode - 為 0 時會生成 dictionary.csv，為 1 時會生成 data.csv
        * number - 當 mode 為 1 時需設置，用來指定生成之 data.csv 的長度
    * 使用 `python generator.py -h` 或 `python generator.py --help` 可取得詳細說明
* <text>classifier.py</text>
    * 用法：`python classifier.py`

### 開發流程與運作原理
#### 設定情境與規則
* 情境：學生是否能夠通過某堂課程的考試？
* 屬性
    * gender：學生的性別
        * 男生 male
        * 女生 female
    * talent：學生的資質
        * 較好 talented
        * 普通 general
        * 較差 clumsy
    * effort：學生的努力程度
        * 努力 hard-working
        * 一般 general
        * 怠惰 lazy
    * state：學生在考試時的狀態
        * 緊張 nervous
        * 放鬆 relaxed
    * retake：學生重修該堂課程的次數
        * 零次 none
        * 一次 once
        * 兩次 twice
    * attend：學生在該堂課程的出席率
        * 較好 good
        * 較差 bad
    * club：學生是否有參加如社團活動之類的課外活動
        * 有的 yes
        * 沒有 no
* 規則
    * 大原則如下
        * 性別完全不影響結果
        * 資質與努力程度影響很大，其中又以資質為主要影響的要素
        * 其餘項目則影響較少
    * 完整的分類流程圖如下
        ![](https://i.imgur.com/8LmqK2r.png)
* 將上述內容手動輸入成 attributes.json 與 rules.csv 兩個檔案，供後續步驟使用
    * attributes.json
        ```json
        {
            "attributes": [
                "gender", "talent", "effort", "state", "retake", "attend", "club"
            ],
            "options": {
                "gender": ["male", "female"],
                "talent": ["talented", "general", "clumsy"],
                "effort": ["hard-working", "general", "lazy"],
                "state" : ["nervous", "relaxed"],
                "retake": ["none", "once", "twice"],
                "attend": ["good", "bad"],
                "club"  : ["yes", "no"]
            }
        }
        ```
    * rules.csv
        ```csvpreview { header="true" }
        gender,talent,effort,state,retake,attend,club
        *,talented,*,*,*,*,*
        *,general,hard-working,*,*,*,*
        *,general,general,*,*,*,*
        *,general,lazy,*,*,good,*
        *,general,lazy,*,twice,bad,*
        *,general,lazy,*,once,bad,*
        *,clumsy,hard-working,*,*,*,*
        *,clumsy,general,*,*,good,*
        *,clumsy,general,*,twice,bad,*
        *,clumsy,general,relaxed,once,bad,no
        ```
#### 生成所有屬性組合
* 命令：`python generator.py -m 0`
* 詳見上方 [dictionary.csv](#dictionary_csv) 說明
#### 生成訓練資料集
* 命令：`python generator.py -m 1 -n <number>`，當前 number 值為 200
* 使用 random seed 為 0 的 pseudo-random number generator 生成兩個隨機序列（長度合計為 \<number>），並根據序列至資料庫（dictionary.csv）對應索引中取得資料，組合成 data.csv
    * 之所以使用固定 random seed 的 pseudo-random number generator 是為了讓每次生成的 data.csv 內容一致
    * 兩個隨機序列所取得的資料之性別屬性分別為男性與女性，而兩序列長度比（即為男女比）約為 4:1
#### 訓練模型
* 選用 `sklearn.tree.DecisionTreeClassifier` 作為模型進行訓練
* 文字版決策樹：使用 `sklearn.tree.export_text()`
    ```cpp
    |--- feature_1 <= 1.50
    |   |--- feature_4 <= 0.50
    |   |   |--- feature_5 <= 0.50
    |   |   |   |--- class: 1
    |   |   |--- feature_5 >  0.50
    |   |   |   |--- feature_2 <= 1.50
    |   |   |   |   |--- class: 1
    |   |   |   |--- feature_2 >  1.50
    |   |   |   |   |--- feature_1 <= 0.50
    |   |   |   |   |   |--- class: 1
    |   |   |   |   |--- feature_1 >  0.50
    |   |   |   |   |   |--- class: 0
    |   |--- feature_4 >  0.50
    |   |   |--- class: 1
    |--- feature_1 >  1.50
    |   |--- feature_2 <= 1.50
    |   |   |--- feature_2 <= 0.50
    |   |   |   |--- class: 1
    |   |   |--- feature_2 >  0.50
    |   |   |   |--- feature_5 <= 0.50
    |   |   |   |   |--- class: 1
    |   |   |   |--- feature_5 >  0.50
    |   |   |   |   |--- feature_4 <= 1.50
    |   |   |   |   |   |--- feature_0 <= 0.50
    |   |   |   |   |   |   |--- class: 0
    |   |   |   |   |   |--- feature_0 >  0.50
    |   |   |   |   |   |   |--- feature_3 <= 0.50
    |   |   |   |   |   |   |   |--- class: 0
    |   |   |   |   |   |   |--- feature_3 >  0.50
    |   |   |   |   |   |   |   |--- class: 1
    |   |   |   |   |--- feature_4 >  1.50
    |   |   |   |   |   |--- class: 1
    |   |--- feature_2 >  1.50
    |   |   |--- class: 0 
    ```
* <span id="DT_img">圖像版決策樹</span>：使用 `sklearn.tree.plot_tree()`
    ![](https://i.imgur.com/dohzC0J.png)

## 分析
* 觀察[上圖](#DT_img)可以發現，訓練出來的模型將理應毫無相關的 gender 屬性列入了分類依據
    * 在此例子中，我特意將理應無影響的 gender 屬性設計成在訓練資料中呈現相當不平衡的樣子，因此在訓練資料不足的情況下，模型便很有可能在較後面的步驟將此屬性作為分類依據
    * 在實際應用時，因為無法得知各屬性的分布情形，因此若選用的訓練資料不足，就有可能導致模型無法辨識出理應有影響的屬性之影響性，反倒選用了理應無影響的屬性作為分類依據
    * 當資料數從 200 增加至 400 時，此問題就不存在了
        ![](https://i.imgur.com/vRJGO5m.png)
* 觀察調整後的決策樹可以發現，其分類過程比起預設的過程繁複了許多，並且部分屬性的判斷順序也與預設的不相同
    * 決策樹模型並不了解各個屬性的意義，因此無法以人類的邏輯去思考，想當然就無法產出與人類相同的分類過程
