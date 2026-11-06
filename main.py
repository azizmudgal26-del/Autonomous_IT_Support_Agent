import sys
from agent.brain import ask_deepseek
from jsonschema.exceptions import ValidationError

from agent.tools import (
    get_server_health,
    get_server_logs,
    validate_json_data,
    fetch_server_logs,
    restart_service,
    escalate_to_engineer,
    investigate_server_errors,
    investigate_memory_usage
)



class Tee:

    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            stream.write(message)

    def flush(self):
        for stream in self.streams:
            stream.flush()


            

def run_agent():


    # ==================================================
    # STEP 1: LOAD SERVER DATA
    # ==================================================

    server_health = get_server_health()
    server_logs = get_server_logs()

    try:
        validate_json_data(
        server_health,
        "schemas/server_health.schema.json"
        )

        validate_json_data(
        server_logs,
        "schemas/server_logs.schema.json"
        )

        print("\nSUCCESS: Both JSON files passed Schema validation.")

    except ValidationError as error:
        print("\nSCHEMA VALIDATION FAILED!")
        print(f"Reason: {error.message}")

        return


    # ==================================================
    # FINAL SUMMARY COUNTERS
    # ==================================================

    total_servers = 0

    healthy_servers = 0

    critical_servers = 0

    warning_servers = 0

    ai_successful = 0

    ai_failed = 0


    # ==================================================
    # STEP 2: PROCESS EACH SERVER
    # ==================================================

    for server_name, details in server_health.items():

        total_servers += 1

        print("\n")
        print("=" * 75)
        print(f"SERVER REPORT: {server_name}")
        print("=" * 75)

        # ----------------------------------------------
        # STEP 2A: DISPLAY SERVER HEALTH DETAILS
        # ----------------------------------------------

        cpu_number = int(details["cpu"].replace("%", ""))
        memory_number = int(details["memory"].replace("%", ""))

        print("\n[1] SERVER HEALTH DETAILS")

        print("CPU Usage    :", details["cpu"])
        print("Memory Usage :", details["memory"])
        print("Server Status:", details["status"])


        # ----------------------------------------------
        # STEP 2B: CLASSIFY SERVER HEALTH
        # ----------------------------------------------

        if details["status"] == "Critical" or details["status"] == "Error":

            classification = "CRITICAL"
            critical_servers += 1

        elif cpu_number > 90:

            classification = "CRITICAL"
            critical_servers += 1

        elif details["status"] == "Warning":

            classification = "WARNING"
            warning_servers += 1

        else:

            classification = "HEALTHY"
            healthy_servers += 1

        print("\n[2] HEALTH CLASSIFICATION")
        print("Classification:", classification)


        # ----------------------------------------------
        # STEP 2C: FETCH AND DISPLAY SERVER LOGS
        # ----------------------------------------------

        logs = fetch_server_logs(server_name, server_logs)

        warning_count = 0
        error_count = 0
        critical_count = 0

        print("\n[3] SERVER LOG DETAILS")

        for message in logs:

            print(" ", message)

            if message.startswith("WARNING"):

                warning_count += 1

            elif message.startswith("ERROR"):

                error_count += 1

            elif message.startswith("CRITICAL"):

                critical_count += 1


        # ----------------------------------------------
        # STEP 2D: DISPLAY LOG SUMMARY
        # ----------------------------------------------

        print("\n[4] LOG SUMMARY")

        print("Total WARNING messages :", warning_count)
        print("Total ERROR messages   :", error_count)
        print("Total CRITICAL messages:", critical_count)


        # ----------------------------------------------
        # STEP 2E: RECOMMEND PYTHON ACTIONS
        # ----------------------------------------------

        print("\n[5] PYTHON RECOMMENDED ACTIONS")

        action_taken = False

        # Rule 1: High CPU usage

        if cpu_number > 90:

            print("\nAction: Restart service")

            restart_result = restart_service(server_name)

            print("Result:", restart_result)

            action_taken = True


        # Rule 2: Critical log messages

        if critical_count > 0:

            print("\nAction: Escalate to human IT engineer")

            escalation_result = escalate_to_engineer(server_name, logs)

            print("Result:", escalation_result)

            action_taken = True


        # Rule 3: Error log messages

        if error_count > 0:

            print("\nAction: Investigate server errors")

            investigation_result = investigate_server_errors(
                server_name,
                logs
            )

            print("Result:", investigation_result)

            action_taken = True


        # Rule 4: High memory usage

        if memory_number > 90:

            print("\nAction: Investigate high memory usage")

            memory_result = investigate_memory_usage(
                server_name,
                memory_number
            )

            print("Result:", memory_result)

            action_taken = True


        # Rule 5: No action required

        if not action_taken:

            print("No action required. Server appears healthy.")


        # ----------------------------------------------
        # STEP 2F: DEEPSEEK AI ANALYSIS
        # ----------------------------------------------

        print("\n[6] DEEPSEEK AI INCIDENT ANALYSIS")

        if classification == "CRITICAL" or classification == "WARNING":

            print("AI analysis required for:", server_name)

            logs_text = "\n".join(logs)

            prompt = f"""
            Analyse the following server incident.

            Server: {server_name}
            CPU Usage: {details["cpu"]}
            Memory Usage: {details["memory"]}
            Status: {details["status"]}

            Server Logs:
            {logs_text}

            Explain the evidence, possible causes, missing information,
            and recommended troubleshooting steps.
            """

            try:
                # Simulate an AI failure for payment-server-01
                #if server_name == "payment-server-01":
                    #raise RuntimeError("Simulated DeepSeek API failure")

                ai_analysis = ask_deepseek(prompt)

                ai_successful += 1
                #raise RuntimeError("Simulated DeepSeek API failure")
                print("\n========== DEEPSEEK AI ANALYSIS ==========\n")

                print(ai_analysis)

            except Exception as error:

                ai_failed += 1

                print("\nDEEPSEEK AI SERVICE UNAVAILABLE")

                print("Python investigation completed.")

                print("AI analysis could not be completed.")

                print("Technical error:", error)

                
        else:

            print("No AI analysis required. Server is healthy.")


        # ----------------------------------------------
        # STEP 2G: END OF SERVER REPORT
        # ----------------------------------------------

        print("\n")
        print("=" * 75)
        print(f"END OF REPORT: {server_name}")
        print("=" * 75)


    print("=" * 55)
    print("FINAL INFRASTRUCTURE SUMMARY")
    print("=" * 55)

    print("Total servers investigated :", total_servers)
    print("Healthy servers             :", healthy_servers)
    print("Critical servers            :", critical_servers)
    print("Warning servers             :", warning_servers)
    print("")
    print("Successful AI analyses      :", ai_successful)
    print("Failed AI analyses          :", ai_failed)

    print("=" * 55)

    print("\nALL SERVER INVESTIGATIONS COMPLETED.")



if __name__ == "__main__":

    original_stdout = sys.stdout

    with open(
        "reports/infrastructure_report.txt",
        "w",
        encoding="utf-8"
    ) as report_file:

        try:

            sys.stdout = Tee(original_stdout, report_file)

            run_agent()

        finally:

            sys.stdout = original_stdout