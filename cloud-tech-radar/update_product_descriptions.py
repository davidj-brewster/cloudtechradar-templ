import json

# Load the existing product_definitions.json
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

# Adding keywords, descriptions, and example use cases
product_updates = {
    "BigQuery": {
        "keywords": "data warehouse",
        "description": "Highly scalable, serverless data warehouse for big data",
        "example_use_cases": ["Data analytics", "Business intelligence", "Big data"]
    },
    "AI Platform": {
        "keywords": "machine learning models",
        "description": "Service for building and deploying machine learning models",
        "example_use_cases": ["Machine learning", "AI workflows", "Model training"]
    },
    "Dataflow": {
        "keywords": "stream and batch processing",
        "description": "Service for stream and batch data processing",
        "example_use_cases": ["Data processing", "Real-time ETL", "Data pipelines"]
    },
    "Dataproc": {
        "keywords": "big data processing",
        "description": "Spark and Hadoop service for big data processing",
        "example_use_cases": ["Big data analytics", "Data transformation", "ETL jobs"]
    },
    "Cloud Storage": {
        "keywords": "scalable object storage",
        "description": "Secure, durable, and scalable object storage",
        "example_use_cases": ["Data backup", "Content storage", "Archival storage", "Content delivery/retrieval", "Tiered storage", "Business critical data", "Batch processing data", "Flow outputs", "Snapshots", "Assets and derivatives"]
    },
    "Filestore": {
        "keywords": "file storage",
        "description": "High performance file storage for applications",
        "example_use_cases": ["File storage", "NFS storage", "Application data"]
    },
    "GKE": {
        "keywords": "Kubernetes clusters",
        "description": "Service for running and managing Kubernetes clusters",
        "example_use_cases": ["Realtime pods", "Batch processing pods", "Horizontal scaling workloads", "Cronjobs", "Service Mesh integration", "Autoscaling workloads", "Autoscaling clusters"]
    },
    "Compute Engine": {
        "keywords": "virtual machines",
        "description": "Scalable virtual machines for compute workloads",
        "example_use_cases": ["Virtual machines", "Compute workloads", "Custom VMs", "Spot instances", "Vertical scaling workloads"]
    },
    "Cloud Functions": {
        "keywords": "serverless functions",
        "description": "Event-driven platform to run code without managing servers",
        "example_use_cases": ["Serverless functions", "Event-driven apps"]
    },
    "Cloud Run": {
        "keywords": "Kubernetes containers",
        "description": "Service to run stateless containers on Kubernetes",
        "example_use_cases": ["Smaller stateless services", "Downscaling to 0", "Simplified container deployments", "Developer branch environments", "Canary deployments"]
    },
    "Cloud Build": {
        "keywords": "CI/CD service",
        "description": "Service for building, testing, and deploying code",
        "example_use_cases": ["Continuous integration", "Continuous deployment", "Build automation"]
    },
    "Artifact Registry": {
        "keywords": "artifact storage",
        "description": "Store and manage build artifacts and dependencies",
        "example_use_cases": ["Artifact storage", "Dependency management", "Container registry"]
    },
    "Container Registry": {
        "keywords": "Docker images",
        "description": "Private Docker image storage on Google Cloud",
        "example_use_cases": ["Docker images", "Container storage", "Image management", "Docker image repo"]
    },
    "Cloud SQL": {
        "keywords": "SQL databases",
        "description": "Relational database service with high availability",
        "example_use_cases": ["SQL databases", "Transactional apps", "Relational data"]
    },
    "AlloyDB": {
        "keywords": "PostgreSQL databases",
        "description": "PostgreSQL-compatible relational database service",
        "example_use_cases": ["PostgreSQL databases", "Enterprise apps", "Transactional workloads"]
    },
    "MongoDB Atlas": {
        "keywords": "NoSQL databases",
        "description": "Managed MongoDB service for modern applications",
        "example_use_cases": ["NoSQL databases", "Document storage", "Scalable apps"]
    },
    "Cloud Spanner": {
        "keywords": "global databases",
        "description": "Horizontally scalable, strongly consistent relational database",
        "example_use_cases": ["Global databases", "Financial services", "High availability"]
    },
    "Firestore": {
        "keywords": "NoSQL document database",
        "description": "Document database for automatic scaling and performance",
        "example_use_cases": ["Mobile apps", "Web apps", "Real-time data"]
    },
    "GitHub": {
        "keywords": "code hosting",
        "description": "Code hosting platform for version control and collaboration",
        "example_use_cases": ["Version control", "Code collaboration", "Open source"]
    },
    "GitHub Actions": {
        "keywords": "CI/CD workflows",
        "description": "Service for automated software workflows on GitHub",
        "example_use_cases": ["CI/CD pipelines", "Automated testing", "Deployment workflows"]
    },
    "Jenkins": {
        "keywords": "automation server",
        "description": "Open-source automation server for CI/CD pipelines",
        "example_use_cases": ["Continuous integration", "Continuous delivery", "Automated builds"]
    },
    "Grafana OSS": {
        "keywords": "monitoring dashboards",
        "description": "Open-source platform for monitoring and observability",
        "example_use_cases": ["Monitoring dashboards", "Metrics visualization", "Alerting"]
    },
    "Grafana Cloud": {
        "keywords": "managed Grafana",
        "description": "Grafana service for metrics, logs, and traces",
        "example_use_cases": ["Monitoring", "Cloud observability", "Dashboarding", "Alerting"]
    },
    "Prometheus": {
        "keywords": "metrics monitoring",
        "description": "Monitoring and alerting toolkit for metrics",
        "example_use_cases": ["Metrics collection", "Alerting", "Monitoring"]
    },
    "VictoriaMetrics OSS": {
        "keywords": "time series database",
        "description": "Open-source time series database for metrics storage",
        "example_use_cases": ["High-performance metrics", "Monitoring", "Metrics storage"]
    },
    "Gradle": {
        "keywords": "build automation",
        "description": "Build automation tool for Java and other languages",
        "example_use_cases": ["Build automation", "Dependency management", "Java builds"]
    },
    "Harbor": {
        "keywords": "container registry",
        "description": "Push-style proxy to upload images to Nexus/GCR instances",
        "example_use_cases": ["Artifact push proxy", "Vulnerability scanning"]
    },
    "Nexus Repository OSS": {
        "keywords": "artifact repository",
        "description": "Artifact repository manager for binaries and build artifacts",
        "example_use_cases": ["Artifact management", "Dependency storage", "Repository management", "Python packages", "Java artifacts", "Docker images", "Helm charts"]
    }
}

# Update product definitions
for product, update in product_updates.items():
    product_definitions[product]["keywords"] = update["keywords"]
    product_definitions[product]["description"] = update["description"]
    product_definitions[product]["example_use_cases"] = update["example_use_cases"]

# Save the updated product_definitions.json
output_path = 'product_definitions_updated.json'
with open(output_path, 'w') as f:
    json.dump(product_definitions, f, indent=4)

print(f"Updated product definitions saved to {output_path}")

