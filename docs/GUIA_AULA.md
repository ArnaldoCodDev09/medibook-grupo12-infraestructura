# Guía de la actividad y evidencias

## Lo que pide la grabación

En el tramo de aproximadamente 2:33–2:38, el profesor indica que cada grupo debe trabajar con su propio proyecto, desplegarlo en `us-east-2`, ejecutar el despliegue con Terraform, guardar evidencia del `apply` y luego evidencia del `destroy`. También explica que el estado de Terraform se guarda en un bucket S3 creado previamente y que el borrado puede automatizarse con un workflow manual de GitHub Actions.

El profesor menciona que el PDF de instrucciones lo adjuntaría a la actividad. Este repositorio implementa el flujo que se alcanza a escuchar en la grabación; revisa el PDF oficial del aula si añade pasos o una plantilla de entrega.

## Pasos

1. Crea el repositorio GitHub del grupo y sube este proyecto.
2. Crea manualmente un bucket S3 de estado en `us-east-2`, con nombre globalmente único, cifrado y versionado. No lo agregues a la infraestructura que se va a destruir.
3. Configura un proveedor OIDC de GitHub en IAM y un rol de despliegue limitado al repositorio. Añade al repositorio las variables `AWS_ROLE_ARN`, `AWS_REGION=us-east-2` y `TF_STATE_BUCKET`.
4. En **Actions → Terraform Apply → Run workflow**, escribe `APPLY`.
5. Comprueba que la ejecución termina en verde. Abre la URL `site_url` desde los logs de Terraform, crea una reserva ficticia y confirma que aparece en la agenda.
6. Toma capturas legibles de: ejecución `apply` exitosa, URL de la aplicación con una reserva de prueba y ejecución `destroy` exitosa.
7. En **Actions → Terraform Destroy → Run workflow**, escribe `DESTROY`.
8. Prepara el PDF de entrega con las capturas reales, el enlace del repositorio, la región y una nota de que el bucket de estado se conserva.

## Qué debe verse en las capturas

- **Apply:** nombre del workflow, estado exitoso, región `us-east-2` y salidas de Terraform `site_url`/`api_url`. Oculta identificadores de cuenta si aparecen.
- **Aplicación:** página MediBook abierta en CloudFront y una reserva de datos ficticios.
- **Destroy:** workflow completado y confirmación de que los recursos administrados se eliminaron.

No presentes `terraform plan` como si fuera un `apply`. El plan no demuestra que los recursos se hayan creado. No inventes ni recrees capturas de una ejecución real.

## Recursos y costos

La demo crea CloudFront, S3 para el sitio, API Gateway, Lambda y dos tablas DynamoDB. La facturación depende del uso, región y condiciones de la cuenta. Ejecuta `destroy` al terminar. El bucket remoto de estado permanece y puede seguir generando cargos pequeños por almacenamiento/solicitudes. Revisa la consola de costos y elimina ese bucket al final del curso solo cuando ya no necesites conservar el estado.

La arquitectura completa del informe MediBook se reserva para una fase posterior porque EC2, ALB, RDS Multi-AZ, NAT Gateways, Redis y la replicación entre regiones amplían el alcance y el costo.

