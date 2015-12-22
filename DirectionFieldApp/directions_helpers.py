__author__ = 'benjamin'


def parser(fun_str):
    from sympy import sympify, lambdify
    from sympy.abc import x

    fun_sym = sympify(fun_str)
    fun_lam = lambdify(x, fun_sym)
    return fun_lam