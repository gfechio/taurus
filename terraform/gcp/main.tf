terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.44.0"
    }
  }
}

provider "google" {
  credentials = file("account.json")
  project     = "taurus"
  region      = "us-central1"
}