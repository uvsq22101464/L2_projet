import pandas as pd
import re
import matplotlib.pyplot as plt
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer

df = pd.read_json('C:/programation/L2/In 304/versailles_tweets_100.json', encoding="utf-8")

class Tweet:
    def __init__(self, line, text, author, entities, tweet_id, tweet_geo, tweet_lang, created_at, metrics, context_annotations):

        tweet_clean = ""
        for caractere in text[line]:
            if re.compile("[\w|\.|,|\?|!|:|;|\s|(|)|\-|@|#|/|'|_|’]").search(caractere) :
                tweet_clean += caractere
            tweet_clean = re.compile(" +").sub(" ", tweet_clean)
        # tweet nettoyés
        self.text = tweet_clean

        # id de l'auteur du tweet
        self.author = author[line]

        # personnes mentionnées dans le tweet
        mentions = []
        if type(entities[line]) != float and 'mentions' in entities[line]:
            for i in range(len(entities[line]['mentions'])):
                mentions.append(entities[line]['mentions'][i]['username'])
        self.mentions = mentions

        # hashtags du tweet
        hashtags = []
        if type(entities[line]) != float and 'hashtags' in entities[line]:
            for i in range(len(entities[line]['hashtags'])):
                hashtags.append(entities[line]['hashtags'][i]['tag'])
        self.hashtags = hashtags

        # id du tweet
        self.id = tweet_id[line]

        # geo du tweet
        self.geo = tweet_geo[line]['place_id']

        # langue du tweet
        self.lang = tweet_lang[line]

        # date de publication
        self.date = created_at[line]

        # retweet
        self.retweet = metrics[line]['retweet_count']

        # réponse
        self.reply = metrics[line]['reply_count']

        # like
        self.like = metrics[line]['like_count']
        
        # retweet avec citation
        self.quote = metrics[line]['quote_count']

        # contexte
        self.context = context_annotations[line]

        # sentiment du tweet
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        blob1 = tb(tweet_clean)
        if blob1.sentiment[0] > 0:
            self.sentiment = "positive"
        elif blob1.sentiment[0] < 0:
            self.sentiment = "négatif"
        else:
            self.sentiment = "neutre"

# zone d'atterissage
atterissage = open("zone d'atterissage.txt", "w")

atterissage.write("text; author; mentions; hashtags; id_tweet; geo; lang; created_at; retweet; reply; like; quote; context\n")
for i in range(len(df)):
    tweet = Tweet(line=i, text=df['text'], author=df['author_id'], entities=df['entities'], tweet_id=df['id'], tweet_geo=df['geo'], tweet_lang=df['lang'], created_at=df['created_at'], metrics=df['public_metrics'], context_annotations=df['context_annotations'])
    atterissage.write(f"{tweet.text}; {tweet.author}; {tweet.mentions}; {tweet.hashtags}; {tweet.id}; {tweet.geo}; {tweet.lang}; {tweet.date}; {tweet.retweet}; {tweet.reply}; {tweet.like}; {tweet.quote}; {tweet.context}\n")

atterissage.close()

tweets = []
for i in range(len(df)):
    tweets.append(Tweet(    line=i, text=df['text'], author=df['author_id'], 
                            entities=df['entities'], tweet_id=df['id'], 
                            tweet_geo=df['geo'], tweet_lang=df['lang'], 
                            created_at=df['created_at'], metrics=df['public_metrics'], 
                            context_annotations=df['context_annotations']))

def auteur_publication(k):
    if abs(k) >= len(tweets):
        return print(f"Le tweet n°{k} n'existe pas, il y a que 0 à {len(tweets)-1} tweets")
    print(f"L'auteur du tweet n°{k} est :\n{tweets[k].author}")

def hashtags_publication(k):
    if abs(k) >= len(tweets):
        return print(f"Le tweet n°{k} n'existe pas, il y a que 0 à {len(tweets)-1} tweets")
    if len(tweets[k].hashtags) == 0:
        print(f"Le tweet n'a pas d'hashtag")
    else:
        print(f"Le tweet a pour hashtags :")
        for i in tweets[k].hashtags:
            print(i)

