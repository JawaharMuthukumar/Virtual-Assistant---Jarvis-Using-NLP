import asyncio
from random import randint
from PIL import Image
import requests
import os
from time import sleep

# Manually setting the API Key
HuggingFaceAPIKey = "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"

# Ensure the correct API URL for image generation
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to load image: {image_path}")

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"API Error {response.status_code}: {response.text}")
        return None
    
    return response.content

async def generate_images(prompt: str):
    tasks = []
    
    os.makedirs("Data", exist_ok=True)  # Ensure Data folder exists

    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            image_path = f"Data/{prompt.replace(' ', '_')}{i+1}.jpg"
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            print(f"Saved: {image_path}")
        else:
            print(f"Failed to generate image {i+1}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data = f.read().strip()

        if not Data:
            break  # If file is empty, stop the loop

        prompt, Status = Data.split(",")

        if Status.strip() == "True":
            print("Generating images...")
            GenerateImages(prompt.strip())

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
