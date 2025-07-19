FROM python:3.9-slim

# Set working directory to /backend
WORKDIR /backend

# Copy only backend files
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
