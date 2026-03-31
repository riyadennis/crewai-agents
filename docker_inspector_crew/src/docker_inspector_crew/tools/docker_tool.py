import json
import subprocess
from crewai_tools import BaseTool


def _run_docker(args: list[str]) -> str:
    """Run a docker command and return stdout, or an error message."""
    try:
        result = subprocess.run(
            ["docker"] + args,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return f"Docker error: {result.stderr.strip()}"
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: docker CLI not found. Is Docker installed and on PATH?"
    except subprocess.TimeoutExpired:
        return "Error: docker command timed out."


class ListContainersTool(BaseTool):
    name: str = "List Docker Containers"
    description: str = (
        "Lists all Docker containers (running and stopped) with their ID, name, "
        "image, status, and creation time. Returns JSON array."
    )

    def _run(self, argument: str = "") -> str:
        format_str = (
            '{"id":"{{.ID}}","name":"{{.Names}}","image":"{{.Image}}",'
            '"status":"{{.Status}}","created":"{{.CreatedAt}}","ports":"{{.Ports}}"}'
        )
        raw = _run_docker(["ps", "-a", f"--format={format_str}"])
        if raw.startswith("Error") or raw.startswith("Docker error"):
            return raw
        lines = [line for line in raw.splitlines() if line.strip()]
        containers = []
        for line in lines:
            try:
                containers.append(json.loads(line))
            except json.JSONDecodeError:
                containers.append({"raw": line})
        return json.dumps(containers, indent=2)


class ListImagesTool(BaseTool):
    name: str = "List Docker Images"
    description: str = (
        "Lists all Docker images with their repository, tag, image ID, and size. "
        "Returns JSON array."
    )

    def _run(self, argument: str = "") -> str:
        format_str = (
            '{"id":"{{.ID}}","repository":"{{.Repository}}","tag":"{{.Tag}}",'
            '"size":"{{.Size}}","created":"{{.CreatedAt}}"}'
        )
        raw = _run_docker(["images", f"--format={format_str}"])
        if raw.startswith("Error") or raw.startswith("Docker error"):
            return raw
        lines = [line for line in raw.splitlines() if line.strip()]
        images = []
        for line in lines:
            try:
                images.append(json.loads(line))
            except json.JSONDecodeError:
                images.append({"raw": line})
        return json.dumps(images, indent=2)


class InspectContainerTool(BaseTool):
    name: str = "Inspect Docker Container"
    description: str = (
        "Inspects a specific Docker container by name or ID to get detailed "
        "configuration including environment variables, mounts, and network settings."
    )

    def _run(self, argument: str) -> str:
        if not argument:
            return "Error: provide a container name or ID."
        raw = _run_docker(["inspect", argument.strip()])
        return raw


class RemoveContainerTool(BaseTool):
    name: str = "Remove Stopped Docker Container"
    description: str = (
        "Removes a single stopped/exited Docker container by name or ID. "
        "Will NOT remove running containers. Pass the container name or ID as argument."
    )

    def _run(self, argument: str) -> str:
        if not argument:
            return "Error: provide a container name or ID."
        container = argument.strip()
        # Safety check: refuse if container is running
        status = _run_docker(
            ["inspect", "--format={{.State.Status}}", container]
        )
        if status == "running":
            return f"Refused: container '{container}' is currently running. Stop it first."
        result = _run_docker(["rm", container])
        if result.startswith("Docker error") or result.startswith("Error"):
            return result
        return f"Removed container: {result}"


class PruneStoppedContainersTool(BaseTool):
    name: str = "Prune All Stopped Containers"
    description: str = (
        "Removes ALL stopped/exited containers in one operation using "
        "'docker container prune -f'. Running containers are never affected."
    )

    def _run(self, argument: str = "") -> str:
        result = _run_docker(["container", "prune", "-f"])
        return result


class PruneDanglingImagesTool(BaseTool):
    name: str = "Prune Dangling Docker Images"
    description: str = (
        "Removes dangling Docker images — untagged images (<none>:<none>) "
        "that are not referenced by any container — using 'docker image prune -f'. "
        "Tagged images are never removed."
    )

    def _run(self, argument: str = "") -> str:
        result = _run_docker(["image", "prune", "-f"])
        return result


class RemoveImageTool(BaseTool):
    name: str = "Remove Docker Image"
    description: str = (
        "Removes a specific Docker image by repository:tag or image ID. "
        "Will fail if any container (even stopped) is still using the image. "
        "Pass the image name or ID as argument."
    )

    def _run(self, argument: str) -> str:
        if not argument:
            return "Error: provide an image name (repository:tag) or ID."
        result = _run_docker(["rmi", argument.strip()])
        if result.startswith("Docker error") or result.startswith("Error"):
            return result
        return f"Removed image: {result}"
