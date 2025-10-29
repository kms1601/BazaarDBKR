import os
import zipfile

from data.const import CWD

FILES = [CWD + "/../popup", CWD + "/../const.js", CWD + "/../content.js", CWD + "/../data.js", CWD + "/../icon128.png", CWD + "/../manifest.json"]

def make_zip_file():
    base_dir = os.path.abspath(os.path.join(CWD, ".."))
    with zipfile.ZipFile(CWD + "/../BazaarDBKR.zip", "w") as zipf:
        for file in FILES:
            if os.path.isdir(file):
                for root, _, files in os.walk(file):
                    for f in files:
                        file_path = os.path.join(root, f)
                        zipf.write(file_path, os.path.relpath(file_path, base_dir))
            else:
                zipf.write(file, os.path.relpath(file, base_dir))

    print("BazaarDBKR.zip 파일 생성 완료!.")


if __name__ == '__main__':
    make_zip_file()