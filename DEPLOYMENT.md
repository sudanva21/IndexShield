# Deployment Guide: Inbox Shield

This guide explains how to deploy the **Inbox Shield** project for free using **Render** (Backend) and **Vercel** (Frontend).

## 1. Prerequisites
- The code is successfully pushed to your GitHub repo: [https://github.com/sudanva21/IndexShield](https://github.com/sudanva21/IndexShield)
- You have accounts on [Render.com](https://render.com) and [Vercel.com](https://vercel.com).

---

## 2. Backend Deployment (Render)
Hosted as a Python Web Service.

1.  **Dashboard**: Go to your Render Dashboard and click **"New +"** -> **"Web Service"**.
2.  **Connect Repo**: Select `sudanva21/IndexShield`.
3.  **Settings**:
    -   **Name**: `inbox-shield-backend`
    -   **Root Directory**: `backend` (Important!)
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
    -   **Instance Type**: Free
4.  **Deploy**: Click "Create Web Service".
5.  **Copy URL**: Once live, copy the URL (e.g., `https://inbox-shield-backend.onrender.com`).

---

## 3. Frontend Deployment (Vercel)
Hosted as a Static React App.

1.  **Dashboard**: Go to Vercel and click **"Add New..."** -> **"Project"**.
2.  **Connect Repo**: Select `sudanva21/IndexShield`.
3.  **Configure Project**:
    -   **Framework Preset**: Vite
    -   **Root Directory**: Click "Edit" and select `frontend`.
4.  **Environment Variables**:
    -   Add a variable named `VITE_API_URL`.
    -   Value: The **Render Backend URL** you copied in Step 2 (e.g., `https://inbox-shield-backend.onrender.com`).
5.  **Deploy**: Click "Deploy".

Your app will now be live and connected!
