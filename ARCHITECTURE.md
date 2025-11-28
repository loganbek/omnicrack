# ARCHITECTURE BLUEPRINT

## System Design
The application follows a 4-layer architecture:

1.  **Ingest Layer (The Eye):** * Accepts paths to `.cap`, `.pcap`, `.hccapx`, or text hashes.
    * Uses `hashid` logic to guess hash types.
    * Uses `hcxpcapngtool` logic to extract handshakes from pcaps.

2.  **Strategy Layer (The Brain):**
    * Input: Hash Type + Hardware capabilities.
    * Output: An "AttackPlan" object (e.g., "Use Hashcat, Mode 22000, Wordlist: RockYou").
    * Selects profiles: "Quick" (Top 10k passwords), "Standard" (RockYou), "Deep" (Brute-force mask).

3.  **Execution Layer (The Hands):**
    * Constructs the subprocess command.
    * Manages the Docker container execution.
    * Streams `stdout` to the parser.

4.  **Presentation Layer (The Face):**
    * Parses raw tool output (e.g., looks for "Recovered..." or "[s]tatus").
    * Updates the `Rich` console UI.
