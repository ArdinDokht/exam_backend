import asyncio
import io
import boto3
import numpy as np
import cv2
from aiobotocore.session import get_session
from pyzbar.pyzbar import decode


def get_images_from_s3_folder(folder_name):
    s3 = boto3.client("s3",
                      aws_access_key_id="kue698sasgcqqkse",
                      aws_secret_access_key="068be239-c495-43a0-a2af-2df170a79899",
                      endpoint_url="https://storage.iran.liara.space",
                      )
    response = s3.list_objects_v2(Bucket='pycrop', Prefix=folder_name)
    images = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.jpg') or obj['Key'].endswith('.png')]
    return images


async def crop_image(image_key):
    session = get_session()

    async with session.create_client("s3",
                                     aws_access_key_id="kue698sasgcqqkse",
                                     aws_secret_access_key="068be239-c495-43a0-a2af-2df170a79899",
                                     endpoint_url="https://storage.iran.liara.space",
                                     ) as s3:
        response = await s3.get_object(Bucket='pycrop', Key=image_key)
        image_data = await response['Body'].read()

        # Decode the image data into a numpy array.
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

        # Convert image to grayscale
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        barcodes = decode(gray_img)
        barcodes = [barcode for barcode in barcodes if barcode.orientation == "UP"]
        barcodes.sort(key=lambda x: x.rect.top)

        # Get exam_user_id from the first barcode
        exam_user_id = barcodes[0].data.decode()

        for i in range(len(barcodes)):
            if i == 0:  # Skip the first barcode
                continue
            if i == len(barcodes) - 1:  # Crop the remaining part of the image
                crop_img = image[barcodes[i].rect.top:, :]
            else:
                top = barcodes[i].rect.top
                bottom = barcodes[i + 1].rect.top
                crop_img = image[top:bottom, :]

            # Get question_id from the current barcode
            question_id = barcodes[i].data.decode()

            # Convert the cropped image to bytes
            _, encoded = cv2.imencode('.jpg', crop_img)
            img_bytes = encoded.tobytes()

            # Upload the image to S3
            key = f"cropped_images/{exam_user_id}_{question_id}.jpg"
            await s3.put_object(Bucket='pycrop', Key=key, Body=io.BytesIO(img_bytes).read())


async def crop_images(images):
    tasks = [crop_image(image_key) for image_key in images]
    await asyncio.gather(*tasks)
