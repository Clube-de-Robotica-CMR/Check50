# 378282246310005 AMEX
# 5105105105105100 MASTERCARD
# 4111111111111111 VISA (16)
# 4222222222222 VISA (13)
# 4111111111112 INVALID

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

program = "main.c"
problem = "cartao"
required_files = ["cartao.c", "cartao.h", "main.c"]
libs = ["cartao.c", "lib/cs50.c", "-Ilib"]
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

def test_AMEX():
    global passed

    expected_stdout = "AMEX"
    expected_code = 0

    stdout, code, error = run_program("378282246310005")

    if error:
        return print(f"{YELLOW} :| Teste com American Express (AMEX)\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    stdout = stdout.split()
    output = stdout[-1]

    condition = (expected_stdout.strip() in output.upper().strip()) 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com American Express (AMEX)\n    {RED} Esperava: {expected_stdout} \n    {RED} Recebeu: {output}{RESET}")
    
    print(f"{GREEN} :) Teste com American Express (AMEX){RESET}")

def test_MASTERCARD():
    global passed

    expected_stdout = "MASTERCARD"
    expected_code = 0

    stdout, code, error = run_program("5105105105105100")

    if error:
        return print(f"{YELLOW} :| Teste com Mastercard\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    stdout = stdout.split()
    output = stdout[-1]

    condition = (expected_stdout.strip() in output.upper().strip()) 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com Mastercard\n    {RED} Esperava: {expected_stdout} \n    {RED} Recebeu: {output}{RESET}")
    
    print(f"{GREEN} :) Teste com Mastercard{RESET}")

def test_VISA13():
    global passed

    expected_stdout = "VISA"
    expected_code = 0

    stdout, code, error = run_program("4222222222222")

    if error:
        return print(f"{YELLOW} :| Teste com Visa (13 dígitos)\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    stdout = stdout.split()
    output = stdout[-1]

    condition = (expected_stdout.strip() in output.upper().strip()) 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com Visa (13 dígitos)\n    {RED} Esperava: {expected_stdout} \n    {RED} Recebeu: {output}{RESET}")
    
    print(f"{GREEN} :) Teste com Visa (13 dígitos){RESET}")

def test_VISA16():
    global passed

    expected_stdout = "VISA"
    expected_code = 0

    stdout, code, error = run_program("4111111111111111")

    if error:
        return print(f"{YELLOW} :| Teste com Visa (16 dígitos)\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    stdout = stdout.split()
    output = stdout[-1]

    condition = (expected_stdout.strip() in output.upper().strip()) 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com Visa (16 dígitos)\n    {RED} Esperava: {expected_stdout} \n    {RED} Recebeu: {output}{RESET}")
    
    print(f"{GREEN} :) Teste com Visa (16 dígitos){RESET}")

def test_invalid():
    global passed

    expected_stdout = "INVALIDO"
    expected_code = 0

    stdout, code, error = run_program("4111111111112")

    if error:
        return print(f"{YELLOW} :| Teste com número inválido\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    stdout = stdout.split()
    output = stdout[-1]

    condition = (expected_stdout.strip() in output.upper().strip()) 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com número inválido\n    {RED} Esperava: {expected_stdout} \n    {RED} Recebeu: {output}{RESET}")
    
    print(f"{GREEN} :) Teste com número inválido{RESET}")


print("Verificando resultados...")
test_files_exist()
test_compile()

test_AMEX()
test_MASTERCARD()
test_VISA13()
test_VISA16()
test_invalid()

clean_executable(problem, reference)

if not passed:
    sys.exit(1)
