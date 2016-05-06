# Parametrization of a curve w.r.t arc length

App, that visualizes the difference of a curve with arbitrary vs. arc length parametrization. This can be visualized through plotting of the tangent vector.

## Implementation outline:

we want to get the parametrization gamma(s^-1(t)), where 

s(t)=\int_0^t ||dgamma(tau)|| dtau

for the computation of s^-1(t) we have to do the following:

- implement a function that computes s(t) via quadrature.
- compute s^-1(t) via root finding routine.

Is this problem really relevant enough to justify the work? Basically one could also just fake this property by normalizing the vector, the good thing about parametrization w.r.t arc length is, that the visual result does not change, but the analytical expression and the parameter space.