import time
import uuid

import requests

URL = "http://127.0.0.1:3773/"


# ---------- Test Texts ----------

HISTORY_TEXT = """
The French Revolution began in 1789 and marked a major turning point in European history.
It was driven by social inequality, economic hardship, and resentment toward absolute
monarchy. French society was divided into three estates, with the clergy and nobility
enjoying privileges while the Third Estate bore heavy taxation.

The revolution led to the fall of the monarchy, the execution of King Louis XVI, and the
establishment of a republic. Key ideas such as liberty, equality, and fraternity emerged
during this period.
"""

TECHNOLOGY_TEXT = """
Cloud computing enables users to access computing resources such as servers, storage,
and applications over the internet. Organizations can scale resources dynamically
without managing physical infrastructure.

Cloud services are divided into IaaS, PaaS, and SaaS models. Benefits include cost
reduction, scalability, high availability, and improved disaster recovery.
"""

BIOLOGY_TEXT = """
Photosynthesis is the process by which green plants produce food using sunlight.
It occurs in chloroplasts and converts carbon dioxide and water into glucose and oxygen.

This process is essential for life on Earth, forming the base of food chains and
maintaining atmospheric oxygen levels.
"""


# ---------- Helpers ----------


def send_message(text: str) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "configuration": {"acceptedOutputModes": ["text"]},
            "message": {
                "messageId": str(uuid.uuid4()),
                "contextId": str(uuid.uuid4()),
                "taskId": str(uuid.uuid4()),
                "role": "user",
                "kind": "message",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"Generate exactly 10 MCQs from the following text:\n\n{text}",
                    }
                ],
            },
        },
    }

    response = requests.post(URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["result"]["id"]


def poll_task(task_id: str, timeout: int = 120) -> dict:
    start = time.time()
    print(f" Polling task: {task_id}")

    while time.time() - start < timeout:
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tasks/get",
            "params": {"taskId": task_id},
        }

        response = requests.post(URL, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()["result"]
        state = result["status"]["state"]
        print(f"Task state: {state}")

        if state == "completed":
            return result

        time.sleep(2)

    raise TimeoutError("Task did not complete in time")


def extract_text(task_result: dict) -> str | None:
    output = task_result.get("output")
    if output:
        for part in output.get("parts", []):
            if part.get("kind") == "text":
                return part.get("text")

    for msg in reversed(task_result.get("history", [])):
        if msg.get("role") == "assistant":
            for part in msg.get("parts", []):
                if part.get("kind") == "text":
                    return part.get("text")

    return None


def validate_and_print(topic: str, output: str):
    print(f"\n🎯 GENERATED MCQs ({topic})\n")
    print(output)

    assert output is not None
    assert len(output.strip()) > 300
    assert output.lower().count("question") >= 5


# ---------- Tests ----------


def test_history_mcqs():
    print("\n🧪 Test 1: History")

    task_id = send_message(HISTORY_TEXT)
    result = poll_task(task_id)
    output = extract_text(result)

    validate_and_print("TopicName", output or "")
    print("✅ History test passed")


def test_technology_mcqs():
    print("\n🧪 Test 2: Technology")

    task_id = send_message(TECHNOLOGY_TEXT)
    result = poll_task(task_id)
    output = extract_text(result)

    validate_and_print("TopicName", output or "")
    print("✅ Technology test passed")


def test_biology_mcqs():
    print("\n🧪 Test 3: Biology")

    task_id = send_message(BIOLOGY_TEXT)
    result = poll_task(task_id)
    output = extract_text(result)

    validate_and_print("TopicName", output or "")
    print("✅ Biology test passed")


# ---------- Runner ----------

if __name__ == "__main__":
    print("🚀 Running Quiz Generator Agent Tests")

    test_history_mcqs()
    test_technology_mcqs()
    test_biology_mcqs()

    print("\n🎉 All tests completed successfully")
