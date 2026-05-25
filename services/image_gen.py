import urllib.parse
import random

def gerar_imagem_saas(image_prompt):
    """
    Gera imagem usando Pollinations.ai com o modelo avançado FLUX e prompts de alta conversão.
    """
    print(f"Acionando IA de Imagem para: {image_prompt[:50]}...")
    
    # Injetamos "esteroides" no prompt para forçar fotorealismo extremo, qualidade 8k e iluminação profissional
    prompt_completo = f"Award-winning professional photography, 8k uhd, dslr, 35mm lens, highly detailed, photorealistic, masterpiece. {image_prompt}"
    
    prompt_codificado = urllib.parse.quote(prompt_completo)
    seed = random.randint(1, 1000000)
    
    # O Segredo: adicionamos model=flux e enhance=true para qualidade absurda
    url_imagem = f"https://image.pollinations.ai/prompt/{prompt_codificado}?width=1080&height=1080&nologo=true&enhance=true&model=flux&seed={seed}"
    
    print("Link da imagem gerado com sucesso (Modelo Flux)!")
    
    return url_imagem