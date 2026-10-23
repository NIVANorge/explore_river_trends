FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt

COPY app/ ./app/
COPY output/ ./output/
COPY README.md ./README.md

EXPOSE 8501

CMD ["streamlit", "run", "app/Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]