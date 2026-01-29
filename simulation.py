from dataclasses import dataclass, field
from math import log10, sqrt

RHO_AIR = 1.225
MU_AIR = 1.81e-5

def colebrook_white(Re, rel_rough):
    if Re < 2300: return 64.0 / max(Re, 1e-9)
    inv_sqrt_f = -1.8 * log10((rel_rough / 3.7)**1.11 + 6.9 / max(Re, 1e-9))
    return (1.0 / inv_sqrt_f)**2

@dataclass
class EjectorModel:
    enabled: bool = True
    mu: float = 8.0
    zeta_mix: float = 0.3
    jet_power_w: float = 100.0
    eta_to_jet: float = 0.35

    def delta_p(self, Q_m3s: float) -> float:
        if not self.enabled or Q_m3s <= 1e-9: return 0.0
        m_flux_total = RHO_AIR * Q_m3s
        m_flux_primary = m_flux_total / (1.0 + self.mu)
        Vp = sqrt(max(0.0, (self.jet_power_w * self.eta_to_jet * 2.0) / (m_flux_primary + 1e-9)))
        Vt = Vp / (1.0 + self.mu)
        dp_gain = 0.25 * RHO_AIR * Vt**2
        dp_pen = self.zeta_mix * 0.5 * RHO_AIR * (Vp - Vt)**2
        return max(0.0, dp_gain - dp_pen)

@dataclass
class DuctNetwork:
    length_m: float = 10.0
    area_m2: float = 0.1
    K_minor: float = 1.5
    roughness_m: float = 1.5e-3

    def hydraulic_diameter(self) -> float:
        return self.area_m2**0.5

    def velocity(self, Q_m3s: float) -> float:
        return Q_m3s / max(self.area_m2, 1e-9)

    def friction_factor(self, Q_m3s: float) -> float:
        v = self.velocity(Q_m3s)
        Dh = self.hydraulic_diameter()
        Re = (RHO_AIR * max(v, 1e-9) * max(Dh, 1e-9)) / MU_AIR
        rel_rough = self.roughness_m / max(Dh, 1e-9)
        return colebrook_white(Re, rel_rough)

    def losses(self, Q_m3s: float) -> float:
        v = self.velocity(Q_m3s)
        Dh = self.hydraulic_diameter()
        f_var = self.friction_factor(Q_m3s)
        dp_fric = f_var * (self.length_m / max(Dh, 1e-9)) * 0.5 * RHO_AIR * v**2
        dp_minor = self.K_minor * 0.5 * RHO_AIR * v**2
        return dp_fric + dp_minor

@dataclass
class Config:
    ejector: EjectorModel = field(default_factory=EjectorModel)
    duct: DuctNetwork = field(default_factory=DuctNetwork)
