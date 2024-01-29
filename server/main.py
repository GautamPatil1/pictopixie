from typing import Union
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware
from api import generate_content, pdf_to_images, generate_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL if you want to restrict it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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

    # Respond with some JSON data to acknowledge successful upload
    # return JSONResponse(content={"message": "File uploaded successfully", "Prompt": prompt, "Result": result})