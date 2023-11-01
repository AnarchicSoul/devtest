resource "helm_release" "nginx_ingress" {
  name       = "pytestapp"
  repository = "https://anarchicsoul.github.io/python"
  chart      = "pytestapp"
  version    = "0.2.0"
  values = [
    "${file("pytestapp.value")}"
  ]
}