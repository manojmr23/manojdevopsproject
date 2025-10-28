resource "kubernetes_service" "app_service" {
  metadata {
    name = "doctor-appointment-service"
  }

  spec {
    selector = {
      app = "doctor-appointment"
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "NodePort"
  }
}
