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
