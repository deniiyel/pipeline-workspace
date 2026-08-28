import time
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Time-Series Metrics API")

class MetricIngest(BaseModel):
    metric_name: str
    value: float
    timestamp: Optional[float] = None

class MetricStats(BaseModel):
    metric_name: str
    count: int
    min_value: float
    max_value: float
    avg_value: float

# In-memory data store for metrics
metrics_db: Dict[str, List[Dict[str, float]]] = {}

@app.post("/metrics", status_code=status.HTTP_201_CREATED)
def record_metric(metric: MetricIngest):
    if not metric.metric_name.strip():
        raise HTTPException(status_code=400, detail="Metric name cannot be empty")
    
    if metric.metric_name not in metrics_db:
        metrics_db[metric.metric_name] = []
    
    entry_timestamp = metric.timestamp if metric.timestamp is not None else time.time()
    
    metrics_db[metric.metric_name].append({
        "value": metric.value,
        "timestamp": entry_timestamp
    })
    return {"message": "Metric recorded successfully", "metric_name": metric.metric_name}

@app.get("/metrics/{metric_name}/stats", response_model=MetricStats)
def get_metric_stats(metric_name: str):
    if metric_name not in metrics_db or not metrics_db[metric_name]:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    values = [entry["value"] for entry in metrics_db[metric_name]]
    count = len(values)
    min_val = min(values)
    max_val = max(values)
    avg_val = sum(values) / count

    return MetricStats(
        metric_name=metric_name,
        count=count,
        min_value=round(min_val, 4),
        max_value=round(max_val, 4),
        avg_value=round(avg_val, 4)
    )

@app.delete("/metrics", status_code=status.HTTP_200_OK)
def clear_metrics():
    metrics_db.clear()
    return {"message": "All metrics cleared"}