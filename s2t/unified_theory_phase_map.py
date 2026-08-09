import numpy as np
import matplotlib.pyplot as plt


class UnifiedTheoryMapper:
    """
    Вычислительный алгоритм из Трактата об устройстве мира.
    Переводит сырые чувствительности теорий в инварианты и строит фазовую карту.
    """

    def __init__(self, eta=1.0, zeta=1.0, epsilon=1e-3):
        self.eta = eta
        self.zeta = zeta
        self.epsilon = epsilon

    def compute_invariants(self, s_b, s_phi, s_int):
        s_cross = 0.1 * min(s_phi, s_int)
        total_s = s_b + s_phi + s_int + s_cross + self.epsilon

        w_b = s_b / total_s
        w_phi = s_phi / total_s
        w_int = s_int / total_s
        w_cross = s_cross / total_s

        xi = (w_phi + w_int + self.eta * w_cross) / (w_b + self.epsilon)
        upsilon = (w_phi - w_int) / (w_phi + w_int + self.zeta * w_cross + self.epsilon)
        return np.log10(xi), upsilon


physics_models = {
    "ОТО (Макро-гравитация)": [100.0, 0.1, 0.0],
    "Эффект Ааронова-Бома": [0.1, 90.0, 0.1],
    "Спектр масс адронов (КХД)": [0.1, 0.1, 100.0],
    "Дробный квантовый эффект Холла": [2.0, 80.0, 60.0],
    "Термодинамика Черных Дыр": [80.0, 5.0, 15.0],
    "Осцилляции нейтрино": [0.0, 10.0, 90.0],
    "Киральная аномалия": [5.0, 50.0, 50.0],
}


def main():
    mapper = UnifiedTheoryMapper()
    results = {
        name: mapper.compute_invariants(*sensitivities)
        for name, sensitivities in physics_models.items()
    }

    plt.figure(figsize=(12, 8))

    plt.axvspan(-2, 0, color="lightgray", alpha=0.3, label="Каркасная область ($P_{core}$)")
    plt.axhspan(0.5, 1.0, xmin=0.4, color="lightblue", alpha=0.3, label="Фазовая область ($P_{\\Phi}$)")
    plt.axhspan(-1.0, -0.5, xmin=0.4, color="lightcoral", alpha=0.3, label="Внутренняя область ($P_{int}$)")
    plt.axhspan(-0.3, 0.3, xmin=0.4, color="plum", alpha=0.3, label="Смешанный режим ($P_{mix}$)")

    colors = plt.cm.jet(np.linspace(0, 1, len(results)))
    for (name, (xi, upsilon)), color in zip(results.items(), colors):
        plt.scatter(xi, upsilon, s=150, color=color, edgecolors="black", zorder=5)
        plt.text(xi + 0.05, upsilon + 0.02, name, fontsize=10, fontweight="bold")

    plt.axvline(0, color="black", linestyle="--")
    plt.axhline(0, color="black", linestyle="--")
    plt.xlim(-1.5, 3.5)
    plt.ylim(-1.1, 1.1)

    plt.title("Фазовый портрет структурных режимов (по Трактату)", fontsize=16)
    plt.xlabel("Инвариант $\\log_{10}(\\Xi)$: уход от геометрического каркаса $\\rightarrow$", fontsize=12)
    plt.ylabel("Инвариант $\\Upsilon$: (внутренняя $\\leftarrow$ смешение $\\rightarrow$ фазовая)", fontsize=12)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig("fig_unified_phase_portrait.png", dpi=220, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()