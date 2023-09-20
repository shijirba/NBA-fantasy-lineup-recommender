from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Player, Rank
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class HomePageView(TemplateView):
    template_name = 'home.html'

def player_list(request):
    return render(request, 'home.html',{
        'players' : Player.objects.order_by().values('name').distinct(),
        'teams' : Player.objects.order_by().values('opponent').distinct()
        })

def compare(request):
    return render(request, 'compare.html',{
        'players' : Player.objects.order_by().values('name').distinct()
        })

def rank(request):
    # Retrieve all rows from the Rank model
    all_ranks = Rank.objects.all()
    # Delete all rows from the Rank model
    all_ranks.delete()

    data = Player.objects.order_by().values('name').distinct()
    result = []
    for d in data:
        allStat = Player.objects.filter(name=d['name'], season='2022-23')
        stat = [0,0,0,0,0,0]
        for x in allStat:
            stat[0] += x.points
            stat[1] += x.total_rebounds
            stat[2] += x.blocks
            stat[3] += x.steals
            stat[4] += x.assists
            stat[5] += x.turnovers
        statResult = (stat[0] + stat[1] + stat[2] + stat[3] + stat[4] - stat[5]) / len(stat)
        result.append({'name': d['name'],'stat': statResult})
    sorted_result = sorted(result, key=lambda x: x["stat"],reverse=True)
    for p in sorted_result:
        player = Rank(
            name=p['name'],
            rank=sorted_result.index(p)+1
        )
        player.save()
    return JsonResponse({ 'data': sorted_result })

def compare_player(request):
    if request.method == "GET":
        playerName1=request.GET['playerName']
        playerName2=request.GET['playerName2']
    
        player1 = Player.objects.filter(name=playerName1)
        player2 = Player.objects.filter(name=playerName2)

        rankData = Rank.objects.filter(name=playerName1)
        for r in rankData:
            rank1 = r.rank
        rankData = Rank.objects.filter(name=playerName2)
        for r in rankData:
            rank2 = r.rank

        p1 = [0,0,0,0,0]
        p2 = [0,0,0,0,0]

        for x in player1:
            p1[0] += x.points
            p1[1] += x.total_rebounds
            p1[2] += x.blocks
            p1[3] += x.steals
            p1[4] += x.assists
        
        p1[0] = round(p1[0]/len(player1),1)
        p1[1] = round(p1[1]/len(player1),1)
        p1[2] = round(p1[2]/len(player1),1)
        p1[3] = round(p1[3]/len(player1),1)
        p1[4] = round(p1[4]/len(player1),1)

        for x in player2:
            p2[0] += x.points
            p2[1] += x.total_rebounds
            p2[2] += x.blocks
            p2[3] += x.steals
            p2[4] += x.assists

        p2[0] = round(p2[0]/len(player2),1)
        p2[1] = round(p2[1]/len(player2),1)
        p2[2] = round(p2[2]/len(player2),1)
        p2[3] = round(p2[3]/len(player2),1)
        p2[4] = round(p2[4]/len(player2),1)
        
        player1Data = {'data':p1,'imgUrl':player1[0].img_url, 'rank': rank1}
        player2Data = {'data':p2,'imgUrl':player2[0].img_url, 'rank': rank2}
        return JsonResponse({ 'message': "Success!", 'player1': player1Data, 'player2': player2Data})

def find(request):
    if request.method == 'GET':
        playerName = request.GET['playerName']
        team = request.GET['team']
        stats = request.GET.getlist('stats[]')
        data = Player.objects.filter(name=playerName, opponent=team)
        rankData = Rank.objects.filter(name=playerName)
        for r in rankData:
            rank = r.rank
        result = []
        years = []
        pts = []
        trb = []
        ast = []
        stl = []
        blk = []

        ptsAve = 0
        trbAve = 0
        astAve = 0
        stlAve = 0
        blkAve = 0

        #    result = [0,0,0,0,0]
        for x in data:
            pts.append(x.points)
            ptsAve += x.points
            years.append(x.date_game.strftime("%Y-%m-%d"))
            trb.append(x.total_rebounds)
            trbAve += x.total_rebounds
            ast.append(x.assists)
            astAve += x.assists
            stl.append(x.steals)
            stlAve += x.steals
            blk.append(x.blocks)
            blkAve += x.blocks

        ptsAve = round(ptsAve/len(pts),1)
        trbAve = round(trbAve/len(trb),1)
        astAve = round(astAve/len(ast),1)
        stlAve = round(stlAve/len(stl),1)
        blkAve = round(blkAve/len(blk),1)
        #    result[0] = round(result[0]/len(data),2)
        #    if 'TRB' in stats:
        #         result[1] = round(result[1]/len(data),2)
        #    if 'AST' in stats:
        #         result[2] = round(result[2]/len(data),2)
        #    if 'STL' in stats:
        #         result[3] = round(result[3]/len(data),2)
        #    if 'BLK' in stats:
        #         result[4] = round(result[4]/len(data),2)
        result.append({'point':pts, 'average': ptsAve})
        result.append({'rebound':trb, 'average': trbAve})
        result.append({'assist':ast, 'average': astAve})
        result.append({'steal':stl, 'average': stlAve})
        result.append({'block':blk, 'average': blkAve})
        
        p = prediction(playerName)
        
        return JsonResponse({ 'message': "Success!", 'data': result, 'label': years, 'stats': stats, 'url': data[0].img_url, 'rank': rank, 'prediction': p})
    else:
           return HttpResponse("Request method is not a GET")

def prediction(playerName):
    data = Player.objects.filter(name=playerName)
    exportData = []
    for x in data:
        exportData.append({'game_date': x.date_game,'game_score': x.points})
    file_path = "data.csv"

    with open(file_path, mode="w", newline="") as csv_file:
        fieldnames = ["game_date", "game_score"]  # Replace with your fieldnames
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Use DictWriter for dictionaries
        writer.writeheader()  # Write the header row

        for row in exportData:
            writer.writerow(row)
    
    player_data = pd.read_csv(r'data.csv')
    # Extract the 'game_date' and 'game_score' columns
    game_dates = player_data['game_date']
    game_scores = player_data['game_score']

    # Convert 'game_date' to a datetime type
    game_dates = pd.to_datetime(game_dates)

    # Create a DataFrame with 'game_date' and 'game_score'
    career_data = pd.DataFrame({'game_date': game_dates, 'game_score': game_scores})

    # Set 'game_date' as the index
    career_data.set_index('game_date', inplace=True)

    # Normalize the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(career_data)

    # Create sequences for LSTM training
    sequence_length = 10  # Adjust as needed
    X = []
    y = []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)

    # Reshape X to match LSTM input shape [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X, y, epochs=20, batch_size=32, verbose=2)

    # Predict the next game score based on the most recent historical data
    last_sequence = scaled_data[-sequence_length:, 0]
    last_sequence = np.reshape(last_sequence, (1, sequence_length, 1))
    predicted_score = model.predict(last_sequence)

    # Transform the prediction back to the original scale
    predicted_score = scaler.inverse_transform(predicted_score)[0][0]
    print(f"Predicted Next Game Score: {predicted_score}")
    python_float = round(float(predicted_score))
    json_data = json.dumps(python_float)
    return json_data

class AboutPageView(TemplateView):
    template_name = 'about.html'
