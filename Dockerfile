FROM node:18-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

COPY backend/ai-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "setuptools<81"

COPY backend/ai-service/ ./

COPY --from=frontend-build /app/frontend/dist ./static

RUN printf '\n\
from fastapi.staticfiles import StaticFiles\n\
from fastapi.responses import FileResponse\n\
import os\n\
\n\
static_dir = os.path.join(os.path.dirname(__file__), "static")\n\
if os.path.exists(static_dir):\n\
    assets_dir = os.path.join(static_dir, "assets")\n\
    if os.path.exists(assets_dir):\n\
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")\n\
\n\
    @app.get("/{path:path}")\n\
    async def serve_spa(path: str):\n\
        file_path = os.path.join(static_dir, path)\n\
        if os.path.isfile(file_path):\n\
            return FileResponse(file_path)\n\
        return FileResponse(os.path.join(static_dir, "index.html"))\n\
' >> ./main.py

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
