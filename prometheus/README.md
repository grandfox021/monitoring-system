# Prometheus Monitoring Configuration

This document describes the `prometheus.yml` configuration file used to monitor a distributed system comprising web applications, databases, and infrastructure components.

## Configuration File

The full `prometheus.yml` configuration is shown below:

```yaml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config
  - job_name: "prometheus"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

  - job_name: "grafana"
    static_configs:
      - targets: ["localhost:3000"]

  # Node exporter on VM1 (web app host)
  - job_name: "node_exporter_webapp"
    static_configs:
      - targets: ["172.16.61.145:9100"]

  # cAdvisor on VM1 (monitor Docker containers)
  - job_name: "cadvisor_webapp"
    static_configs:
      - targets: ["172.16.61.145:8080"]

  # Node exporter on VM2 (MongoDB host)
  - job_name: "node_exporter_mongodb"
    static_configs:
      - targets: ["172.16.61.150:9100"]

  # MongoDB exporter on VM2
  - job_name: "mongodb_exporter_mongodb"
    static_configs:
      - targets: ["172.16.61.150:9216"]

  # cAdvisor on VM2 (MongoDB host)
  - job_name: "cadvisor_mongodb"
    static_configs:
      - targets: ["172.16.61.150:8080"]

  # FastAPI app metrics
  - job_name: "fastapi_app"
    static_configs:
      - targets: ["172.16.61.145:8000"]

  # Blackbox HTTP monitoring
  - job_name: "blackbox_http"
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - http://172.16.61.145:8000  # your FastAPI app
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 172.16.61.141:9115  # blackbox exporter host:port