import shutil
from pathlib import Path

import yaml


tests = [
    "test_exporters.yml",
    "test_dummy_inputs.yml",
    "test_bettertransformer.yml",
    "test_onnx.yml",
    "test_fx.yml",
    "test_onnxruntime.yml",
    "test_benckmark.yml",
    "test_optimum_common.yml",
]

for test_name in tests:
    new_name = "dev_" + test_name

    with open(Path("workflows", test_name), "r") as file:
        workflox_yml = yaml.load(file, yaml.BaseLoader)

        workflox_yml["name"] = "dev_" + workflox_yml["name"]
        workflox_yml["on"] = {"schedule": [{"cron": "0 7 * * *"}]}

        for i, step in enumerate(workflox_yml["jobs"]["build"]["steps"]):
            if "name" in step and step["name"] == "Install dependencies":
                workflox_yml["jobs"]["build"]["steps"][i][
                    "run"
                ] += "pip install -U git+https://github.com/huggingface/evaluate\npip install -U git+https://github.com/huggingface/diffusers\npip install -U git+https://github.com/huggingface/transformers\n"

    with open(Path("workflows", new_name), "w") as outfile:
        yaml.dump(
            workflox_yml,
            outfile,
            default_flow_style=False,
            allow_unicode=True,
            width=float("inf"),
            sort_keys=False,
        )

    with open(Path("workflows", new_name), "r+") as outfile:
        workflox_yml = outfile.read()
        workflox_yml = "# This yml file is autogenerated. Do not edit.\n\n" + workflox_yml

        workflox_yml = workflox_yml.replace("'", "")
        workflox_yml = workflox_yml.replace("run:", "run: |\n       ")

        workflox_yml = "\n".join([ll.rstrip() for ll in workflox_yml.splitlines() if ll.strip()])

        outfile.seek(0)
        outfile.write(workflox_yml)
        outfile.truncate()
