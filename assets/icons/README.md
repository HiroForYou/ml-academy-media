# Íconos / Icons

Logos usados en los diagramas de arquitectura (gráficos y videos). Solo se guardan los SVG que usa algún diagrama.
Logos used in the architecture diagrams (charts and videos). Only the SVGs some diagram uses are kept.

Los gráficos los rasterizan con `resvg-py` en `output/_icons/` (no versionado); los videos los cargan como `SVGMobject`.
Charts rasterize them with `resvg-py` into `output/_icons/` (not committed); videos load them as `SVGMobject`.

## `aws/` — AWS Architecture Icons

- Fuente / source: paquete oficial «Icon package» publicado el 31-07-2026, descargado el 22-10-2026 desde
  <https://aws.amazon.com/architecture/icons/>
  (`Icon-package_07312026.…zip`: `Architecture-Service-Icons_07312026/*/64/` y `Resource-Icons_07312026/`). Se descargó de nuevo el 28-10-2026 para añadir los íconos de Athena, Lake Formation, herramientas de costo, contenedores, orquestación y otros servicios; cuando un servicio aparece en dos categorías con colores distintos se usa la de la guía del examen (Compute Optimizer: Management and Governance; Kinesis Video Streams: Media). Sin ícono oficial: Service Quotas, Cost Anomaly Detection, Bedrock Guardrails, AWS Inferentia/Trainium/Graviton y SageMaker Feature Store/Model Monitor/Pipelines (esos usan el de SageMaker AI).
- Términos / terms: AWS ofrece estos íconos para que clientes y socios dibujen **diagramas de arquitectura** de AWS.
  Se usan sin modificar (solo se renombran los archivos y se escalan), no como logos propios ni para insinuar
  patrocinio de AWS. Los nombres y logos son marcas de Amazon.com, Inc. o sus filiales; ver
  <https://aws.amazon.com/trademark-guidelines/>.
  AWS provides these icons so customers and partners can draw AWS **architecture diagrams**. They are used unmodified
  (files renamed and scaled only), not as our own logos and without implying AWS endorsement. Names and logos are
  trademarks of Amazon.com, Inc. or its affiliates.

