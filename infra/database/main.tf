resource "helm_release" "consul" {
  name  = "database"
  chart = "bitnami/influxdb"
}