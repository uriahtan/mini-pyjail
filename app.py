from io import StringIO
import sys
import contextlib
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    eval_result = ""
    exec_result = ""
    if request.method == "POST":
        eval_input = request.form.get("eval_input", "")
        try:
            eval_result = str(eval(eval_input))   # vulnerable on purpose
            # result = str(exec(expr))   # vulnerable on purpose
        except Exception as e:
            eval_result = f"Error: {e}"
        
        # print(f"eval result: {eval_result}")

        exec_input = request.form.get("exec_input", "")
        try:
            exec_locals = {}

            with StringIO() as output:
                with contextlib.redirect_stdout(output):
                    exec(exec_input, {}, exec_locals)
        

                captured_output = output.getvalue().strip()

            if captured_output:
                exec_result = f"Output:\n{captured_output}"
            else:
                exec_result = "Code executed but produced no output"

        except Exception as e:
            exec_result = f"Error: {e}"

        # print(exec_result)
        print(f"exec result: {exec_result}")

    return f"""
    <h2>Vulnerable Calculator (using the eval function)</h2>
    <p>Try typing 1+1</p>
    <form method="POST">
        <input name="expr_input" placeholder="Enter input">
        <input type="submit" value="Calculate">
    </form>
    <pre>{eval_result}</pre>

    <h2>Vulnerable Calculator (using the exec function)</h2>
    <p>Try typing print(1+1)</p>
    <form method="POST">
        <input name="exec_input" placeholder="Enter input">
        <input type="submit" value="Calculate">
    </form>
    # <pre>{exec_result}</pre>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
