import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PacoteViagem, Reserva, HistoricoClima

# Substitua pela sua chave (key) gratuita obtida no site da HG Brasil
HG_BRASIL_KEY = 'b722fe1c'

def obter_previsao_hg_brasil(cidade_nome):
    try:
        url = "https://api.hgbrasil.com/weather"
        params = {
            "key": HG_BRASIL_KEY,
            "city_name": cidade_nome
        }
        
        resposta = requests.get(url, params=params)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            # Retorna o dicionário contendo os resultados da HG Brasil
            return dados.get('results')
            
    except Exception as e:
        print(f"Erro ao conectar com a API da HG Brasil: {e}")
    
    return None

def pagina_inicial(request):
    pacotes = PacoteViagem.objects.all()
    clima_info = None
    cidade_selecionada = request.GET.get('clima_cidade')

    if cidade_selecionada:
        dados_api = obter_previsao_hg_brasil(cidade_selecionada)
        if dados_api:
            # Estrutura de dados retornada pela HG Brasil
            cidade_nome = dados_api.get('city_name', cidade_selecionada)
            temperatura = dados_api.get('temp')
            descricao = dados_api.get('description')
            
            clima_info = {
                'cidade': cidade_nome,
                'temp_min': dados_api.get('forecast', [{}])[0].get('min', temperatura), # HG Brasil fornece previsão detalhada na lista 'forecast'
                'temp_max': dados_api.get('forecast', [{}])[0].get('max', temperatura),
                'descricao': descricao,
            }
            
            # Grava no histórico do banco de dados
            HistoricoClima.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                cidade_buscada=cidade_nome,
                temperatura=f"{temperatura}°C" if temperatura else "N/A",
                condicao=descricao or "Indefinido"
            )

    historico = []
    if request.user.is_authenticated:
        historico = HistoricoClima.objects.filter(usuario=request.user).order_by('-data_pesquisa')[:5]

    context = {
        'pacotes': pacotes,
        'clima_info': clima_info,
        'historico': historico,
    }
    return render(request, 'viagens/index.html', context)

@login_required
def realizar_reserva(request, pacote_id):
    pacote = get_object_or_404(PacoteViagem, id=pacote_id)
    if pacote.vagas_disponiveis > 0:
        Reserva.objects.create(usuario=request.user, pacote=pacote)
        pacote.vagas_disponiveis -= 1
        pacote.save()
    return redirect('pagina_inicial')
