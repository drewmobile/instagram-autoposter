# Instagram AutoPoster

This is a Python CLI tool that automates the posting of short-form video content to a business's Instagram account. It runs on a private server via scheduled cron jobs and uses the Instagram Graph API to upload videos stored in a secure AWS S3 bucket. This is an internal automation tool used only by the brand.

---

## 🔍 Use Case Overview

This tool allows our brand to schedule and post Reels directly from an S3 bucket using cron. The Instagram Graph API is used to:

- Create media containers from pre-signed S3 URLs
- Poll for media readiness
- Publish videos as Reels

---

## 📂 Project Structure

```bash
instagram-autoposter/
├── instpost.py              # Main posting script (cron-based)
├── verify_instagram_post.py # One-off script to verify credentials & test upload
├── generate_oauth_url.py   # OAuth URL generator
├── .env.example            # Example environment configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```
