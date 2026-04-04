# Faz 2.C Oturum, Trajectory ve Gecmis Politikasi

Bu belge Faz 2.C icin oturum kaliciligi, trajectory kaydi ve history compaction davranisini sabitler.

## Oturum kaliciligi

- Varsayilan yol: `session.directory`
- Format: oturum basi bir JSON dosyasi
- Her dosyada `session_id`, `profile`, `provider`, `created_at`, `messages` tutulur
- Profil veya provider degisirse mevcut history uyumsuz sayilir ve yeni oturum onerilir

## Trajectory

- Varsayilan kapali: `session.trajectory_enabled = false`
- Etkin oldugunda JSONL biciminde `trajectory_directory` altina yazilir
- E-posta ve token benzeri kaliplar regex ile redakte edilir
- Secret, API key ve bearer degerleri duz metin olarak tutulmaz

## History compaction

- Heuristik context esigi asildiginda ilk kullanici hedefi + son N mesaj korunur
- Araya `Eski mesajlar ... kirpildi` notu eklenir
- Bu ilk surumde ek ozet LLM cagrisi yoktur; deterministic truncation kullanilir

## Hook ve approval sirasi

1. Tool parse ve schema validation
2. Approval gate
3. Pre-tool hook
4. Tool execute
5. Post-tool hook

Post hook hatasi varsayilan olarak sonucu geri almaz; config'e gore warn/block davranisi kullanilir.
