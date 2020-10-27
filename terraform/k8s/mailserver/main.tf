resource "helm_release" "mailserver" {
  name  = "mailserver"
  chart = "halkeye/postfix"
}