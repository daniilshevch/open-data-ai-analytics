output "public_ip_address" {
  value = azurerm_public_ip.main.ip_address
}

output "web_app_url" {
  value = "http://${azurerm_public_ip.main.ip_address}:5000"
}

output "grafana_url" {
  value = "http://${azurerm_public_ip.main.ip_address}:3000"
}