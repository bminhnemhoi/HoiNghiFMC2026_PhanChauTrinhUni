# Kaggle GPU runner (2×T4). Rendered per job by vnsoc.run.kaggle_jobs: __JOB__ is replaced with JSON.
# One vLLM process per GPU (data parallel), greedy decoding unless the request says otherwise,
# results flushed every batch to /kaggle/working so a timeout still leaves partial output.
# T4 = compute capability 7.5: no bf16 -> dtype "half" (gemma2/gemma3/glm4 refuse fp16 in vLLM -> "float32"
# or do not run them on T4); FlashAttention needs SM80+, vLLM falls back to another attention backend.
import json
import os
import subprocess
import sys
import time

JOB = json.loads(r'''__JOB__''')

WORKER = r'''
import json, os, sys, time


def main():
    shard = json.loads(sys.argv[1])
    from vllm import LLM, SamplingParams
    import vllm
    t0 = time.time()
    kw = dict(model=shard["model"], dtype=shard.get("dtype", "half"),
              max_model_len=shard.get("max_model_len", 8192),
              gpu_memory_utilization=shard.get("gpu_memory_utilization", 0.90),
              enable_prefix_caching=True, seed=0,
              tensor_parallel_size=shard.get("tensor_parallel_size", 1))
    if shard.get("quantization") not in (None, "none"):
        kw["quantization"] = shard["quantization"]
    llm = LLM(**kw)
    load_s = time.time() - t0
    reqs = [json.loads(l) for l in open(shard["requests"], encoding="utf-8") if l.strip()]
    reqs = [r for r in reqs if r.get("model_key") == shard["model_key"]] or reqs
    out_path = shard["out"]
    done = set()
    for prev in [out_path, *shard.get("resume_from", [])]:  # resume_from: earlier outputs under /kaggle/input
        if os.path.exists(prev):
            done |= {json.loads(l)["request_id"] for l in open(prev, encoding="utf-8") if l.strip()}
    todo = [r for r in reqs if r["request_id"] not in done]
    groups = {}
    for r in todo:
        s = r.get("sampling", {})
        key = (s.get("temperature", 0.0), s.get("top_p", 1.0), s.get("n", 1), s.get("max_tokens", 128))
        groups.setdefault(key, []).append(r)
    n_tok_out, t_gen = 0, time.time()
    with open(out_path, "a", encoding="utf-8") as f:
        for (temp, top_p, n, mx), rs in groups.items():
            sp = SamplingParams(temperature=temp, top_p=top_p, n=n, max_tokens=mx, seed=0, logprobs=1)
            B = shard.get("batch", 256)
            for i in range(0, len(rs), B):
                chunk = rs[i:i + B]
                outs = llm.chat([r["messages"] for r in chunk], sp, use_tqdm=False,
                                chat_template_kwargs=shard.get("chat_template_kwargs") or None)
                for r, o in zip(chunk, outs):
                    n_tok_out += sum(len(c.token_ids) for c in o.outputs)
                    f.write(json.dumps({"request_id": r["request_id"], "outputs": [c.text for c in o.outputs],
                                        "tokens_in": len(o.prompt_token_ids),
                                        "tokens_out": [len(c.token_ids) for c in o.outputs],
                                        "cum_logprob": [c.cumulative_logprob for c in o.outputs],
                                        "model_key": shard["model_key"], "vllm": vllm.__version__},
                                       ensure_ascii=False) + "\n")
                f.flush()
                print(f"[{shard['model_key']}] {i + len(chunk)}/{len(rs)} done", flush=True)
    stats = {"model_key": shard["model_key"], "load_s": load_s, "gen_s": time.time() - t_gen,
             "requests": len(todo), "tokens_out": n_tok_out, "vllm": vllm.__version__}
    open(out_path + ".stats.json", "w").write(json.dumps(stats))
    print(json.dumps(stats), flush=True)


if __name__ == "__main__":
    main()
'''


def sh(cmd: str) -> None:
    print("+", cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)


def main() -> None:
    os.chdir("/kaggle/working")
    sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv")
    if JOB.get("pip"):
        # e.g. ["vllm==<version found at T0.4>", "--extra-index-url", "https://download.pytorch.org/whl/cu129"]
        sh("pip install -q " + " ".join(JOB["pip"]))
    try:
        from kaggle_secrets import UserSecretsClient

        tok = UserSecretsClient().get_secret("HF_TOKEN")
        if tok:
            os.environ["HF_TOKEN"] = tok
            os.environ["HUGGING_FACE_HUB_TOKEN"] = tok
    except Exception as e:  # secret not attached to THIS kernel: gated models will fail with a clear error
        print("HF_TOKEN secret not available:", type(e).__name__, flush=True)
    open("worker.py", "w").write(WORKER)
    procs = []
    for gpu, shard in enumerate(JOB["shards"]):
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=shard.get("gpus", str(gpu)))
        procs.append(subprocess.Popen([sys.executable, "worker.py", json.dumps(shard)], env=env))
        time.sleep(20)  # stagger model loading
    codes = [p.wait() for p in procs]
    json.dump({"job_id": JOB["job_id"], "exit_codes": codes}, open("job_status.json", "w"))
    if any(codes):
        sys.exit(1)


if __name__ == "__main__":
    main()
