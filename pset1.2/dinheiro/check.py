import subprocess
import os
import sys
import random
import re

# Códigos de cores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"  # Essencial para a cor não "vazar" para o resto do terminal
BOLD = "\033[1m"
TAB = "    "

program = "main.c"
problem = "dinheiro"
required_files = ["dinheiro.c", "dinheiro.h", "main.c"]
libs = ["dinheiro.c", "lib/cs50.c", "-Ilib"]
missing_files = []

reference = "dinheiro-check"

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

def compile_ref():
    compile_cmd = ["gcc", reference + ".c", "-o", reference]
    
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
    compiled = compile_ref()
    
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

def test_25():
    global passed

    expected_stdout, expected_code, error = run_reference("25")

    stdout, code, error = run_program("25")

    if error:
        return print(f"{YELLOW} :| Teste com 25 centavos\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    output = re.findall(r'\d+', stdout)
    ref = re.findall(r'\d+', expected_stdout)

    output = output[-1]
    ref = ref[-1]

    if output and ref:
        condition = (output == ref)
    else:
        condition = False 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com 25 centavos\n    {RED} Esperava: {ref or expected_stdout} \n    {RED} Recebeu: {output or stdout}{RESET}")
    
    print(f"{GREEN} :) Teste com 25 centavos{RESET}")
    
def test_10():
    global passed

    expected_stdout, expected_code, error = run_reference("10")

    stdout, code, error = run_program("10")

    if error:
        return print(f"{YELLOW} :| Teste com 10 centavos\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    output = re.findall(r'\d+', stdout)
    ref = re.findall(r'\d+', expected_stdout)

    output = output[-1]
    ref = ref[-1]

    if output and ref:
        condition = (output == ref)
    else:
        condition = False 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com 10 centavos\n    {RED} Esperava: {ref or expected_stdout} \n    {RED} Recebeu: {output or stdout}{RESET}")
    
    print(f"{GREEN} :) Teste com 10 centavos{RESET}")
  
def test_5():
    global passed

    expected_stdout, expected_code, error = run_reference("5")

    stdout, code, error = run_program("5")

    if error:
        return print(f"{YELLOW} :| Teste com 5 centavos\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    output = re.findall(r'\d+', stdout)
    ref = re.findall(r'\d+', expected_stdout)

    output = output[-1]
    ref = ref[-1]

    if output and ref:
        condition = (output == ref)
    else:
        condition = False 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com 5 centavos\n    {RED} Esperava: {ref or expected_stdout} \n    {RED} Recebeu: {output or stdout}{RESET}")
    
    print(f"{GREEN} :) Teste com 5 centavos{RESET}")
  
def test_1():
    global passed

    expected_stdout, expected_code, error = run_reference("1")

    stdout, code, error = run_program("1")

    if error:
        return print(f"{YELLOW} :| Teste com 1 centavo\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    output = re.findall(r'\d+', stdout)
    ref = re.findall(r'\d+', expected_stdout)

    output = output[-1]
    ref = ref[-1]

    if output and ref:
        condition = (output == ref)
    else:
        condition = False 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com 1 centavo\n    {RED} Esperava: {ref or expected_stdout} \n    {RED} Recebeu: {output or stdout}{RESET}")
    
    print(f"{GREEN} :) Teste com 1 centavo{RESET}")
  
def test_random_value():
    global passed

    input = str(random.randint(80, 100))
    expected_stdout, expected_code, error = run_reference(input)

    stdout, code, error = run_program(input)

    if error:
        return print(f"{YELLOW} :| Teste com valor aleatório\n    {YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    output = re.findall(r'\d+', stdout)
    ref = re.findall(r'\d+', expected_stdout)

    output = output[-1]
    ref = ref[-1]

    if output and ref:
        condition = (output == ref)
    else:
        condition = False 

    if not condition:
        passed = False
        return print(f"{RED} :( Teste com valor aleatório\n    {RED} Esperava: {ref or expected_stdout} \n    {RED} Recebeu: {output or stdout}{RESET}")
    
    print(f"{GREEN} :) Teste com valor aleatório{RESET}")

print("Verificando resultados...")
test_files_exist()
test_compile()

test_1()
test_5()
test_10()
test_25()
test_random_value()

clean_executable(problem, reference)

if not passed:
    sys.exit(1)
