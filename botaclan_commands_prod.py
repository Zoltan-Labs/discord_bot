import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import datetime
import requests
import os


#vars init
current_datetime = datetime.datetime.now().strftime("%d %b %Y %H:%M")

#bot events
bot=commands.Bot(command_prefix="!")

#Heroku config vars init
ow_appid=os.environ.get('ow_appid')
token=os.environ.get('token')


@bot.event
async def on_ready():
        print("Bot logged in!")
        print("I am running %s" % bot.user.name)
        print("With the ID: %s" % bot.user.id)
        print("Instance run at: "+current_datetime)

#Help
@bot.command()
async def helpme():
        await bot.say("-----Botaclan Help-----")
        await bot.say("!add x y")
        await bot.say("!today")
        await bot.say("!whois <member_name>")
        await bot.say("!weather <coruche|lisboa|portimao>")


#error handling
@bot.event
async def on_command_error(error,ctx):
        if isinstance(error,commands.BadArgument):
                await bot.send_message(ctx.message.channel,
                        "[ERROR] That member does not exist!")
        elif isinstance(error,commands.NoPrivateMessage):
                await bot.send_message(ctx.message.channel,
                        "[ERROR] This command can't be used in private messages.")
        elif isinstance(error,commands.CheckFailure):
                await bot.send_message(ctx.message.channel,
                        "[ERROR] You don't have permissions to run this command")
        elif isinstance(error,commands.CommandNotFound):
                await bot.send_message(ctx.message.channel,
                        "[ERROR] This command does not exist.")
        else:
                print(error)



#Sums 2 numbers
@bot.command()
async def add(left: int, right: int):
        print("add")
        await bot.say(left + right)


        
#Whois Function
@bot.command(pass_context=True)
async def whois(ctx,member: discord.Member=None):

        if member is None:
                member=ctx.message.author

        await bot.say("{0} joined at: {0.joined_at}".format(member))
        await bot.say("{0} status is: {0.status}".format(member))
        
        await bot.say("{0} server is: {0.server}".format(member))
        await bot.say("{0} top role is: {0.top_role}".format(member))


#Date and time for today
@bot.command()
async def today():
        today=datetime.datetime.today()
        await bot.say("{0:%d} {0:%B} {0:%Y}".format(today))
        await bot.say("{0:%I}:{0:%M} {0:%p}".format(today))


#Weather forecast for 3 cities
@bot.command()
async def weather(cidade):

        cidades={"portimao":"2264456","coruche":"2268946","lisboa":"2267057"}

        if cidade not in cidades:
          await bot.say("Cities im my list: portimao,coruche,lisboa")
          return


        diaSemana={0:"Segunda-Feira",1:"Terça-Feira",2:"Quarta-Feira",3:"Quinta-Feira",
                   4:"Sexta-Feira",5:"Sabado",6:"Domingo"}

        mes={'January':'Janeiro','February':'Fevereiro','March':'Março','April':'Abril',
             'May':'Maio','June':'Junho','July':'Julho','August':'Agosto','September':'Setembro',
             'October':'Outubro','November':'Novembro','December':'Dezembro'}

        condTempo={200:'Trovoada com chuviscos',201:'Trovoada com chuva',
                   202:'Trovoada com chuva intensa',210:'Trovoada ligeira',
                   211:'Trovoada',212:'Trovoada intensa',221:'Trovoada violenta',
                   230:'Trovoada com chuviscos ligeiros',
                   231:'Trovoada com chuviscos',232:'trovoada com chuviscos intensos',
                   300:'Chuviscos pouco intensos',301:'Chuviscos',
                   302:'Chuviscos muito intensos',310:'Chuva fraca pouco intensa',
                   311:'Chuva fraca',312:'Chuva fraca mas intensa',
                   313:'Chuva e chuviscos',314:'Chuva intensa e chuviscos',
                   321:'Chuviscos intensos',
                   500:'Chuviscos',501:'Chuva moderada',502:'Chuva intensa',
                   503:'Chuva muito intensa',504:'Chuva extrema',
                   511:'Chuva gelada',520:'Aguaceiros',521:'Chuva',
                   522:'Chuva intensa',531:'Chuva muito intensa',
                   600:'Neve ligeira',601:'Neve',602:'Muita neve',
                   611:'Aguaceiros',612:'Muitos aguaceiros',
                   615:'Neve e pouca chuva',616:'Neve e chuva',
                   620:'Pouca neve',621:'Neve',622:'Muita neve',
                   701:'Neblina',711:'Nevoeiro ligeiro',721:'Nevoa',
                   731:'Remoinhos vento,Pó',741:'Nevoeiro',751:'Nuvens de areia',
                   761:'Nuvens de pó',
                   762:'Cinza vulcânica',771:'Rajadas de vento',781:'Tornado',
                   800:'Céu limpo',801:'Nuvens dispersas',
                   802:'Pouco nublado',803:'Nublado',804:'Muito nublado',
                   900:'Tornado',901:'Tempestade tropical',902:'Furacão',
                   903:'Frio',904:'Quente',905:'Ventoso',906:'Granizo',
                   951:'Calmo',952:'Brisa muito ligeira',953:'Brisa ligeira',
                   954:'Brisa moderada',955:'Brisa fresca',956:'Brisa intensa',
                   957:'Vento intenso,quase vendaval',958:'Vendaval',
                   959:'Vendaval intenso',960:'Tempestade',
                   961:'Tempestade violenta',962:'Furacão'
                   }


        #API request
        response=requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?id="+cidades[cidade]+"&APPID="+ow_appid+"&cnt=7&units=metric")
        w=response.json()

        #----Header----
        await bot.say("O tempo para {},{} ".format(w['city']['name'],w['city']['country']))

        #----Data----
        for i in range(0,2):
            #Tradução e formatação da data
            data=datetime.datetime.fromtimestamp(w['list'][i]['dt'])
            dia=data.strftime("%d")
            mesIng=data.strftime("%B")
            ano=data.strftime("%Y")
            codDia=data.weekday()

            tempo=w['list'][i]['weather'][0]['id']

            await bot.say("----------------------------")
            await bot.say("{3} de {0} de {1},{2}".format(dia,mes[mesIng],ano,diaSemana[codDia]))
            await bot.say("Temp Min : {} C".format(w['list'][i]['temp']['min']))
            await bot.say("Temp Max : {} C".format(w['list'][i]['temp']['max']))
            #await bot.say("Humidade : {} %".format(w['list'][i]['humidity']))
            #await bot.say("Nuvens   : {} %".format(w['list'][i]['clouds']))
            await bot.say("Condições: {}  ".format(condTempo[tempo]))
            await bot.say("Vel vento: {} m/s".format(w['list'][i]['speed']))
        await bot.say("----------------------------")



        
#login info to discord server
bot.run(token)
