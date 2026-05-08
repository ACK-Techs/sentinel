---
name: juju-secrets-management
description: "Juju secrets mekanizmasıyla charm'lara güvenli credential dağıtmak, secret oluşturmak/güncellemek/erişim vermek ve secret'ın unit tarafından tüketildiğini doğrulamak gerektiğinde kullan."
---

## Purpose
Juju 3.x'ten itibaren built-in secret yönetimi ile config üzerinden plaintext credential geçirme ihtiyacı ortadan kalkmıştır. Secret'lar model düzeyinde saklanır ve yalnızca yetkili uygulamalara erişim verilir.

## Secret oluşturma
```bash
# Basit key-value:
juju add-secret db-credentials username=admin password=gizli123

# Dosyadan:
juju add-secret tls-cert --file=cert.pem
```

## Secret listeleme ve okuma
```bash
juju secrets
juju show-secret db-credentials --reveal
```

## Secret güncelleme
```bash
juju update-secret db-credentials password=yeni-gizli
```

## Charm'a erişim verme
```bash
juju grant-secret db-credentials myapp
# Artık myapp içinde secret-get ile okunabilir
```

## Charm içinde tüketim (charm kodu)
```python
from ops import SecretNotFoundError
secret = self.model.get_secret(label="db-credentials")
content = secret.get_content(refresh=True)
password = content["password"]
```

## User-defined secret vs charm-owned secret
- `juju add-secret`: kullanıcı tarafından oluşturulan, charm'a açılan.
- Charm-owned: charm kod içinde `add_secret()` ile oluşturur, lifecycle charm'a aittir.

## Common mistakes
- `juju config` ile plaintext şifre geçirmeye devam etmek — `juju secrets` daha güvenli.
- Erişim izni vermeden `secret-get` çağrısı yapmak — "not found" hatası.
- Secret label ile secret ID'yi karıştırmak; her ikisi de erişimde kullanılabilir.

## References
- `skills/juju-config-management`
- `skills/juju-charm-deploy`
- `skills/k8s-sec-secrets-management`
