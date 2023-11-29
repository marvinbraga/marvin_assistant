import os

from dotenv import load_dotenv, find_dotenv
from invoke import task

load_dotenv(find_dotenv())

compose_cmd = os.environ["COMPOSE_CMD"]


@task
def status(c):
    """Exibe a situação dos serviços do Docker Compose."""
    c.run(f"{compose_cmd} ps")


@task
def start(c):
    """Inicia todos os serviços definidos no docker-compose.yml."""
    c.run(f"{compose_cmd} up -d")


@task
def stop(c):
    """Para todos os serviços rodando."""
    c.run(f"{compose_cmd} stop")


@task
def down(c):
    """Para e exclui todos os serviços rodando."""
    c.run(f"{compose_cmd} down --remove-orphans")


@task
def build(c):
    """Reconstrói e inicia os serviços."""
    c.run(f"{compose_cmd} up -d --build")


@task
def logs(c, service=None):
    """Exibe os logs dos serviços. Use --service para um serviço específico."""
    command = f"{compose_cmd} logs"
    if service:
        command += f" {service}"
    c.run(command)


@task
def shell(c, service):
    """Acessa o shell de um serviço específico."""
    c.run(f"{compose_cmd} exec {service} /bin/bash")


@task
def prune_all(c):
    """
    Ex.: inv prune-all
    """
    c.run("docker system prune --all")
    c.run("docker volume prune")
    c.run("sudo service docker restart")


@task
def sh(c, svc=""):
    cmd = f'{compose_cmd} exec "{svc}" bash'
    c.run(cmd)
