
from flask import Flask, render_template, request, redirect, url_for, session
import os

# 診断プログラムを読み込む
from diagnosis import get_current_node

# Flaskの準備
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")


# トップページ・診断ページ
@app.route("/", methods=["GET", "POST"])
def home():

    # これまでの回答を取得する
    answers = session.get("answers", [])

    # 診断するアイテムを取得する
    diagnosis_type = session.get("diagnosis_type")

    # ボタンが押されたとき
    if request.method == "POST":

        # アイテム選択ボタンが押された場合
        selected_item = request.form.get("item")

        if selected_item in ["cleansing", "toner", "serum"]:
            session["diagnosis_type"] = selected_item
            session["answers"] = []
            return redirect(url_for("home"))

        # はい・いいえボタンが押された場合
        answer = request.form.get("answer")

        if answer in ["yes", "no"] and diagnosis_type:
            answers.append(answer)
            session["answers"] = answers

        return redirect(url_for("home"))

    # まだアイテムが選ばれていない場合
    if not diagnosis_type:
        return render_template(
            "index.html",
            selected_item=None,
            node=None
        )

    # 選んだアイテムに応じて質問・結果を取得
    node = get_current_node(answers, diagnosis_type)

    return render_template(
        "index.html",
        selected_item=diagnosis_type,
        node=node
    )


# 診断を最初からやり直す
@app.route("/restart")
def restart():
    session.pop("answers", None)
    session.pop("diagnosis_type", None)
    return redirect(url_for("home"))


# Flaskを起動する
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)