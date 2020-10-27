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

module "api" {
      source              = "./api"
}
module "config_manager" {
      source              = "./config_manager"
}
module "database" {
      source              = "./database"
}
module "mailserver" {
      source              = "./mailserver"
}