resource "helm_release" "consul" {
  name  = "config_manager"
  chart = "hashicorp/consul"

  set {
    name  = "global.name"
    value =  "consul"
  }
}