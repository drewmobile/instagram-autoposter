import os
import time
import boto3
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
VIDEO_KEY = os.getenv("TEST_VIDEO_KEY")


def generate_presigned_url():
    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": S3_BUCKET, "Key": VIDEO_KEY},
        ExpiresIn=3600,
    )
    return url


def create_media_container(video_url):
    print("📤 Creating media container...")
    endpoint = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": "🎬 Automated test post via Instagram Graph API.",
        "access_token": ACCESS_TOKEN,
    }

    res = requests.post(endpoint, data=payload)

    # Enhanced error logging
    if res.status_code != 200:
        print(
            f"❌ Instagram response:\nStatus Code: {res.status_code}\nResponse Body: {res.text}"
        )
        res.raise_for_status()

    container_id = res.json()["id"]
    print(f"✅ Media container ID: {container_id}")
    return container_id


def wait_for_processing(container_id, max_attempts=10):
    endpoint = f"https://graph.facebook.com/v19.0/{container_id}?fields=status_code&access_token={ACCESS_TOKEN}"
    for attempt in range(max_attempts):
        time.sleep(5)
        res = requests.get(endpoint)
        res.raise_for_status()
        status = res.json().get("status_code", "")
        print(f"   ▶️ Attempt {attempt + 1}: Status = {status}")
        if status == "FINISHED":
            return True
        elif status == "ERROR":
            raise Exception("❌ Instagram processing failed.")
    raise Exception("❌ Timeout waiting for processing.")


def publish_media(container_id):
    print("🚀 Publishing post...")
    endpoint = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    payload = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }
    res = requests.post(endpoint, data=payload)
    if res.status_code == 200:
        print("✅ Reels post published successfully!")
    else:
        print(f"❌ Error publishing post:\n{res.status_code} {res.text}")


def main():
    print(f"🚀 Starting test post for '{VIDEO_KEY}'...")
    try:
        presigned_url = generate_presigned_url()
        print("🔗 Presigned URL generated:")
        print(presigned_url)

        container_id = create_media_container(presigned_url)
        if wait_for_processing(container_id):
            publish_media(container_id)
    except Exception as e:
        print(f"❌ {str(e)}")


if __name__ == "__main__":
    main()
