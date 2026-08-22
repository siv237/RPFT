# Version VI: родительская масса и портал бозонного дефекта

> Status: working
> Type: question
> Updated: 2026-08-20

## Summary

Текущий родитель фиксирует безразмерный профиль дефекта, но сохраняет две
независимые единицы — длины и энергии. Поэтому абсолютные масса и радиус не
выводятся. В функционале `M300` поле Хиггса связано с общей амплитудой
семейного моста, но коэффициент портала `Tr(Q^2)H†H` точно равен нулю.

## Results

- допустима лоренц-ковариантная форма с `Tr(D_mu Q D^mu Q)`, `Tr(F^2)` и
  потенциалом, но её общая временная нормировка не выведена;
- для пробного профиля получены `r*=0.8301754154...` и безразмерная энергия
  `60.7698954459...`;
- преобразование `c_D=E0/L0`, `c_F=E0 L0`, `c_V=E0/L0^3` оставляет
  безразмерное уравнение неизменным;
- физические величины равны `R*=L0 r*` и `M*=E0 m*`, а `L0,E0` проект не
  фиксирует;
- блок `Tr(T R-|H|^2 I)^2` раскрывается как
  `T^2 Tr(R^2)-2T|H|^2+3|H|^4`;
- смешанный коэффициент формы `Q=R-I/3` и поля Хиггса равен нулю, тогда как
  радиальная связь имеет смешанную производную `-2`.

## Boundary

Разрешённый симметрией портал не является частью минимального родителя.
Выбирать масштаб или портал по феноменологии запрещено. Следующая проверка
должна исследовать полные уравнения Эйлера--Лагранжа и безразмерную
устойчивость независимо от абсолютных единиц.

## Next Result

Эта проверка выполнена в
[[version6-bosonic-defect-full-euler-lagrange-stability-gate]]. Полная
радиальная краевая задача имеет решение с энергией `54.5482543023...`, а
радиальный гессиан не имеет отрицательных мод в семи проверенных точках.
Открытой осталась нерадиальная устойчивость пятикомпонентного поля.

## Links

- [[version6-bosonic-defect-collective-quantization-gate]]
- [[version6-bosonic-defect-full-euler-lagrange-stability-gate]]
- [[bosonic-defect-parent-scale-and-portal-literature-2026]]
- [[version6-bosonic-defect-field-identification-gate]]
- [[version6-gauged-projective-spin-cover-parent-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_mass_portal_parent_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_mass_portal_parent_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_mass_portal_parent_gate_results.json`