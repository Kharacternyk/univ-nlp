from subprocess import Popen

import modal

image = (
    modal.Image.from_registry("nvidia/cuda:13.1.0-devel-ubuntu24.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install("vllm[flashinfer]")
    .env(dict(HF_XET_HIGH_PERFORMANCE="1"))
)

app = modal.App("prolog-llm", image=image)


@app.function(
    gpu="H100",
    scaledown_window=3600,
    startup_timeout=900,
    volumes={"/root/.cache": modal.Volume.from_name("prolog-llm")},
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=900, requires_proxy_auth=True)
def serve():
    Popen(["vllm", "serve", "openai/gpt-oss-120b", "--max-num-seqs=8"])
