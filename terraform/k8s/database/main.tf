resource "kubernetes_deployment" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = "default"

    labels = {
      app = "influxdb"
    }

    annotations = {
      "deployment.kubernetes.io/revision" = "1"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "influxdb"
      }
    }

    template {
      metadata {
        labels = {
          app = "influxdb"
        }
      }

      spec {
        volume {
          name = "var-lib-influxdb"

          persistent_volume_claim {
            claim_name = "influxdb"
          }
        }

        container {
          name  = "influxdb"
          image = "docker.io/influxdb:1.6.4"

          volume_mount {
            name       = "var-lib-influxdb"
            mount_path = "/var/lib/influxdb"
          }

          image_pull_policy = "Always"
        }

        restart_policy                   = "Always"
        termination_grace_period_seconds = 30
        dns_policy                       = "ClusterFirst"
      }
    }

    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_unavailable = "25%"
        max_surge       = "25%"
      }
    }

    revision_history_limit    = 10
    progress_deadline_seconds = 600
  }
}

resource "kubernetes_service" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = "default"

    labels = {
      app = "influxdb"
    }
  }

  spec {
    port {
      protocol    = "TCP"
      port        = 8086
      target_port = "8086"
    }

    selector = {
      app = "influxdb"
    }

    cluster_ip       = "10.43.164.44"
    type             = "ClusterIP"
    session_affinity = "None"
  }
}

