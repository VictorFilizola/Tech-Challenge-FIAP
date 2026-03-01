# Amazon Bestsellers: Data Pipeline & Analytics API
**Tech Challenge - Phase 1 | Machine Learning Engineering**

This project is a containerized REST API built with **FastAPI** and **Selenium**. It automates the extraction of the Top 100 Amazon Bestselling books, persists the data in a local JSON cache, and provides specialized analytical endpoints for market research.

## Project Architecture
The system follows a **Decoupled Data Pipeline** pattern:
1.  **Ingestion:** Selenium (Headless Edge) bypasses lazy-loading to scrape 100 records.
2.  **Persistence:** Data is saved to `data/bestsellers.json`. This acts as a **Temporary Local Dataset**, ensuring that analytical queries are near-instant and do not trigger unnecessary web requests.
3.  **Analytics:** Dedicated routes use Pandas to process the cached JSON.

---

## Execution Guide

### Option 1: Local Terminal (Virtual Environment)
Ideal for quick testing if you have Microsoft Edge installed on Windows.
1.  **Create & Activate VENV:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Server:**
    ```bash
    uvicorn src.main:app --reload
    ```
4.  **Access:** `http://127.0.0.1:8000/docs`

### Option 2: Docker Container 
The most stable method. It bundles a Linux-compatible Edge browser internally.
1.  **Build Image:**
    ```bash
    docker build -t amazon-api .
    ```
2.  **Run Container:**
    ```bash
    docker run -p 8000:8000 amazon-api
    ```
3.  **Access:** `http://localhost:8000/docs`

### Option 3: Cloud Deployment (Railway/Render)
For remote testing without local installation:
1.  Push this repository to GitHub.
2.  Connect the repository to **Railway** or **Render**.
3.  Ensure the `PORT` environment variable is set to `8000`.
4.  **Live Docs:** `https://your-app-name.railway.app/docs`

---

## API Workflow & Testing
To properly test the application, follow this sequence in the Swagger UI:

1.  **Check Health:** Execute `GET /health` to confirm the API is up.
2.  **Trigger Scrape:** Execute `POST /api/scrape`. 
    * *What happens:* A browser opens (headless), scrolls, and saves 100 items to a local file.
3.  **Retrieve Data:** Execute `GET /api/books`. It reads directly from the generated file.
4.  **Run Analytics:** Use `/api/analysis/pricing`, `/api/analysis/authors`, etc. 
    * *Note:* These routes perform calculations on the **cached dataset** generated in step 2.

---

## Data Storage Notice
The API generates a `data/bestsellers.json` file inside the environment. If running in **Docker**, this file exists inside the container's isolated filesystem. To persist this to your host machine, use a volume:
`docker run -p 8000:8000 -v %cd%/data:/app/data amazon-api`