---
name: juju-troubleshoot-blocked
description: "Juju uygulamasının 'blocked' durumunda kalmasını, hook hatasını veya 'waiting' takılmasını teşhis edip çözmek gerektiğinde kullan."
---

## Purpose
`blocked` = charm bir şeyin yapılmasını bekliyor (relation eksik, config yanlış, manuel müdahale gerekli). `error` = hook exception. İkisi farklı müdahale gerektirir.

## Teşhis akışı

### 1. Neyin blocked olduğunu anla
```bash
juju status
# "Message" sütununa bak: "waiting for relation: grafana-source"
juju status --format=json | jq '.applications | to_entries[] | select(.value.status.current != "active") | {app: .key, status: .value.status}'
```

### 2. Hook hatası varsa
```bash
juju status | grep error
juju debug-log --include unit:<app>/0 --replay | grep -B5 "hook failed"
```

Hook retry:
```bash
juju resolve --no-retry <unit>   # hatayı kabul et, bir sonraki hook
juju resolve <unit>               # hook'u tekrar çalıştır
```

### 3. Relation eksikliği
```bash
juju status --relations  # hangi relation bekleniyor?
juju integrate <app1> <app2>
```

### 4. Config hatası
```bash
juju config <app>  # tüm config değerlerini gözden geçir
juju debug-log --include unit:<app>/0 --replay | grep -i "config\|error"
```

### 5. Resource eksikliği
```bash
juju resources <app>
# Rev 0 = Charmhub'dan henüz indirilmedi veya eksik
juju attach-resource <app> <resource>=<değer>
```

## Nükleer seçenek
```bash
juju remove-application <app> --force
juju deploy <app>  # sıfırdan kur
```

## Common mistakes
- `error` state'i `blocked` ile karıştırmak — resolve komutu yalnızca `error` için.
- Blocked mesajını okumadan config değiştirmeye çalışmak.

## References
- `skills/juju-debug-log`
- `skills/juju-ssh-debug`
- `skills/juju-relation-add-remove`
