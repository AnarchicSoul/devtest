resource "helm_release" "nginx_ingress" {
  name       = "pytestapp"
  repository = "https://anarchicsoul.github.io/python"
  chart      = "pytestapp"
  version    = "<version>"
  values = [
    "${file("pytestapp.value")}"
  ]
}