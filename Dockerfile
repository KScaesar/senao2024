# https://snyk.io/blog/best-practices-containerizing-python-docker/

# First stage: Install dependencies and build application
FROM python:3.10-slim AS builder

WORKDIR /build

COPY ./requirements.txt .

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    pip install --no-cache-dir --prefix=/build -r requirements.txt

# Second stage: Create the final lightweight image
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH="/app"

# Copy only necessary files and dependencies from the builder stage
COPY --from=builder /build /usr/local
COPY ./main.py .
COPY ./src ./src

EXPOSE 12450

CMD ["fastapi", "run", "main.py" ,"--port", "12450"]
#CMD ["python", "main.py" ]