import subprocess
from subprocess import TimeoutExpired
import json
from flask import Flask, jsonify, request
import resource
import psutil
import time
from JudgeException import *
from Submission import Submission


app = Flask(__name__)

@app.route('/judge', methods=['POST'])
def judge_solution():
    submission_json = json.loads(request.data)
    submission = Submission(submission_json)
    result = {}
    try:
        submission.process()
        result["status"] = "SUCCESS"
    except RuntimeError:
        result["status"] = "ERUNTIME"
    except TimeoutExpired:
        result["status"] = "TLE"
    except MLE:
        result["status"] = "MLE"
    except CompilationError:
        result["status"] = "ECOMPILATION"
    except Exception as e:
        print(e)
        result["status"] = "ESYS"
    return submission.get_result()

if __name__ == '__main__':
   app.run(port=5010, debug=True)


