import boto3
import random
import requests
import os
import time
from dotenv import load_dotenv

# === LOAD ENV ===
load_dotenv()

# === CONFIG FROM .env ===
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET = os.getenv("S3_BUCKET")
REGION = os.getenv("REGION")
S3_PREFIX = os.getenv("S3_PREFIX", "")  # Optional
CAPTION = os.getenv("CAPTION", "📲 Daily drop! #automation #postedviaS3")

# === STATIC CONFIG ===
POSTED_LOG = "posted_local_s3.txt"
FAILED_LOG = "failed_posts.log"
EXPIRATION = 900  # 15 minutes

# === AWS SESSION ===
session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client("s3", region_name=REGION)

# === HELPERS ===


def list_s3_mp4_objects(bucket, prefix=""):
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    files = []
    for page in pages:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".mp4"):
                files.append(key)
    return files


def load_posted_log():
    if not os.path.exists(POSTED_LOG):
        return set()
    with open(POSTED_LOG, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_to_posted_log(filename):
    with open(POSTED_LOG, "a") as f:
        f.write(filename + "\n")


def save_to_failed_log(filename):
    with open(FAILED_LOG, "a") as f:
        f.write(filename + "\n")


def generate_presigned_url(bucket, key, expiration=900):
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration,
    )


def upload_and_publish_video(video_url, caption, key):
    print(f"📤 Sending video to Instagram...")
    create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    status_url_base = f"https://graph.facebook.com/v19.0"
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"

    # Step 1: Create media container
    r = requests.post(
        create_url,
        data={
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS",
            "access_token": ACCESS_TOKEN,
        },
    )

    if not r.ok:
        print("❌ Instagram rejected the media container request:")
        print("Status Code:", r.status_code)
        print("Response:", r.text)
        if "media_type" in r.text:
            print(
                "👉 Tip: Use media_type='REELS' instead of 'VIDEO' to upload video content."
            )
        r.raise_for_status()

    creation_id = r.json()["id"]
    print(f"✅ Created media container ID: {creation_id}")

    # Step 2: Poll for media readiness
    print("⏳ Waiting for Instagram to process the media...")
    status_url = f"{status_url_base}/{creation_id}?fields=status_code&access_token={ACCESS_TOKEN}"
    for i in range(12):  # Max 60 seconds wait
        time.sleep(5)
        status_resp = requests.get(status_url)
        if not status_resp.ok:
            print("⚠️ Failed to check status. Retrying...")
            continue
        status = status_resp.json().get("status_code", "")
        print(f"   ▶️ Attempt {i+1}: Status = {status}")
        if status == "FINISHED":
            break
        elif status in ["ERROR", "EXPIRED", "FAILED"]:
            print(f"❌ Upload failed with status: {status}")
            save_to_failed_log(key)
            return False
    else:
        print("❌ Media not ready after timeout. Skipping.")
        save_to_failed_log(key)
        return False

    # Step 3: Publish post (with retry)
    for attempt in range(3):
        r = requests.post(
            publish_url, data={"creation_id": creation_id, "access_token": ACCESS_TOKEN}
        )

        if r.ok:
            print("✅ Instagram post published.")
            return True

        print(f"⚠️ Publish attempt {attempt + 1} failed: {r.status_code}")
        print("Response:", r.text)

        if r.status_code >= 500:
            time.sleep(5)
            continue
        else:
            break

    print("❌ Failed to publish after retries.")
    save_to_failed_log(key)
    r.raise_for_status()


# === MAIN ===


def main():
    print("🚀 Starting Instagram AutoPoster...")
    print(f"📂 Scanning S3 for unposted .mp4 files...")
    print(f"Using bucket: {S3_BUCKET}, prefix: '{S3_PREFIX}'")

    all_files = list_s3_mp4_objects(S3_BUCKET, S3_PREFIX)
    print(f"🔍 Found {len(all_files)} total .mp4 files in S3")

    posted = load_posted_log()
    unposted = [f for f in all_files if f not in posted]
    print(f"🧾 {len(unposted)} files have not yet been posted")

    if not unposted:
        print("🎉 All videos have been posted.")
        return

    key = random.choice(unposted)
    print(f"🎯 Selected video: {key}")

    try:
        url = generate_presigned_url(S3_BUCKET, key, EXPIRATION)
        print(f"🔗 Generated pre-signed URL: {url}")
        if upload_and_publish_video(url, CAPTION, key):
            save_to_posted_log(key)
            print(f"📝 Logged '{key}' as posted.")
    except Exception as e:
        print(f"❌ Unexpected error posting '{key}': {e}")
        save_to_failed_log(key)


# === ENTRY POINT ===

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("🚨 Script crashed unexpectedly:", str(e))
