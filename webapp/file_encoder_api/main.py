from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse,Response
import hashlib
import uvicorn
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
from bson import ObjectId
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Counter: total HTTP requests
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

load_dotenv()

# mongo_password = os.getenv("MONGO_PASSWORD")
# mongo_username = os.getenv("MONGO_USERNAME")

# client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@172.16.61.138:27017")
client = MongoClient("mongodb://172.16.61.150:27017")

if client is None:
    raise Exception("Failed to connect to MongoDB")

db = client['pass_hash_db']
ccollection = db['pass_hash_collection']

# Ensure uniqueness on file_hash
ccollection.create_index("file_hash", unique=True)

app = FastAPI()


@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    endpoint = request.url.path
    method = request.method
    status = response.status_code
    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=status).inc()
    return response



# temporary storage
files = []
last_uploaded_raw = ""  # keep original file content for hashing

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
    <head>
        <title>Password Hasher DB</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                padding: 20px;
            }
            h1, h2 { color: #333; }
            form {
                background: #fff;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input[type=file], input[type=text], input[type=submit] {
                padding: 8px;
                margin: 5px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            input[type=submit] {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            input[type=submit]:hover { background-color: #45a049; }
            .red { background-color: #f44336; }
            .blue { background-color: #2196F3; }
            .yellow { background-color: #ff9800; }
            .green { background-color: #4CAF50; }
            pre { background: #e8e8e8; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Password Hasher DB</h1>

        <!-- Upload File -->
        <h2>Upload Raw File</h2>
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
            <input name="file" type="file" required>
            <input type="submit" value="Upload" class="green">
        </form>

        <!-- Hash Last Uploaded File -->
        <h2>Hash Last Uploaded File</h2>
        <form action="/hashfile/" method="post">
            <input type="submit" value="Hash & Save" class="blue">
        </form>

        <!-- List All Files -->
        <h2>List All Files</h2>
        <form action="/files/" method="get" onsubmit="listFiles(event)">
            <input type="submit" value="Show Files" class="yellow">
        </form>
        <pre id="files_list"></pre>

        <!-- Read File By ID -->
        <h2>Read File by ID</h2>
        <form onsubmit="readFile(event)">
            <input id="read_id" type="text" placeholder="Enter File ID" required>
            <input type="submit" value="Read File" class="green">
        </form>
        <pre id="read_result"></pre>

        <!-- Delete File By ID -->
        <h2>Delete File by ID</h2>
        <form onsubmit="deleteFile(event)">
            <input id="delete_id" type="text" placeholder="Enter File ID" required>
            <input type="submit" value="Delete File" class="red">
        </form>
        <pre id="delete_result"></pre>

        <!-- Update File By ID -->
        <h2>Update File by ID</h2>
        <form onsubmit="updateFile(event)" enctype="multipart/form-data">
            <input id="update_id" type="text" placeholder="Enter File ID" required><br>
            <input id="update_file" name="file" type="file" required><br>
            <input type="submit" value="Update File" class="blue">
        </form>
        <pre id="update_result"></pre>

        <!-- Search User -->
        <h2>Search User by ID</h2>
        <form onsubmit="getUserById(event)">
            <input id="user_id" type="text" placeholder="Enter User ID" required>
            <input type="submit" value="Search" class="green">
        </form>
        <pre id="user_id_result"></pre>

        <h2>Search User by Username</h2>
        <form onsubmit="getUserByUsername(event)">
            <input id="username" type="text" placeholder="Enter Username" required>
            <input type="submit" value="Search" class="green">
        </form>
        <pre id="user_name_result"></pre>

        <script>
            async function listFiles(event){
                event.preventDefault();
                const res = await fetch('/files/');
                const data = await res.json();
                document.getElementById('files_list').textContent = JSON.stringify(data, null, 2);
            }

            async function readFile(event){
                event.preventDefault();
                const id = document.getElementById('read_id').value;
                const res = await fetch(`/files/${id}`);
                const data = await res.json();
                document.getElementById('read_result').textContent = JSON.stringify(data, null, 2);
            }

            async function deleteFile(event){
                event.preventDefault();
                const id = document.getElementById('delete_id').value;
                const res = await fetch(`/files/${id}`, { method: 'DELETE' });
                const data = await res.json();
                document.getElementById('delete_result').textContent = JSON.stringify(data, null, 2);
            }

            async function updateFile(event){
                event.preventDefault();
                const id = document.getElementById('update_id').value;
                const file = document.getElementById('update_file').files[0];
                const formData = new FormData();
                formData.append('file', file);
                const res = await fetch(`/files/${id}`, { method: 'PUT', body: formData });
                const data = await res.json();
                document.getElementById('update_result').textContent = JSON.stringify(data, null, 2);
            }

            async function getUserById(event){
                event.preventDefault();
                const id = document.getElementById('user_id').value;
                const res = await fetch(`/user/id/${id}`);
                const data = await res.json();
                document.getElementById('user_id_result').textContent = JSON.stringify(data, null, 2);
            }

            async function getUserByUsername(event){
                event.preventDefault();
                const username = document.getElementById('username').value;
                const res = await fetch(`/user/username/${username}`);
                const data = await res.json();
                document.getElementById('user_name_result').textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    global last_uploaded_raw

    content = await file.read()
    text = content.decode("utf-8") if isinstance(content, bytes) else content
    last_uploaded_raw = text  # save raw file content for hashing

    users = {}
    for line in text.splitlines():
        if ":" in line:
            username, password = line.split(":", 1)
            users[username.strip()] = password.strip()

    # store both filename and users
    files.append({"filename": file.filename, "users": users})
    return JSONResponse(content={"filename": file.filename, "users": users})

# Get user by username
@app.get("/user/username/{username}")
def get_user_by_username(username: str):
    for doc in ccollection.find():
        for user in doc["users"]:
            if user["username"] == username:
                return user
    return JSONResponse(content={"error": "User not found"}, status_code=404)

@app.get("/show/")
def show_files():
    if not files:
        return JSONResponse(content={"error": "No files uploaded"}, status_code=404)
    return JSONResponse(content=files[-1])


# Get user by user ID
@app.get("/user/id/{user_id}")
def get_user_by_id(user_id: int):
    for doc in ccollection.find():
        for user in doc["users"]:
            if user["_id"] == user_id:  # both are now ints
                return user
    return JSONResponse(content={"error": "User not found"}, status_code=404)



@app.post("/hashfile/")
def hash_file():
    global last_uploaded_raw

    if not files:
        return JSONResponse(content={"error": "No file uploaded"}, status_code=400)

    last_file = files[-1]
    raw_users = last_file["users"]
    filename = last_file["filename"]

    users_with_ids = []
    for i, (username, password) in enumerate(raw_users.items()):
        users_with_ids.append({
            "_id": i,  # integer ID
            "username": username,
            "hashed_password": hashlib.sha512(password.encode()).hexdigest()
        })

    # Compute file hash
    file_hash = hashlib.sha256(last_uploaded_raw.encode()).hexdigest()

    try:
        ccollection.insert_one({
            "file_name": filename,
            "file_hash": file_hash,
            "users": users_with_ids
        })
    except errors.DuplicateKeyError:
        return JSONResponse(
            content={"error": "This file already exists in the database"},
            status_code=400,
        )

    return JSONResponse(
        content={
            "message": "File successfully hashed and uploaded to the database",
            "file_name": filename,
            "users": users_with_ids
        },
        status_code=201,
    )


@app.get("/files/{file_id}")
def get_file(file_id: str):
    try:
        doc = ccollection.find_one({"_id": ObjectId(file_id)})
        if not doc:
            return JSONResponse(content={"error": "File not found"}, status_code=404)
        doc["_id"] = str(doc["_id"])
        return doc
    except Exception:
        return JSONResponse(content={"error": "Invalid file id"}, status_code=400)

@app.delete("/files/{file_id}")
def delete_file(file_id: str):
    try:
        result = ccollection.delete_one({"_id": ObjectId(file_id)})
        if result.deleted_count == 0:
            return JSONResponse(content={"error": "File not found"}, status_code=404)
        return {"message": f"File {file_id} deleted successfully"}
    except Exception:
        return JSONResponse(content={"error": "Invalid file id"}, status_code=400)



@app.get("/files/")
def list_files():
    files = []
    for doc in ccollection.find({}, {"file_name": 1, "file_hash": 1}):
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string for JSON
        files.append(doc)
    return {"files": files}


@app.get("/files/{file_id}/users")
def get_file_users(file_id: str):
    try:
        doc = ccollection.find_one({"_id": ObjectId(file_id)}, {"users": 1})
        if not doc:
            return JSONResponse(content={"error": "File not found"}, status_code=404)
        return {"file_id": file_id, "users": doc["users"]}
    except Exception:
        return JSONResponse(content={"error": "Invalid file id"}, status_code=400)


@app.put("/files/{file_id}")
async def update_file(file_id: str, file: UploadFile):
    try:
        # Read uploaded file
        content = await file.read()
        text = content.decode('utf-8') if isinstance(content, bytes) else content

        # Parse and hash users
        new_users = {}
        for line in text.splitlines():
            if ':' in line:
                username, password = line.split(':', 1)
                hashed_password = hashlib.sha512(password.strip().encode()).hexdigest()
                new_users[username.strip()] = hashed_password

        # Compute new file hash for uniqueness check
        file_hash = hashlib.sha256(text.encode()).hexdigest()

        # Update MongoDB document
        result = ccollection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": {"hashed_users": new_users, "file_hash": file_hash, "file_name": file.filename}}
        )

        if result.matched_count == 0:
            return JSONResponse(content={"error": "File not found"}, status_code=404)

        return {"message": "File updated successfully", "file_id": file_id, "hashed_users": new_users}

    except errors.DuplicateKeyError:
        return JSONResponse(content={"error": "Another file with the same content already exists"}, status_code=400)
    except Exception:
        return JSONResponse(content={"error": "Invalid file id"}, status_code=400)




@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)


