from .model import Task

def dependencies_satisfied(task: Task, completed_ids: set[str]) -> bool:
    return all(dep in completed_ids for dep in task.dependencies)

def validate_dependency_graph(tasks: list[Task]) -> None:
    ids = {t.task_id for t in tasks}
    graph = {t.task_id: t.dependencies for t in tasks}
    missing = {d for deps in graph.values() for d in deps if d not in ids}
    if missing:
        raise ValueError(f"missing dependencies: {sorted(missing)}")
    visiting, visited = set(), set()
    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError("dependency cycle detected")
        if node in visited:
            return
        visiting.add(node)
        for dep in graph[node]:
            visit(dep)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)

def idempotency_identity(task: Task) -> str:
    return task.idempotency_key or task.task_id
