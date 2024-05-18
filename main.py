import subprocess
from subprocess import TimeoutExpired
import json
from flask import Flask, jsonify, request
import resource
import psutil
import time

class CompilationError(Exception):
    pass

class RuntimeError(Exception):
    pass

class TLE(Exception):
    pass

class MLE(Exception):
    pass

MAX_VIRTUAL_MEMORY = 10 * 1024 * 1024 # 10 MB
def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

def compile(source_code):
    try:
        # Checks that 
        process = subprocess.check_call(["g++", source_code, "-o", source_code[:-4]], stderr=subprocess.PIPE)
        print("Compilation Successufl");
    except Exception as e:
        print(e)
        raise(CompilationError)

def measure_memory_usage(pid):
    try:
        process = psutil.Process(pid)
        memory_info = process.memory_info()
        return memory_info.rss  # Return the Resident Set Size (RSS) in bytes
    except psutil.NoSuchProcess:
        return None

def run(exe_name):
    with open("input.in", "r") as in_stream:
        with open("out.out", "w+") as out_stream:
            process = subprocess.check_call(
                    ["./" + exe_name],
                    stdin=in_stream,
                    stdout=out_stream,
                    timeout = 3
            )

submission_id = 0
app = Flask(__name__)

@app.route('/judge', methods=['POST'])
def judge_solution():
    submission = json.loads(request.data)
    global submission_id
    submission_id += 1
    source_file_name = "sub" + str(submission_id) + ".cpp"
    with open(source_file_name, "w+") as source_code:
        source_code.write(submission['sourceCode']['content'])
    result = {}
    try:
        compile(source_file_name)
        try:
            run(source_file_name[:-4])
            result["status"] = "SUCCESS"
        except IOError:
            result["status"] = "EINTERNAL"
        except RuntimeError:
            result["status"] = "ERUNTIME"
        except TimeoutExpired:
            result["status"] = "TLE"
        except MLE:
            result["status"] = "MLE"
    except CompilationError:
        result["status"] = "ECOMPILATION"
    return json.dumps(result)

if __name__ == '__main__':
   app.run(port=5010, debug=True)