def user_mention_publication(k):
    if abs(k) >= len(tweets):
        return print(f"Le tweet n°{k} n'existe pas, il y a que 0 à {len(tweets)-1} tweets")
    if len(tweets[k].mentions) == 0:
        print(f"Le tweet n'a pas d'utilisateur mentionné")
    else:
        print(f"Le tweet a pour utilisateurs mentionnés :")
        for i in tweets[k].mentions:
            print(i)

def sentiment_publication(k):
    if abs(k) >= len(tweets):
        return print(f"Le tweet n°{k} n'existe pas, il y a que 0 à {len(tweets)-1} tweets")
    print(f"Le sentiment du tweet est {tweets[k].sentiment}")

def text_publication(k):
    if abs(k) >= len(tweets):
        return print(f"Le tweet n°{k} n'existe pas, il y a que 0 à {len(tweets)-1} tweets")
    print(f"Le text du tweet n°{k} est :\n{tweets[k].text}")

def top_user(k):
    a = []
    y, x = [], []
    for i in range(len(tweets)):
        a.append(tweets[i].author)
        b = []
    while len(a) != 0:
        b.append([a.count(a[0]), a[0]])
        c=a[0]
        for i in range(a.count(a[0])):
            a.remove(c)
    b = sorted(b, reverse=True)
    print(f"{len(b)} utilisateurs différents au total")
    if k =="all" or k > len(b):
        for i in range(len(b)):
            print(f"{b[i][0]} messages envoyé par {b[i][1]}")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("auteurs")
        plt.ylabel("nombres de tweets")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()
    else:
        for i in range(k):
            print(f"{b[i][0]} messages envoyé par {b[i][1]}")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("Auteurs")
        plt.ylabel("Nombres de tweets")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()

def top_hashtags(k):
    a = []
    x, y =[], []
    for i in range(len(tweets)):
        try:
            for j in range(len(tweets[i].hashtags[0])):
                a.append(tweets[i].hashtags[j])
        except:
            continue
    b = []
    while len(a) != 0:
        b.append([a.count(a[0]), a[0]])
        c=a[0]
        for i in range(a.count(a[0])):
            a.remove(c)
    b = sorted(b, reverse=True)
    print(f"{len(b)} hashtags différents au total")
    if k == "all" or k > len(b):
        for i in range(len(b)):
            print(f"{b[i][1]} avec {b[i][0]} apparitions")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("Hashtag")
        plt.ylabel("Nombre d'apparition")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()
    else:
        for i in range(k):
            print(f"{b[i][1]} avec {b[i][0]} apparitions")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("Hashtag")
        plt.ylabel("Nombre d'apparition")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()

def top_mentions(k):
    a = []
    x, y = [], []
    for i in range(len(tweets)):
        try:
            for j in range(len(tweets[i].mentions[0])):
                a.append(tweets[i].mentions[j])
        except:
            continue
    b = []
    while len(a) != 0:
        b.append([a.count(a[0]), a[0]])
        c=a[0]
        for i in range(a.count(a[0])):
            a.remove(c)
    b = sorted(b, reverse=True)
    print(f"{len(b)} mentions différentes au total")
    if k == "all" or k > len(b):
        for i in range(len(b)):
            print(f"{b[i][1]} avec {b[i][0]} mentions")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("Mentions")
        plt.ylabel("Nombre d'apparition")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()
    else:
        for i in range(k):
            print(f"{b[i][1]} avec {b[i][0]} mentions")
            y.append(b[i][0])
            x.append(str(b[i][1]))
        plt.bar(x, y)
        plt.xlabel("Mentions")
        plt.ylabel("Nombre d'apparition")
        plt.tick_params(axis='x', rotation=60)
        plt.yticks(y)
        plt.tight_layout()
        plt.show()

