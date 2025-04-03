# from fastapi import FastAPI, File, UploadFile
# import pandas as pd
# from io import StringIO
# import json
# import os

# app = FastAPI()

# FILES_JSON_PATH = "files.json"
# CHUNK_SIZE = 1000  # Define chunk size for large files


# @app.post("/upload-csv/")
# async def upload_csv(file: UploadFile = File(...)):
#     # Read and process file
#     content = await file.read()
#     decoded_content = content.decode("utf-8")
#     df = pd.read_csv(StringIO(decoded_content), header=0)
    
#     # Clean column names and replace NaN/Infinity values
#     df.columns = df.columns.str.strip()
#     df.fillna("", inplace=True)
#     df.replace([float("inf"), float("-inf")], None, inplace=True)

#     # Load existing data from JSON
#     existing_data = {}
#     if os.path.exists(FILES_JSON_PATH):
#         with open(FILES_JSON_PATH, "r") as json_file:
#             try:
#                 existing_data = json.load(json_file)
#             except json.JSONDecodeError:
#                 pass

#     # Split DataFrame into chunks and save to JSON
#     chunks = [df[i:i + CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]
#     for idx, chunk in enumerate(chunks):
#         existing_data[f"{file.filename}_chunk_{idx}"] = chunk.to_dict(orient="records")

#     with open(FILES_JSON_PATH, "w") as json_file:
#         json.dump(existing_data, json_file, indent=4)

#     return {"message": "File processed and saved successfully", "filename": file.filename}















from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO
import json
import os

app = FastAPI()

FILES_JSON_PATH = "files.json"
CHUNK_SIZE = 1000  # Define chunk size for large files

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Read and process file
    content = await file.read()
    decoded_content = content.decode("utf-8")
    df = pd.read_csv(StringIO(decoded_content), header=0)

    # Clean column names and replace NaN/Infinity values
    df.columns = df.columns.str.strip()
    df.fillna("", inplace=True)
    df.replace([float("inf"), float("-inf")], None, inplace=True)

    # Load existing data from JSON
    existing_data = {}
    if os.path.exists(FILES_JSON_PATH):
        with open(FILES_JSON_PATH, "r") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                pass

    # Split DataFrame into chunks and save to JSON
    chunks = [df[i:i + CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks):
        existing_data[f"{file.filename}_chunk_{idx}"] = chunk.to_dict(orient="records")

    with open(FILES_JSON_PATH, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    return {"message": "File processed and saved successfully", "filename": file.filename}
