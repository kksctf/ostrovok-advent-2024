#!/usr/bin/env python3

# typer==0.9.0
# rich==13.3.2
# PyYAML==6.0

from dataclasses import dataclass, asdict
import re
from enum import Enum
from pathlib import Path
from typing_extensions import Self, override
from typing import Optional

import rich.console
import typer
import yaml


class Dumper(yaml.SafeDumper):
    @override
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


c = rich.console.Console()
app = typer.Typer()

FLAG_PREFIX = "crab"

flag_re = re.compile(FLAG_PREFIX + r"""\{[\w\d_\-+=?!@#$%^&*()"';:<>/]+\}""")

_ER = "[red]\\[!][/]"
_OK = "[green]\\[+][/]"

TASKS_PATH = Path(".") / "tasks"
TASK_FILENAME = "task.yaml"
FOLDERS_DESCRIBED: dict[str, str] = {
    "deploy": "[yellow]файлов, которые раскатываются на сервер. docker-compose и так далее",
    "dev": "[purple]файлов, которые относятся к разработке таска",
    "public": "[red][bold]файлов, которые отдаются участникам",
    "solution": "[green]файлов, относящихся к решению (и само решение в виде readme.md)",
}


class Category(str, Enum):
    web = "web"
    rev = "rev"
    crypto = "crypto"
    forensics = "forensic"
    misc = "misc"


@dataclass
class Task:
    name: str
    description: str

    author: str
    category: Category

    flag: str

    server_port: int | None = None

    is_http: bool = True
    domain_prefix: str | None = None

    def dicted(self) -> dict:
        ret = asdict(self)
        ret["category"] = str(self.category.value)
        return ret

    def to_yaml(self) -> str:
        return yaml.dump(
            self.dicted(),
            sort_keys=False,
            Dumper=Dumper,
            allow_unicode=True,
        )

    @classmethod
    def from_yaml(cls, data: str) -> Self:
        return cls(**yaml.safe_load(data))


@app.command(short_help="подготовить дерево папок")
def build_tree():
    for category in Category:
        path = TASKS_PATH / category.value
        path.mkdir(exist_ok=True, parents=True)
        (path / ".gitkeep").write_text("")
        c.print(f"Создаю {path!r}: {_OK}")


@app.command(short_help="создать таск")
def add(
    category: Category,
    name: str,
    *,
    author: Optional[str] = None,
):
    base_path = TASKS_PATH / category.value / name

    if (base_path / TASK_FILENAME).exists():
        c.print(f"Таск {category.value}/{name} уже существует")
        raise typer.Exit(code=1)

    c.print(f"Создаю таск под названием '{name}' в категории '{category.value}'.")
    c.print(f"Папка с таском: '{base_path}'")

    base_path.mkdir(exist_ok=True)
    for folder, desc in FOLDERS_DESCRIBED.items():
        c.print(f"Создаю папку: '{folder}'.\n\tЭто папка для: {desc}")
        (base_path / folder).mkdir(exist_ok=True)

    c.print(
        f"Создаю файл с информацией о таске: '{base_path / TASK_FILENAME}'. "
        "\n\tВ нём [red][b]необходимо[/][/] поправить все значения на нужные.",
    )
    (base_path / TASK_FILENAME).write_text(
        Task(
            name=name,
            description="Описание таска. Тут можно использовать markdown. Multiline - через |-",
            author=author or "@change me",
            category=category,
            flag=FLAG_PREFIX + "{example_flag}",
        ).to_yaml(),
        encoding="utf-8",
    )


@app.command(short_help="проверить, что все таски нормальные")
def validate():
    used_ports: dict[int, str] = {}

    for category in Path("tasks").glob("*"):
        if not category.is_dir():
            continue

        if category.name[0] == ".":
            continue

        for task in category.glob("*"):
            if not task.is_dir():
                continue

            formatted_bp = f"\\[{category.name} / {task.name}]"

            task_dirs = {i.name for i in task.glob("*") if i.is_dir()}
            valid_dirs = set(FOLDERS_DESCRIBED.keys())
            if len(task_dirs - valid_dirs) != 0:
                c.print(f"{_ER} {formatted_bp} Найдены лишние папки: {task_dirs - valid_dirs}")
                continue

            if not (task / TASK_FILENAME).exists():
                c.print(f"{_ER} {formatted_bp} Не найден '{TASK_FILENAME}'")
                continue
            try:
                task_info = Task.from_yaml((task / TASK_FILENAME).read_text(encoding="utf-8"))
            except Exception as ex:
                c.print(f"{_ER} {formatted_bp} Плохой файл: {ex!r}")
                continue

            if not (flag_re.match(task_info.flag) or flag_re.match(f"{FLAG_PREFIX}{{{task_info.flag}}}")):
                c.print(f"{_ER} {formatted_bp} Плохой флаг: '{task_info.flag}'")
                continue

            if port := task_info.server_port:
                if port in used_ports:
                    c.print(f"{_ER} {formatted_bp} - порт {port = } уже занят таском {used_ports[port] = }")
                else:
                    used_ports[port] = task_info.name

            c.print(
                f"{_OK} {formatted_bp} хороший: "  # x
                f"name={task_info.name}; "  # x
                f"cat={task_info.category}; ",
            )
            # c.print(f"{task_info.description}")


if __name__ == "__main__":
    app()
