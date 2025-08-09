# 🤖 AI Code Review Bot

A GitHub App that automatically reviews pull requests using GPT-4o. Built with FastAPI + Next.js.

![AI Code Review Bot](https://img.shields.io/badge/AI-Code%20Review-blue) ![Python](https://img.shields.io/badge/Python-FastAPI-green) ![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)

## ✨ Features
- 🔍 **Automatic PR Reviews**: Reviews PRs on open/update with intelligent feedback
- 🎯 **Smart Analysis**: Checks for correctness, security, performance, and readability
- ⚙️ **Configurable**: Respects `.aicodereview.yml` rules in your repository
- 🚀 **Stateless**: No database required - lightweight and fast
- 📝 **Single Comment**: Posts one consolidated review comment to avoid spam

## 🏗️ Architecture

- **Backend**: FastAPI webhook server (deploy on Railway/Heroku)
- **Frontend**: Next.js landing page (deploy on Vercel)
- **AI**: GPT-4o for intelligent code analysis

## 🚀 Quick Start

### 1. Deploy Backend to Railway

1. **Create Railway Project**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository
   - Set **Root Directory** to `backend/`

2. **Environment Variables** (Add in Railway)
   ```env
   OPENAI_API_KEY=sk-your-openai-key
   GITHUB_APP_ID=123456
   GITHUB_WEBHOOK_SECRET=your-webhook-secret
   GITHUB_PRIVATE_KEY_BASE64=your-base64-encoded-private-key
   BOT_COMMENT_TAG=ai-review-bot
   MAX_PATCH_CHARS=12000
   ```

3. **Note your Railway URL**: `https://your-app.railway.app`

### 2. Create GitHub App

1. **GitHub Settings** → **Developer settings** → **GitHub Apps** → **New GitHub App**

2. **App Configuration**:
   - **GitHub App name**: `AI Code Review Bot`
   - **Homepage URL**: `https://your-frontend.vercel.app`
   - **Webhook URL**: `https://your-app.railway.app/webhook`
   - **Webhook secret**: Same as `GITHUB_WEBHOOK_SECRET`

3. **Permissions**:
   - **Pull requests**: Read & write
   - **Contents**: Read
   - **Metadata**: Read

4. **Subscribe to events**: 
   - ✅ Pull request

5. **Generate Private Key**:
   ```bash
   # Download the .pem file, then:
   base64 -w 0 your-private-key.pem
   # Copy output to GITHUB_PRIVATE_KEY_BASE64
   ```

6. **Install App** on your repositories

### 3. Deploy Frontend to Vercel

1. **Import to Vercel**
   - Connect your GitHub repository
   - Set **Root Directory** to `frontend/`
   - Deploy

2. **Update Links** (Optional)
   - Edit `frontend/components/Hero.tsx`
   - Update "Install the GitHub App" link to your App's installation URL

## 💻 Local Development

### Backend Setup

```bash
cd backend

# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env

# Edit .env with your values
# Run the server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## ⚙️ Configuration

Create `.aicodereview.yml` in your repository root:

```yaml
severity_threshold: minor   # info | minor | major | critical
max_findings_per_file: 5
focus:
  - correctness
  - security  
  - performance
  - readability
ignore_globs:
  - "*.md"
  - "dist/**"
  - "build/**"
  - "node_modules/**"
style: "Prefer early returns; avoid deep nesting; consistent naming."
```

## 🧪 Testing

1. **Install the App** on a test repository
2. **Create a Pull Request** with some code changes
3. **Watch the magic** ✨ - the bot will post a review comment

## 📋 Example Review Output

```markdown
## 🤖 AI Code Review

Found 3 potential improvements in this PR:

### `src/utils/helper.js`
- **MAJOR** — **Potential Security Issue**
  The function uses eval() which can execute arbitrary code. Consider using JSON.parse() for safer parsing.
  
  _Suggestion_: Replace `eval(userInput)` with `JSON.parse(userInput)` and add try-catch.

- **MINOR** — **Performance Optimization**
  The loop creates a new array on each iteration. Consider using array methods.

### `src/components/Button.tsx`
- **INFO** — **Code Style**
  Consider extracting the inline styles to a CSS class for better maintainability.

> _Re-run automatically on new commits (synchronize)_
```

## 🔧 Troubleshooting

### Common Issues

1. **"Invalid signature" error**
   - Check your `GITHUB_WEBHOOK_SECRET` matches in both GitHub App and Railway

2. **"Cannot find module" in backend**
   - Make sure you're in the `backend/` directory
   - Activate virtual environment: `source .venv/bin/activate`

3. **OpenAI API errors**
   - Verify your `OPENAI_API_KEY` is valid
   - Check you have sufficient credits

4. **Frontend build errors**
   - Run `npm install` in the `frontend/` directory
   - Make sure Node.js version is 18+

### Logs

- **Railway**: Check logs in Railway dashboard
- **Vercel**: Check Function logs in Vercel dashboard
- **Local**: Check terminal output

## 🚀 Why Teams Love This Bot

- ⚡ **Faster Reviews**: Catch issues before human reviewers
- 🎯 **Consistent Standards**: Enforce coding standards automatically  
- 🔒 **Security Focus**: Identify potential security vulnerabilities
- 📈 **Performance Insights**: Spot performance bottlenecks early
- 🧹 **Clean Code**: Maintain readability and best practices

## 📈 Roadmap

- [ ] **Inline Comments**: Add file-specific inline suggestions
- [ ] **Language-Specific Rules**: Tailored prompts for different languages
- [ ] **Security Presets**: OWASP-based security checks
- [ ] **Integration**: Slack/Teams notifications
- [ ] **Analytics**: Review metrics and insights

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [Next.js](https://nextjs.org/)
- AI reviews by [OpenAI GPT-4o](https://openai.com/)

---

**Ready to ship? Let's make your code reviews smarter! 🚀**

[Deploy Backend](https://railway.app) | [Deploy Frontend](https://vercel.com) | [Create GitHub App](https://github.com/settings/apps)
