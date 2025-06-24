# Instagram AutoPoster

A robust Python CLI tool that automates the posting of short-form video content to Instagram business accounts. The system integrates with AWS S3 for video storage and uses the Instagram Graph API for seamless content publishing via scheduled cron jobs.

## 🚀 Features

- **🎬 Automated Video Posting**: Randomly selects and posts unposted videos from S3
- **📹 Instagram Reels Support**: Optimized for short-form video content
- **☁️ AWS S3 Integration**: Secure video storage with pre-signed URLs
- **🔄 Retry Logic**: Robust error handling with automatic retries
- **📊 Logging System**: Comprehensive tracking of posted and failed uploads
- **⏰ Cron-Ready**: Designed for scheduled automated execution
- **🔐 Secure Authentication**: Uses long-lived Instagram access tokens
- **🧪 Testing Suite**: Multiple scripts for validation and testing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AWS S3 Bucket │    │  Python Script  │    │ Instagram Graph │
│                 │    │                 │    │      API        │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Video 1   │ │    │ │ instpost.py │ │    │ │ Create Media│ │
│ │   Video 2   │ │◄───┤ │             │ ├───►│ │ Container   │ │
│ │   Video 3   │ │    │ │ - Selects   │ │    │ │ Publish     │ │
│ │     ...     │ │    │ │ - Uploads   │ │    │ │ Monitor     │ │
│ └─────────────┘ │    │ │ - Logs      │ │    │ └─────────────┘ │
└─────────────────┘    │ └─────────────┘ │    └─────────────────┘
                       └─────────────────┘
```

## 📂 Project Structure

```
instagram-autoposter/
├── instpost.py                 # Main automation script (cron-ready)
├── verify_instagram_post.py    # Credential verification & test upload
├── test_post.py               # Single video test script
├── requirements.txt           # Python dependencies
├── REVIEWER_INSTRUCTIONS.md   # Detailed testing instructions
├── README.md                 # This documentation
├── .gitignore               # Git ignore patterns
├── posted_local_s3.txt      # Log of successfully posted videos
└── failed_posts.log         # Log of failed upload attempts
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- AWS CLI configured with appropriate permissions
- Instagram Business Account with Graph API access
- Long-lived Instagram Access Token

### 1. Clone Repository

```bash
git clone <repository-url>
cd instagram-autoposter
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Instagram API Configuration
ACCESS_TOKEN=your_long_lived_instagram_access_token
IG_USER_ID=your_instagram_business_user_id

# AWS Configuration
AWS_PROFILE=your_aws_profile_name
S3_BUCKET=your_s3_bucket_name
REGION=your_aws_region

# Optional Configuration
S3_PREFIX=folder/path/in/bucket/
CAPTION=📲 Daily drop! #automation #postedviaS3
```

### 5. AWS Setup

Ensure your AWS profile has the following S3 permissions:
- `s3:GetObject`
- `s3:ListBucket`

## 🎯 Usage

### Automated Posting (Production)

The main script is designed for automated execution:

```bash
python instpost.py
```

**What it does:**
1. Scans S3 bucket for `.mp4` files
2. Filters out already posted videos
3. Randomly selects one unposted video
4. Generates pre-signed URL (15-minute expiry)
5. Uploads to Instagram as a Reel
6. Monitors processing status
7. Publishes when ready
8. Logs success/failure

### Testing & Verification

#### Test with Known Video
```bash
python test_post.py
```
Posts a specific test video to validate the complete workflow.

#### Verify Credentials
```bash
python verify_instagram_post.py
```
Uses a hardcoded test video to verify API credentials and permissions.

## 📋 Logging System

### Posted Videos Log (`posted_local_s3.txt`)
- Tracks successfully posted video filenames
- Prevents duplicate postings
- One filename per line

### Failed Posts Log (`failed_posts.log`)
- Records videos that failed to upload
- Includes timestamp and error context
- Used for troubleshooting and retry logic

## 🔄 Cron Automation

Add to your crontab for automated posting:

