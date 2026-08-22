# Литература по носителю спина три и конечным стрелкам

> Status: working
> Type: source
> Updated: 2026-08-20

## Summary

Литература фиксирует две независимые части нового гейта: каноническое
выделение неприводимых представлений коэффициентами Клебша--Гордана и
описание внедиагональных стрелок конечными спектральными цепями. Она
поддерживает носитель `V3` внутри `Hom(V1,V2)`, но не выбирает
односторонний угол кривизны проекта.

## Sources

- I. Mäkinen, `arXiv:1910.06821`: ортогональность и полнота
  коэффициентов Клебша--Гордана и сплетающих тензоров `SU(2)`.
- T. Krajewski, `arXiv:hep-th/9701081`: конечные спектральные тройки и
  внедиагональные блоки конечного оператора.
- M. Marcolli, W. D. van Suijlekom, `arXiv:1301.3480`: сети
  спектральных троек, колчаны и дискретные операторы Дирака.
- J. Berger, Y. Grossman, `arXiv:0910.4392`, и Y. Abe et al.,
  `arXiv:2607.12366`: семимерное представление спина три как полностью
  симметричный бесследовый тензор и нарушение `SO(3) -> A4`.

## Project Consequence

Разложение `V2 tensor V1=V1+V2+V3` даёт единственный канонический
семимерный подноситель. Однако литература о конечных стрелках требует
учитывать оба диагональных угла квадрата самосопряжённого оператора.
Именно второй угол обнаруживает двумерное коядро, поэтому проект не может
оставить только удобный триплетный квадрат без дополнительного
родительского вывода.

## Links

- [[version6-bosonic-defect-minimal-spin-three-carrier-embedding-gate]]
- [[tetrahedratic-composite-order-literature-2026]]
- [[so3-a4-spin3-parent-action-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_minimal_spin_three_carrier_embedding_gate.tex`
- `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex`
- `s2t/gates/version5_graded_correspondence_superconnection_gate.tex`