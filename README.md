# 🚀 Cloud Run Multi-Service Kit with Firebase Auth and Identity Tokens

This repo demonstrates a secure architecture where:

- `React App` authenticates users using Firebase
- `App A (Gateway)` validates users and securely calls
- `App B`, `App C`, and `App D` using Google-signed identity tokens

---

## 🔐 Auth Flow

1. User logs in via Firebase (React App)
2. React sends Firebase ID token to `App A`
3. `App A` verifies token and fetches identity token via metadata server
4. `App A` calls `App B/C/D` (which are protected by Cloud Run IAM)

---

## 📁 Folder Structure

| Folder             | Description                              |
|--------------------|------------------------------------------|
| `react-frontend/`  | ReactJS app with Firebase login          |
| `cloudrun-app-a/`  | FastAPI gateway (verifies token + routing) |
| `cloudrun-app-b/`  | Example backend API (e.g., prediction)   |
| `cloudrun-app-c/`  | Example backend API (e.g., profile)      |
| `cloudrun-app-d/`  | Example backend API (e.g., logging)      |

---

## 🚀 Deployment Steps

### 1. Firebase Setup
- Create Firebase project
- Enable Email/Google auth
- Get `apiKey`, `authDomain`, and `projectId` for frontend

### 2. Deploy Backend APIs (App B/C/D)
```bash
gcloud run deploy app-b --source=cloudrun-app-b --no-allow-unauthenticated
gcloud run deploy app-c --source=cloudrun-app-c --no-allow-unauthenticated
gcloud run deploy app-d --source=cloudrun-app-d --no-allow-unauthenticated
```

### 3. Deploy App A (Gateway)
```bash
gcloud run deploy app-a \
  --source=cloudrun-app-a \
  --allow-unauthenticated \
  --update-env-vars=FIREBASE_PROJECT_ID=<your-firebase-id>,\
                    APP_B_URL=https://app-b-url.a.run.app,\
                    APP_C_URL=https://app-c-url.a.run.app,\
                    APP_D_URL=https://app-d-url.a.run.app
```

### 4. IAM Binding (Allow App A to Call Others)
```bash
gcloud run services add-iam-policy-binding app-b \
  --member='serviceAccount:<app-a-sa>@<project>.iam.gserviceaccount.com' \
  --role='roles/run.invoker'
```
(Repeat for `app-c`, `app-d`)

### 5. Deploy Frontend (React)
Use Firebase Hosting:
```bash
cd react-frontend
firebase init hosting
firebase deploy
```

Or deploy to Cloud Run with a Dockerfile.

---

## 🧪 Testing

Use curl:
```bash
curl -X POST https://<APP_A_URL>/predict \
     -H "Authorization: Bearer <firebase_id_token>" \
     -H "Content-Type: application/json" \
     -d '{"inputs": [10, 20, 30]}'
```

---

## ✅ Next Steps

- Add monitoring/logging
- Extend Firebase claims for roles
- Add rate limiting via API Gateway
