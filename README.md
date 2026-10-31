# MediBook — despliegue de demostración

Repositorio de aula para desplegar una versión pequeña de MediBook en AWS con Terraform. Sigue la indicación del profesor: desplegar en `us-east-2`, conservar el estado remoto en un bucket S3 creado previamente y guardar evidencia del `apply` y del `destroy`.

## Alcance

Esta versión de demostración publica una página estática en S3/CloudFront y una API HTTP en API Gateway con Lambda y DynamoDB para registrar turnos de prueba. Conserva el flujo de reservas de MediBook y permite demostrar el ciclo de infraestructura como código.

No despliega todavía la arquitectura completa del informe (EC2 Auto Scaling, ALB, RDS Multi-AZ, NAT, Redis, respaldos y región secundaria). Esa topología representa el diseño objetivo y puede generar cargos relevantes. Este repositorio evita presentar como implementados recursos que aún no se han desplegado. No ingreses datos reales de pacientes: la API de demostración no tiene autenticación y no es apta para información clínica.

## Requisitos previos

- Cuenta de AWS de aula y región `us-east-2`.
- AWS CLI, Terraform `>= 1.10`, Python 3 y Git.
- Un bucket S3 único, creado manualmente en `us-east-2`, para el estado de Terraform. Activa versionado, cifrado y bloqueo de acceso público. El bucket del estado queda fuera del `destroy` de esta aplicación.
- Para GitHub Actions: un rol IAM con proveedor OIDC de GitHub y permisos limitados al prefijo `medibook-demo-*`; configura `AWS_ROLE_ARN`, `AWS_REGION` y `TF_STATE_BUCKET` como variables del repositorio. No uses claves permanentes de AWS.

Consulta [docs/GUIA_AULA.md](docs/GUIA_AULA.md) para la configuración inicial, el flujo de despliegue y la lista de capturas requeridas.

## Despliegue local

1. Crea `infra/backend.hcl` a partir de `infra/backend.hcl.example` y completa el nombre del bucket remoto.
2. Empaqueta la función: `python scripts/package_lambda.py`.
3. Ejecuta:

   ```powershell
   cd infra
   terraform init -backend-config=backend.hcl
   terraform plan -out=tfplan
   terraform apply tfplan
   terraform output
   ```

4. Abre la URL `site_url` de la salida y registra un turno de prueba. Guarda una captura del despliegue exitoso y otra de la aplicación funcionando.
5. Al terminar la demostración, ejecuta `terraform destroy` y confirma que finalice. Guarda una captura de esa salida.

## GitHub Actions

Los workflows se disparan manualmente desde **Actions**. `Terraform Apply` crea la demo. `Terraform Destroy` exige escribir `DESTROY` antes de borrar los recursos de la aplicación. El bucket del estado no forma parte de Terraform y se conserva.

## Evidencias y entrega

Prepara un PDF con: repositorio y arquitectura desplegada; evidencia del `terraform apply` exitoso; URL de la demo y reserva de prueba; evidencia del `terraform destroy` exitoso; y una nota de que el bucket de estado remoto se mantiene. Usa capturas reales de la ejecución; no sustituyas evidencia de AWS por capturas de un plan local.

## Limpieza

`terraform destroy` elimina los recursos administrados por este proyecto. Revisa que los dos buckets que se esperan queden claros: el bucket de la web se elimina junto con sus objetos; el bucket remoto del estado permanece para conservar historial y poder volver a ejecutar el laboratorio.

