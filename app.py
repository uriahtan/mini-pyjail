from io import StringIO
import sys
import contextlib
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/no_blacklist.html", methods=["GET", "POST"])
def noblacklist():
    no_blacklist_eval_result = ""
    no_blacklist_exec_result = ""
    if request.method == "POST":
        no_blacklist_eval_input = request.form.get("no_blacklist_eval_input", "")
        try:
            no_blacklist_eval_result = str(eval(no_blacklist_eval_input))   # vulnerable on purpose
            # result = str(exec(expr))   # vulnerable on purpose
        except Exception as e:
            no_blacklist_eval_result = f"Error: {e}"
        
        print(f"eval result: {no_blacklist_eval_result}")

        no_blacklist_exec_input = request.form.get("no_blacklist_exec_input", "")
        try:
            no_blacklist_exec_locals = {}

            with StringIO() as output:
                with contextlib.redirect_stdout(output):
                    exec(no_blacklist_exec_input, {}, no_blacklist_exec_locals)
        

                captured_output = output.getvalue().strip()

            if captured_output:
                no_blacklist_exec_result = f"Output:\n{captured_output}"
            else:
                no_blacklist_exec_result = "Code executed but produced no output"

        except Exception as e:
            no_blacklist_exec_result = f"Error: {e}"

        # print(exec_result)
        # print(f"exec result: {no_blacklist_exec_result}")

    return render_template(
        "no_blacklist.html",
        eval_result = no_blacklist_eval_result,
        exec_result = no_blacklist_exec_result
    )

@app.route("/weak_blacklist.html", methods=["GET", "POST"])
def weakblacklist():
    weak_blacklist_eval_result = ""
    weak_blacklist_exec_result = ""
    if request.method == "POST":
        weak_blacklist_eval_input = request.form.get("weak_blacklist_eval_input", "")
        try:
            weak_blacklist_eval_result = str(eval(weak_blacklist_eval_input))   # vulnerable on purpose
            # result = str(exec(expr))   # vulnerable on purpose
        except Exception as e:
            weak_blacklist_eval_result = f"Error: {e}"
        
        print(f"eval result: {weak_blacklist_eval_result}")

        weak_blacklist_exec_input = request.form.get("weak_blacklist_exec_input", "")
        try:
            weak_blacklist_exec_locals = {}

            with StringIO() as output:
                with contextlib.redirect_stdout(output):
                    exec(weak_blacklist_exec_input, {}, weak_blacklist_exec_locals)
        

                captured_output = output.getvalue().strip()

            if captured_output:
                weak_blacklist_exec_result = f"Output:\n{captured_output}"
            else:
                weak_blacklist_exec_result = "Code executed but produced no output"

        except Exception as e:
            weak_blacklist_exec_result = f"Error: {e}"

        # print(exec_result)
        print(f"exec result: {weak_blacklist_exec_result}")
    
    return render_template(
        "weak_blacklist.html",
        eval_result = weak_blacklist_eval_result,
        exec_result = weak_blacklist_exec_result
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
