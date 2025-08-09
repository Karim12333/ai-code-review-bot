# 🚀 Deployment Checklist

## Pre-Deployment Setup

### 1. Prerequisites
- [ ] OpenAI API key with GPT-4o access
- [ ] GitHub account with admin access to target repositories
- [ ] Railway account (for backend)
- [ ] Vercel account (for frontend)

### 2. Local Testing (Optional but Recommended)
- [ ] Clone repository
- [ ] Set up backend virtual environment
- [ ] Install Python dependencies: `pip install -r backend/requirements.txt`
- [ ] Create `.env` file in backend with test values
- [ ] Run test demo: `python backend/test_demo.py`
- [ ] Install frontend dependencies: `npm install` in frontend/
- [ ] Test frontend build: `npm run build` in frontend/

## Backend Deployment (Railway)

### 3. Deploy Backend
- [ ] Create new Railway project
- [ ] Connect GitHub repository
- [ ] Set root directory to `backend/`
- [ ] Add environment variables:
  - [ ] `OPENAI_API_KEY=sk-...`
  - [ ] `GITHUB_APP_ID=` (will fill after GitHub App creation)
  - [ ] `GITHUB_WEBHOOK_SECRET=` (choose a strong secret)
  - [ ] `GITHUB_PRIVATE_KEY_BASE64=` (will fill after GitHub App creation)
  - [ ] `BOT_COMMENT_TAG=ai-review-bot`
  - [ ] `MAX_PATCH_CHARS=12000`
- [ ] Deploy and note the public URL: `https://your-app.railway.app`
- [ ] Test health endpoint: `https://your-app.railway.app/health`

## GitHub App Creation

### 4. Create GitHub App
- [ ] Go to GitHub Settings → Developer settings → GitHub Apps
- [ ] Click "New GitHub App"
- [ ] Fill out app details:
  - [ ] **GitHub App name**: `AI Code Review Bot` (or your preferred name)
  - [ ] **Homepage URL**: `https://your-frontend.vercel.app` (or GitHub repo URL)
  - [ ] **Webhook URL**: `https://your-app.railway.app/webhook`
  - [ ] **Webhook secret**: Same as `GITHUB_WEBHOOK_SECRET` from Railway
  
### 5. Configure Permissions
- [ ] **Repository permissions**:
  - [ ] **Pull requests**: Read & write
  - [ ] **Contents**: Read  
  - [ ] **Metadata**: Read
- [ ] **Subscribe to events**:
  - [ ] ✅ Pull request

### 6. Generate Keys and Update Environment
- [ ] Generate private key (download .pem file)
- [ ] Convert to base64: `base64 -w 0 your-private-key.pem`
- [ ] Copy App ID from GitHub App page
- [ ] Update Railway environment variables:
  - [ ] `GITHUB_APP_ID=123456`
  - [ ] `GITHUB_PRIVATE_KEY_BASE64=your-base64-key`
- [ ] Redeploy backend on Railway

### 7. Install GitHub App
- [ ] Go to GitHub App page → "Install App"
- [ ] Choose repositories to install on
- [ ] Grant permissions

## Frontend Deployment (Vercel)

### 8. Deploy Frontend
- [ ] Import repository to Vercel
- [ ] Set root directory to `frontend/`
- [ ] Deploy
- [ ] Note the public URL: `https://your-app.vercel.app`

### 9. Update Frontend Links (Optional)
- [ ] Edit `frontend/components/Hero.tsx`
- [ ] Update "Install the GitHub App" link to your App's installation URL
- [ ] Redeploy frontend

## Testing & Validation

### 10. End-to-End Testing
- [ ] Create a test repository or use existing one
- [ ] Ensure GitHub App is installed on the repository
- [ ] Create a new branch with some code changes
- [ ] Open a Pull Request
- [ ] Wait for AI review comment (usually 30-60 seconds)
- [ ] Verify comment appears with `<!-- ai-review-bot -->` marker

### 11. Test Different Scenarios
- [ ] Test PR with no significant changes (should get minimal review)
- [ ] Test PR with security issues (should flag them)
- [ ] Test PR with style issues (should provide suggestions)
- [ ] Push additional commits to same PR (should update existing comment)

## Configuration & Customization

### 12. Repository Configuration (Optional)
- [ ] Create `.aicodereview.yml` in target repository root
- [ ] Customize review rules (severity, focus areas, ignored files)
- [ ] Test with new PR to verify custom rules work

### 13. Monitoring & Maintenance
- [ ] Check Railway logs for any errors
- [ ] Monitor OpenAI API usage and costs
- [ ] Set up alerts for webhook failures (optional)

## Troubleshooting

### Common Issues & Solutions
- [ ] **"Invalid signature" error**: Check webhook secret matches in GitHub App and Railway
- [ ] **"401 Unauthorized"**: Verify GitHub App permissions and private key
- [ ] **"No review posted"**: Check Railway logs, verify OpenAI API key has credits
- [ ] **Frontend build errors**: Ensure Node.js 18+ and run `npm install`

## Going Live

### 14. Production Readiness
- [ ] Test with multiple repositories
- [ ] Verify error handling works
- [ ] Check performance with large PRs
- [ ] Document usage for team members

### 15. Sharing & Promotion
- [ ] Update README with your specific deployment URLs
- [ ] Share with team or on social media
- [ ] Consider contributing improvements back to the project

---

## Quick Reference

**Backend Health Check**: `https://your-app.railway.app/health`
**GitHub App Settings**: `https://github.com/settings/apps/your-app-name`
**Railway Dashboard**: `https://railway.app/dashboard`
**Vercel Dashboard**: `https://vercel.com/dashboard`

**Need Help?**
- Check the logs in Railway dashboard
- Review GitHub App webhook deliveries
- Test locally with the demo script
- Open an issue in the repository
