FROM python:3.12-slim
WORKDIR /app
COPY agent/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY agent /app/agent
COPY shared /app/shared
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "-m", "agent.agentcore_app"]
