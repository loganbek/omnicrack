# AGENT CONTEXT: OmniCrack

## Project Mission
OmniCrack is a "meta-wrapper" for hash cracking and wifi security auditing. 
**Core Philosophy:** Intent over Syntax. 
The user should say "Crack this file," and the tool decides whether to use Hashcat, John the Ripper, or AirCrack-ng based on hardware availability and file type.

## Critical Guidelines for Agents
1. **Safety First:** This tool is for authorized security auditing only. 
2. **Abstraction:** The user must never be forced to calculate a hash mode (e.g., `-m 22000`). The tool must auto-detect this.
3. **State Management:** All sessions must be resumable. Use SQLite to track job state.
4. **Hardware Awareness:** Always check for NVIDIA/AMD GPUs. Prefer Hashcat if GPU exists; fallback to John (CPU) otherwise.
5. **Dockerization:** All underlying tools (hashcat, hcxtools) will be encapsulated in Docker containers. The Python script is a wrapper around these containers.

## Tech Stack Constraints
* **Language:** Python 3.12+
* **CLI Framework:** `Typer` (for modern, type-driven CLI)
* **Output:** `Rich` (for beautiful spinners and tables)
* **Packet Handling:** `Scapy` or `TShark` (for .pcap analysis)
* **Database:** `SQLite` (via `SQLAlchemy` or raw SQL)
