const techRadar: TechRadar = {
    title: "Tech Radar - Cloud",
    quadrants: [
        {
            id: "data_ml",
            name: "Data and Machine Learning"
        },
        {
            id: "storage",
            name: "Storage Solutions"
        },
        {
            id: "compute",
            name: "Compute and GKE"
        },
        {
            id: "build_ci",
            name: "Build and Deployment"
        }
    ],
    rings: [
        {
            id: "adopt",
            name: "Adopt",
            color: "#93c47d"
        },
        {
            id: "trial",
            name: "Trial",
            color: "#93d2c2"
        },
        {
            id: "assess",
            name: "Assess",
            color: "#fbdb84"
        },
        {
            id: "hold",
            name: "Hold",
            color: "#efafa9"
        }
    ],
    entries: [
        {
            id: "BigQuery",
            title: "BigQuery",
            description: "Highly scalable, serverless data warehouse for big data",
            key: "BigQuery",
            url: "https://cloud.google.com/bigquery",
            quadrant: "data_ml",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "AI Platform",
            title: "AI Platform",
            description: "Service for building and deploying machine learning models",
            key: "AI Platform",
            url: "https://cloud.google.com/ai-platform",
            quadrant: "data_ml",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Dataflow",
            title: "Dataflow",
            description: "Service for stream and batch data processing",
            key: "Dataflow",
            url: "https://cloud.google.com/dataflow",
            quadrant: "data_ml",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Dataproc",
            title: "Dataproc",
            description: "Spark and Hadoop service for big data processing",
            key: "Dataproc",
            url: "https://cloud.google.com/dataproc",
            quadrant: "data_ml",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Cloud Storage",
            title: "Cloud Storage",
            description: "Secure, durable, and scalable object storage",
            key: "Cloud Storage",
            url: "https://cloud.google.com/storage",
            quadrant: "storage",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Filestore",
            title: "Filestore",
            description: "High performance file storage for applications",
            key: "Filestore",
            url: "https://cloud.google.com/filestore",
            quadrant: "storage",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "GKE",
            title: "Google Kubernetes Engine (GKE)",
            description: "Service for running and managing Kubernetes clusters",
            key: "GKE",
            url: "https://cloud.google.com/kubernetes-engine",
            quadrant: "compute",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "GKE Autopilot",
            title: "Google Kubernetes Engine (GKE) Autopilot",
            description: "Cluster, Pod and container environment with reduced management overhead",
            key: "GKE Autopilot",
            url: "https://cloud.google.com/kubernetes-engine",
            quadrant: "compute",
            timeline: [
                {
                    ring: "assess",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Compute Engine",
            title: "Compute Engine",
            description: "Scalable virtual machines for compute and memory intensive workloads",
            key: "Compute Engine",
            url: "https://cloud.google.com/compute",
            quadrant: "compute",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Cloud Functions",
            title: "Cloud Functions",
            description: "Event-driven platform to run code without managing servers",
            key: "Cloud Functions",
            url: "https://cloud.google.com/functions",
            quadrant: "compute",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Cloud Run",
            title: "Cloud Run",
            description: "Service to run stateless containers on compute instances that scale on demand",
            key: "Cloud Run",
            url: "https://cloud.google.com/run",
            quadrant: "compute",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Cloud Build",
            title: "Cloud Build",
            description: "Integrated service for building, testing, and deploying code",
            key: "Cloud Build",
            url: "https://cloud.google.com/cloud-build",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Artifact Registry",
            title: "Artifact Registry",
            description: "Store and manage build artifacts and dependencies",
            key: "Artifact Registry",
            url: "https://cloud.google.com/artifact-registry",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Container Registry",
            title: "Container Registry",
            description: "Private Docker image storage on Google Cloud",
            key: "Container Registry",
            url: "https://cloud.google.com/container-registry",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "assess",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Cloud SQL",
            title: "Cloud SQL",
            description: "Relational database service with high availability",
            key: "Cloud SQL",
            url: "https://cloud.google.com/sql",
            quadrant: "storage",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "AlloyDB",
            title: "AlloyDB",
            description: "PostgreSQL-compatible relational database service",
            key: "AlloyDB",
            url: "https://cloud.google.com/alloydb",
            quadrant: "storage",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "MongoDB Atlas",
            title: "MongoDB Atlas",
            description: "Managed MongoDB service for modern applications",
            key: "MongoDB Atlas",
            url: "https://www.mongodb.com/cloud/atlas",
            quadrant: "storage",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Firestore",
            title: "Firestore",
            description: "Document database for automatic scaling and performance",
            key: "Firestore",
            url: "https://cloud.google.com/firestore",
            quadrant: "storage",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "GitHub",
            title: "GitHub",
            description: "Code hosting platform for version control and collaboration",
            key: "GitHub",
            url: "https://github.com",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "GitHub Actions",
            title: "GitHub Actions",
            description: "Automation service for CI/CD workflows on GitHub",
            key: "GitHub Actions",
            url: "https://github.com/features/actions",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Jenkins",
            title: "Jenkins",
            description: "Automation server for CI/CD pipelines defined in code",
            key: "Jenkins",
            url: "https://www.jenkins.io",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "retire",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Grafana OSS",
            title: "Grafana OSS",
            description: "Open-source platform for monitoring and observability",
            key: "Grafana OSS",
            url: "https://grafana.com/oss/grafana/",
            quadrant: "observability",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Grafana Cloud",
            title: "Grafana Cloud",
            description: "Paid service for storing and discovering metrics, logs, and traces plus alerting",
            key: "Grafana Cloud",
            url: "https://grafana.com/products/cloud/",
            quadrant: "observability",
            timeline: [
                {
                    ring: "assess",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Prometheus",
            title: "Prometheus",
            description: "Monitoring and alerting toolkit for metrics",
            key: "Prometheus",
            url: "https://prometheus.io",
            quadrant: "observability",
            timeline: [
                {
                    ring: "retire",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "VictoriaMetrics OSS",
            title: "VictoriaMetrics OSS",
            description: "Open-source time series database for metrics and alerts, compatible with PromQL",
            key: "VictoriaMetrics OSS",
            url: "https://victoriametrics.com/",
            quadrant: "observability",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Gradle",
            title: "Gradle",
            description: "Build automation tooling for Java and other languages",
            key: "Gradle",
            url: "https://gradle.org",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "adopt",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Harbor",
            title: "Harbor",
            description: "Push-style proxy to upload docker images to an artifact registry",
            key: "Harbor",
            url: "https://goharbor.io",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        },
        {
            id: "Nexus Repository OSS",
            title: "Nexus Repository OSS",
            description: "Artifact repository manager for binaries and build artifacts",
            key: "Nexus Repository OSS",
            url: "https://www.sonatype.com/products/repository-oss",
            quadrant: "build_ci",
            timeline: [
                {
                    ring: "hold",
                    date: "2023-06-07"
                }
            ]
        }
    ]
};
