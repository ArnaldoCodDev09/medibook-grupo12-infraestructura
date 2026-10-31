# Preparación manual de AWS y GitHub

El proveedor OIDC y el bucket de estado son prerrequisitos. No se crean con `terraform destroy`, para que el estado sobreviva al ciclo `apply`/`destroy`.

## 1. Bucket de estado

Usa un nombre globalmente único y una cuenta/región de aula. Sustituye `BUCKET_STATE_UNICO` en estos comandos:

```powershell
aws s3api create-bucket --bucket BUCKET_STATE_UNICO --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
aws s3api put-bucket-versioning --bucket BUCKET_STATE_UNICO --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket BUCKET_STATE_UNICO --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
aws s3api put-public-access-block --bucket BUCKET_STATE_UNICO --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

Después copia `infra/backend.hcl.example` a `infra/backend.hcl` y reemplaza el nombre del bucket.

## 2. GitHub OIDC

1. En IAM crea el proveedor de identidad `token.actions.githubusercontent.com` con audiencia `sts.amazonaws.com`. Si ya existe, reutilízalo.
2. Reemplaza `ACCOUNT_ID`, `OWNER` y `REPOSITORY` en `github-oidc-trust-policy.example.json`.
3. Crea un rol IAM de despliegue con esa política de confianza. La confianza queda limitada al entorno de GitHub `medibook-demo` de ese repositorio.
4. Copia `github-deploy-policy.example.json`, reemplaza `STATE_BUCKET` y adjúntala como política inline al rol. Es un perfil para una cuenta de aula; revísalo con el docente/administrador de AWS antes de usarlo en una cuenta compartida.
5. En GitHub, crea el environment `medibook-demo` y las variables de repositorio: `AWS_ROLE_ARN` con el ARN del rol, `AWS_REGION` con `us-east-2` y `TF_STATE_BUCKET` con el bucket.

No coloques `AWS_ACCESS_KEY_ID` ni `AWS_SECRET_ACCESS_KEY` en el repositorio. Los workflows intercambian el token OIDC de GitHub por una sesión temporal.

## 3. Importante para la entrega

La primera vez, ejecuta `terraform init -backend-config=backend.hcl` desde `infra`. El bucket de estado debe existir antes. El workflow de GitHub usa las mismas propiedades de backend desde variables y deja el archivo local fuera del repositorio.

