from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# لینک API (الان دیتای سفارشات ووکامرس)
URL = "https://account4allmail.ir/export.php?table=wp_wc_order_stats"

# خوندن دیتا
df = pd.read_json(URL)

@app.route("/", methods=["GET", "POST"])
def index():
    global df
    preview = df.head(5)  # فقط ۵ ردیف اول
    
    if request.method == "POST":
        new_names = {}
        for old_col in df.columns:
            new_name = request.form.get(old_col, old_col)
            new_names[old_col] = new_name
        df.rename(columns=new_names, inplace=True)
        df.to_csv("renamed_table.csv", index=False)  # ذخیره CSV
        return redirect(url_for("index"))

    return render_template("index.html", columns=df.columns, preview=preview.to_html(classes="table table-striped"))

if __name__ == "__main__":
    app.run(debug=True)
