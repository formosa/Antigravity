Controlled Terms
================

.. term:: Core Process
   :id: TERM-CORE-PROCESS
   :status: open

   The central orchestrator of the Maggie system. Responsible for lifecycle management, message routing, and service coordination. Never referred to as "Manager" or "Host".

.. term:: Runtime Process
   :id: TERM-RUNTIME-PROCESS
   :status: open

   A generic term for any independent operating system process spawned or managed by the Core Process.

.. term:: Audio Process
   :id: TERM-AUDIO-PROCESS
   :status: open

   A specialized Runtime Process dedicated to audio capture, processing, or playback.

.. term:: UI Process
   :id: TERM-UI-PROCESS
   :status: open

   A specialized Runtime Process dedicated to rendering the graphical user interface.

.. term:: Tool
   :id: TERM-TOOL
   :status: open

   A discrete, executable unit of logic that can be invoked by an agent or the Core Process to perform a specific task.

.. term:: Routine
   :id: TERM-ROUTINE
   :status: open

   A predefined sequence of Tool invocations or logic steps designed to achieve a higher-level goal.

.. term:: HSM
   :id: TERM-HSM
   :status: open

   Hierarchical State Machine. The primary architectural pattern for managing complex system states.

.. term:: Service
   :id: TERM-SERVICE
   :status: open

   A long-running, addressable component providing specific functionality (e.g., LogServer, CommandDispatcher).

.. term:: LogServer
   :id: TERM-LOGSERVER
   :status: open

   The centralized logging service that aggregates and persists system logs from all processes.
