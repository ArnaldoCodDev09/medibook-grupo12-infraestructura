"""API de demostración de reservas MediBook; no usar datos personales reales."""

import json
import os
import re
import uuid
from datetime import datetime, timezone, timedelta

import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.client("dynamodb")
APPOINTMENTS_TABLE = os.environ["APPOINTMENTS_TABLE"]
SLOTS_TABLE = os.environ["SLOTS_TABLE"]


def response(status, payload):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json; charset=utf-8"},
        "body": json.dumps(payload, ensure_ascii=False),
    }


def parse_body(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        import base64

        raw = base64.b64decode(raw).decode("utf-8")
    return json.loads(raw)


def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("rawPath", "/")

    if method == "GET" and path.endswith("/health"):
        return response(200, {"status": "ok", "service": "medibook-demo"})

    if method == "GET" and path.endswith("/appointments"):
        result = dynamodb.scan(TableName=APPOINTMENTS_TABLE, Limit=100)
        items = [
            {key: value["S"] for key, value in item.items() if "S" in value}
            for item in result.get("Items", [])
        ]
        items.sort(key=lambda item: (item.get("date", ""), item.get("time", "")))
        return response(200, {"appointments": items})

    if method == "POST" and path.endswith("/appointments"):
        try:
            body = parse_body(event)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response(400, {"error": "El cuerpo debe ser JSON válido."})

        required = ("patientName", "specialty", "doctor", "date", "time")
        if any(not isinstance(body.get(key), str) or not body[key].strip() for key in required):
            return response(400, {"error": "Completa todos los campos de la cita de prueba."})
        if len(body["patientName"]) > 80 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", body["date"]):
            return response(400, {"error": "Revisa el nombre y la fecha."})
        if not re.fullmatch(r"\d{2}:\d{2}", body["time"]):
            return response(400, {"error": "La hora debe tener formato HH:MM."})

        appointment_id = str(uuid.uuid4())
        slot_key = f"{body['doctor']}#{body['date']}#{body['time']}"
        expires_at = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())
        item = {
            "appointment_id": {"S": appointment_id},
            "patient_name": {"S": body["patientName"].strip()},
            "specialty": {"S": body["specialty"].strip()},
            "doctor": {"S": body["doctor"].strip()},
            "date": {"S": body["date"]},
            "time": {"S": body["time"]},
            "created_at": {"S": datetime.now(timezone.utc).isoformat()},
        }
        lock = {
            "slot_key": {"S": slot_key},
            "appointment_id": {"S": appointment_id},
            "expires_at": {"N": str(expires_at)},
        }
        try:
            dynamodb.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": APPOINTMENTS_TABLE,
                            "Item": item,
                            "ConditionExpression": "attribute_not_exists(appointment_id)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": SLOTS_TABLE,
                            "Item": lock,
                            "ConditionExpression": "attribute_not_exists(slot_key)",
                        }
                    },
                ]
            )
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code")
            if code == "TransactionCanceledException":
                return response(409, {"error": "Ese horario ya fue reservado."})
            raise
        return response(201, {"appointmentId": appointment_id, "message": "Cita de prueba registrada."})

    return response(404, {"error": "Ruta no encontrada."})

