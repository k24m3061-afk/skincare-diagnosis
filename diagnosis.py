
# -----------------------------------------------------
# クレンジングの診断の質問
# -----------------------------------------------------
kurennzingu = {
    "q": "普段のメイクは濃い方ですか？",
    "yes": {
        "q": "肌が乾燥しやすいですか？",
        "yes": {"answer": "バームタイプ"},

        "no":{"answer": "オイルタイプ"}
    },
    "no": {
        "q": "肌が乾燥しやすいですか？",
        "yes": {
            "q": "敏感になりやすいですか？",
            "yes":{
                "q":"さっぱりした洗い心地が好きですか？",
                "yes":{"answer":"ウォータータイプ"},
                "no":{"answer":"ミルクタイプ"},
            },

            "no": {"answer": "クリームタイプ"}
        },
       "no": {"answer": "ジェルタイプ"}
        }
    }
# -----------------------------------------------------
# 化粧水・乳液／美容液の診断質問
# -----------------------------------------------------
Tzone = "Tゾーン（おでこ・鼻）も乾燥しやすいですか？"
Nikibi = "ニキビができやすいですか？"

common_skincare = {
    "q": "頬が乾燥しやすいですか？",
    "yes": {
        "q": Tzone,
        "yes": {
            "q":Nikibi,
            "yes":{"answer":"高保湿"},
            "no":{"answer":"高保湿"},
        },

        "no":{
            "q":Nikibi,
            "yes":{
                "q":"ニキビは主に乾燥部分にできますか？",
                "yes":{"answer":"高保湿ニキビ予防"},
                "no":{"answer":"ニキビ予防"}
            },
            "no": {
                "q":"使用感はさっぱりよりしっとりの方が好きですか？",
                "yes":{"answer":"高保湿"},
                "no":{"answer":"さっぱり系"}
                },
       }
    },
    "no": {
        "q": Tzone,
        "yes": {
            "q": Nikibi,
            "yes":{
                "q":"ニキビは主に乾燥部分にできますか？",
                "yes":{"answer":"高保湿"},
                "no":{"answer":"ニキビ予防"},
            },

            "no": {
                "q":"使用感はさっぱりよりしっとりの方が好きですか？",
                "yes":{"answer":"高保湿"},
                "no":{"answer":"さっぱり系"}
                },
        },
        "no": {
            "q":"少しの刺激で肌が赤くなったり、荒れたりしやすいですか？",
            "yes":{
                "q":Nikibi,
                "yes":{"answer":"刺激に弱いニキビ予防"},
                "no":{"answer":"刺激に弱いニキビ予防"}
              },
            "no":{
                "q":Nikibi,
                "yes":{"answer":"強力なニキビ予防"},
                "no":{"answer":"さっぱり系"}
              }
          }
        }
    }

# -----------------------------------------------------
# 判定を行う共通エンジン
# -----------------------------------------------------

def run_akinator(node):
    # 1. 答えに達した場合
    if "answer" in node:
        print(f"\n あなたにおすすめなのは【 {node['answer']} 】です！")
        return

    # 2. 質問の提示と入力の受け付け
    # 全角入力や大文字、前後の余計なスペースを自動で修正（正規化）します
    raw_input = input(f" {node['q']} (y/n): ")

    # 文字列の整理(全角英数を半角にし、小文字に揃える)
    # str.translate を使って簡易的に全角「ｙ」「ｎ」を半角に変換します
    zenkaku_to_hankaku = str.maketrans('ｙｎＹＮ', 'ynyn')
    cleaned_input = raw_input.translate(zenkaku_to_hankaku).strip().lower()

    # 3. 分岐処理
    if cleaned_input == 'y':
        run_akinator(node["yes"])
    elif cleaned_input == 'n':
        run_akinator(node["no"])
    else:
        print("⚠️ 'y' か 'n' で入力してください。もう一度質問します。")
        run_akinator(node) # 同じ質問をリトライ

# -----------------------------------------------------
# Webサイト用の共通エンジン
# -----------------------------------------------------

def get_current_node(answers, diagnosis_type="cleansing"):

    # 診断の種類によって、使う質問データを選ぶ
    if diagnosis_type == "cleansing":
        node = kurennzingu
    elif diagnosis_type in ["toner", "serum"]:
        node = common_skincare
    else:
        return None

    # これまでの回答に応じて質問を進める
    for answer in answers:

        # すでに診断結果に到達していたら終了
        if "answer" in node:
            break

        if answer == "yes":
            node = node["yes"]
        elif answer == "no":
            node = node["no"]

    # 現在の質問または診断結果を返す
    return node


