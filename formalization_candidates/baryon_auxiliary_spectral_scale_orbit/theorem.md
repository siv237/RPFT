# Масштабная орбита однополюсного вспомогательного родителя

> Status: spec-frozen

Требуется доказать, что подстановка стационарной точки даёт

```text
parent(phiStar,J) = -couplingSq*J^2/(2*(z+massSq)).
```

Если `couplingSq=lambda*massSq`, то статический коэффициент равен `lambda`.
Для любого `q>0` преобразование

```text
massSq     -> q*massSq,
couplingSq -> q*couplingSq
```

сохраняет это отношение и `scaledForm(q,massSq,0)=1`, но

```text
d/dz scaledForm(q,massSq,z) at z=0 = -1/(q*massSq).
```

В частности, при `z=massSq` формы для `q=1` и `q=2` равны `1/2` и `2/3`.
Следовательно, статическое сопоставление не выбирает спектральную массу.