import os
import time
import requests
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET = os.getenv("S3_BUCKET")
REGION = os.getenv("REGION")

VIDEO_KEY = "Animation Reels by The Digital Era page (314).mp4"
CAPTION = "🎬 Test reel: small video upload to verify credentials"

session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client("s3", region_name=REGION)


def generate_presigned_url(bucket, key, expiration=900):
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration,
    )


def test_post():
    print(f"🚀 Starting test post for '{VIDEO_KEY}'...")
    video_url = generate_presigned_url(S3_BUCKET, VIDEO_KEY)
    print(f"🔗 Presigned URL generated:\n{video_url}\n")

    # Step 1: Upload as REEL
    create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    print("📤 Creating media container...")
    create_resp = requests.post(
        create_url,
        data={
            "video_url": video_url,
            "caption": CAPTION,
            "media_type": "REELS",
            "access_token": ACCESS_TOKEN,
        },
    )

    if not create_resp.ok:
        print("❌ Error creating media container:")
        print(create_resp.status_code, create_resp.text)
        return

    container_id = create_resp.json()["id"]
    print(f"✅ Media container ID: {container_id}")

    # Step 2: Poll for readiness
    print("⏳ Waiting for video to finish processing...")
    status_url = f"https://graph.facebook.com/v19.0/{container_id}?fields=status_code&access_token={ACCESS_TOKEN}"

    for i in range(12):
        time.sleep(5)
        status_resp = requests.get(status_url)
        if not status_resp.ok:
            print("⚠️ Status check failed. Retrying...")
            continue

        status = status_resp.json().get("status_code")
        print(f"   ▶️ Attempt {i + 1}: Status = {status}")

        if status == "FINISHED":
            break
        elif status in ["FAILED", "EXPIRED", "ERROR"]:
            print(f"❌ Video processing failed with status: {status}")
            return
    else:
        print("❌ Timeout waiting for video readiness.")
        return

    # Step 3: Publish post
    print("🚀 Publishing post...")
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_resp = requests.post(
        publish_url, data={"creation_id": container_id, "access_token": ACCESS_TOKEN}
    )

    if not publish_resp.ok:
        print("❌ Error publishing post:")
        print(publish_resp.status_code, publish_resp.text)
        return

    post_id = publish_resp.json().get("id", "(no id returned)")
    print(f"✅ Successfully published post. ID: {post_id}")


if __name__ == "__main__":
    try:
        test_post()
    except Exception as e:
        print("🚨 Script crashed:", e)
