import requests

# Dados para enviar ao DeepSeek
data = {
    "original_sm_file": "...conteúdo do arquivo SM original...",  # ou em base64
    "stats": {  # DataFrame convertido para JSON/dict
        "total_notes": 500,
        "density_per_measure": [...],
        "difficulty": "Medium",
        "bpm_changes": [...]
    },
    "instructions": "Gere uma nova versão com 20% mais notas e dificuldade Hard"
}

# Chamar a API do DeepSeek
response = requests.post(
    "https://api.deepseek.com/v1/stepmania/generate",
    json=data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

# Salvar o novo arquivo SM
new_sm_content = response.json()["generated_sm_file"]
with open("new_chart.sm", "w") as f:
    f.write(new_sm_content)