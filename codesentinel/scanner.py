import ast
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    severity: str
    message: str
    def as_dict(self):
        return asdict(self)

class Scanner(ast.NodeVisitor):
    def __init__(self, path):
        self.path, self.findings = path, []
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            self.findings.append(Finding(self.path,node.lineno,"PY001","high","Review dynamic code execution"))
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr == "run":
            if any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords):
                self.findings.append(Finding(self.path,node.lineno,"PY002","high","Review shell=True"))
        self.generic_visit(node)

def scan_source(source, path="<memory>"):
    visitor=Scanner(path)
    visitor.visit(ast.parse(source,filename=path))
    return visitor.findings

def scan_file(path: Path):
    return scan_source(path.read_text(encoding="utf-8"),str(path))
