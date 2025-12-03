# PROJECT ROADMAP & TASKS

## Phase 1: The Skeleton (Current Priority)

- [x] Set up Python project structure with Poetry or `pyproject.toml`.
- [x] Create `OmniCrack` Typer entry point.
- [x] Implement `HardwareDetector` class (detects CUDA/OpenCL).

## Phase 2: The Identifier

- [x] Build `HashIdentifier` module (integrate logic similar to `hashid`).
- [x] Build `PcapAnalyzer` module using Scapy (detect EAPOL handshakes).

## Phase 3: The Engine

- [x] Create `DockerManager` to handle pulling/running `dizcza/docker-hashcat`.
- [x] Implement the `SessionManager` (SQLite) to save/resume jobs.

## Phase 4: The UI

- [x] detailed `Rich` dashboard with live hash-rate telemetry.