| Archivo / file | Original |
| --- | --- |
| `sagemaker-ai.svg` | `Arch_Amazon-SageMaker-AI_64.svg` |
| `bedrock.svg` | `Arch_Amazon-Bedrock_64.svg` |
| `comprehend.svg`, `textract.svg`, `rekognition.svg`, `transcribe.svg` | `Arch_Amazon-<Service>_64.svg` |
| `s3.svg` | `Arch_Amazon-Simple-Storage-Service_64.svg` |
| `glue.svg` | `Arch_AWS-Glue_64.svg` |
| `kinesis-data-streams.svg` | `Arch_Amazon-Kinesis-Data-Streams_64.svg` |
| `data-firehose.svg` | `Arch_Amazon-Data-Firehose_64.svg` |
| `cloudwatch.svg` | `Arch_Amazon-CloudWatch_64.svg` |
| `cloudtrail.svg` | `Arch_AWS-CloudTrail_64.svg` |
| `kms.svg` | `Arch_AWS-Key-Management-Service_64.svg` |
| `organizations.svg` | `Arch_AWS-Organizations_64.svg` |
| `vpc.svg` | `Arch_Amazon-Virtual-Private-Cloud_64.svg` |
| `privatelink.svg` | `Arch_AWS-PrivateLink_64.svg` |
| `sns.svg` | `Arch_Amazon-Simple-Notification-Service_64.svg` |
| `vpc-endpoints.svg` | `Res_Amazon-VPC_Endpoints_48.svg` |
| `iam-role.svg` | `Res_AWS-Identity-Access-Management_Role_48.svg` |
| `sagemaker-model.svg` | `Res_Amazon-SageMaker-AI_Model_48.svg` |
| `sagemaker-train.svg` | `Res_Amazon-SageMaker-AI_Train_48.svg` |
| `sagemaker-shadow-testing.svg` | `Res_Amazon-SageMaker-AI_Shadow-Testing_48.svg` |
| `cloudwatch-logs.svg` | `Res_Amazon-CloudWatch_Logs_48.svg` |
| `athena.svg` | `Arch_Amazon-Athena_64.svg` |
| `redshift.svg` | `Arch_Amazon-Redshift_64.svg` |
| `emr.svg` | `Arch_Amazon-EMR_64.svg` |
| `lake-formation.svg` | `Arch_AWS-Lake-Formation_64.svg` |
| `quick.svg` | `Arch_Amazon-Quick_64.svg` |
| `cost-explorer.svg` | `Arch_AWS-Cost-Explorer_64.svg` |
| `budgets.svg` | `Arch_AWS-Budgets_64.svg` |
| `trusted-advisor.svg` | `Arch_AWS-Trusted-Advisor_64.svg` |
| `compute-optimizer.svg` | `Arch_AWS-Compute-Optimizer_64.svg` |
| `lambda.svg` | `Arch_AWS-Lambda_64.svg` |
| `eventbridge.svg` | `Arch_Amazon-EventBridge_64.svg` |
| `step-functions.svg` | `Arch_AWS-Step-Functions_64.svg` |
| `mwaa.svg` | `Arch_Amazon-Managed-Workflows-for-Apache-Airflow_64.svg` |
| `cloudformation.svg` | `Arch_AWS-CloudFormation_64.svg` |
| `cdk.svg` | `Arch_AWS-Cloud-Development-Kit_64.svg` |
| `ecs.svg` | `Arch_Amazon-Elastic-Container-Service_64.svg` |
| `eks.svg` | `Arch_Amazon-Elastic-Kubernetes-Service_64.svg` |
| `ecr.svg` | `Arch_Amazon-Elastic-Container-Registry_64.svg` |
| `batch.svg` | `Arch_AWS-Batch_64.svg` |
| `dynamodb.svg` | `Arch_Amazon-DynamoDB_64.svg` |
| `opensearch.svg` | `Arch_Amazon-OpenSearch-Service_64.svg` |
| `macie.svg` | `Arch_Amazon-Macie_64.svg` |
| `secrets-manager.svg` | `Arch_AWS-Secrets-Manager_64.svg` |
| `inspector.svg` | `Arch_Amazon-Inspector_64.svg` |
| `config.svg` | `Arch_AWS-Config_64.svg` |
| `systems-manager.svg` | `Arch_AWS-Systems-Manager_64.svg` |
| `codepipeline.svg` | `Arch_AWS-CodePipeline_64.svg` |
| `codebuild.svg` | `Arch_AWS-CodeBuild_64.svg` |
| `codedeploy.svg` | `Arch_AWS-CodeDeploy_64.svg` |
| `codecommit.svg` | `Arch_AWS-CodeCommit_64.svg` |
| `codeartifact.svg` | `Arch_AWS-CodeArtifact_64.svg` |
| `personalize.svg` | `Arch_Amazon-Personalize_64.svg` |
| `lex.svg` | `Arch_Amazon-Lex_64.svg` |
| `polly.svg` | `Arch_Amazon-Polly_64.svg` |
| `translate.svg` | `Arch_Amazon-Translate_64.svg` |
| `comprehend-medical.svg` | `Arch_Amazon-Comprehend-Medical_64.svg` |
| `healthlake.svg` | `Arch_AWS-HealthLake_64.svg` |
| `kinesis-video-streams.svg` | `Arch_Amazon-Kinesis-Video-Streams_64.svg` |
| `datasync.svg` | `Arch_AWS-DataSync_64.svg` |
| `storage-gateway.svg` | `Arch_AWS-Storage-Gateway_64.svg` |
| `direct-connect.svg` | `Arch_AWS-Direct-Connect_64.svg` |
| `x-ray.svg` | `Arch_AWS-X-Ray_64.svg` |
| `rds.svg` | `Arch_Amazon-RDS_64.svg` |
| `aurora.svg` | `Arch_Amazon-Aurora_64.svg` |
| `neptune.svg` | `Arch_Amazon-Neptune_64.svg` |
| `ebs.svg` | `Arch_Amazon-Elastic-Block-Store_64.svg` |
| `efs.svg` | `Arch_Amazon-EFS_64.svg` |
| `ec2.svg` | `Arch_Amazon-EC2_64.svg` |
| `api-gateway.svg` | `Arch_Amazon-API-Gateway_64.svg` |
| `managed-flink.svg` | `Arch_Amazon-Managed-Service-for-Apache-Flink_64.svg` |
| `msk.svg` | `Arch_Amazon-Managed-Streaming-for-Apache-Kafka_64.svg` |
| `devops-guru.svg` | `Arch_Amazon-DevOps-Guru_64.svg` |
| `codeguru.svg` | `Arch_Amazon-CodeGuru_64.svg` |
| `ground-truth.svg` | `Arch_Amazon-SageMaker-Ground-Truth_64.svg` |
| `a2i.svg` | `Arch_Amazon-Augmented-AI-A2I_64.svg` |
| `application-auto-scaling.svg` | `Arch_AWS-Application-Auto-Scaling_64.svg` |
| `bedrock-agentcore.svg` | `Arch_Amazon-Bedrock-AgentCore_64.svg` |
| `s3-glacier.svg` | `Arch_Amazon-Simple-Storage-Service-Glacier_64.svg` |
| `cognito.svg` | `Arch_Amazon-Cognito_64.svg` |
| `s3-glacier-deep-archive.svg` | `Res_Amazon-Simple-Storage-Service_S3-Glacier-Deep-Archive_48.svg` |
| `s3-intelligent-tiering.svg` | `Res_Amazon-Simple-Storage-Service_S3-Intelligent-Tiering_48.svg` |
| `s3-object-lock.svg` | `Res_Amazon-Simple-Storage-Service_S3-Object-Lock_48.svg` |
| `s3-vectors.svg` | `Res_Amazon-Simple-Storage-Service_S3-Vectors_48.svg` |
| `glue-data-catalog.svg` | `Res_AWS-Glue_Data-Catalog_48.svg` |
| `glue-crawler.svg` | `Res_AWS-Glue_Crawler_48.svg` |
| `glue-data-quality.svg` | `Res_AWS-Glue_Data-Quality_48.svg` |
| `lake-formation-data-lake.svg` | `Res_AWS-Lake-Formation_Data-Lake_48.svg` |
| `lambda-function.svg` | `Res_AWS-Lambda_Lambda-Function_48.svg` |
| `cloudformation-stack.svg` | `Res_AWS-CloudFormation_Stack_48.svg` |
| `cloudwatch-alarm.svg` | `Res_Amazon-CloudWatch_Alarm_48.svg` |
| `sagemaker-canvas.svg` | `Res_Amazon-SageMaker-AI_Canvas_48.svg` |
| `sagemaker-notebook.svg` | `Res_Amazon-SageMaker-AI_Notebook_48.svg` |
| `ec2-instance.svg` | `Res_Amazon-EC2_Instance_48.svg` |
| `ec2-spot-instance.svg` | `Res_Amazon-EC2_Spot-Instance_48.svg` |
| `dynamodb-table.svg` | `Res_Amazon-DynamoDB_Table_48.svg` |
| `application.svg`, `client.svg`, `internet.svg`, `logs.svg`, `user.svg`, `users.svg` | `Res_General-Icons/Res_48_Light/Res_<Name>_48_Light.svg` |

## `tools/` — Simple Icons

- Fuente / source: [Simple Icons](https://simpleicons.org/) 13.21.0,
  `https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/<slug>.svg`.
- Licencia / license: los SVG de Simple Icons se publican con **CC0 1.0**
  (<https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md>). Los logos siguen siendo marcas de sus
  dueños; se usan solo para identificar la herramienta. The logos remain their owners' trademarks; they are used only
  to identify the tool.
- Los SVG son monocromos; el color de marca se aplica al dibujar (`TOOL_COLORS` en `charts/style.py` y
  `videos/style.py`). SVGs are monochrome; the brand color is applied when drawing.

| Archivo / file | Herramienta / tool | Color |
| --- | --- | --- |
| `pytorch.svg` | PyTorch | `#EE4C2C` |
| `tensorflow.svg` | TensorFlow | `#FF6F00` |

XGBoost no tiene un ícono en Simple Icons; su caja queda solo con texto.
XGBoost has no Simple Icons entry; its box stays text-only.
