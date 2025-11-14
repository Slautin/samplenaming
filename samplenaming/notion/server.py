from flask import Flask, request, jsonify

from samplenaming.notion.notion_loader import NotionLoader
from dotenv import load_dotenv
import os

load_dotenv()

#database adresses
compositions_id = os.getenv("COMPOSITIONS_ID")
samples_id      = os.getenv("SAMPLES_ID")
datasets_id     = os.getenv("DATASETS_ID")
notebooks_id    = os.getenv("NOTEBOOKS_ID")
results_id      = os.getenv("RESULTS_ID")
people_id       = os.getenv("PEOPLE_ID")

#token
token=os.getenv("NOTION_TOKEN")
print(token)
folder_pass = os.getenv("FILE_DIR")

loader = NotionLoader(token)


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    res_dict = loader.get_data_from_sample_entry(data['data'])
    #print(res_dict)

    return jsonify({"status": "ok"}), 200

@app.route("/webhook_res", methods=["POST"])
def webhook_res():
    data = request.get_json(silent=True)
    res_dict = loader.get_data_from_result_entry(data['data'])
    #print(res_dict)

    return jsonify({"status": "ok"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)