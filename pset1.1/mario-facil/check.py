import subprocess
import os
import sys
import random

# Códigos de cores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"  # Essencial para a cor não "vazar" para o resto do terminal
BOLD = "\033[1m"

problem = "mario"
required_files = ["mario.c"]
missing_files = []

reference = "mario-check"

passed = True

def compile(file):
    return subprocess.run(
        ["make", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
        )

def clean_executable(*files):
    for file in files:
        if os.path.exists(f"./{file}"):
            os.remove(f"./{file}")

def run_program(input="", input_cli=""):
    clean_executable(problem)
    compiled = compile(problem)
    
    if compiled.returncode != 0:
        return None, None, True

    commands = [f"./{problem} {input_cli}"]

    result = subprocess.run(commands, input=input, capture_output=True, text=True)

    return result.stdout, result.returncode, False

def run_reference(input="", input_cli=""):
    clean_executable(reference)
    compiled = compile(reference)
    
    if compiled.returncode != 0:
        return None, None, True

    commands = [f"./{problem}"]
    if input_cli != "":
        commands.append(input_cli)

    result = subprocess.run(commands, input=input, capture_output=True, text=True)

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

def test_valid_height():
    global passed
    height = str(random.randint(1, 8))
    expected_stdout, expected_code, e = run_reference(height)
    stdout, code, error = run_program(height)

    if error:
        return print(f"{YELLOW} :| Teste com altura válida\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
        

    condition = (expected_stdout in stdout) and (code == expected_code)
    
    if not condition:
        passed = False
        return print(f"{RED} :( Teste com altura válida\n    {RED} Esperava '{expected_stdout}', mas recebeu '{stdout}' {RESET}")
    
    print(f"{GREEN} :) Teste com altura válida{RESET}")

def test_invalid_height1():
    global passed
    height = "-1\n0\n4"
    stdout, code, error = run_program(height)

    if error:
        return print(f"{YELLOW} :| Teste com altura menor que 1\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    condition = stdout.count("Altura:") > 2
    
    if not condition:
        passed = False
        return print(f"{RED} :( Teste com altura menor que 1\n    {RED} O programa não perguntou 'Altura: ' novamente{RESET}")
    
    print(f"{GREEN} :) Teste com altura menor que 1{RESET}")

def test_invalid_height2():
    global passed
    height = "9\n42\n4"
    stdout, code, error = run_program(height)

    if error:
        return print(f"{YELLOW} :| Teste com altura maior que 8\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    condition = stdout.count("Altura:") > 2
    
    if not condition:
        passed = False
        return print(f"{RED} :( Teste com altura maior que 8\n    {RED} O programa não perguntou 'Altura: ' novamente{RESET}")
    
    print(f"{GREEN} :) Teste com altura maior que 8{RESET}")

    

print("Verificando resultados...")
test_files_exist()
test_compile()

test_valid_height()
test_invalid_height1()
test_invalid_height2()

clean_executable(problem, reference)

if not passed:
    sys.exit(1)