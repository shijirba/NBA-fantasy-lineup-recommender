from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Player
from django.core import serializers
from django.http import HttpResponse, JsonResponse

class HomePageView(TemplateView):
    template_name = 'home.html'

def player_list(request):
    return render(request, 'home.html',{
        'players' : Player.objects.order_by().values('name').distinct(),
        'teams' : Player.objects.order_by().values('opponent').distinct()
        })

def player_compare(request):
    return render(request, 'compare.html',{
        'players' : Player.objects.order_by().values('name').distinct()
        })

def find(request):
    if request.method == 'GET':
        playerName = request.GET['playerName']
        team = request.GET['team']
        stats = request.GET.getlist('stats[]')
        data = Player.objects.filter(name=playerName, opponent=team)
        result = []
        years = []
        pts = []
        trb = []
        ast = []
        stl = []
        blk = []

        #    result = [0,0,0,0,0]
        for x in data:
            pts.append(x.points)
            years.append(x.date_game.strftime("%Y-%m-%d"))
            trb.append(x.total_rebounds)
            ast.append(x.assists)
            stl.append(x.steals)
            blk.append(x.blocks)

        #    result[0] = round(result[0]/len(data),2)
        #    if 'TRB' in stats:
        #         result[1] = round(result[1]/len(data),2)
        #    if 'AST' in stats:
        #         result[2] = round(result[2]/len(data),2)
        #    if 'STL' in stats:
        #         result[3] = round(result[3]/len(data),2)
        #    if 'BLK' in stats:
        #         result[4] = round(result[4]/len(data),2)
        result.append(pts)
        result.append(trb)
        result.append(ast)
        result.append(stl)
        result.append(blk)
           
        return JsonResponse({ 'message': "Success!", 'data': result, 'label': years, 'stats': stats, 'url': data[0].img_url})
    else:
           return HttpResponse("Request method is not a GET")

class AboutPageView(TemplateView):
    template_name = 'about.html'