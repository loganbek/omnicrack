import typer
from rich.console import Console
from rich.table import Table
from omnicrack.hardware import HardwareDetector

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

if __name__ == "__main__":
    app()
