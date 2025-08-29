"""
Configurações da API para o sistema PlayerStats

Este arquivo permite configurar facilmente os parâmetros da API
sem modificar o código principal.

IMPORTANTE: 
- Crie um arquivo .env na raiz do projeto com suas chaves de API
- Use o arquivo env_template.txt como base
- Nunca committe chaves de API no código
"""

# Carrega variáveis de ambiente do arquivo .env
import os
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)  # Carrega .env se python-dotenv estiver disponível
except ImportError:
    # Se python-dotenv não estiver disponível, usa apenas os.getenv
    pass

# ======= ESCOLHA DA API =======
# A API ativa é definida pela variável de ambiente ACTIVE_API no arquivo .env
# Valores possíveis: "deepseek", "openai", "claude"
ACTIVE_API = os.getenv("ACTIVE_API", "deepseek")  # Padrão: deepseek
# ===============================================

# ======= CONFIGURAÇÕES DAS APIS =======
DEEPSEEK_CONFIG = {
    "url": "https://api.deepseek.com/v1/chat/completions",
    "key": os.getenv("DEEPSEEK_API_KEY", ""),  # Carregada do .env
    "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    "timeout": int(os.getenv("API_TIMEOUT", "300")),
    "max_tokens": int(os.getenv("API_MAX_TOKENS", "4000")),
    "temperature": float(os.getenv("API_TEMPERATURE", "0.7"))
}

OPENAI_CONFIG = {
    "url": "https://api.openai.com/v1/chat/completions",
    "key": os.getenv("OPENAI_API_KEY", ""),  # Carregada do .env
    "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
    "timeout": int(os.getenv("API_TIMEOUT", "300")),
    "max_completion_tokens": int(os.getenv("API_MAX_TOKENS", "4000")),
    "temperature": float(os.getenv("API_TEMPERATURE", "0.7"))  # GPT-5 ignora este valor (usa sempre 1.0)
}

CLAUDE_CONFIG = {
    "url": "https://api.anthropic.com/v1/messages",
    "key": os.getenv("CLAUDE_API_KEY", ""),  # Carregada do .env
    "model": os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219"),
    "timeout": int(os.getenv("API_TIMEOUT", "300")),
    "max_tokens": int(os.getenv("API_MAX_TOKENS", "4000")),
    "temperature": float(os.getenv("API_TEMPERATURE", "0.7"))
}

# Configuração ativa baseada na escolha
API_CONFIGS = {
    "deepseek": DEEPSEEK_CONFIG,
    "openai": OPENAI_CONFIG,
    "claude": CLAUDE_CONFIG
}

# Normaliza ACTIVE_API caso esteja inválido (ex.: typos no .env)
if ACTIVE_API not in API_CONFIGS:
    print(f"⚠️ ACTIVE_API inválido no .env: '{ACTIVE_API}'. Usando 'deepseek' como padrão.")
    ACTIVE_API = "deepseek"

# Configuração atual ativa
API_CONFIG = API_CONFIGS[ACTIVE_API].copy()

# ======= MODELOS DISPONÍVEIS POR API =======
AVAILABLE_MODELS = {
    "deepseek": {
        "deepseek-chat": "Modelo de chat geral",
        "deepseek-coder": "Modelo especializado em código",
        "deepseek-math": "Modelo especializado em matemática"
    },
    "openai": {
        "gpt-5": "GPT-5 (mais recente)",
        "gpt-4o": "GPT-4o (mais barato)",
        "gpt-4": "GPT-4 (modelo anterior)",
        "gpt-3.5-turbo": "GPT-3.5 Turbo (mais rápido e barato)",
        "gpt-4o-mini": "GPT-4o Mini (mais barato)"
    },
    "claude": {
        "claude-3-7-sonnet-20250219": "Claude 3.7 Sonnet (mais recente)",
        "claude-sonnet-4-20250514": "Claude 4 Sonnet",
        "claude-3-5-haiku-20241022": "Claude 3 Haiku (mais rápido)",
        "claude-opus-4-20250514": "Claude 4 Opus (mais potente)"
    }
}

# ======= FUNÇÕES DE CONFIGURAÇÃO =======
def get_api_config():
    """Retorna a configuração atual da API"""
    return API_CONFIG.copy()

def set_active_api(api_name):
    """Muda a API ativa"""
    global API_CONFIG, ACTIVE_API
    if api_name in API_CONFIGS:
        ACTIVE_API = api_name
        API_CONFIG = API_CONFIGS[api_name].copy()
        print(f"✅ API alterada para: {api_name}")
        return True
    else:
        print(f"❌ API '{api_name}' não disponível. Opções: {list(API_CONFIGS.keys())}")
        return False

