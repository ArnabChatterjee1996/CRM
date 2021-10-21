class ApiUtils:
    def __init__(self):
        self.baseUrl = "https://api.pipedrive.com/v1"
        self.detail_person_url = "{}/persons/".format(self.baseUrl)
        self.search_person_by_name_url = "{}/persons/find".format(self.baseUrl)
        self.add_note_url = "{}/notes".format(self.baseUrl)