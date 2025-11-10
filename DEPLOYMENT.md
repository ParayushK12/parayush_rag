# Deploying to Vercel - Step by Step Guide

## Prerequisites
1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional but recommended): `npm i -g vercel`
3. Git repository pushed to GitHub, GitLab, or Bitbucket

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/dashboard
   - Click "Add New Project"
   - Import your GitHub repository (parayush_rag)
   - Vercel will auto-detect the project

3. **Configure Project Settings**
   - **Framework Preset**: Select "Other" or "Vite"
   - **Root Directory**: Leave as `./` (root)
   - **Build Command**: `cd frontend1-react && npm install && npm run build`
   - **Output Directory**: `frontend1-react/dist`
   - **Install Command**: `pip install -r requirements.txt`

4. **Environment Variables** (if needed)
   Add any API keys or secrets in the Environment Variables section:
   - `MISTRAL_API_KEY` (if using Mistral AI)
   - `GOOGLE_API_KEY` (if using Google Gemini)
   
   These should be stored in Vercel's environment variables, NOT in your code.

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (5-10 minutes first time)
   - Your app will be available at `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not installed)
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project root**
   ```bash
   cd /home/darpan/Desktop/para
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? Yes
   - Which scope? (Select your account)
   - Link to existing project? No
   - Project name? parayush-rag (or your choice)
   - Directory? `./`
   - Override settings? No

5. **Production Deployment**
   ```bash
   vercel --prod
   ```

## Important Notes

### API Keys & Environment Variables
⚠️ **NEVER commit API keys to Git!**

Add API keys in Vercel Dashboard:
1. Go to Project Settings
2. Navigate to Environment Variables
3. Add variables like:
   - `MISTRAL_API_KEY`
   - `GOOGLE_API_KEY`
   - etc.

### File Upload Limitations
- Vercel serverless functions have a **4.5MB request body limit**
- PDF uploads larger than 4.5MB won't work
- Consider using Vercel Blob Storage for larger files

### Python Dependencies
Make sure all dependencies in `requirements.txt` are compatible with Vercel's Python runtime:
- Some packages like `PyMuPDF` might have issues
- Consider alternatives or using Vercel's Edge Functions if needed

### Local Development
To test locally with the production-like setup:
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend1-react
npm install
npm run dev
```

The Vite dev server will proxy API requests to the Flask backend.

## Troubleshooting

### Build Fails
- Check build logs in Vercel Dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility (Vercel uses Python 3.9)

### API Not Working
- Check function logs in Vercel Dashboard
- Verify routes in `vercel.json`
- Ensure CORS is properly configured in Flask app

### Frontend Not Loading
- Check if build completed successfully
- Verify `vite.config.js` is correct
- Check browser console for errors

### 504 Gateway Timeout
- Vercel serverless functions timeout after 10s (Hobby) or 60s (Pro)
- PDF processing might be too slow for large files
- Consider optimizing processing or upgrading Vercel plan

## Post-Deployment

1. **Test your deployment**
   ```bash
   curl https://your-project.vercel.app/health
   ```

2. **Monitor logs**
   - Go to Vercel Dashboard → Your Project → Deployments
   - Click on latest deployment
   - View Function Logs

3. **Set up custom domain** (optional)
   - Go to Project Settings → Domains
   - Add your custom domain

## Project Structure for Vercel

```
/
├── backend/
│   ├── api/
│   │   └── index.py          # Vercel serverless entry point
│   ├── app.py                # Main Flask app
│   ├── endtoend.py
│   └── ...
├── frontend1-react/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
├── requirements.txt           # Python dependencies
├── vercel.json               # Vercel configuration
└── .vercelignore             # Files to ignore in deployment
```

## Resources
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
