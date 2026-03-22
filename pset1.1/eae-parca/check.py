import subprocess
import os
import sys

# Códigos de cores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"  # Essencial para a cor não "vazar" para o resto do terminal
BOLD = "\033[1m"

problem = "desafio"
required_files = ["desafio.c"]
missing_files = []

passed = True

def compile(file):
    return subprocess.run(
        ["make", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
        )

def clean_executable(file):
    if os.path.exists(f"./{file}"):
        os.remove(f"./{file}")

def run_program(*input):
    clean_executable(problem)
    compiled = compile(problem)
    
    if compiled.returncode != 0:
        return None, None, True

    commands = [f"./{problem}"]
    for i in input:
        commands.append(i)

    result = subprocess.run(commands, capture_output=True, text=True)

    return result.stdout, result.returncode, False

def test_files_exist():
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if len(missing_files) != 0:
        mfiles_str = ", ".join(missing_files)
        print(f"{RED} :( O(s) arquivo(s) {mfiles_str} não existe(m) {RESET}")
        return sys.exit(1)

    files_str = ", ".join(required_files)
    print(f"{GREEN} :) O(s) arquivo(s) {files_str} existe(m) {RESET}")

def test_compile():
    global passed
    compiled = compile(problem)

    if compiled.returncode != 0:
        passed = False
        return print(f"{RED} :( O programa não compila\n    {RED} Esperava código de retorno 0, não {compiled.returncode} {RESET}")
    
    print(f"{GREEN} :) O programa compila {RESET}")

def test_davi():
    global passed
    expected_stdout = "Eae, Davi"
    expected_code = 0
    stdout, code, error = run_program()

    if error:
        return print(f"{YELLOW} :| O programa imprime 'Eae, Davi'\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
        

    condition = (expected_stdout in stdout) and (code == expected_code)
    
    if not condition:
        passed = False
        return print(f"{RED} :( O programa imprime 'Eae, Davi'\n    {RED} Esperava '{expected_stdout}', mas recebeu '{stdout}' {RESET}")
    
    print(f"{GREEN} :) O programa imprime 'Eae, Davi' {RESET}")

print("Verificando resultados...")
test_files_exist()
test_compile()

test_davi()

clean_executable(problem)

if not passed:
    sys.exit(1)