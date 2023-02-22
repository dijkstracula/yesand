import logging
import os
import sys
import z3

from pathlib import Path
from typing import Tuple

from ivy import ivy_art as iart
from ivy import ivy_compiler as ic
from ivy import ivy_isolate as iiso
from ivy import ivy_logic_utils as ilu
from ivy import ivy_module as imod
from ivy import ivy_solver as islv

from . import bmc

def compile_progtext(path: Path) -> iart.AnalysisGraph:
    print(f"Compiling {path}")
    cwd = os.getcwd()
    os.chdir(path.parent)
    with open(path) as f:
        ic.ivy_load_file(f, create_isolate=False)
        iiso.create_isolate('this')
    os.chdir(cwd)
    return ic.ivy_new()

def ordered_model(s: z3.Solver) -> list[Tuple[str, z3.FuncDeclRef]]:
    m = s.model()
    d = []
    for k in m:
        d.append((str(k), m[k]))
    return sorted(d, key=lambda p: p[0])

def handle_isolate(path: Path):
    with imod.Module() as im:
        ag = compile_progtext(path)
        clauses = bmc.unroll(ag, 10)

        # 1. extract a counterexample
        s = z3.Solver()
        s.set(unsat_core=True)
        s.add(islv.clauses_to_z3(clauses))

        s.push()
        neg_conjs = ilu.dual_clauses(ilu.and_clauses(*im.conjs))
        s.add(islv.clauses_to_z3(neg_conjs))

        assert(s.check() == z3.sat)
        m = ordered_model(s)
