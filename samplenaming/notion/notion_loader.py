from notion_client import Client
import os
import json
from datetime import datetime, timezone
from samplenaming.core.snglobal import CSV_HEADERS
from samplenaming.core.classes import SNComposition, QRCode
from samplenaming.notion.aux import upload_qr
from samplenaming.periodictable.composition import Composition

from dotenv import load_dotenv
import requests

load_dotenv()  # reads .env file
folder = os.getenv("FILE_DIR")

class NotionLoader:
    def __init__(self, token = None):
        if token is None:
            raise ValueError('Please provide your token')
        self.notion = Client(auth=token)
        self.compositions = None
        self.samples = None

        self.token = token
    
    def upload_samples(self, database_id, update=True):

        if update:
            self.original_samples = self.query_updated_pages(database_id)
        else:
            self.original_samples = self._query_database(database_id)

        self.samples = {}
        for entry in self.original_samples:
            res_dict = self.get_data_from_sample_entry(entry)
            self.samples[res_dict["EntryID"]] = res_dict

    def get_data_from_sample_entry(self, entry):
        props = entry.get("properties", {})
        id = entry["id"]
        name = self._get_text(entry, "Name")

        status = (
            (props.get("Status", {}).get("select") or {}).get("name", "")
        )

        sample_type = (
            (props.get("Sample type", {}).get("select") or {}).get("name", "")
        )

        history = [id, ]

        if sample_type == "Sub-Sample":
            parent_sample = self._get_relation_id(props.get("Parent Sample", {}))[0]
            _parent_page = self.notion.pages.retrieve(parent_sample)
            composition = self._get_text(_parent_page, "Composition")

            history.extend(self._get_sample_history(parent_sample))

        else:
            composition = self._get_text(entry, "Composition")
            parent_sample = ""

        try:
            a = SNComposition(composition)
            comp = Composition(a.compstr)
            elements = [e.symbol for e in comp.elements]
            self._post_composition(id, a.compstr, elements)
        except:
            print('Composition is incorrect')
        
        proc_details = self._get_text(entry, 'Processing Details')
        location = self._get_text(entry, 'Location')
        synthesis = self._get_multiselect(props.get("Synthesis", {}))
        synth_details = self._get_text(entry, 'Synthesis Details')
        processing = self._get_multiselect(props.get("Processing", {}))
        

        if 'Radiation' in processing:
            radiation = True
        else:
            radiation = False

        sources = self._get_relation_id(props.get("Source", {}))
        assigned_to = self._get_people_id_email(props.get("Assigned To", {}))

        #upload_qrcode
        qr_ = QRCode(entry['url'])
        img = qr_.generate_qrimage()
        qr_name = name+"_qr.png"
        upload_qr(img, id, self.token, qr_name)

        file_dir = os.path.join(folder,
                                        composition.replace("/", "_"),
                                        name.replace("/", "_")
                                        )

        qr_.save_qr(img, file_dir, qr_name)


        return {
            "EntryID": id,
            "CommonName": name,
            "Composition": composition,
            "Elements": elements,
            "Status": status,

            "Synthesis": synthesis,
            "SynDetails": synth_details,
            "Processing": processing,
            "ProcDetails": proc_details,
            "Radiation": radiation,
            "Location": location,

            "iCreated": entry["created_by"]["id"],
            "iUsage": assigned_to,
            "YourName": entry["last_edited_by"]["id"],
            "DateTime": entry["last_edited_time"],
            "ResearchGroup": sources,

            "NearestSampleID": parent_sample,
            "History": history,
            "FirstSampleID": history[-1]
        }

    def upload_results(self, database_id, update=True):
        # Query the Notion database
        if update:
            self.original_results = self.query_updated_pages(database_id, db='results')
        else:
            self.original_results = self._query_database(database_id)

        self.results = {}
        for entry in self.original_results:
            res_dict = self.get_data_from_result_entry(entry)
            self.results[res_dict["EntryID"]] = res_dict

    def get_data_from_result_entry(self, entry):
        props = entry.get("properties", {})
        
        id = entry['id']
        name = self._get_text(entry, 'Name')

        type_ = (
            (props.get("Data Type", {}).get("select") or {}).get("name", "")
        )

        upload_method_ = (
            (props.get("Upload Method", {}).get("select") or {}).get("name", "")
        )

        comment = self._get_text(entry, 'Brief Description')
        characterization = self._get_multiselect(props.get("Characterization", {}))

        sample = self._get_relation_id(entry['properties']['Sample'])[0]
        _sample_page = self.notion.pages.retrieve(sample)
        sample_dict = self.get_data_from_sample_entry(_sample_page)
        assigned_to = self._get_people_id_email(props.get("Assigned To", {}))
        sources = self._get_relation_id(props.get("Source", {}))

        #upload qr_code
        qr_ = QRCode(entry['url'])
        img = qr_.generate_qrimage()
        qr_name = name+"_qr.png"

        upload_qr(img, id, self.token, qr_name)
        
        file_names = []
        link = None
        file_dir = ""

        if upload_method_ == 'link':
            link = (props.get("Link", {}).get("url", None))

        if upload_method_ == 'file':
            files_ = props['Files']['files']

            file_dir = os.path.join(folder,
                                        sample_dict['Composition'].replace("/", "_"),
                                        sample_dict['CommonName'].replace("/", "_")
                                        )
            os.makedirs(file_dir, exist_ok=True)

            for fs in files_:
                filename = fs['name']
                url = fs['file']['url']
                file_names.append(filename)

                file_path = os.path.join(file_dir, filename)

                r = requests.get(url)
                with open(file_path, "wb") as f:
                    f.write(r.content)

                qr_.save_qr(img, file_dir, qr_name)

        #upload qr
        


            return {
            "EntryID": id,
            "CommonName": name,
            "Composition": sample_dict['Composition'],
            "Elements": sample_dict['Elements'],

            "Characterization": characterization,
            "CharDetails": comment,
            "DataType": type_,

            "FileLinks": link,
            "FileFolder": file_dir,
            "FileHeader": file_names,


            "Synthesis": sample_dict['Synthesis'],
            "SynDetails": sample_dict['SynDetails'],
            "Processing": sample_dict['Processing'],
            "ProcDetails": sample_dict['ProcDetails'],
            "Radiation": sample_dict['ProcDetails'],
            "Location": sample_dict['Location'],

            "iCreated": entry["created_by"]["id"],
            "iUsage": assigned_to,
            "YourName": entry["last_edited_by"]["id"],
            "DateTime": entry["last_edited_time"],
            "ResearchGroup": sources,

            "NearestSampleID": sample,
            "History": sample_dict['History'],
            "FirstSampleID": sample_dict['FirstSampleID']
            }

    def upload_people(self, database_id):
        # Query the database
        self.original_people = self._query_database(database_id)

        self.people = {}
        for entry in self.original_people:
            id = entry['id']
            name = self._get_text(entry, 'Person')

            # If there is an “Email” or “Contact” field (rich_text or email type)
            email = (
                        entry.get("properties", {})
                        .get("Email", {})
                        .get("email")  # or get("rich_text")[0]["plain_text"] if rich_text
                    ) or "N/A"

            # Metadata fields
            created_by = entry.get("created_by", {}).get("id", "N/A")
            created_time = entry.get("created_time", "N/A")
            last_edited_by = entry.get("last_edited_by", {}).get("id", "N/A")
            last_edited_time = entry.get("last_edited_time", "N/A")

            # Optional comment/brief description
            affiliation = self._get_text(entry, 'Affiliation')

            self.people[id] = {
                'name': name,
                'email': email,
                'created_by': created_by,
                'created_time': created_time,
                'last_edited_by': last_edited_by,
                'last_edited_time': last_edited_time,
                'affiliation': affiliation
            }

    def _query_database(self, database_id):
        response = self.notion.databases.query(
            **{
                "database_id": database_id,
            }
        )
        return response['results']

    def _query_page(self, page_id):
        page = self.notion.pages.retrieve(page_id=page_id)
        return page

    @staticmethod
    def _get_text(entry, key):
        ttype = entry['properties'][key]['type']
        rich_text = entry['properties'][key][ttype]
        if len(rich_text) > 0:
            return rich_text[0]['plain_text']
        else:
            return 'N/A'

    @staticmethod
    def _get_multiselect(entry):
        if len(entry['multi_select']) == 0:
            return 'N/A'
        names = []
        for ent in entry['multi_select']:
            names.append(ent['name'])
        return names

    @staticmethod
    def _get_relation_id(entry):
        return [rel['id'] for rel in entry['relation']]
    
    @staticmethod
    def _get_people_id_email( entry):
        """
        Safely extract user IDs, names, and emails from a Notion 'people' property.
        Handles missing or malformed fields gracefully.
        """
        if not entry or entry.get("type") != "people":
            return {}

        people = {}
        for person in entry.get("people", []):
            user_id = person.get("id", "N/A")
            name = person.get("name", "Unknown")
            email = (
                person.get("person", {}).get("email")  # safe access
                if "person" in person
                else person.get("owner", {}).get("email", "N/A")  # edge case
            )
            people[user_id] = {"name": name, "email": email or "N/A"}

        return people

    def _get_relation(self, entry):
        if entry['type'] != 'relation':
            raise TypeError('_get_relation() is applicable only to relation properties')

        if len(entry['relation']) == 0:
            return ['N/A',], None

        names, ids = [], []
        for rel in entry['relation']:
            id = rel['id']
            page = self._query_page(id)
            names.append(self._get_text(page, 'Name'))
            ids.append(id)
        return names, ids

    def _get_relation_locally(self, entry, database):
        if entry['type'] != 'relation':
            raise TypeError('_get_relation() is applicable only to relation properties')

        if len(entry['relation']) == 0:
            return ['N/A',], ['N/A',]

        names, ids = [], []
        for rel in entry['relation']:
            id = rel['id']
            names.append(database[id]['name'])
            ids.append(id)
        return names, ids

    def _post_composition(self, page_id, composition, elements):
        dictt = {"Composition": {"rich_text": [{'text': {'content': composition}}]},}
        dictt.update(self._make_multiselect_property("Elements", elements))
        print(dictt)
        self.notion.pages.update(
            **{
                "page_id": page_id,
                "properties": dictt
            }
        )

