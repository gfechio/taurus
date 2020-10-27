module "worker" {
      source              = "./worker"
}

module "api" {
      source              = "./worker"
}

module "searcher" {
      source              = "./worker"
}