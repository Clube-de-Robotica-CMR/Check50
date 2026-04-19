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

program = "caesar.c"
problem = "caesar"
required_files = ["caesar.c"]
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

def test_compile(check=True):
    global passed
    compiled = compile(problem)

    if compiled.returncode != 0:
        passed = False
        if check: print(f"{RED} :( Um dos programas não compila\n    {RED} Esperava código de retorno 0, não {compiled.returncode} {RESET}")
        return False
    
    if check: print(f"{GREEN} :) Os programas compilam {RESET}")
    return True

def test_caesar_valid(text, key, expected, description):
    global passed

    stdout, code, error = run_program(f"{text}\n", key)

    if error:
        return print(f"{YELLOW} :| {description}\n{TAB}{YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    out = stdout.split()
    findex = out.index("ciphertext:") + 1
    tmp = []
    for i in range(findex, len(out)):
        tmp.append(out[i])

    out = " ".join(tmp)

    condition = expected == out

    condition =  expected == out

    if not condition:
        passed = False
        return print(f"{RED} :( {description}\n{TAB}{RED} Esperava: {expected}\n{RED}{TAB} Recebeu: {out}{RESET}")
    
    print(f"{GREEN} :) {description}{RESET}")

def test_caesar_invalid(key, exp_code, description, compiled):
    global passed

    stdout, code, error = run_program(input_cli=key)

    if not compiled:
        return print(f"{YELLOW} :| {description}\n{TAB}{YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")

    condition =  exp_code == code

    if not condition:
        passed = False
        return print(f"{RED} :( {description}\n{TAB}{RED} Esperava código de retorno {exp_code}, não {code}{RESET}")
    
    print(f"{GREEN} :) {description}{RESET}")

    
    

print("Verificando resultados...")
test_files_exist()
test_compile()

test_caesar_invalid("", 1, "Teste com chave vazia", test_compile(check=False))
test_caesar_invalid("1 2", 1, "Teste com chaves múltiplas", test_compile(check=False))
test_caesar_invalid("20x", 1, "Teste com chave não numérica", test_compile(check=False))

test_caesar_valid("A", "1", "B", "Teste com chave simples 1")
test_caesar_valid("hello, world", "13", "uryyb, jbeyq", "Teste com chave simples 2")

test_caesar_valid("BarfoO", "26", "BarfoO", "Teste de rotação do alfabeto")

test_caesar_valid("a", "27", "b", "Teste de chave maior que o alfabeto 1")
test_caesar_valid("HELLO", "52", "HELLO", "Teste de chave maior que o alfabeto 2")

test_caesar_valid("be sure to drink your Ovaltine", "13", "or fher gb qevax lbhe Binygvar", "Teste com frase completa")

if not passed:
    sys.exit(1)
