# main.tf

# Provider configuration (using your existing Kubernetes setup)
provider "kubernetes" {
  config_path = "~/.kube/config"
}

# Create a new namespace for your app
resource "kubernetes_namespace" "doctor_app" {
  metadata {
    name = "doctor-appointment"
  }
}

# Deploy a Kubernetes deployment (optional)
resource "kubernetes_deployment" "doctor_app_deploy" {
  metadata {
    name = "doctor-app"
    namespace = kubernetes_namespace.doctor_app.metadata[0].name
    labels = {
      app = "doctor-app"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "doctor-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "doctor-app"
        }
      }

      spec {
        container {
          image = "doctor-appointment-app:latest"
          name  = "doctor-app"
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}
