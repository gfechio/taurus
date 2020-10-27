resource "helm_release" "consul" {
  name  = "grafana"
  chart = "bitnami/grafana"
}