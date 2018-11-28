import os, zipfile
import json

appConfigFilePath = os.getcwd()+'/app.json'
# Load config files

with open(appConfigFilePath) as config_json_file:
    appConfig = json.load(config_json_file)

fileName = appConfig['fileName']
fileTargetPath = appConfig['dataFolder']

with zipfile.ZipFile(fileTargetPath + fileName,"r") as zip_ref:
    for zip_info in zip_ref.infolist():
        if zip_info.filename[-1] == '/':
            continue
        zip_info.filename = os.path.basename(zip_info.filename)
        print(zip_info)
        zip_ref.extract(zip_info, fileTargetPath)