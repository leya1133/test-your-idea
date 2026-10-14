import sys
import os

# Configure stdout encoding to UTF-8 to prevent Windows cp1254 encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import uvicorn

def main():
    print("=================================================================")
    print("   [TSI] - TEST YOUR IDEA (Cok Ajanli Fikir Test Etme Sistemi)   ")
    print("=================================================================")
    print("Web Sunucusu Baslatiliyor: http://127.0.0.1:8000")
    print("Tarayicinizda http://127.0.0.1:8000 adresini acarak arayuzu kullanabilirsiniz.")
    print("=================================================================\n")
    
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
