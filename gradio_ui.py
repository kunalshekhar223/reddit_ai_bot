import gradio as gr
import subprocess
import sys
import os

def run_script(execute_script):
    # Execute the Python script if the option is selected
    if execute_script:
        command = f"python main.py"
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.output}"
    return output

execute_script = gr.inputs.Checkbox(label="Execute Python script")
output_text = gr.outputs.Textbox(label="Output")

gr.Interface(fn=run_script, inputs=[execute_script], outputs=output_text).launch(share=True)
