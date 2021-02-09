class ExamException(Exception):
        pass
#funzione 
def daily_stats(time_series):
    
    #la lista che conterrà a le liste delle singole giornate
    days=[]
    start = time_series[0][0]
    if start%86400==0 :
        end_this_day = start + 86400
    else :
        end_this_day = start - (start%86400) + 86400

    #la lista contentente le temperature di un singolo giorno, che verrà inserita in 'days[]'
    day=[]
    for ora in time_series:
        #se l'ora non ha superato l'epoch che contrassegna l'inizio della giornata successiva, aggiungo la sua temperatura ai valori di questa giornata
        if ora[0]<end_this_day:
            #assegno alla lista il valore 
            day.append(ora[1])
        #se l'ora ha superato la fine del giorno, quindi aggiungo il day alla lista days, dopodiché aggiorno la fine della giornata e creo il nuovo giorno:
        else:
            days.append(day)
            end_this_day = end_this_day + 86400
            day=[]
            
    #dichiaro la lista statistiche
    stats=[]
    #calcolo le statistiche di ogni singolo giorno
    for day in days:
        #inizializzo le statistiche con dei valori di base
        max=day[0]
        min=day[0]
        sum=0
        for i in range(0,len(day)):
            #se la temperatura fosse più bassa della minima, aggiorno il valore minimo
            if day[i]<min:
                min=day[i]
            #se la temperatura fosse più alta della  massima, aggiorno il valore massimo
            if day[i]>max:
                max=day[i]
            #aggiorno la somma totale del giorno
            sum+=day[i]
        #finito il ciclo, quindi quando la somma è stata incrementata con tutte le temperature rilevate durante una giornata, calcolo la temperatura media come la somma delle temperature divisa per il numero di esse
        media=sum/len(day)
        #nella lista delle statistiche di un singolo giorno inserisco i dati trovati 
        stat=[min,max,media]
        #procedo a inserirla nella lista stats, che sarà ritornata
        stats.append(stat)
    return stats



class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
    
    def get_data(self):
        values = []
        dates = []
        #provo ad aprire il file
        try:
            my_file = open(self.name, 'r')
        except ExamException as e: 
            # Stampo l'errore
            print('Errore nella lettura del file: "{}"'.format(e))
            raise
        for line in my_file:    
            try :
                elements = line.split(",")
            except :
                continue
            if elements[0] != 'epoch' : 
                if len(elements)!=2 :
                    continue
                data = elements[0]
                val = elements[1]                       
                try :
                    data = int(data)
                    val = float(val)
                    if (data!=0 and data!=None): 
                        dates.append(data)
                        values.append(val)
                except :
                    pass
        i=0
        real_dates = []
        real_values = []
        #creo la lista real_dates e real_values, in cui salverò solamente i valori accettabili
        for i in range(0, len(dates)-1):
            
            if dates[i]>=dates[i+1]:
                raise ExamException('L elemento è fuori ordine o duplicato')
                
                

            else :
                real_dates.append(dates[i]) 
                real_values.append(values[i])
    
        #creo la lista returnable, in cui salvo i dati finali, come verranno returnati   
        returnable = []
        for i in range(0, len(real_values)):
            now = [real_dates[i], real_values[i]]
            returnable.append(now)
            
        self.values = values
        my_file.close()
        return returnable

time_series_file = CSVTimeSeriesFile(name = 'data.csv')
time_series = time_series_file.get_data()
print(daily_stats(time_series))

 