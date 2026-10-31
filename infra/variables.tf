variable "aws_region" {
  description = "Región indicada para la actividad del curso."
  type        = string
  default     = "us-east-2"
}

variable "environment" {
  description = "Sufijo de los recursos de demostración."
  type        = string
  default     = "demo"

  validation {
    condition     = can(regex("^[a-z0-9-]{2,12}$", var.environment))
    error_message = "Usa 2 a 12 caracteres: minúsculas, números o guiones."
  }
}

variable "lambda_zip_path" {
  description = "ZIP generado por scripts/package_lambda.py."
  type        = string
  default     = "../lambda/build/medibook-api.zip"
}

