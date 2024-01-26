import sys, fitz
import PIL.Image
import os

import google.generativeai as genai

genai.configure(api_key='AIzaSyA28GlONavltkud6g8BYg40PerzxCE8Wa8')

chat_response = ''

def generate(prompt=None, image=None):
    if image:
        print(f"Generating content with image: {image}")
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([prompt, image], stream=True)
    else:
        print(f"Generating content without image")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
    response.resolve()
    global chat_response
    chat_response += response.text + '\n'
    print(f"Generated response: {response.text}")


def response(prompt=None, image=None):
    if image:
        generate(prompt, PIL.Image.open(f"uploads/{image}"))
    else:
        generate(prompt)
    return chat_response

def write_to_txt(filename, text, extra_string=""):
  mode = 'a' if os.path.exists(filename) else 'w'
  with open(filename, mode) as file:
      if mode == 'w':
          file.write(text + extra_string)
      else:
          file.write("\n" + text + extra_string)


def pdf_to_images(filename):
    file_path = os.path.join('uploads', filename)
    doc = fitz.open(file_path)
    if len(doc) > 4:
        return False
    for page in doc:
        pix = page.get_pixmap()
        pix.save("page_%i.png" % page.number)
        

def generate_from_pdf(prompt="Solve These Questions for me they are for 5 marks each so solve them in detail and be lengthy."):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    image_files = [file for file in os.listdir(script_directory) if file.endswith('.png')]
    for image_file in image_files:
        print(image_file)
        if image_file:
            generate(prompt, PIL.Image.open(image_file))
        else:
            generate(prompt)

def get_result():
    return chat_response
      


