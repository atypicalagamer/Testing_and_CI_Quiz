FROM python:3.10-slim
WORKDIR /home
COPY requirements.txt /home
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Optional: Default command to run tests
CMD ["pytest", "--cov=engagement", "test_engagement.py"]