def tweet_de_auteur(k):
    a = f"les tweets de {k} sont :"
    for i in range(len(tweets)):
        if tweets[i].author == k:
            print(a)
            a = ""
            print(tweets[i].text)
    if a != "":
        print("L'utilisateur n'existe pas ou n'a pas de tweets.")

def nb_tweet_auteur():
    top_user("all")
    
def nb_tweet_hashtags():
    top_hashtags("all")

def tweet_mentionnant_user(k):
    """mettre le nom de la personne mentionné"""
    a = f"les tweets mentionnant {k} sont :"
    for i in range(len(tweets)):
        if k in tweets[i].text:
            print(a)
            a = ""
            print(tweets[i].text) 
    if a != "":
        print(f"La personne n'est pas mentionnée ou n'existe pas.")  

def user_mentionnant_hashtag(k):
    """ mettre le hashtags voulu"""
    print(f"les utilisateurs mentionnant le hashtag {k} sont :")
    for i in range(len(tweets)):
        if k in tweets[i].text:
            print(f"{tweets[i].author}")

def user_mentionne_par_user(k):
    """mettre auteur id pour k"""
    a = f"les mentions de {k} sont :"
    for i in range(len(tweets)):
        if k == tweets[i].author and len(tweets[i].mentions) != 0:
            for j in range(len(tweets[i].mentions)):
                print(a)
                a = ""
                print(f"{tweets[i].mentions[j]}")
    if a != "":
        print("L'utilisateur n'est pas mentionné ou n'existe pas")

def stats():
    p = input("L’ensemble de tweets d’un utilisateur spécifique : 1\nL’ensemble de tweets mentionnant un utilisateur spécifique : 2\nLes utilisateurs mentionnant un hashtag spécifique : 3\nLes utilisateurs mentionnés par un utilisateur spécifique : 4\nMenu : 5\n")
    while True:
        if p == "1":
            break
        elif p == "2":
            break
        elif p == "3":
            break
        elif p == "4":
            break
        elif p == "5":
            break
        else : 
            p = input("erreur !\nL’ensemble de tweets d’un utilisateur spécifique : 1\nL’ensemble de tweets mentionnant un utilisateur spécifique : 2\nLes utilisateurs mentionnant un hashtag spécifique : 3\nLes utilisateurs mentionnés par un utilisateur spécifique : 4\nMenu : 5\n")
    p = int(p)
    if p == 1:
        k = input("Entrer l'id d'un utilisateur. ")
        while True:
            try:
                k = int(k)
                break
            except ValueError:
                k = input("Entrer un id valide d'utilisateur avec des chiffres ")
        print("")
        tweet_de_auteur(k)
        input("...")
        print("")
        stats()
    elif p == 2:
        k = input("Entrer le nom d'un utilisateur mentionné. @")
        print("")
        tweet_mentionnant_user(k)
        input("...")
        print("")
        stats()
    elif p == 3:
        k = input("Entrer un hashtag. #")
        print("")
        user_mentionnant_hashtag(k)
        input("...")
        print("")
        stats()
    elif p == 4:
        k = input("Entrer un utilisateur. ")
        while True:
            try:
                k = int(k)
                break
            except ValueError:
                k = input("Entrer un id valide d'utilisateur avec des chiffres ")
        print("")
        user_mentionne_par_user(k)
        input("...")
        print("")
        stats()
    else :
        print("")
        menu()
        
