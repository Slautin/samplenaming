from flask import Flask, request, jsonify

from notion_client import Client
from notion_loader import NotionLoader
from core.classes import SNComposition, PrettyFormula

a = SNComposition('BaTiO3') 
b = PrettyFormula('BaTiO3')
print(a.compstr, b)

#database adresses
compositions_id = "2866e75c45cb80008c31ff983263ec54"
samples_id = "2866e75c45cb804884f1c0d76d555431"
datasets_id = "2331cf7faaeb4aed9e02630ad4374f83"
notebooks_id = "9bafd0ac9a3b4068a2fcca73bdc6c664"
results_id = "37d1952c479d4ebc9122d4b4b2dcf707"
people_id = "8e779a7364db43ec9935d78d7130c288"

#token
token=""

loader = NotionLoader(token)



app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    res_dict = loader.get_data_from_sample_entry(data['data'])
    print(res_dict)

    #print(data['data'])

    #print("📩 Received webhook data:", data)
    return jsonify({"status": "ok"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)