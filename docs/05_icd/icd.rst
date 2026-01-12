ICD — Interface & Data Schemas (Contracts)
====================================================================================================

Configuration Schemas


.. icd:: IPC Configuration (ipc_config.yaml)
   :id: ICD-1
   :links: SAD-5.1,NFR-3.3,NFR-3.4,NFR-3.5,NFR-3.6,NFR-3

   .. code-block:: yaml

      core:
        router_bind: "tcp://127.0.0.1:5555"
        push_connect: "tcp://127.0.0.1:5556"    # Added for Core logging
        router_hwm: 1000
        queue_maxsize: 1000
        poll_timeout_ms: 100
        response_timeout_s: 5.0
        extensions:
          path: "./extensions"      # Root for tools/routines discovery

      logserver:
        pull_bind: "tcp://127.0.0.1:5556"
        poll_timeout_ms: 1      # Tight loop for high throughput
        log_rotation_mb: 50
        log_retention_days: 30

      services:
        ui:
          dealer_connect: "tcp://127.0.0.1:5555"
          push_connect: "tcp://127.0.0.1:5556"
          queue_maxsize: 100
          poll_timeout_ms: 100
        runtime:
          dealer_connect: "tcp://127.0.0.1:5555"
          push_connect: "tcp://127.0.0.1:5556"
          queue_maxsize: 50
          poll_timeout_ms: 100
        audio:
          dealer_connect: "tcp://127.0.0.1:5555"
          push_connect: "tcp://127.0.0.1:5556"
          queue_maxsize: 50
          poll_timeout_ms: 10

   Message Protocols


.. icd:: Frame Structure
   :id: ICD-2
   :links: SAD-3.2,SAD-3.6,SAD-1.4,SAD-1

.. icd:: **Core ↔ Services (ROUTER-DEALER):**
   :id: ICD-2.1
   :links: ICD-2

.. icd:: **Outbound (DEALER):** `[metadata_json, payload_bytes...]`
   :id: ICD-2.2
   :links: ICD-2

.. icd:: **Inbound (ROUTER):** `[service_identity, b'', metadata_json, payload_bytes...]`
   :id: ICD-2.3
   :links: ICD-2

.. icd:: **All → LogServer (PUSH-PULL):**
   :id: ICD-2.4
   :links: ICD-2

.. icd:: **Frame:** `[metadata_json, message_string]`
   :id: ICD-2.5
   :links: ICD-2

.. icd:: **Payloads:**
   :id: ICD-2.6
   :links: ICD-2

.. icd:: Text: JSON-encoded UTF-8 bytes.
   :id: ICD-2.7
   :links: ICD-2

.. icd:: Binary: Raw bytes (PCM, tensors).
   :id: ICD-2.8
   :links: ICD-2

.. icd:: Multi-part: Supported for zero-copy efficiency.
   :id: ICD-2.9
   :links: ICD-2



.. icd:: Metadata Schema (JSON)
   :id: ICD-3
   :links: FSD-6.3,SAD-4.7,SAD-4

   Every IPC message frame 0 (Metadata) must validate against:

   .. code-block:: json

      {
        "source": "UI | Audio | Runtime | Core",
        "destination": "Target_Service_Name",
        "command": "function_name_or_signal",
        "request_id": "uuid-v4-string",
        "timestamp": "ISO-8601-string",
        "priority": 1,
        "payload_type": "json | binary | text"
      }

   Note: Priority 0 = High, 1 = Normal


.. icd:: Response Payload Schema
   :id: ICD-4
   :links: ICD-3

   .. code-block:: json

      {
        "source": "Runtime",
        "destination": "UI",
        "command": "llm_inference_response",
        "request_id": "uuid-echoed",
        "timestamp": "ISO-8601-string",
        "status": "success | error",
        "error_code": "optional_string_or_null"
      }



.. metadata:
   :file-id: icd-root
   :title: "Interface & Data Schemas"
   :version: "5.0"
   :date: "2025-12-17"
   :author: "Anthony Formosa"
   :roadmap_version: "5.0"
   :template_version: "2.0"
   :status: "Active"
   :llm-permissions: read-only
   :purpose: "Define Data Shapes and Contracts"

