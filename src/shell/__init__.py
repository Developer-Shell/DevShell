class Shell:
    def __init__(self, download_url):
        self.download_url = download_url
    def execute(self, command: list[str | list[str] | None]) -> None | Exception:
        exec(f"import {command[0]}")
        if command[1] is not None:
            exec(f"{command[0]}.main()")
        else:
            exec(f"{command[0]}.main({command[1]})")

    def install(self, path, repo, branch="main"):
        import os, requests, zipfile

        if path.removesuffix("/") in os.listdir(path.removesuffix("/")):
            os.mkdir(path.removesuffix("/") + "/packages")

        repo = self.download_url + repo

        output_zip = "temp.zip"
        url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
        try:
            response = requests.get(url, stream=True)
        except ConnectionError:
            print("Connection Error!")
        updated = "Downloaded"

        with open(output_zip, "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        try:
            with zipfile.ZipFile(output_zip, "r") as zip_ref:
                found_files = [f for f in zip_ref.namelist()]
                if f"{path.removesuffix("/")}/PAM_Packages/{repo.split("/")[1]}-{branch}" in os.listdir(
                        f"{path.removesuffix("/")}/PAM_Packages/"):
                    updated = "Updated"
                for file in found_files:
                    zip_ref.extract(file, path.removesuffix("/") + "/PAM_Packages")

        except zipfile.BadZipfile:
            print("Could not find a package")
            os.remove("temp.zip")
            raise SystemExit

        os.remove(output_zip)
        print(f"{updated} package in {path.removesuffix("/")}/packages/{repo.split("/")[1]}-{branch}")
