---
name: test-mock-llm
description: "LLM API'yi mock'layan test fixture'ı; deterministik yanıt üretimi, token sayımı simülasyonu, streaming mock ve Sentinel agent testlerinde LLM bağımlılığını kaldırma"
---

## Purpose
Sentinel'in LLM tabanlı bileşenlerini (alert analiz agent, anomali açıklama) gerçek API çağrısı yapmadan test etmek; maliyetsiz, deterministik ve hızlı test suite sağlamak.

## Workflow

### Anthropic SDK Mock Fixture
```python
# tests/fixtures/llm_mock.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from anthropic.types import Message, ContentBlock, Usage

def make_mock_message(content: str, input_tokens: int = 100, output_tokens: int = 50) -> Message:
    return Message(
        id="msg_test_123",
        type="message",
        role="assistant",
        content=[ContentBlock(type="text", text=content)],
        model="claude-sonnet-4-6",
        stop_reason="end_turn",
        stop_sequence=None,
        usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens)
    )

@pytest.fixture
def mock_anthropic(monkeypatch):
    """Anthropic client'ı mock'la"""
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(
        return_value=make_mock_message("Test yanıtı")
    )
    
    monkeypatch.setattr("sentinel.llm.client._client", mock_client)
    return mock_client
```

### Senaryoya Göre Yanıt Yönlendirme
```python
@pytest.fixture
def mock_llm_with_scenarios():
    """Prompt içeriğine göre farklı yanıt dönen mock"""
    scenarios = {}
    
    async def smart_response(messages, **kwargs):
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            ""
        )
        
        # Keyword matching ile senaryo seç
        for keyword, response in scenarios.items():
            if keyword.lower() in last_user_msg.lower():
                return make_mock_message(response)
        
        # Default yanıt
        return make_mock_message("Bu alert muhtemelen ağ gecikmesinden kaynaklanıyor.")
    
    mock = AsyncMock(side_effect=smart_response)
    scenarios["memory"] = "Yüksek bellek kullanımı tespit edildi. OOM riski var."
    scenarios["cpu"] = "CPU spike görülüyor. Darboğaz analizi önerilir."
    scenarios["error rate"] = "Error rate artışı deployment ile örtüşüyor."
    
    with patch("sentinel.llm.client.create_message", mock):
        yield mock, scenarios
```

### Streaming Mock
```python
from anthropic.types import RawMessageStartEvent, RawContentBlockDeltaEvent

@pytest.fixture
def mock_streaming_llm():
    """Streaming yanıt mock'u"""
    async def fake_stream():
        chunks = ["Bu ", "alert ", "kritik ", "öneme ", "sahip."]
        for chunk in chunks:
            yield RawContentBlockDeltaEvent(
                type="content_block_delta",
                index=0,
                delta={"type": "text_delta", "text": chunk}
            )
    
    with patch("sentinel.llm.client.stream_message", return_value=fake_stream()):
        yield
```

### Agent Test Örneği
```python
# tests/unit/test_alert_analyzer.py
import pytest
from sentinel.agents.alert_analyzer import AlertAnalyzer

@pytest.mark.asyncio
async def test_analyze_memory_alert(mock_llm_with_scenarios):
    mock, scenarios = mock_llm_with_scenarios
    
    analyzer = AlertAnalyzer()
    result = await analyzer.analyze({
        "alertname": "HighMemoryUsage",
        "instance": "pod-1",
        "value": "95%"
    })
    
    assert "bellek" in result.explanation.lower()
    assert result.severity == "high"
    mock.assert_called_once()
    
    # LLM'e gönderilen prompt'u doğrula
    call_args = mock.call_args
    messages = call_args.kwargs.get("messages") or call_args.args[0]
    assert "HighMemoryUsage" in str(messages)

@pytest.mark.asyncio
async def test_llm_error_handled_gracefully(mock_anthropic):
    from anthropic import APIStatusError
    mock_anthropic.messages.create.side_effect = APIStatusError(
        "rate limit", response=MagicMock(status_code=429), body={}
    )
    
    analyzer = AlertAnalyzer()
    result = await analyzer.analyze({"alertname": "Test"})
    
    # Hata durumunda fallback yanıt döner
    assert result.explanation == "Analiz şu an mevcut değil"
    assert result.error is True
```

## Common mistakes
- `patch` path'i yanlış yazmak — `sentinel.llm.client._client` değil, modülün kendi namespace'ini patch'le
- Streaming'i mock'lamazken streaming test etmek — `AsyncGenerator` mock'u ayrı kurulum gerektiriyor
- Her test için ayrı fixture kurmak — `session` scope ile paylaşılan mock daha hızlı
- Token sayısını sıfır olarak mock'lamak — maliyet hesaplama testleri yanlış sonuç verir; gerçekçi değerler ekle

## References
- `skills/test-mock-http`
- `skills/test-golden-dataset`
