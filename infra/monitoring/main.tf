provider "kubernetes" {
}

terraform {
  backend "local" {
    path = "/mnt/SSD/_terraform_states/taurus.tfstate"
  }
}

resource "kubernetes_namespace" "taurus" {
  metadata {
    name = "taurus"
  }
}