def get_active_api():
    """Retorna o nome da API ativa"""
    return ACTIVE_API

def get_available_apis():
    """Retorna as APIs disponíveis"""
    return list(API_CONFIGS.keys())

def get_available_models(api_name=None):
    """Retorna os modelos disponíveis para a API especificada ou ativa"""
    if api_name is None:
        api_name = ACTIVE_API
    return AVAILABLE_MODELS.get(api_name, {})

def set_model(model_name):
    """Altera o modelo da API ativa"""
    global API_CONFIG
    available = get_available_models()
    if model_name in available:
        API_CONFIG["model"] = model_name
        print(f"✅ Modelo alterado para: {model_name}")
        return True
    else:
        print(f"❌ Modelo '{model_name}' não disponível para {ACTIVE_API}")
        print(f"   Opções: {list(available.keys())}")
        return False

def validate_api_key(api_key):
    """Valida se a API key tem formato correto"""
    if not api_key or len(api_key) < 20:
        return False
    return True

def check_api_keys_loaded():
    """Verifica se as chaves de API foram carregadas corretamente"""
    print("\n=== VERIFICAÇÃO DE CHAVES DE API ===")
    
    # Verifica chave ativa
    active_config = API_CONFIGS[ACTIVE_API]
    active_key = active_config["key"]
    
    if validate_api_key(active_key):
        print(f"✅ Chave da API ativa ({ACTIVE_API}): carregada corretamente")
    else:
        print(f"❌ Chave da API ativa ({ACTIVE_API}): NÃO carregada ou inválida")
        print("💡 Verifique se o arquivo .env existe e contém a chave correta")
    
    # Verifica todas as chaves
    for api_name, config in API_CONFIGS.items():
        key = config["key"]
        status = "✅" if validate_api_key(key) else "❌"
        print(f"   {status} {api_name.upper()}: {'válida' if validate_api_key(key) else 'inválida/vazia'}")
    
    # Instruções se necessário
    if not validate_api_key(active_key):
        print(f"\n📋 INSTRUÇÕES:")
        print(f"1. Copie env_template.txt para .env")
        print(f"2. Edite .env e adicione suas chaves reais")
        print(f"3. Reinicie o programa")

def load_from_environment():
    """Carrega configurações de variáveis de ambiente (legacy - agora é automático)"""
    print("⚠️ Função load_from_environment() é desnecessária - variáveis são carregadas automaticamente")
    print("✅ Configurações já carregadas do arquivo .env")
    
    # Verifica se as chaves foram carregadas
    check_api_keys_loaded()

def show_config():
    """Mostra a configuração atual"""
    print("=== CONFIGURAÇÃO ATUAL DA API ===")
    print(f"🔗 API Ativa: {ACTIVE_API.upper()}")
    print(f"🌐 URL: {API_CONFIG['url']}")
    print(f"🔑 API Key: {API_CONFIG['key'][:10]}...{API_CONFIG['key'][-4:]}")
    print(f"🤖 Modelo: {API_CONFIG['model']}")
    print(f"⏱️ Timeout: {API_CONFIG['timeout']}s")
    
    # Mostra o parâmetro correto baseado na API
    if ACTIVE_API == "openai":
        tokens_value = API_CONFIG.get('max_completion_tokens', 'N/A')
        print(f"📝 Max Completion Tokens: {tokens_value}")
    else:
        tokens_value = API_CONFIG.get('max_tokens', 'N/A')
        print(f"📝 Max Tokens: {tokens_value}")
    
    print(f"🌡️ Temperature: {API_CONFIG.get('temperature', 'N/A')}")
    
    print(f"\n📋 Modelos disponíveis para {ACTIVE_API}:")
    for model, desc in get_available_models().items():
        status = "✅" if model == API_CONFIG['model'] else "  "
        print(f"   {status} {model}: {desc}")
    
    print(f"\n🔄 APIs disponíveis:")
    for api in get_available_apis():
        status = "✅" if api == ACTIVE_API else "  "
        print(f"   {status} {api}")

# Verifica chaves automaticamente ao importar
def _initialize():
    """Inicialização automática das configurações"""
    if not any(validate_api_key(config["key"]) for config in API_CONFIGS.values()):
        print("⚠️ AVISO: Nenhuma chave de API válida encontrada!")
        print("💡 Para configurar, execute: python api_config.py")
        print("📁 Ou crie o arquivo .env baseado em env_template.txt")

# Executa inicialização
_initialize()

# Se executado diretamente, mostra configurações e verifica chaves
if __name__ == "__main__":
    check_api_keys_loaded()
    show_config()
