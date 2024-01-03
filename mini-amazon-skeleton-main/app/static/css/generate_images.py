import requests
import os

def download_images(image_count=2000, save_path='random_images'):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    base_url = 'https://picsum.photos/200/?random&dummyParam=1'

    for i in range(image_count):
        image_url = base_url
        response = requests.get(image_url)

        if response.status_code == 200:
            image_path = os.path.join(save_path, f"{i}.png")
            with open(image_path, 'wb') as f:
                f.write(response.content)
                print(f"Image {i} saved at {image_path}")

download_images(image_count=2000)