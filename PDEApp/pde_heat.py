from __future__ import division
import scipy.sparse as sp
import scipy.sparse.linalg as lin


def do_explicit_step(ux, u0, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j) with spatial meshwidth h and temporal meshwidth k for
    the 1D heat equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.894 ff."
    Stability criterion:
        r  = k / h**2 <= 1
    :param u0: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u1: solution u(x,t=t+k)
    """
    n = u0.shape[0]
    r = k / (h ** 2)
    iteration_matrix = (r * sp.eye(n, n, -1) - 2 * r * sp.eye(n, n) + r * sp.eye(n, n, 1)).tocsr()
    iteration_matrix[0, 0] = 0  # enforcing dirichlet BC -> no change!
    iteration_matrix[0, 1] = 0
    iteration_matrix[n - 1, n - 1] = 0
    iteration_matrix[n - 1, n - 2] = 0
    iteration_matrix += sp.eye(n, n)
    u1 = iteration_matrix.dot(u0)
    return u1


def do_implicit_step(ux, u0, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j) with spatial meshwidth h and temporal meshwidth k for
    the 1D heat equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.894 ff."
    Since we are using an implicit time stepping scheme, there is no stability criterion. We use
    scipy.linalg.solve_banded for solving the implicit equation. Theferfore we need to convert our implicit equation
    into ordered diagonal format:
        u1 = u0 + A_h * u1
    ->  (Id - A_h) * u1 = u0
    This is a system of linear equations: A * x = b with
        A = Id - A_h
        x = u1
        b = u0

    :param u0: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u1: solution u(x,t=t+k)
    """
    n = u0.shape[0]
    r = k / (h ** 2)
    iteration_matrix = (r * sp.eye(n, n, -1) - 2 * r * sp.eye(n, n) + r * sp.eye(n, n, 1)).tocsr()
    iteration_matrix[0, 0] = 0  # enforcing dirichlet BC -> no change!
    iteration_matrix[0, 1] = 0
    iteration_matrix[n - 1, n - 1] = 0
    iteration_matrix[n - 1, n - 2] = 0
    iteration_matrix = -iteration_matrix
    iteration_matrix += sp.eye(n, n)
    u1 = lin.spsolve(iteration_matrix, u0)
    return u1
