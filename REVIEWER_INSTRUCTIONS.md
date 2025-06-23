

# Instagram AutoPoster – Reviewer Instructions

## 🔍 Use Case Overview

This app is a Python CLI tool that automates the posting of short-form video content to our business's Instagram account. It runs on a private server via scheduled cron jobs and uses the Instagram Graph API to upload videos stored in a secure AWS S3 bucket. This is an internal tool used only by our brand.

---

## 👩‍💻 Test Instructions (Manual Testing of API Flow)

Although the app runs via cron automation in production, reviewers can manually test the full Instagram posting workflow using any of the provided scripts:

---

### 🧪 Option 1: One-Time Test with `test_post.py`

This script posts a **single known test video** to validate credentials and permissions.

#### 1. Clone the Repository

```bash
git clone https://github.com/blockvest/instagram-autoposter.git
cd instagram-autoposter

2. Create and Activate a Python Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Create a .env File

Provide valid access token and environment configuration:

ACCESS_TOKEN=IG...your long-lived Instagram token
IG_USER_ID=1784...your Instagram user ID
S3_BUCKET=drews-instagram-bucket
REGION=us-east-1
AWS_PROFILE=instagram-poster
TEST_VIDEO_KEY=Animation Reels by The Digital Era page (314).mp4

4. Run the Test Script

python test_post.py

5. Expected Result

    Script generates a pre-signed S3 video URL

    Uploads to Instagram via /media

    Polls for processing status

    Publishes to Instagram feed using /media_publish

    Output is printed in terminal

🔁 Option 2: Automated Posting with instpost.py

This script is designed to automatically post one unposted video at a time from the S3 bucket.
Run the Main Script

python instpost.py

Expected Result

    Scans drews-instagram-bucket for unposted videos

    Selects one at random

    Posts to Instagram using the same API steps

    Logs output and marks video as posted

    Intended to run via scheduled cron job

✔️ Option 3: Verification Post with verify_instagram_post.py

This script is used to verify posting capability using a known small video, uploaded as a REEL.
Run the Script

python verify_instagram_post.py

What It Does

    Uses a hardcoded test video:
    Animation Reels by The Digital Era page (314).mp4

    Generates a pre-signed S3 URL

    Uploads video to /media with media_type=REELS

    Polls the media container until status_code = FINISHED

    Publishes to feed via /media_publish

    Logs each step of the process and prints any errors

📌 Additional Notes

    This tool is used only internally by our brand

    It does not collect, store, or process user data

    All video content is created and owned by us

    No public or third-party users interact with this system
