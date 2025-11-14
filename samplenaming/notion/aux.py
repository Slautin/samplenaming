import requests
from dotenv import load_dotenv
import os
from samplenaming.core.classes import QRCode
from io import BytesIO


def upload_qr(img, page_id, token, name="qr.png"):

    #image bufferization
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    #headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2025-09-03",#"2022-06-28",
    }

    #get temporary link to upload
    r = requests.post(
    "https://api.notion.com/v1/file_uploads",
    headers=headers,)

    upload_url = r.json()['upload_url']

    files = {
    "file": (name, buffer, "image/png"),
    }
    data = {"part_number": "1"}
    r2 = requests.post(upload_url, headers=headers, files=files, data=data)
    file_id = r2.json()["id"]

    page_payload = {
        "properties": {
                        "QRCode": {
                        "type": "files",
                        "files": [
                                    {
                                    "name": name,
                                    "type": "file_upload",
                                    "file_upload": {"id": file_id },
                                    }
                                ]
                            }
                        }
    }


    r2 = requests.patch(f"https://api.notion.com/v1/pages/{page_id}",
                headers=headers, json=page_payload)
    
    print(r2.status_code)




# if __name__ == "__main__":
#     load_dotenv()
#     token=os.getenv("NOTION_TOKEN")
#     page_id = "28a6e75c45cb80e4958be222a2ecacad"

#     qr = QRCode("https://www.notion.so/camm-sample-tracking/Presentation-1-28a6e75c45cb80e4958be222a2ecacad?v=669a966bfe534e92a9aacceebdc3a1b2&source=copy_link")
#     img = qr.generate_qrimage('ffd')

#     upload_qr(img, page_id, name="qr.png")
