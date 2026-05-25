from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.brands.models import BrandProfile
from .models import GeneratedContent
from services.openrouter_api import gerar_conteúdo_completo
from services.image_gen import gerar_imagem_saas
import mercadopago
import uuid

# INSIRA SEU ACCESS TOKEN DE PRODUÇÃO AQUI
MP_ACCESS_TOKEN = "APP_USR-5402725203039388-020123-10a75c260cf12f6663994256fc156b5d-1365742803" # Pegue isso no painel do MP

# ... importações continuam iguais ...

@login_required(login_url='/login/')
def dashboard(request):
    try:
        brand = request.user.brand_profile
    except BrandProfile.DoesNotExist:
        return redirect('register')
    
    last_content = GeneratedContent.objects.filter(brand=brand).first()
    post_gerado = last_content.caption_text if last_content else None
    image_url = last_content.image_url if last_content else None
    
    if request.method == "POST" and brand:
        
        # BARREIRA DE CRÉDITOS (Se zerou, manda pro Pix!)
        if brand.credits <= 0:
            return redirect('checkout')
            
        objetivo_escolhido = request.POST.get('objective', 'Engajar e movimentar a audiência')
        formato_escolhido = request.POST.get('format_type', 'feed')
        
        conteudo_ia = gerar_conteúdo_completo(brand, objetivo_escolhido, formato_escolhido)
        
        if conteudo_ia:
            final_image_url = None
            texto_legenda = conteudo_ia.get('legenda', 'Erro: Texto não retornado pela IA. Tente novamente.')
            prompt_imagem = conteudo_ia.get('image_prompt', '')
            
            if formato_escolhido == 'feed' and prompt_imagem:
                final_image_url = gerar_imagem_saas(prompt_imagem)
                
            GeneratedContent.objects.create(
                brand=brand,
                content_type=formato_escolhido,
                caption_text=texto_legenda,
                image_url=final_image_url,
                image_prompt=prompt_imagem
            )
            
            # GASTA 1 CRÉDITO E SOMA NO HISTÓRICO GERAL
            brand.credits -= 1
            brand.generations_count += 1
            brand.save()
            
            return redirect('dashboard')

    context = {
        'brand': brand,
        'post_gerado': post_gerado,
        'image_url': image_url,
        'credits': brand.credits # Mandamos os créditos para mostrar na tela
    }
    return render(request, 'content/dashboard.html', context)


@login_required(login_url='/login/')
def checkout(request):
    brand = request.user.brand_profile
    sdk = mercadopago.SDK(MP_ACCESS_TOKEN)
    
    # Prepara o Pedido do PIX para 100 Créditos
    payment_data = {
        "transaction_amount": 19.99,
        "description": "Pacote 100 Criativos Premium - Criativo.AI",
        "payment_method_id": "pix",
        "payer": {
            "email": request.user.email,
            "first_name": request.user.first_name,
        }
    }
    
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response.get("response", {})
    
    pix_copia_cola = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code", "")
    qr_code_base64 = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64", "")
    
    context = {
        "pix_copia_cola": pix_copia_cola,
        "qr_code_base64": qr_code_base64,
        "valor": "19,99",
        "pacote": "100"
    }
    return render(request, 'content/checkout.html', context)


@login_required(login_url='/login/')
def history(request):
    try:
        brand = request.user.brand_profile
    except BrandProfile.DoesNotExist:
        return redirect('register')

    historico_posts = GeneratedContent.objects.filter(brand=brand).order_by('-created_at')

    context = {
        'historico_posts': historico_posts,
    }
    return render(request, 'content/history.html', context)


@login_required(login_url='/login/')
def settings_view(request):
    try:
        brand = request.user.brand_profile
    except BrandProfile.DoesNotExist:
        return redirect('register')

    if request.method == 'POST':
        brand.brand_name = request.POST.get('brand_name')
        brand.city = request.POST.get('city')
        brand.niche = request.POST.get('niche')
        brand.tone_of_voice = request.POST.get('tone_of_voice')
        brand.save()
        
        return redirect('/ajustes/?saved=true')

    context = {
        'brand': brand,
    }
    return render(request, 'content/settings.html', context)