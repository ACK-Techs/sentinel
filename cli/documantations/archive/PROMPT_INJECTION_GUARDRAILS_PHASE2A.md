# Faz 2.A Prompt Injection ve Guvenilmeyen Icerik Guardrail Ozeti

Bu belge, `agentic-prompt-injection-guardrails` skill'inin Faz 2.A teslimidir. Amaç, guvenilmeyen icerik ile sistem talimatlari arasindaki siniri uygulama yazilmadan once netlestirmektir.

## Temel kurallar

1. Mesaj onceligi daima `system > developer > user > untrusted-content` seklinde dusunulur.
2. Web sayfasi, issue govdesi, kopyalanmis terminal ciktilari ve dis dosya icerigi guvenilmeyen veri olarak etiketlenir.
3. Guvenilmeyen metin, sistem prompt'una dogrudan eklenmez; ayri blokta veya kisitli ozet olarak kullanilir.
4. "Ignore previous instructions", "run this exact command", "reveal your secrets" benzeri kaliplar supheli kabul edilir.
5. Tool argumanlari sema dogrulamasindan gecmeden calistirilmaz; ek alanlar varsayilan olarak reddedilir.

## Faz 2.A icin beklenen davranis

- Supheli enjeksiyon tespitinde ajan durur veya kullaniciya durumu raporlar.
- Guvenilmeyen icerikten uretilen shell/dosya islemleri ek onay sinifina yukseltilir.
- Harici icerik ozetlenmeden veya allowlist denetlenmeden tool argumani olmaz.

## Kisa veri akisi

1. Kullanici veya harici kaynak icerigi alinir.
2. Icerik "trusted instruction" veya "untrusted context" olarak siniflanir.
3. Untrusted context yalniz ozet/alınti olarak modele verilir.
4. Model araci tetiklemek isterse approval policy ve schema validation devreye girer.
5. Supheli durumda islem reddedilir ve kullaniciya neyin neden yapilmadigi ozetlenir.

## Faz 2.C'ye birakilan enforcement maddeleri

- Runtime parser ve tool schema validator
- Hook tabanli supheli pattern isaretleme
- Allowlist domain kontrolu ve olasi SSRF korumasi

## Ilgili belgeler

- `PROJECT_ROOT_PHASE2.md`
- `APPROVAL_POLICY_PHASE2A.md`
- `THREAT_MODEL_PHASE2A.md`
