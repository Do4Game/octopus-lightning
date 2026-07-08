from octopus_lightning import LightningClient

def main():
    print("--- Octopus Lightning SDK Quickstart ---")
    
    # 1. Wpisz swój wygenerowany klucz API (np. octo_12345...)
    api_key = "octo_twój_klucz_z_panelu"
    
    # 2. Inicjalizacja lekkiego klienta
    client = LightningClient(api_key=api_key)
    
    # 3. Zapis kontekstu w chmurze
    print("[1] Zapisywanie danych do pamięci...")
    success = client.set("agent_status", "Gotowy do działania w roju!", ttl_seconds=3600)
    
    if success:
        print("✅ Zapis udany.")
    else:
        print("❌ Błąd zapisu. Sprawdź swój klucz API.")
        return
        
    # 4. Odczyt przez innego agenta
    print("[2] Pobieranie danych z pamięci...")
    data = client.get("agent_status")
    print(f"Dane odczytane w ułamku sekundy: {data}")

if __name__ == "__main__":
    main()
