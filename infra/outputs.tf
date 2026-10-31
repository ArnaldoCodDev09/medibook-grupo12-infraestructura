output "site_url" {
  description = "URL HTTPS del sitio MediBook de demostración."
  value       = "https://${aws_cloudfront_distribution.site.domain_name}"
}

output "api_url" {
  description = "URL base de la API de demostración."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "aws_region" {
  value = var.aws_region
}

