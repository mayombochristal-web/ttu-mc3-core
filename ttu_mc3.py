# ttu_mc3.py — Copiez dans votre repo
import numpy as np
from scipy.integrate import solve_ivp

def ttu_mc3(t, Phi, alpha=2.3e-18, beta=1.18, gamma=1e-15, 
            delta=1.0, eta=1e-10, mu=1e-18, rho0=1e-27, L=3.086e19):
    """Système triadique dissipatif TTU-MC³"""
    PhiM, PhiC, PhiD = Phi
    scale = rho0 * L**3
    return [
        -alpha*PhiM + beta*PhiC*PhiD/scale,
        -gamma*PhiC + delta*PhiM*PhiD/scale,
        eta*PhiC**2/(scale*L**2) - mu*PhiD
    ]

# Test stabilité
sol = solve_ivp(ttu_mc3, [0, 3e17], [1e10, 1e12, 1e8], rtol=1e-9)
print("Stabilité:", np.all(np.isfinite(sol.y)))
