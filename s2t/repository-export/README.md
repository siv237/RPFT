# Выгрузка репозитория S2T

Файл `s2t.bundle.b64.txt` содержит полный Git bundle, закодированный в Base64. В него входит вся история проекта на момент создания выгрузки.

## Linux и macOS

```bash
base64 -d s2t.bundle.b64.txt > s2t.bundle
git clone s2t.bundle s2t
cd s2t
git branch -M main
git remote set-url origin https://github.com/siv237/s2t.git
git push -u origin main
```

## Windows PowerShell

```powershell
[IO.File]::WriteAllBytes("s2t.bundle", [Convert]::FromBase64String((Get-Content "s2t.bundle.b64.txt" -Raw)))
git clone s2t.bundle s2t
cd s2t
git branch -M main
git remote set-url origin https://github.com/siv237/s2t.git
git push -u origin main
```

После успешной отправки необходимо отозвать временный токен GitHub.