```bash
# Post once daily at 2 PM
0 14 * * * cd /path/to/instagram-autoposter && /path/to/venv/bin/python instpost.py

# Post twice daily at 10 AM and 6 PM
0 10,18 * * * cd /path/to/instagram-autoposter && /path/to/venv/bin/python instpost.py
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ACCESS_TOKEN` | ✅ | Instagram long-lived access token | - |
| `IG_USER_ID` | ✅ | Instagram business user ID | - |
| `AWS_PROFILE` | ✅ | AWS CLI profile name | - |
| `S3_BUCKET` | ✅ | S3 bucket containing videos | - |
| `REGION` | ✅ | AWS region | - |
| `S3_PREFIX` | ❌ | Folder path in S3 bucket | `""` |
| `CAPTION` | ❌ | Default post caption | `"📲 Daily drop! #automation #postedviaS3"` |

### Script Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| `EXPIRATION` | 900 seconds | Pre-signed URL validity |
| `Max Retries` | 3 attempts | Publication retry limit |
| `Polling Timeout` | 60 seconds | Media processing wait time |
| `Media Type` | `REELS` | Instagram content type |

## 🔍 API Workflow

### 1. Media Container Creation
```http
POST https://graph.facebook.com/v19.0/{user-id}/media
Content-Type: application/x-www-form-urlencoded

video_url={presigned_s3_url}
caption={post_caption}
media_type=REELS
access_token={access_token}
```

### 2. Processing Status Check
```http
GET https://graph.facebook.com/v19.0/{container-id}?fields=status_code&access_token={access_token}
```

**Status Codes:**
- `IN_PROGRESS`: Still processing
- `FINISHED`: Ready to publish
- `ERROR`: Processing failed
- `EXPIRED`: Container expired

### 3. Media Publication
```http
POST https://graph.facebook.com/v19.0/{user-id}/media_publish
Content-Type: application/x-www-form-urlencoded

creation_id={container_id}
access_token={access_token}
```

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors**
```
❌ Instagram rejected the media container request: HTTP 401
```
- Verify `ACCESS_TOKEN` is valid and not expired
- Ensure `IG_USER_ID` matches the token's account
- Check Instagram Business Account permissions

**S3 Access Issues**
```
❌ AWS credentials not found
```
- Verify AWS profile configuration: `aws configure list --profile your-profile`
- Check S3 bucket permissions
- Ensure bucket exists and contains `.mp4` files

**Video Processing Timeout**
```
❌ Media not ready after timeout
```
- Video file may be too large or corrupted
- Check Instagram's video requirements (max 60 seconds, specific formats)
- Verify S3 pre-signed URL accessibility

### Debug Mode

Add debug logging to any script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Monitoring

### Success Metrics
- Check `posted_local_s3.txt` for posting history
- Monitor Instagram account for published content
- Track S3 bucket for new video additions

### Error Tracking
- Review `failed_posts.log` for upload failures
- Check cron logs: `grep CRON /var/log/syslog`
- Monitor AWS CloudWatch for S3 access patterns

## 🔒 Security Considerations

- **Access Tokens**: Store securely, rotate regularly
- **S3 Permissions**: Use least-privilege access
- **Pre-signed URLs**: Short expiration times (15 minutes)
- **Environment Variables**: Never commit `.env` files
- **Logging**: Avoid logging sensitive credentials

## 📋 Requirements

### Instagram Requirements
- Instagram Business Account
- Facebook Developer Account
- Valid long-lived access token
- Proper app permissions (`instagram_basic`, `instagram_content_publish`)

### AWS Requirements
- S3 bucket with video files
- IAM user/role with S3 read permissions
- Configured AWS CLI profile

### Video Requirements
- Format: MP4
- Duration: 3-60 seconds (Instagram Reels)
- Resolution: 1080x1920 (9:16 aspect ratio recommended)
- File size: Under 100MB

## 🤝 Contributing

This is an internal automation tool. For modifications:

1. Test changes with `verify_instagram_post.py`
2. Validate with `test_post.py`
3. Update documentation
4. Test cron integration

## 📄 License

Internal use only. All video content is owned by the brand.

---

**⚠️ Important**: This tool is designed for internal brand use only. It does not collect, store, or process user data from external sources.
