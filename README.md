# Instagram AutoPoster – Reviewer Instructions

## 🔍 Use Case Overview

This app is a Python CLI tool that automates the posting of short-form video content to our business's Instagram account. It runs on a private server via scheduled cron jobs and uses the Instagram Graph API to upload videos stored in a secure AWS S3 bucket. This is an internal tool used only by our brand.

---

## 👩‍💻 Test Instructions (Manual Testing of API Flow)

Although the app runs via cron automation in production, reviewers can manually test the full Instagram posting workflow as follows:

### 1. Clone the Repository

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

4. Run the One-Time Test Script

python test_post.py

This script will:

    Generate a pre-signed S3 video URL

    Upload the video via /media

    Poll /media for FINISHED status

    Call /media_publish to post to the feed

5. Expected Result

A successful Instagram post should appear on the linked business account. The script will log each API step, including status and errors (if any).
📌 Additional Notes

    This tool is used only internally by our brand.

    It does not collect, store, or process user data.

    All video content is owned and created by us.

    No third-party or public users interact with the tool.