# --- Incremental sync helpers ---
    @staticmethod
    def parse_notion_time(ts):
        """Parse Notion timestamp literally, without timezone conversion."""
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def to_notion_format(dt):
        """Return ISO string in Notion-like format."""
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _save_last_timestamp(self, dt, filename="notion_state.json", db='sample'):
        """Update or create 'last_timestamp_<db>' field in JSON file without overwriting others."""
        ts_str = self.to_notion_format(dt)  # ✅ format datetime → string

        # Step 1: Load existing content if file exists
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # If file is empty or invalid JSON
        else:
            data = {}

        # Step 2: Update or add the timestamp field
        data[f"last_timestamp_{db}"] = ts_str

        # Step 3: Save updated data back to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def _datetime_to_iso(self, dt):
        """Convert datetime → Notion-compatible ISO string."""
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def _load_last_timestamp(self, filename="notion_state.json", db='sample'):
        """Load last sync timestamp from file."""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                if f"last_timestamp_{db}" in data:
                    return datetime.fromisoformat(data[f"last_timestamp_{db}"].replace("Z", "+00:00"))
        return None
   
    def query_updated_pages(self, database_id, timestamp=None, db='sample'):
        """
        Query database for pages created or updated after `timestamp`.
        If `timestamp` is None, returns all.
        Automatically updates saved timestamp.
        """
        if timestamp is not None:
            ts = timestamp
        else:
            ts = self._load_last_timestamp(db=db)

        if ts:
            ts_str = ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            filter_clause = {
                "or": [
                    {"timestamp": "last_edited_time", "last_edited_time": {"after": ts_str}},
                    {"timestamp": "created_time", "created_time": {"after": ts_str}},
                ]
            }
            response = self.notion.databases.query(database_id=database_id, filter=filter_clause)
        else:
            response = self.notion.databases.query(database_id=database_id)
        results = response["results"]
        if results:
            new_ts = max(self.parse_notion_time(r["last_edited_time"]) for r in results)
            self._save_last_timestamp(new_ts, db=db)

        return results
  
    @staticmethod
    def _make_multiselect_property(property_name: str, values):
        """
        Prepare a Notion-compatible multi_select property.

        Args:
            property_name (str): Name of the property in your Notion database.
            values (list | str): Either a list of choices or a comma-separated string.

        Returns:
            dict: Property entry for Notion API.
        """
        # If it's a comma-separated string, split it
        if isinstance(values, str):
            values = [v.strip() for v in values.split(",") if v.strip()]

        # If it's empty or None
        if not values:
            return {property_name: {"multi_select": []}}

        # Convert to proper Notion structure
        return {
            property_name: {
                "multi_select": [{"name": str(v)} for v in values]
            }
        }

    def _get_sample_history(self, page_id: str):
        """
        Retrieve a single property value from a Notion page using its display name.
        """
        flag = True
        history = [page_id, ]
        while flag:
            page = self.notion.pages.retrieve(page_id)
            parent_sample = self._get_relation_id(page["properties"].get("Parent Sample", {}))
            parent_sample = parent_sample[0] if parent_sample else ""
            if parent_sample != "":
                history.append(parent_sample)
                page_id = parent_sample
            else:
                flag = False
        return history


class SNRecord:
    def __init__(self, **kwargs):
        for key in CSV_HEADERS:
            value = kwargs.get(key, "")
            # Convert lists or tuples to comma-separated strings
            if isinstance(value, (list, tuple)):
                value = ",".join(map(str, value))
            setattr(self, key, value)

        if not getattr(self, "nFiles", None):
            setattr(self, "nFiles", 0)
        if not getattr(self, "FileLinks", None):
            setattr(self, "FileLinks", "")
        if not getattr(self, "History", None):
            setattr(self, "History", "")

    def to_dict(self):
        return {key: getattr(self, key, "") for key in CSV_HEADERS}



