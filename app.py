###Health Management System
from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("AIzaSyDFoHL7FFHwLMLocYi7TvCMRVCM8ZFUgPw"))


#----------------------------------------------------------------------------
# Function to load Google Gemini Pro Vision API and get a response

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

#----------------------------------------------------------------------------
# Function to handle the image input and prepare it for the API call

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Prepare image data with mime type
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#----------------------------------------------------------------------------
# Input prompt for the AI model

input_prompt = """
You are an expert nutritionist. Your task is to analyze the food items visible in the uploaded image
and calculate the total calories. Also, provide the calorie details of each individual food item.

Use the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
...
Total Calories: <total>
"""
#---------------------------------------------------------------------------

st.set_page_config(page_title="AI Nutritionist App")

# App title
st.header("AI Nutritionist App")

# Input prompt from the user
input = st.text_input("Input Prompt:", key="input")

# File uploader for images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Submit button
submit = st.button("Tell me the total calories")


#----------------------------------------------------------------------------
# If submit button is clicked
if submit:
    # Prepare the image data in required format
    image_data = input_image_setup(uploaded_file)

    # Get response from Gemini Vision model
    response = get_gemini_response(input_prompt, image_data, input)

    # Display the response
    st.subheader("The Response is:")
    st.write(response)
