import urllib.parse
import random

def gerar_imagem_saas(image_prompt):
    """
    Gera imagem usando Pollinations.ai com o modelo avançado FLUX (estilo Midjourney)
    com prompts de qualidade profissional e Marca d'Água.
    """
    print(f"Renderizando imagem Flux 8K para: {image_prompt[:50]}...")
    
    # Injetamos "esteroides" de qualidade premium e realismo no prompt
    prompt_completo = f"Award-winning professional food photography, 8k uhd, dslr, highly detailed, photorealistic, cinematic lighting. {image_prompt}"
    
    prompt_codificado = urllib.parse.quote(prompt_completo)
    seed = random.randint(1, 1000000)
    
    # Usamos nologo=true e model=flux para qualidade máxima
    url_imagem = f"https://image.pollinations.ai/prompt/{prompt_codificado}?width=1080&height=1080&nologo=true&enhance=true&model=flux&seed={seed}"
    
    print("Link da imagem premium gerado com sucesso!")
    
    return url_imagem