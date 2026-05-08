---
name: microk8s-addon-gpu
description: "MicroK8s kümesinde NVIDIA GPU'yu Kubernetes pod'larına açmak için gpu addon'unu etkinleştirmek, nvidia device plugin kurulumunu doğrulamak ve GPU talep eden pod manifest'i yazmak gerektiğinde kullan."
---

## Purpose
Makine öğrenmesi iş yükleri, LLM çıkarımı veya GPU hızlandırmalı işlemler için NVIDIA device plugin'ini MicroK8s'e entegre etmek.

## Ön koşullar
- NVIDIA sürücüsü kurulu ve `nvidia-smi` çalışıyor olmalı.
- CUDA toolkit isteğe bağlı (container içinde ayrıca yönetilir).
- `nvidia-container-toolkit` kurulu olmalı.

```bash
# NVIDIA container toolkit kurulumu (Ubuntu)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
```

## Addon etkinleştirme
```bash
microk8s enable gpu
microk8s kubectl get pods -n gpu-operator-resources
```

## GPU talep eden pod
```yaml
spec:
  containers:
    - name: gpu-app
      image: nvidia/cuda:12.0-base
      resources:
        limits:
          nvidia.com/gpu: 1
```

## Doğrulama
```bash
microk8s kubectl run gpu-test --image=nvidia/cuda:12.0-base \
  --restart=Never --limits=nvidia.com/gpu=1 \
  -- nvidia-smi
microk8s kubectl logs gpu-test
```

## Common mistakes
- `nvidia-smi` host'ta çalışıyor ama `nvidia-container-toolkit` kurulmamış; containerd GPU'yu göremez.
- Birden fazla GPU'yu `nvidia.com/gpu: 2` ile talep edip yalnızca 1 GPU olan node'a schedule etmeye çalışmak.
- `gpu-operator` pod'larının CrashLoop durumunu kontrol etmeden GPU testi yapmak.

## References
- `skills/microk8s-addons-overview`
- `skills/llm-local-gpu-memory`
- `skills/llm-local-vllm-setup`
