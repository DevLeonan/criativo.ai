import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

def gerar_conteúdo_completo(brand, objective, format_type):
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Instruções detalhadas de formatação visual para humanos
    if format_type == 'reels':
        format_instruction = "Crie um ROTEIRO PARA REELS formatado em texto corrido. Use títulos em negrito, separe 'Cena Visual' de 'Fala' usando quebras de linha e adicione emojis. Foque em reter a atenção nos 3 primeiros segundos."
    elif format_type == 'stories':
        format_instruction = "Crie uma SEQUÊNCIA DE 3 STORIES formatada em texto corrido. Separe nitidamente [Slide 1], [Slide 2] e [Slide 3] com quebras de linha. Indique o texto da tela e sugestões de interação (enquetes/caixinhas)."
    else:
        format_instruction = "Crie um POST DE FEED tradicional com uma legenda altamente conversiva, hashtags e emojis perfeitamente espaçados."

    prompt = f"""
    Aja como um especialista em social media. Crie um conteúdo para o Instagram da marca '{brand.brand_name}', 
    que atua em '{brand.city}' no nicho de '{brand.get_niche_display()}'. 
    Tom de voz: '{brand.tone_of_voice}'. Cor principal: '{brand.primary_color}'.

    🎯 OBJETIVO DO POST: {objective}
    📱 FORMATO EXIGIDO: {format_instruction}

    REGRA VITAL DE FORMATAÇÃO:
    A resposta "legenda" DEVE ser uma única STRING de texto (texto corrido) pronta para leitura humana. 
    NUNCA retorne dicionários, arrays (listas) ou formatos JSON aninhados dentro do campo "legenda".
    Use "\\n" para criar parágrafos e separar cenas/slides.

    Retorne APENAS um JSON válido. O formato exato deve ser:
    {{
        "legenda": "Seu texto final lindamente formatado aqui, pronto para o cliente ler.",
        "image_prompt": "A highly detailed, professional photography description in ENGLISH for an AI image generator. Emphasize realism, 8k, lighting, and niche relevance."
    }}
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "google/gemini-2.5-flash", 
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    if response.status_code == 200:
        texto_puro = response.json()['choices'][0]['message']['content']
        try:
            texto_limpo = re.sub(r'```json\n?', '', texto_puro)
            texto_limpo = re.sub(r'```', '', texto_limpo).strip()
            return json.loads(texto_limpo)
        except Exception as e:
            print(f"Erro ao formatar JSON: {e}")
            return None
    return None