from ivy import ivy_actions as ia
from ivy import ivy_art as iart
from ivy import ivy_bmc as ibmc
from ivy import logic as lg
from ivy import ivy_logic as il
from ivy import ivy_logic_utils as ilu
from ivy import ivy_module as im
from ivy import ivy_solver as islv

def unroll(ag: iart.AnalysisGraph, n: int) -> ilu.Clauses:
    """ This is essentially ivy.ivy_bmc.check_isolate() but without actually
    passing any of the intermediary transitions to the solver."""
    # TODO: we need to fix the postcondition not just for the final state
    # but for all intermediary ones, too.  Or something.

    conj = ilu.and_clauses(*im.module.conjs)

    used_names = frozenset(x.name for x in il.sig.symbols.values())
    def witness(v):
        c = lg.Const('@' + v.name, v.sort)
        assert c.name not in used_names
        return c
    clauses = ilu.dual_clauses(conj, witness)

    with ag.context as ac:
        ag.add_initial_state(ag.init_cond)
        post = ag.states[0]
    if 'initialize' in im.module.actions:
        init_action = im.module.actions['initialize']
        post = ag.execute(init_action, None, None, 'initialize')

    step_actions = ia.env_action(None)
    for i in range(n):
        post = ag.execute(step_actions)
        history = ag.get_history(post)
        clauses = ilu.and_clauses(history.post, im.module.background_theory())

    history = ag.get_history(post)
    return ilu.and_clauses(history.post, im.module.background_theory())

