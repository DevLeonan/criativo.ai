from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from apps.brands.models import BrandProfile

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        brand_name = request.POST.get('brand_name')
        city = request.POST.get('city')
        niche = request.POST.get('niche')
        tone_of_voice = request.POST.get('tone_of_voice')
        
        # Busca se o usuário já existe
        user = User.objects.filter(username=email).first()
        
        if user:
            # Se o usuário existe E já tem uma empresa vinculada, é um cadastro duplicado real
            if hasattr(user, 'brand_profile'):
                return render(request, 'accounts/register.html', {'error': 'Este e-mail já está cadastrado.'})
            
            # Se o usuário existe mas NÃO tem empresa (caso do looping), vamos atualizar os dados dele
            user.set_password(password)
            user.first_name = name
            user.save()
        else:
            # Se não existe mesmo, cria um usuário totalmente do zero
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        
        # Cria ou recria o perfil da marca que estava faltando
        BrandProfile.objects.create(
            user=user,
            brand_name=brand_name,
            city=city,
            niche=niche,
            tone_of_voice=tone_of_voice,
            primary_color='#6366f1'  # Cor roxa premium padrão do novo layout
        )
        
        # Loga e manda para o painel
        login(request, user)
        return redirect('dashboard')
        
    return render(request, 'accounts/register.html')