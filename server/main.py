# from typing import List, Optional
# import os
# import shutil
# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pymongo import MongoClient
# from pydantic import BaseModel
# from api import generate_content, pdf_to_images, generate_from_pdf


# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# # MongoDB connection
# client = MongoClient("mongodb+srv://gautampatil:MGsxw0XPIc2qFGaK@gautam.5nbd8ho.mongodb.net/?retryWrites=true&w=majority")
# db = client['user-database-ai']
# posts = db['posts']

# # Define Pydantic models
# class ContentData(BaseModel):
#     userSub: str
#     content: List[str]

# class UserData(BaseModel):
#     userSub: str
#     content: Optional[List[str]] = []

# # API routes
# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# @app.put("/users/posts/")
# def receive_content(data: ContentData):
#     try:
#         # Check if the user exists in the collection
#         existing_user = posts.find_one({"userSub": data.userSub})
#         print(data.con)
#         if existing_user:
#             # If the user exists, update the content array
#             posts.update_one(
#                 {"userSub": data.userSub},
#                 {"$addToSet": {"content": {"$each": data.content}}}
#             )
#             return {"message": "Data Updated."}
#         else:
#             # If the user does not exist, insert a new document
#             posts.insert_one(data.dict())
#             return {"message": "Data Inserted."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/user/{item_id}")
# def read_item(item_id: str):
#     user_data = posts.find_one({"userSub": item_id}, {'_id': 0})
#     if user_data:
#         return user_data
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(None), prompt: str = Form(None)):
#     try:
#         if not file and not prompt:
#             raise HTTPException(status_code=400, detail="No file or prompt provided.")

#         result = ""
#         if file:
#             # Handle file upload
#             if file.filename.endswith('.pdf'):
#                 pdf_to_images(file.filename)
#                 result += generate_from_pdf(prompt)
#             else:
#                 result += generate_content(prompt=prompt, image=file.filename)

#             # Remove uploaded file
#             os.remove(file.filename)
#         elif prompt:
#             # Generate content based on prompt
#             result = generate_content(prompt=prompt)

#         return {"message": "File uploaded successfully", "prompt": prompt, "result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from typing import Union
import os
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware
from api import generate_content, pdf_to_images, generate_from_pdf
from pymongo import MongoClient, UpdateOne
from typing import Optional, List
import json
from pydantic import BaseModel


client = MongoClient("mongodb+srv://gautampatil:MGsxw0XPIc2qFGaK@gautam.5nbd8ho.mongodb.net/?retryWrites=true&w=majority")
db = client['user-database-ai']
collection = db['user-database-collection']
posts = db['posts']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL if you want to restrict it
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class ContentData(BaseModel):
    userSub : str
    content : List[str]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/users/posts/")
def receive_content(data: ContentData):
    try:
        data_dict = data.dict()
        # Check if the user exists in the collection
        existing_user = posts.find_one({"userSub": data_dict["userSub"]})
        if existing_user:
            # If the user exists, update the content array
            posts.update_one(
                {"userSub": data_dict["userSub"]},
                {"$addToSet": {"content":{"$each" : data_dict["content"]}}}
            )
            return {"Message": "Data Updated."}
        else:
            # If the user does not exist, insert a new document
            posts.insert_one(data_dict)
            return {"Message": "Data Inserted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{item_id}")
def read_item(item_id: str, q: Optional[str] = None):
    return posts.find_one({"userSub": item_id}, {'_id': 0})
    
    
    

@app.post("/upload")
async def upload_file(file: UploadFile = File(None), prompt: str = Form(None)):
    if file is None and prompt is None:
        return JSONResponse(content={"Message": "No file or prompt provided."})

    result = ""
    if file:
        upload_directory = "uploads"
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        file_path = os.path.join(upload_directory, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith('.pdf'):
            pdf_to_images(file.filename)
            result += generate_from_pdf(prompt)
        else:
            result += generate_content(prompt=prompt, image=file.filename)

        os.remove(file_path)
    elif prompt:
        result = generate_content(prompt=prompt)

    return JSONResponse(content={"message": "File uploaded successfully", "Prompt": prompt, "Result": result})



# @app.post("/upload")
# async def upload_file(file: UploadFile = File(None), prompt: str = Form(None)):
#     if file is None and prompt is None:
#         return JSONResponse(content={"Message": "lol"})
#     if file is None:
#         result = response( prompt=prompt)
#         return JSONResponse(content={"message": "File uploaded successfully", "Prompt": prompt, "Result": result})
#     elif file.filename.endswith('.pdf'):
#         upload_directory = "uploads"
#         if not os.path.exists(upload_directory):
#             os.makedirs(upload_directory)
#         file_path = os.path.join(upload_directory, file.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         pdf_to_images(file.filename)
#         generate_from_pdf(prompt)
#         result = get_result()
#         image_files = [file for file in os.listdir() if file.endswith('.png')]
#         for image_file in image_files:
#             os.remove(image_file)
#     else:
#     # Define the directory where you want to save the files
#         upload_directory = "uploads"
#     # Create the directory if it doesn't exist
#         if not os.path.exists(upload_directory):
#             os.makedirs(upload_directory)

#     # Save the file to disk
#         file_path = os.path.join(upload_directory, file.filename)
#         print(file.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         result = response( prompt=prompt, image=file.filename)
#     os.remove("uploads/" + file.filename)

#     return JSONResponse(content={"message": "File uploaded successfully", "Prompt": prompt, "Result": result})