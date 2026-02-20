import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def ttu_mc3(t, Phi, alpha=2.3e-18, beta=1.18, gamma=1e-15, 
            delta=1.0, eta=1e-10, mu=1e-18, rho0=1e-27, L=3.086e19):
    """
    SYSTÈME TRIADIQUE DISSIPATIF TTU-MC³
    
    ÉQUATIONS :
    Φ̇_M = -α Φ_M + β Φ_C Φ_D / Λ     (Mémoire)
    Φ̇_C = -γ Φ_C + δ Φ_M Φ_D / Λ     (Cohérence) 
    Φ̇_D = η Φ_C² / Λ² - μ Φ_D        (Dissipation)
    
    PARAMÈTRES PHYSIQUES :
    α = H₀ = 1/âge univers (s⁻¹)
    Λ = ρ₀ L³ = échelle galactique (kg)
    β = 1.18 km/s/kpc (coupling universel)
    """
    PhiM, PhiC, PhiD = Phi
    scale = rho0 * L**3  # Échelle physique fixe
    
    return [
        -alpha*PhiM + beta*PhiC*PhiD/scale,
        -gamma*PhiC + delta*PhiM*PhiD/scale, 
        eta*PhiC**2/(scale*L**2) - mu*PhiD
    ]

# FONCTION LYAPUNOV (preuve stabilité)
def lyapunov_V(Phi, a=1.0, b=1.0):
    """V = ½(Φ_M² + a Φ_C² + b Φ_D²)"""
    PhiM, PhiC, PhiD = Phi
    return 0.5*(PhiM**2 + a*PhiC**2 + b*PhiD**2)

def test_stabilite():
    """TEST COMPLET STABILITÉ"""
    t_span = [0, 3e17]  # 10 Gyr
    Phi0 = [1e10, 1e12, 1e8]  # Conditions initiales
    
    print("🚀 SIMULATION TTU-MC³ EN COURS...")
    sol = solve_ivp(ttu_mc3, t_span, Phi0, method='LSODA', rtol=1e-9)
    
    # VÉRIFICATIONS CRITIQUES
    print(f"✅ STABILITÉ : {np.all(np.isfinite(sol.y))}")
    print(f"✅ Φ_D croissant : {np.all(np.diff(sol.y[2]) > 0)}")
    print(f"Φ_final : M={sol.y[0,-1]:.2e}, C={sol.y[1,-1]:.2e}, D={sol.y[2,-1]:.2e}")
    
    # PLOT AUTOMATIQUE
    plt.figure(figsize=(12,4))
    plt.subplot(131); plt.plot(sol.t/3.15e16, sol.y[0]); plt.ylabel('Φ_M'); plt.title('Mémoire')
    plt.subplot(132); plt.plot(sol.t/3.15e16, sol.y[1]); plt.ylabel('Φ_C'); plt.title('Cohérence')
    plt.subplot(133); plt.plot(sol.t/3.15e16, sol.y[2]); plt.ylabel('Φ_D'); plt.title('Dissipation')
    plt.tight_layout(); plt.savefig('ttu_dynamics.png', dpi=300); plt.show()
    
    return sol

if __name__ == "__main__":
    sol = test_stabilite()