def top():
    p = input("Top K hashtags : 1\nTop K utilisateurs : 2\nTop K utilisateurs mentionnés : 3\nLe nombre de publications par utilisateur : 4\nLe nombre de publications par hashtag : 5\nMenu : 6\n")
    while True:
        if p == "1":
            break
        elif p == "2":
            break
        elif p == "3":
            break
        elif p == "4":
            break
        elif p == "5":
            break
        elif p == "6":
            break
        else : 
            p = input("erreur !\nTop K hashtags : 1\nTop K utilisateurs : 2\nTop K utilisateurs mentionnés : 3\nLe nombre de publications par utilisateur : 4\nLe nombre de publications par hashtag : 5\nMenu : 6\n")
    p = int(p)
    if p == 1:
        k = input("Entrer un entier. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                if k == "all":
                    break
                else :
                    k = input("erreur\nEntrer un entier. ") 
        print("")
        top_hashtags(k)
        input("...")
        print("")
        top()
    elif p == 2:
        k = input("Entrer un entier. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                if k == "all":
                    break
                else :
                    k = input("erreur\nEntrer un entier. ")
        print("")
        top_user(k)
        input("...")
        print("")
        top()
    elif p == 3:
        k = input("Entrer un entier. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                if k == "all":
                    break
                else :
                    k = input("erreur\nEntrer un entier. ")
        print("")
        top_mentions(k)
        input("...")
        print("")
        top()
    elif p == 4:
        print("")
        nb_tweet_auteur()
        input("...")
        print("")
        top()
    elif p == 5:
        print("")
        nb_tweet_hashtags()
        input("...")
        print("")
        top()
    else:
        print("")
        menu()

def traitement():
    p = input("Auteur de la publication : 1\nListe de hashtags de la publication : 2\nListe des utilisateurs mentionnés dans la publication : 3\nSentiment de la publication : 4\nText publication : 5\nMenu : 6\n")
    while True:
        if p == "1":
            break
        elif p == "2":
            break
        elif p == "3":
            break
        elif p == "4":
            break
        elif p == "5":
            break
        elif p == "6":
            break
        else:
            p = input("erreur !\nAuteur de la publication : 1\nListe de hashtags de la publication : 2\nListe des utilisateurs mentionnés dans la publication : 3\nSentiment de la publication : 4\nText publication : 5\nMenu : 6\n")
    p = int(p)
    if p == 1:
        k = input(f"Il y a de 0 à {len(tweets)-1} tweets\nEntrer le numéro du tweet. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                k = input("erreur\nEntrer un entier. ") 
        print("")
        auteur_publication(k)
        input("...")
        print("")
        traitement()
    elif p == 2:
        k = input(f"Il y a de 0 à {len(tweets)-1} tweets\nEntrer le numéro du tweet. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                k = input("erreur\nEntrer un entier. ") 
        print("")
        hashtags_publication(k)
        input("...")
        print("")
        traitement()
    elif p == 3:
        k = input(f"Il y a de 0 à {len(tweets)-1} tweets\nEntrer le numéro du tweet. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                k = input("erreur\nEntrer un entier. ") 
        print("")
        user_mention_publication(k)
        input("...")
        print("")
        traitement()
    elif p == 4:
        k = input(f"Il y a de 0 à {len(tweets)-1} tweets\nEntrer le numéro du tweet. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                k = input("erreur\nEntrer un entier. ") 
        print("")
        sentiment_publication(k)
        input("...")
        print("")
        traitement()
    elif p == 5:
        k = input(f"Il y a de 0 à {len(tweets)-1} tweets\nEntrer le numéro du tweet. ")
        while True:
            try : 
                k = int(k)
                break
            except ValueError :
                k = input("erreur\nEntrer un entier. ") 
        print("")
        text_publication(k)
        input("...")
        print("")
        traitement()
    else:
        print("")
        menu()

def menu():
    p = input("Stats : 1\nTop : 2\nTraitement de données : 3\nStop : 4\n")
    while True:
        if p == "1":
            break
        elif p == "2":
            break
        elif p == "3":
            break
        elif p == "4":
            break
        else : 
            p = input("erreur !\nStats : 1\nTop : 2\nTraitement de données : 3\n")
    p = int(p)
    
    #stat
    if p == 1:
        print("")
        stats()

    #top
    elif p == 2:
        print("")
        top()
    #traitement
    elif p == 3:
        print("")
        traitement()
    else :
        pass

menu()
