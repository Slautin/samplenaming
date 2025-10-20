from notion_client import Client

class NotionLoader:
    def __init__(self, token = None):
        if token is None:
            raise ValueError('Please provide your token')
        self.notion = Client(auth=token)

        self.compositions = None
        self.samples = None

    def upload_compositions(self, database_id):
        self.original_compositions = self._query_database(database_id)
        self.compositions = {}

        for entry in self.original_compositions:
            id = entry['id']
            name = self._get_text(entry, 'Name')
            comment = self._get_text(entry, 'Brief description')
            samples = self._get_relation_id(entry['properties']['🧫 Samples'])
            self.compositions[id] = {
                'name': name,
                'comment': comment,
                'samples': samples,
                'created_by': entry['created_by']['id'],
                'created_time': entry['created_time'],
                'last_edited_by': entry['last_edited_by']['id'],
                'samples': samples
            }

    def upload_samples(self, database_id):
        self.original_samples = self._query_database(database_id)

        if self.compositions is None:
            load_composition = self._get_relation
        else:
            load_composition = lambda x: self._get_relation_locally(x, database=self.compositions)

        self.samples = {}
        for entry in self.original_samples:
            id = entry['id']
            name = self._get_text(entry, 'Name')

            status = (
                (entry.get("properties", {})
                 .get("Status", {})
                 .get("select") or {})
                .get("name", "N/A")
            )

            composition, composition_id = load_composition(entry['properties']['🧪Composition'])
            synthesis = self._get_multiselect(entry['properties']['Synthesis'])

            parent_sample = self._get_relation_id(entry['properties']['🧫 Parent Sample'])

            if len(parent_sample) == 0:
                parent_sample = 'N/A'
            else:
                parent_sample = parent_sample[0]

            assigned_to = self._get_people_id_email(entry['properties']['Assigned To'])
            datasets = self._get_relation_id(entry['properties']['🗂️ Datasets'])
            sub_samples = self._get_relation_id(entry['properties']['Sub-samples'])
            sources = self._get_relation_id(entry['properties']['👥 Source'])
            location = self._get_text(entry, 'Location')
            results = self._get_relation_id(entry['properties']['📊 Other Results'])



            self.samples[id] = {'name': name,
                                'status': status,
                                'composition': composition[0],
                                'composition_id': composition_id[0],
                                'synthesis': synthesis,
                                'closest_sample': parent_sample,
                                'created_by': entry['created_by']['id'],
                                'created_time': entry['created_time'],
                                'last_edited_by': entry['last_edited_by']['id'],
                                'assigned_to': assigned_to,
                                'datasets': datasets,
                                'sub_samples': sub_samples,
                                'location': location,
                                'results': results,
                                'sources': sources
                                }

    def upload_datasets(self, database_id):
        self.original_datasets = self._query_database(database_id)

        self.datasets = {}
        for entry in self.original_datasets:
            id = entry['id']
            name = self._get_text(entry, 'Name')
            link = entry['properties']['Link']['url']
            sample = self._get_relation_id(entry['properties']['🧫 Sample'])[0]
            characterization = self._get_multiselect(entry['properties']['Characterization'])
            comment = self._get_text(entry, 'Brief description')
            notebooks = self._get_relation_id(entry['properties']['📝 Notebooks'])
            source = self._get_relation_id(entry['properties']['👥Source'])

            self.datasets[id] = {
                'name': name,
                'link': link,
                'sample': sample,
                'characterization': characterization,
                'comment': comment,
                'notebooks': notebooks,
                'source': source
            }

    def upload_notebooks(self, database_id):
        # Query all entries from the Notion database
        self.original_notebooks = self._query_database(database_id)

        self.notebooks = {}
        for entry in self.original_notebooks:
            id = entry['id']
            name = self._get_text(entry, 'Name')

            # Optional link property (may be None)
            link = (
                entry.get('properties', {})
                .get('Link', {})
                .get('url', None)
            )

            # Relation to datasets
            datasets = self._get_relation_id(entry['properties']['🗂️ Datasets'])

            # Created_by info
            created_by = entry.get('created_by', {}).get('id', 'N/A')
            created_time = entry.get('created_time', 'N/A')
            last_edited_by = entry.get('last_edited_by', {}).get('id', 'N/A')
            last_edited_time = entry.get('last_edited_time', 'N/A')

            # Optional brief description or comment field
            comment = self._get_text(entry, 'Brief description')

            # If notebooks have any additional relevant property, e.g., Source or Tags
            source = (
                self._get_relation_id(entry['properties']['👥 Source'])
                if '👥 Source' in entry['properties']
                else []
            )

            self.notebooks[id] = {
                'name': name,
                'link': link,
                'datasets': datasets,
                'created_by': created_by,
                'created_time': created_time,
                'last_edited_by': last_edited_by,
                'last_edited_time': last_edited_time,
                'comment': comment,
                'source': source
            }

    def upload_results(self, database_id):
        # Query the Notion database
        self.original_results = self._query_database(database_id)

        self.results = {}
        for entry in self.original_results:
            id = entry['id']
            name = self._get_text(entry, 'Name')

            # Handle 'Type' select property
            type_ = (
                (entry.get("properties", {})
                 .get("Type", {})
                 .get("select") or {})
                .get("name", "N/A")
            )

            # Link field (may be None)
            link = (
                entry.get("properties", {})
                .get("Link", {})
                .get("url", None)
            )

            # Relation to Sample
            sample = self._get_relation_id(entry['properties']['🧫 Samples'])

            # Metadata from Notion
            created_by = entry.get("created_by", {}).get("id", "N/A")
            created_time = entry.get("created_time", "N/A")
            last_edited_by = entry.get("last_edited_by", {}).get("id", "N/A")
            last_edited_time = entry.get("last_edited_time", "N/A")

            # Optional description/comment property
            comment = self._get_text(entry, 'Brief description')

            # Optional Source relation, if present
            source = (
                self._get_relation_id(entry['properties']['👥 Source'])
                if '👥 Source' in entry['properties']
                else []
            )

            self.results[id] = {
                'name': name,
                'type': type_,
                'link': link,
                'sample': sample[0] if sample else 'N/A',
                'created_by': created_by,
                'created_time': created_time,
                'last_edited_by': last_edited_by,
                'last_edited_time': last_edited_time,
                'comment': comment,
                'source': source
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
    def _get_people_id_email(entry):
        ttype = entry['type']
        people = {}
        for person in entry[ttype]:
            id = person['id']
            email = person['person']['email']
            name = person['name']
            people[id] = {'name': name, 'e-mail': email}
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








