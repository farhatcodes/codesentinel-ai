from codesentinel.scanner import scan_source

def test_eval():
    assert scan_source("eval('2+2')")[0].rule=="PY001"

def test_shell():
    assert scan_source("subprocess.run('ls', shell=True)")[0].rule=="PY002"

def test_safe():
    assert scan_source("print(1+1)")==[]
