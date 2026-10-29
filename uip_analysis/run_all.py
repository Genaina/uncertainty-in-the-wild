"""Executa RQ1-RQ4 em sequencia. Uso: python run_all.py  (saidas em ./output)"""
import sys, io, contextlib
import rq1, rq2, rq3, rq4
from common import load_raw, OUT

if __name__ == "__main__":
    raw = load_raw()
    buf = io.StringIO()
    class Tee(io.TextIOBase):
        def write(self, s):
            sys.__stdout__.write(s); buf.write(s); return len(s)
    with contextlib.redirect_stdout(Tee()):
        for m in (rq1, rq2, rq3, rq4):
            m.run(raw)
    (OUT / "full_report.txt").write_text(buf.getvalue(), encoding="utf-8")
