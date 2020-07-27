resource "kubernetes_cron_job" "taurus" {
  metadata {
    name = "taurus"

    labels = {
      app = "taurus"
    }
  }

  spec {
    schedule           = "15 * * * *"
    concurrency_policy = "Replace"

    job_template {
      metadata {}

      spec {
        template {
          metadata {}

          spec {
            container {
              name              = "taurus"
              image             = "carnage/taurus"
              image_pull_policy = "Always"
            }

            restart_policy = "Never"
          }
        }
      }
    }

    successful_jobs_history_limit = 3
    failed_jobs_history_limit     = 3
  }
}

