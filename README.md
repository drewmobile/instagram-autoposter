✅ Complete README.md Structure

# 📸 Instagram AutoPoster – Internal CLI Tool

## 🔍 Use Case Overview

This is an internal Python CLI application that automates posting short-form videos (Reels) to our business's Instagram account. It runs on a private server via cron jobs and uses the Instagram Graph API and AWS S3 for storage.

This tool is **used only by our business**. It does **not** involve any public users, user authentication, or data collection.

---

## 🛠️ Environment Configuration

Copy `.env.example` to `.env` and provide your credentials:

```env
ACCESS_TOKEN=your_instagram_access_token
IG_USER_ID=your_instagram_user_id
AWS_PROFILE=your_aws_cli_profile
S3_BUCKET=your_s3_bucket_name
REGION=your_aws_region
TEST_VIDEO_KEY=Animation Reels by The Digital Era page (314).mp4

📦 Installation Instructions

git clone https://github.com/drewmobile/instagram-autoposter.git
cd instagram-autoposter

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Then edit `.env` with real values

🧪 Test the Integration (Manual Reviewer Test)

    These scripts are for reviewer validation and debugging.

✅ verify_instagram_post.py

python verify_instagram_post.py

This script:

    Generates a pre-signed S3 URL

    Uploads a video to /media as a Reel

    Polls /media for status

    Publishes the Reel via /media_publish

✅ A successful Instagram Reel will appear in the connected business account.
✅ test_post.py

This is a simplified one-time test script. It performs the same API flow as above using the test video key defined in your .env.

python test_post.py

🔐 Data Handling

    No user data is collected, stored, or shared.

    All video content is owned by our business.

    There are no frontend components or third-party user interactions.

🔗 Reviewer Access

This repo is publicly available at:

https://github.com/drewmobile/instagram-autoposter

Please use the .env.example, install instructions, and the test scripts (verify_instagram_post.py, test_post.py) to validate API permission usage.


---

### ✅ Recap: What You Need

| File                     | Purpose                                       |
|--------------------------|-----------------------------------------------|
| `README.md`              | Reviewer instructions & setup                 |
| `.env.example`           | Shows expected environment variables          |
| `verify_instagram_post.py` | Demonstrates Instagram Reels upload flow     |
| `test_post.py`           | One-time simplified API test                  |
| `requirements.txt`       | Lists `boto3`, `requests`, `python-dotenv`    |

