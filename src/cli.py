import sys
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rsa_core import generate_rsa_keypair, save_keys, load_public_key, load_private_key
from src.file_handler import encrypt_file, decrypt_file

console = Console()

BANNER = """
██████╗ ███████╗ █████╗     ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗
██╔══██╗██╔════╝██╔══██╗    ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝
██████╔╝███████╗███████║    █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  
██╔══██╗╚════██║██╔══██║    ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  
██║  ██║███████║██║  ██║    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝
"""


def show_menu():
    console.print(Panel(BANNER, style="bold cyan", subtitle="[italic]RSA Cryptographic Engine v1.0[/italic]"))

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[bold green][1][/bold green]", "Generate new RSA key pair")
    table.add_row("[bold yellow][2][/bold yellow]", "Encrypt a file")
    table.add_row("[bold red][3][/bold red]", "Decrypt a file")
    table.add_row("[bold blue][4][/bold blue]", "View key info")
    table.add_row("[bold white][5][/bold white]", "Exit")

    console.print(Panel(table, title="[bold]Main Menu[/bold]", border_style="dim"))


def cmd_generate_keys():
    console.print("\n[bold cyan]🔑 RSA Key Generation[/bold cyan]")

    console.print("Key size (bits) [1024/2048/4096] (default 2048): ", end="")
    bit_choice = input().strip() or "2048"
    if bit_choice not in ["1024", "2048", "4096"]:
        bit_choice = "2048"
    bit_length = int(bit_choice)

    console.print(f"\n[yellow]⚙ Generating {bit_length}-bit RSA key pair...[/yellow]")
    console.print("[dim]This involves finding two large prime numbers. Please wait...[/dim]\n")

    start = time.time()
    public_key, private_key = generate_rsa_keypair(bit_length)
    elapsed = time.time() - start

    pub_path, priv_path = save_keys(public_key, private_key)

    console.print(f"\n[bold green]✅ Keys generated in {elapsed:.2f}s[/bold green]")
    console.print(f"  [green]Public key →[/green]  {pub_path}")
    console.print(f"  [red]Private key →[/red] {priv_path}")
    console.print("\n[bold red]⚠  NEVER share your private key.[/bold red]")


def cmd_encrypt():
    console.print("\n[bold yellow]🔒 Encrypt a File[/bold yellow]")

    console.print("Path to plaintext file: ", end="")
    input_path = input().strip()

    if not os.path.exists(input_path):
        console.print(f"[red]Error: File '{input_path}' not found.[/red]")
        return

    console.print("Path to public key (default: keys/public_key.json): ", end="")
    pub_key_path = input().strip() or "keys/public_key.json"

    if not os.path.exists(pub_key_path):
        console.print(f"[red]Error: Public key not found at '{pub_key_path}'.[/red]")
        return

    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f"encrypted/{filename}.enc.json"

    console.print(f"\n[yellow]⚙ Encrypting '{input_path}'...[/yellow]")

    public_key = load_public_key(pub_key_path)
    encrypt_file(input_path, output_path, public_key)

    console.print(f"[bold green]✅ Encrypted file saved to:[/bold green] {output_path}")


def cmd_decrypt():
    console.print("\n[bold red]🔓 Decrypt a File[/bold red]")

    console.print("Path to encrypted file (.enc.json): ", end="")
    input_path = input().strip()

    if not os.path.exists(input_path):
        console.print(f"[red]Error: File '{input_path}' not found.[/red]")
        return

    console.print("Path to private key (default: keys/private_key.json): ", end="")
    priv_key_path = input().strip() or "keys/private_key.json"

    if not os.path.exists(priv_key_path):
        console.print(f"[red]Error: Private key not found at '{priv_key_path}'.[/red]")
        return

    filename = os.path.splitext(os.path.basename(input_path))[0].replace(".enc", "")
    output_path = f"decrypted/{filename}_decrypted.txt"

    console.print(f"\n[yellow]⚙ Decrypting '{input_path}'...[/yellow]")

    private_key = load_private_key(priv_key_path)
    decrypt_file(input_path, output_path, private_key)

    console.print(f"[bold green]✅ Decrypted file saved to:[/bold green] {output_path}")


def cmd_view_key_info():
    console.print("\n[bold blue]🔍 Key Information[/bold blue]")

    pub_path = "keys/public_key.json"
    priv_path = "keys/private_key.json"

    if not os.path.exists(pub_path):
        console.print("[red]No keys found. Generate a key pair first.[/red]")
        return

    pub = load_public_key(pub_path)
    priv = load_private_key(priv_path)

    table = Table(title="RSA Key Details", border_style="blue")
    table.add_column("Property", style="bold")
    table.add_column("Value", style="dim")

    table.add_row("Key Size (bits)", str(pub.n.bit_length()))
    table.add_row("Public Exponent (e)", str(pub.e))
    table.add_row("Modulus n (first 40 chars)", str(pub.n)[:40] + "...")
    table.add_row("Private Exponent d (first 40 chars)", str(priv.d)[:40] + "...")

    console.print(table)


def main():
    while True:
        show_menu()

        console.print("\n[bold]Choose an option [1/2/3/4/5]:[/bold] ", end="")
        choice = input().strip()
        while choice not in ["1", "2", "3", "4", "5"]:
            console.print("[red]Invalid. Enter 1, 2, 3, 4, or 5:[/red] ", end="")
            choice = input().strip()

        if choice == "1":
            cmd_generate_keys()
        elif choice == "2":
            cmd_encrypt()
        elif choice == "3":
            cmd_decrypt()
        elif choice == "4":
            cmd_view_key_info()
        elif choice == "5":
            console.print("\n[bold cyan]Goodbye. Stay encrypted. 🔐[/bold cyan]\n")
            break

        console.print()
        input("Press Enter to continue...")
        console.clear()


if __name__ == "__main__":
    main()