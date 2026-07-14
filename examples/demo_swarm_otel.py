import asyncio
import httpx
import json
import time
from datetime import datetime

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject, extract

# Konfiguracja OTel do lokalnego Jaegera
resource = Resource.create({"service.name": "octopus-lightning-swarm"})
provider = TracerProvider(resource=resource)
# Jaeger nasłuchuje OTLP HTTP na porcie 4318
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("swarm.tracer")

API_URL_BASE = "https://api.octopusclass.pl/v1/lightning/swarm-demo"
API_KEY = "octo_8851c76eab9ba9f7076c897e78e6c401"

C_BLUE = "\033[94m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_RESET = "\033[0m"

async def ai_agent_tts_subscriber():
    print(f"{C_BLUE}[AI Agent 2 - TTS]{C_RESET} Initializing... Waiting for LLM vectors (Zero-Polling active).")
    headers = {
        "x-api-key": API_KEY,
        "Accept": "text/event-stream"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("GET", f"{API_URL_BASE}/subscribe", headers=headers, timeout=None) as response:
                if response.status_code != 200:
                    print(f"{C_RED}[!] Subscription error: {response.status_code}{C_RESET}")
                    return
                    
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        event = json.loads(data_str)
                        if event.get("event") == "subscribed":
                            print(f"{C_BLUE}[AI Agent 2 - TTS]{C_RESET} Listening on IPC channel 'swarm-demo'.")
                        elif event.get("event") == "updated":
                            receive_time = time.time()
                            payload = event.get('value', {})
                            if isinstance(payload, str):
                                payload = json.loads(payload)
                            
                            chunk_id = payload.get('chunk_id', 'unknown')
                            send_time = payload.get('timestamp', receive_time)
                            latency_ms = (receive_time - send_time) * 1000
                            
                            # Ekstrakcja kontekstu trace'a z przesłanego JSONa
                            trace_ctx = payload.get("trace_ctx", {})
                            ctx = extract(trace_ctx)
                            
                            with tracer.start_as_current_span(f"TTS_Receive_Chunk_{chunk_id}", context=ctx) as span:
                                span.set_attribute("agent", "TTS")
                                span.set_attribute("chunk_id", chunk_id)
                                span.set_attribute("latency_ms", latency_ms)
                                
                                print(f"{C_GREEN} ⚡ [AI Agent 2 - TTS] INSTANT PUSH RECEIVED (Chunk {chunk_id}) -> Latency: {latency_ms:.2f} ms{C_RESET}")
                            
        except Exception as e:
            print(f"Connection error: {e}")

async def ai_agent_llm_publisher():
    await asyncio.sleep(2)
    print(f"\n{C_YELLOW}[AI Agent 1 - LLM]{C_RESET} Reasoning logic... Initiating continuous lossless transfer.")
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        for i in range(1, 11):
            await asyncio.sleep(0.5)
            
            with tracer.start_as_current_span(f"LLM_Generate_And_Push_Chunk_{i}") as span:
                span.set_attribute("agent", "LLM")
                span.set_attribute("chunk_id", i)
                span.set_attribute("vector_size_bytes", 1024)
                
                # Wstrzyknięcie aktualnego trace_id do payloadu (Propagacja Distributed Tracing)
                trace_ctx = {}
                inject(trace_ctx)
                
                payload = {
                    "chunk_id": i,
                    "vector_data": "0x" + "F" * 1024,
                    "timestamp": time.time(),
                    "trace_ctx": trace_ctx
                }
                
                print(f"{C_YELLOW}[AI Agent 1 - LLM]{C_RESET} Pushing continuous vector [Chunk {i}] (size: 1024 bytes)...")
                response = await client.post(API_URL_BASE, headers=headers, json={"value": payload})
                
                if response.status_code != 200:
                     print(f"{C_RED}[!] Push error: {response.status_code}{C_RESET}")
                     span.set_attribute("error", True)

async def main():
    print("="*60)
    print("OCTOPUS LIGHTNING - OTel OBSERVABILITY DEMO")
    print("="*60)
    
    await asyncio.gather(
        ai_agent_tts_subscriber(),
        ai_agent_llm_publisher()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest completed.")
    finally:
        # Wymuś zrzut trace'ów przed zamknięciem
        provider.shutdown()
