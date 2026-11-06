import json
from jsonschema import validate

def get_server_health():

    with open("data/server_health.json", "r") as file:
        health_data = json.load(file)

    return health_data


def get_server_logs():

    with open("data/server_logs.json", "r") as file:
        logs_data = json.load(file)

    return logs_data


def fetch_server_logs(server_name, server_logs):
    
    return server_logs[server_name]



def restart_service(server_name):

    print(f"SIMULATION: Restarting service for {server_name}")

    return {
        "server": server_name,
        "action": "restart",
        "status": "simulated_success"
    }



def escalate_to_engineer(server_name, logs):

    print(f"SIMULATION: Escalating {server_name} to a human IT engineer")

    return {
        "server": server_name,
        "action": "escalation",
        "status": "simulated_success",
        "logs": logs
    }



def investigate_server_errors(server_name, logs):

    error_logs = []

    for message in logs:
        if message.startswith("ERROR"):
            error_logs.append(message)

    return {
        "server": server_name,
        "action": "investigate_errors",
        "status": "simulated_success",
        "errors_found": error_logs
    }


def investigate_memory_usage(server_name, memory_number):

    return {
        "server": server_name,
        "action": "investigate_memory",
        "memory_usage": memory_number,
        "status": "investigation_required"
    }


def validate_json_data(data, schema_path):

    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)

    validate(instance=data, schema=schema)

    return True