"""Zpracuje texty modelem UDPipe 1 do CoNLL-U.

Každý soubor začíná uprostřed věty (tam skončil prompt), první věta proto
dostane v CoNLL-U komentář `# fragment = 1` a analýza ji vynechává.

Použití:
  python3 -I parse.py MODEL.udpipe INDIR OUTDIR [--jobs 2]
INDIR má podsložky po skupinách s *.txt (výstup sample.py).
"""
import argparse
import os
import sys
from multiprocessing import Pool

_model = None
_pipe = None


def _init(model_path):
    global _model, _pipe
    from ufal.udpipe import Model, Pipeline
    _model = Model.load(model_path)
    if _model is None:
        raise SystemExit(f"model se nepodařilo načíst: {model_path}")
    _pipe = Pipeline(_model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")


def _work(job):
    src, dst = job
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst, "skip"
    from ufal.udpipe import ProcessingError
    with open(src, encoding="utf-8") as f:
        text = f.read()
    err = ProcessingError()
    out = _pipe.process(text, err)
    if err.occurred():
        return dst, "error: " + err.message
    # označ první větu jako fragment
    lines = out.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# sent_id"):
            lines.insert(i + 1, "# fragment = 1")
            break
    tmp = dst + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    os.replace(tmp, dst)
    return dst, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("indir")
    ap.add_argument("outdir")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    a = ap.parse_args()

    jobs = []
    for g in sorted(os.listdir(a.indir)):
        gd = os.path.join(a.indir, g)
        if not os.path.isdir(gd):
            continue
        od = os.path.join(a.outdir, g)
        os.makedirs(od, exist_ok=True)
        for fn in sorted(os.listdir(gd)):
            if fn.endswith(".txt"):
                jobs.append((os.path.join(gd, fn), os.path.join(od, fn[:-4] + ".conllu")))
    print(f"souborů: {len(jobs)}", file=sys.stderr)
    done = 0
    with Pool(a.jobs, initializer=_init, initargs=(a.model,)) as pool:
        for dst, status in pool.imap_unordered(_work, jobs, chunksize=4):
            done += 1
            if status.startswith("error"):
                print(dst, status, file=sys.stderr)
            if done % 200 == 0:
                print(f"{done}/{len(jobs)}", file=sys.stderr)
    print("hotovo", file=sys.stderr)


if __name__ == "__main__":
    main()
