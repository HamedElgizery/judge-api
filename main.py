import subprocess
import json

class CompilationError(Exception):
    pass

class RuntimeError(Exception):
    pass

def compile(source_code):
    try:
        # Checks that 
        subprocess.check_call(["g++", source_code, "-o", source_code[:-4]], stderr=subprocess.PIPE)
        print("Compilation Successufl");
    except:
        raise(CompilationError)

def run(exe_name):
    try:
        with open("input.in", "r") as in_stream:
            with open("out.out", "w") as out_stream:
                subprocess.check_call(["./main"], stdin=in_stream, stdout=out_stream)
    except:
        raise(RuntimeError)
    

compile("main.cpp")
run("main")

