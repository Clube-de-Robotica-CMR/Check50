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

program = "legibilidade.c"
problem = "legibilidade"
required_files = ["legibilidade.c"]
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

def test_readability(text, expected, description):
    global passed

    stdout, code, error = run_program(f"{text}\n")

    if error:
        return print(f"{YELLOW} :| {description}\n{TAB}{YELLOW} Não é possível checar até que a carinha vire um sorriso {RESET}")
    
    out = stdout.split()
    out = out[-1]

    condition =  expected in out

    if not condition:
        passed = False
        return print(f"{RED} :( {description}\n{TAB}{RED} Esperava: {expected}\n{RED}{TAB} Recebeu: {out}{RESET}")
    
    print(f"{GREEN} :) {description}{RESET}")
    

print("Verificando resultados...")
test_files_exist()
test_compile()

test_readability("One fish. Two fish. Red fish. Blue fish.", "-1", "Teste com texto simples 1")
test_readability("Congratulations! Today is your day. You're off to Great Places! You're off and away!", "3", "Teste com texto simples 2")

test_readability("In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since.", "7", "Teste com texto intermediário 1")
test_readability("Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, \"and what is the use of a book,\" thought Alice \"without pictures or conversation?\"", "8", "Teste com texto intermediário 2")

test_readability("It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.", "10", "Teste com texto complexo 1")
test_readability("A large class of computational problems involve the determination of properties of graphs, digraphs, integers, arrays of integers, finite families of finite sets, boolean formulas and elements of other countable domains.", "16+", "Teste com texto complexo 2")

if not passed:
    sys.exit(1)
