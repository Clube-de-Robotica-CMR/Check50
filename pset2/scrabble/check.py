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
TAB = "    "

program = "scrabble.c"
problem = "scrabble"
required_files = ["scrabble.c"]
libs = ["lib/cs50.c", "-Ilib"]
missing_files = []

reference = ""

passed = True

def compile(file):
    compile_cmd = ["gcc", program]
    for cmd in libs:
        compile_cmd.append(cmd)
    
    compile_cmd.append("-o")
    compile_cmd.append(file)

    return subprocess.run(
        compile_cmd,
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

    commands = [f"./{problem}"]
    if input_cli != "":
        commands.append(input_cli)

    result = subprocess.run(commands, input=input, capture_output=True, text=True)

    return result.stdout, result.returncode, False

def run_reference(input="", input_cli=""):
    clean_executable(reference)
    compiled = compile(reference)
    
    if compiled.returncode != 0:
        return None, None, True

    commands = [f"./{reference}"]
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
        return print(f"{RED} :( Um dos programas não compila\n    {RED} Esperava código de retorno 0, não {compiled.returncode} {RESET}")
    
    print(f"{GREEN} :) Os programsa compilam {RESET}")

def test_scrabble(p1, p2, expected, description):
    global passed

    stdout, code, error = run_program(f"{p1}\n{p2}\n")

    if error:
        return print(f"{YELLOW} :| {description}\n{TAB}{YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    out = stdout.split()
    out_str = ""
    for i in range (4, len(out)):
            out_str += f" {out[i]}"

    if out_str: out = stdout
    else: out = out_str


    condition =  expected in stdout

    if not condition:
        passed = False
        return print(f"{RED} :( {description}\n{TAB}{RED} Esperava: {expected}\n{RED} {TAB}Recebeu: {out}{RESET}")
    
    print(f"{GREEN} :) {description}{RESET}")
    

print("Verificando resultados...")
test_files_exist()
test_compile()

test_scrabble("a", "z", "Player 2 vence!", "Teste com letras")
test_scrabble("APPLE", "apple", "Empate!", "Teste de insensibilidade de maiúsculas e minúsculas")
test_scrabble("Scrabble!", "Scrabble", "Empate!", "Teste com caracteres especiais e pontuação")
test_scrabble("a", "123", "Player 1 vence!", "Teste com números")

if not passed:
    sys.exit(1)
