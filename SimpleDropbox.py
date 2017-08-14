import dropbox

class SimpleDropbox:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

    def download_file_to_machine(self, where_to_save_path, remote_file_path):
        dbx = dropbox.Dropbox(self.access_token)
        dbx.files_download_to_file(where_to_save_path, remote_file_path)