from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Aula

def home(request):
    return render(request, "Html/home.html")


def cadastrar_aula(request):
    if request.method == 'POST':
        materia = request.POST.get('materia')
        conteudo = request.POST.get('conteudo')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        vagas = request.POST.get('vagas')

        Aula.objects.create(
            materia=materia,
            conteúdo=conteudo,
            data=data,
            horario=horario,
            vagas=vagas
        )
        return redirect('cadastrar_aula')

    return render(request, 'Html/cadastro_aulas.html')


def listar_aulas(request):
    aulas = Aula.objects.all().order_by('data', 'horario')
    
    aulas_inscritas = request.session.get('aulas_inscritas', [])
    
    context = {
        'aulas': aulas,
        'aulas_inscritas': aulas_inscritas
    }
    return render(request, 'Html/inscricao_aula.html', context)

def inscrever_aula(request, aula_id):
    if request.method == 'POST':
        aula = get_object_or_404(Aula, id=aula_id)
        
        aulas_inscritas = request.session.get('aulas_inscritas', [])
        
        if aula_id in aulas_inscritas:
            messages.warning(request, 'Você já está inscrito nesta aula')
        elif aula.vagas > 0:
            aula.vagas -= 1
            aula.save()
            
            aulas_inscritas.append(aula_id)
            request.session['aulas_inscritas'] = aulas_inscritas
            
            messages.success(request, f'Inscrição realizada com sucesso na aula de {aula.materia}!')
        else:
            messages.error(request, 'As vagas para esta aula esgotaram')
            
    return redirect('listar_aulas')


def aulas_inscritas(request):
    aulas_inscritas_ids = request.session.get('aulas_inscritas', [])
    aulas = Aula.objects.filter(id__in=aulas_inscritas_ids).order_by('data', 'horario')
    
    return render(request, 'Html/aulas_inscritas.html', {'aulas': aulas})


def cancelar_inscricao(request, aula_id):
    if request.method == 'POST':
        aulas_inscritas = request.session.get('aulas_inscritas', [])
        
        if aula_id in aulas_inscritas:
            aula = get_object_or_404(Aula, id=aula_id)
            aula.vagas += 1  
            aula.save()
            
            
            aulas_inscritas.remove(aula_id)
            request.session['aulas_inscritas'] = aulas_inscritas
            
            messages.success(request, f'Inscrição na aula de {aula.materia} cancelada com sucesso.')
            
    return redirect('aulas_inscritas')