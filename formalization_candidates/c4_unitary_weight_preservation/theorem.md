# Сохранение характерных весов при C4-эквивариантном унитарном шаге

> Status: spec-frozen

Пусть `U4` — комплексный оператор на двумерном пространстве,
`U4^2 = -I`, а `P_plus`, `P_minus` — его спектральные проекторы для
собственных значений `+i` и `-i`. Для нормированного `Psi` положим

```text
w_plus(Psi)  = <Psi, P_plus Psi>
w_minus(Psi) = <Psi, P_minus Psi>
D_chi(Psi)   = 1 - |<Psi, U4 Psi>|^2.
```

Требуется доказать:

```text
w_plus + w_minus = 1,
D_chi = 4 w_plus w_minus >= 0,
D_chi = 0 <-> U4 Psi = i Psi or U4 Psi = -i Psi.
```

Кроме того, если `T` унитарен и `T U4 = U4 T`, то

```text
w_plus(T Psi)  = w_plus(Psi),
w_minus(T Psi) = w_minus(Psi),
D_chi(T Psi)   = D_chi(Psi).
```

Следовательно, такой шаг не может перевести состояние с обоими ненулевыми
весами в чистый сектор `+i` или `-i`.
