import typer
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from typing import Optional

from omnicrack.hardware import HardwareDetector
from omnicrack.identifier import HashIdentifier
from omnicrack.pcap import PcapAnalyzer
from omnicrack.docker import DockerManager
from omnicrack.session import SessionManager

app = typer.Typer()
console = Console()

@app.command()
def info():
    """
    Display detected hardware and system information.
    """
    detector = HardwareDetector()
    detector.detect()

    table = Table(title="OmniCrack System Info")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="magenta")

    if detector.has_gpu:
        table.add_row("GPU Detected", "Yes")
        table.add_row("GPU Type", detector.gpu_type)
    else:
        table.add_row("GPU Detected", "No")
        table.add_row("GPU Type", "N/A (CPU Fallback)")

    console.print(table)

@app.command()
def crack(
    target_file: str = typer.Argument(..., help="Path to hash file or .pcap"),
    wordlist: Optional[str] = typer.Option(None, help="Path to wordlist"),
):
    """
    Intelligent crack command. Auto-detects hardware and file type.
    """
    # 1. Hardware Detection
    console.print("[bold blue]Step 1: Detecting Hardware...[/bold blue]")
    hardware = HardwareDetector()
    hardware.detect()
    
    if hardware.has_gpu:
        console.print(f"[green]✔ GPU Detected: {hardware.gpu_type}[/green]")
        engine = "hashcat"
    else:
        console.print("[yellow]⚠ No GPU Detected. Falling back to CPU (Hashcat via Docker).[/yellow]")
        engine = "hashcat" # We use hashcat for now as per plan, it supports CPU too via OpenCL usually

    # 2. Identify Target
    console.print(f"[bold blue]Step 2: Identifying Target {target_file}...[/bold blue]")
    
    hash_type = "unknown"
    hash_mode = "0" # Default MD5
    
    if target_file.endswith(".pcap") or target_file.endswith(".cap"):
        console.print("[cyan]Analyzing PCAP for handshakes...[/cyan]")
        analyzer = PcapAnalyzer()
        result = analyzer.analyze(target_file)
        if result["handshake_found"]:
            console.print(f"[green]✔ Handshake found for SSID: {result.get('ssid')}[/green]")
            hash_type = "WPA/WPA2"
            hash_mode = "2500" # WPA/WPA2
            # TODO: Extract handshake to hccapx/pmkid for hashcat
            console.print("[yellow]⚠ PCAP extraction to hashcat format not yet implemented. Assuming 2500 mode.[/yellow]")
        else:
            console.print("[red]✘ No handshake found in PCAP.[/red]")
            raise typer.Exit(code=1)
    else:
        # Assume text file with hash
        with open(target_file, "r") as f:
            content = f.read().strip()
        
        identifier = HashIdentifier()
        possible_types = identifier.identify(content)
        
        if possible_types:
            console.print(f"[green]✔ Identified Hash Type(s): {', '.join(possible_types)}[/green]")
            # Simple mapping logic for demo - in real world we need a robust mapper
            if "MD5" in possible_types:
                hash_type = "MD5"
                hash_mode = "0"
            elif "SHA-1" in possible_types:
                hash_type = "SHA-1"
                hash_mode = "100"
            elif "Bcrypt" in possible_types:
                hash_type = "Bcrypt"
                hash_mode = "3200"
            else:
                console.print("[yellow]⚠ Could not map to specific Hashcat mode. Defaulting to 0 (MD5).[/yellow]")
        else:
            console.print("[red]✘ Could not identify hash type.[/red]")
            # Continue anyway?
            
    # 3. Create Job
    console.print("[bold blue]Step 3: Creating Job...[/bold blue]")
    session_mgr = SessionManager()
    # Construct args
    cmd_args = ["-m", hash_mode, "/data/" + target_file]
    if wordlist:
        cmd_args.append("/data/" + wordlist)
    else:
        cmd_args.append("?a?a?a?a?a") # Brute force 5 chars default
        
    job = session_mgr.create_job(
        hash_type=hash_type,
        target_file=target_file,
        wordlist=wordlist,
        command_args=" ".join(cmd_args)
    )
    console.print(f"[green]✔ Job #{job.id} created.[/green]")

    # 4. Run Docker
    console.print("[bold blue]Step 4: Starting Cracking Engine...[/bold blue]")
    docker_mgr = DockerManager()
    
    if not docker_mgr.check_docker_available():
        console.print("[red]✘ Docker is not available or not running.[/red]")
        raise typer.Exit(code=1)
        
    # Live Dashboard
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    
    layout["header"].update(Panel(f"OmniCrack Job #{job.id} - {hash_type}", style="bold white on blue"))
    layout["footer"].update(Panel("Press Ctrl+C to stop", style="dim"))
    
    output_text = ""
    
    with Live(layout, refresh_per_second=4) as live:
        session_mgr.update_job_status(job.id, "running")
        
        try:
            for line in docker_mgr.run_hashcat_stream(cmd_args):
                output_text += line
                # Keep last 20 lines
                lines = output_text.splitlines()[-20:]
                layout["body"].update(Panel("\n".join(lines), title="Hashcat Output", border_style="green"))
                
                # Parse progress (very basic example)
                if "Recovered" in line:
                    # Maybe update a progress bar here
                    pass
                    
        except KeyboardInterrupt:
            console.print("[yellow]Stopping job...[/yellow]")
            session_mgr.update_job_status(job.id, "paused")
        else:
            session_mgr.update_job_status(job.id, "completed")
            
    console.print("[bold green]Job Finished.[/bold green]")

if __name__ == "__main__":
    app()
