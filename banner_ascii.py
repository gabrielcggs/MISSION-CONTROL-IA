import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.text import Text

console = Console()


def main() -> None:
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text(
                "── 2026.1 · Prompt Engineering and AI · FIAP ──",
                style="italic #8484A0",
            )
        )
    )


if __name__ == "__main__":
    main()
