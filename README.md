# Start2Impact MongoDb project: Exchange.
Applicazione web che permette di acquistare e vendere bitcoin. 

#### Requisiti progetto:
1) La piattaforma deve prevedere un endpoint per gestire la registrazione e l’accesso degli utenti.
2) Assegna automaticamente a ciascun utente registrato una cifra variabile tra gli 1 e i 10 bitcoin.
3) Ciascun utente può pubblicare uno o più ordini di vendita o di acquisto di una certa quantità di bitcoin ad un certo prezzo.
4) Al momento della pubblicazione, se il prezzo di acquisto dell’ordine è pari o superiore al prezzo di vendita di un qualsiasi altro utente, registra la transazione e contrassegna entrambi gli ordini come eseguiti.
5) Prevedi un endpoint per ottenere tutti gli ordini di acquisto e vendita attivi.
6) Prevedi anche un endpoint per calcolare il profitto o la perdita totale derivante dalle operazioni di ciascun utente.
7) Ipotizza che la piattaforma in questione sia totalmente gratuita per gli utenti e che non trattenga alcun tipo di commissione sulle operazioni.

## Framework e Tecnologie usate:
- [Django](https://docs.djangoproject.com/it/4.0/) - Back-end
- [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - Front-end
- [MongoDB]([https://redis.io](https://www.mongodb.com)) - Server

## Setup progetto:
```
progetto_dango_pierfrancesco_tripodi % python3 -m venv myvenv(=nome ambiente virtuale)
progetto_dango_pierfrancesco_tripodi % source venv/bin/activate
(venv)progetto_dango_pierfrancesco_tripodi % pip install -r requirements.txt
```

## Avvio del progetto: 
```
progetto_dango_pierfrancesco_tripodi % cd social_dex
social_dex % python manage.py runserver
```
