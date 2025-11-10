# Deploying to Vercel (Separate Frontend & Backend Projects)

You will manage **two Vercel projects**, both pointing to this same Git repository but with different root directories:

- `frontend1-react/` → React SPA (static build)
- `backend/` → Flask API (serverless Python)

Keeping the deployments isolated avoids the monorepo routing/build issues you observed.

## Prerequisites
- Vercel account (https://vercel.com)
- GitHub repo pushed and accessible by Vercel
- Optional: Vercel CLI (`npm i -g vercel`)
- Keep sensitive values (e.g. `GEMINI_API_KEY`) **out of git** and add them only in Vercel → Project Settings → Environment Variables

## Repository Layout

```
/
├── backend/
│   ├── api/index.py        # Serverless handler
│   ├── app.py              # Flask app (imported by index.py)
│   ├── requirements.txt
│   └── vercel.json         # Backend-specific config
├── frontend1-react/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json         # Frontend-specific config
└── .vercelignore
```

## Deploying the Frontend (React)

1. **Push latest changes**
   ```bash
   git add .
   git commit -m "Prepare frontend deployment"
   git push origin main
   ```

2. **Create/Link project in Vercel**
   - Dashboard → “Add New Project” → import this repo
   - When prompted for *Root Directory*, choose `frontend1-react`
   - Vercel will detect the `frontend1-react/vercel.json` file and use it automatically

3. **Default build behaviour** (no manual overrides needed)
   - Install: `npm install`
   - Build: `npm run build`
   - Output: `dist/`

4. **Environment variables**
   - If the backend runs on a separate domain, set `VITE_API_BASE=https://<your-backend-domain>` so React calls the live API
   - Add any analytics or feature flags here as well

5. **Deploy**
   - Hit “Deploy” and wait for the build to finish
   - The SPA is exposed at `https://<frontend-project>.vercel.app`

## Deploying the Backend (Flask)

1. **Push changes** (if not already done)

2. **Create/Link project in Vercel**
   - “Add New Project” → import the same repo
   - Set *Root Directory* to `backend`
   - The `backend/vercel.json` file tells Vercel to package `api/index.py` using `@vercel/python`

3. **Environment variables**
   - Add `GEMINI_API_KEY` (and any other secrets such as `MISTRAL_API_KEY`)
   - Rotate the existing key that was committed locally; never push real values to git

4. **Deploy**
   - Click “Deploy” (or run `vercel --prod --cwd backend` from the CLI)
   - Health check: `curl https://<backend-project>.vercel.app/health`

## After Both Deployments

- Update the frontend project’s `VITE_API_BASE` (or use relative `/api` if you configure a reverse proxy/CDN)
- Redeploy the frontend so it consumes the live API endpoint
- Test end-to-end flows manually (text + PDF uploads) and watch the backend function logs in Vercel for errors/timeouts

## Local Development

```bash
# Backend
cd backend
python app.py  # serves http://localhost:5001

# Frontend (new terminal)
cd frontend1-react
npm install
npm run dev     # serves http://localhost:3000 and proxies /api to 5001
```

## Troubleshooting

- **Large PDFs**: serverless functions reject bodies > 4.5 MB. Use smaller files or external storage.
- **Slow processing**: hobby plan timeouts hit at ~10 s; optimise or consider a background job.
- **Module errors**: ensure every Python dependency is listed in `backend/requirements.txt` and compatible with Python 3.12 (current Vercel runtime).
- **CORS failures**: Flask already enables CORS for `*`; tighten to your domains if needed once everything works.

## Useful Commands

```bash
# Frontend prod build locally
cd frontend1-react && npm run build

# Backend smoke test
cd backend && curl http://localhost:5001/health

# Deploy via CLI (optional)
vercel --cwd frontend1-react --prod
vercel --cwd backend --prod
```

## References
- [Vercel Python runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel static builds](https://vercel.com/docs/deployments/static-sites)
- [Vite deployment guide](https://vitejs.dev/guide/static-deploy.html)
