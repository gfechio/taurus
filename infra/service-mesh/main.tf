resource "kubernetes_pod" "consul_example" {
  metadata {
    name = "consul-example"
  }

  spec {
    container {
      name    = "example"
      image   = "consul:latest"
      command = ["/bin/sh", "-ec", "export CONSUL_HTTP_ADDR=\"$${HOST_IP}:8500\"\nconsul kv put hello world\n"]

      env {
        name = "HOST_IP"

        value_from {
          field_ref {
            field_path = "status.hostIP"
          }
        }
      }
    }

    restart_policy = "Never"
  }
}

resource "kubernetes_pod" "consul" {
  metadata {
    name = "consul"
  }

  spec {
    container {
      name    = "consul"
      image   = "consul:latest"
      command = ["/bin/sh", "-ec", "export CONSUL_HTTP_ADDR=\"192.168.178.23:8500\"\nconsul kv put hello world\n"]

      env {
        name = "192.168.178.23"

        value_from {
          field_ref {
            field_path = "status.hostIP"
          }
        }
      }
    }

    restart_policy = "Never"
  }
}

