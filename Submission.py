import json
import subprocess
from subprocess import TimeoutExpired
from JudgeException import *
from subprocess import TimeoutExpired
import time
import os
import shutil
import filecmp

class Submission:
    def __init__(self, submission_json):
        self._parse_submission(submission_json);


    def _parse_submission(self, submission_json):
        self.submission_id = submission_json["submission_id"]
        self.submission_dir = "sub" + str(self.submission_id)
        self.input_file_path = os.path.join(self.submission_dir, "in.in")
        self.output_file_path = os.path.join(self.submission_dir, "out.out")
        self.result_file_path = os.path.join(self.submission_dir, "result.out")
        self.source_code = submission_json["source_code"]["content"]
        self.code_lang = submission_json["source_code"]["language"]
        self.time_limit = submission_json["time_limit"]
        self.memory_limit = submission_json["memory_limit"]
        self.test_cases = submission_json["test_cases"] # list of tuples: input is 0, output is 1
        self.results = []
        self.time_limit_flag = False
        self.memory_limit_flag = False
        

    def process(self):
        os.mkdir(self.submission_dir)
        self._compile();
        self._run();

    def get_result(self):
        result = {}
        result["submission_id"] = self.submission_id
        result["tests_verdicts"] = self.results
        return json.dumps(result)

        


    def _compile(self):
        self.source_file_name = os.path.join(self.submission_dir, self.submission_dir + ".cpp")
        with open(self.source_file_name, "w+") as source_code:
            source_code.write(self.source_code)
        try:
            process = subprocess.check_call(["g++", self.source_file_name, "-o", self.source_file_name[:-4]], stderr=subprocess.PIPE)
            print("Compilation Successufl");
        except Exception as e:
            print(e)
            raise(CompilationError)

    def _run(self):
        for test in self.test_cases:
            with open(self.input_file_path, "w+") as input_file:
                      input_file.write(test["input"])
            with open(self.output_file_path, "w+") as input_file:
                      input_file.write(test["output"])
            self.results.append(self._run_test())


    def _run_test(self):
        verdict = "AC"
        #TODO: Calculate time
        #TODO: Calculate memory
        exe_time = 1
        memory_usage = 20000
        try:
            input_file = open(self.input_file_path, "r")
            output_file = open(self.result_file_path, "w")
            process = subprocess.check_call(
                    ["./" + self.source_file_name[:-4]],
                    stdin=input_file,
                    stdout=output_file,
                    timeout = self.time_limit 
                    )
            input_file.close()
            output_file.close()
        except TimeoutExpired:
            self.time_limit_flag = True
            verdict = "TLE"
            exe_time = self.time_limit
        except RuntimeError:
            verdict = "ERUN"
        except Exception as e:
            print(e)
            verdict = "ESYS"
        if verdict == "AC":
            if not filecmp.cmp(self.result_file_path, self.output_file_path):
                verdict = "WA"
        return {
                "verdict" : verdict,
                "run_time" : exe_time,
                "memory_used" : memory_usage
        }

        


    def __del__(self):
        shutil.rmtree(self.submission_dir)
        

