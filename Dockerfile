FROM python:3.11-slim

WORKDIR /opt/workshop
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && useradd --create-home --uid 10001 workshop
USER workshop
ENV WORKSHOP_PROVIDER=fake \
    WORKSHOP_ENABLE_LIVE_PROVIDER=0 \
    PYTHONUNBUFFERED=1
CMD ["python", "-m", "workshop", "demo"]
