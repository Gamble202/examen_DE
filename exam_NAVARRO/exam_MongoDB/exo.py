from pymongo import MongoClient
from pprint import pprint
import re
import datetime

print ("_Connexion à la base de données_")
print("\n----------------------------------------------------------")
print ("(a) Pour se connecter à MongoDB via pymongo, ajoutez l\'authentification aux lignes de codes suivantes puis lancez-les")
# A
client = MongoClient(
    host="127.0.0.1",
    port = 27017,
    username = "datascientest",
    password = "dst123" 
)

# B
print("\n----------------------------------------------------------")
print("\n(b) Afficher la liste des bases de données disponibles.:")
print(client.list_database_names())

# C
print("\n----------------------------------------------------------")
print("\n(c) Afficher la liste des collections disponibles dans cette base de données (sample).")
db_str = "sample"
print("\nListe des collections disponibles dans:" + db_str)
db = client[db_str]
print(db.list_collection_names())

#D
print("\n----------------------------------------------------------")
print("\n(d) Afficher un des documents de cette collection (books).")
books = db["books"]
pprint(books.find_one())

# E
print("\n----------------------------------------------------------")
print("\nAfficher le nombre de documents dans book: ", books.count_documents({}))

print("\n----------------------------------------------------------")
print ("\n_Exploration de la base_")
print("\n----------------------------------------------------------")

print ("\n(a) Afficher le nombre de livres avec plus de 400 pages:",books.count_documents({"pageCount": {"$gte":400}}))
print ("\naffichez ensuite le nombre de livres ayant plus de 400 pages ET qui sont publiés: ",books.count_documents({"pageCount": {"$gte":400}, "status": "PUBLISH"}))

print("\n----------------------------------------------------------")
print ("\n(b) Afficher le nombre de livres ayant le mot-clé Android dans leur description (brève ou longue).")
print(books.count_documents({"$or": [{"shortDescription": re.compile("Android")}, {"longDescription": re.compile("Android")}]}))

print("\n----------------------------------------------------------")
print("\n(c) Chaque document possède un attribut categories qui est une liste. Vous devez grouper tous les documents en un à l'aide de l'opérateur $group. Puis, à l'aide de l'opérateur $addToSet, créez 2 set à partir des catégories contenus dans la liste categories selon leur index 0 ou 1. Pour cibler, les catégories utilisez l'opérateur $arrayElemAt.")

pprint(list(books.aggregate(
            [
                {"$group": {
                    "_id": "$categories",
                    "set_0": {"$addToSet":{"$arrayElemAt":["$categories",0]}},
                    "set_1": {"$addToSet":{"$arrayElemAt":["$categories",1]}},
                }},
                {"$project": {"_id":0, "categories": 1, "set_0":1, "set_1":1}}
            ]
        )
    ))


print("\n----------------------------------------------------------")
print("\n_n(d) Afficher le nombre de livres qui contiennent des noms de langages suivant dans leur description longue:") 
print("Python, Java, C++, Scala. On pourra s'appuyer sur des expressions régulières et une condition or.")
print(books.count_documents({"$or": [{"longDescription": re.compile("Python")}, {"longDescription": re.compile("Java")}, {"longDescription": re.compile("C\+\+")}, {"longDescription": re.compile("Scala")}]}))


print("\n----------------------------------------------------------")
print("(e) Afficher diverses informations statistiques sur notre bases de données : nombre maximal, minimal, et moyen de pages par catégorie. On utilisera une pipeline d'aggregation, le mot clef $group, ainsi que les accumulateurs appropriés. N\'oubliez pas d'aller voir \"$unwind\" pour ce problème.")
pprint(list(
    books.aggregate([
        {"$unwind":"$categories"},
        {
            "$group": {
                "_id": "$categories",  # Nous groupons tous les documents ensemble
                "page_max": {"$max": "$pageCount"},
                "page_min": {"$min": "$pageCount"},
                "page_moy": {"$avg": "$pageCount"}
            }
        }
    ])
))
print("\n----------------------------------------------------------")
print("(f) Via une pipeline d'aggrégation, Créer de nouvelles variables en extrayant info depuis l'attribut dates : année, mois, jour. On rajoutera une condition pour filtrer seulement les livres publiés après 2009. N'affichez que les 20 premiers.")

pprint(list(
    books.aggregate([
        {"$match" : {"publishedDate":{"$gt":datetime.datetime(2009,12,31)}}},
        {"$project":{"_id":0, "annee": {"$year":"$publishedDate"}, "mois":{"$month":"$publishedDate"}, "jour":{"$dayOfMonth":"$publishedDate"}}},
        {"$limit": 20}
    ])
))
print("\n----------------------------------------------------------")
print("(g) À partir de la liste des auteurs, créez de nouveaux attributs (author_1, author_2 ... author_n). Observez le comportement de \"$arrayElemAt\". N\'affichez que les 20 premiers dans l\'ordre chronologique.")
print("Commentaire: je n'ai pas reussi a faire une creation de nom de champs dynamique sans passer par python, ni filtrer les author = ''")
pprint(list(
    db.books.aggregate([
        {"$set":{
            "author_1":{ "$arrayElemAt": [ "$authors", 0 ] },
            "author_2":{ "$arrayElemAt": [ "$authors", 1 ] },
            "author_3":{ "$arrayElemAt": [ "$authors", 2 ] },
            "author_4":{ "$arrayElemAt": [ "$authors", 3 ] },
            "author_5":{ "$arrayElemAt": [ "$authors", 4 ] },
            "author_6":{ "$arrayElemAt": [ "$authors", 5 ] }
        }},
        {"$project":{"_id":0}},
        {"$sort":{"publishedDate":1}},
        {"$limit": 20}
    ])
))

print("\n----------------------------------------------------------")
print ("(h) En s\'inspirant de la requête précédente, créer une colonne contenant le nom du premier auteur, puis agréger selon cette colonne pour obtenir le nombre d'articles pour chaque premier auteur. Afficher le nombre de publications pour les 10 premiers auteurs les plus prolifiques. On pourra utiliser un pipeline d'agrégation avec les mots-clefs $group, $sort, $limit.")

pprint(list(
    db.books.aggregate([
        {"$set":{
            "author_1":{ "$arrayElemAt": [ "$authors", 0 ] }
        }},
        {"$group":{"_id":"$author_1", "nbArticle":{"$sum" : 1}}},
        {"$sort":{"nbArticle":-1}},
        {"$project":{"_id":0}},
        {"$limit": 10}
    ])
))

print("\n----------------------------------------------------------")
print("(i) [OPTIONNEL] Afficher la distribution du nombre d'auteurs : Commencer par créer une nouvelle colonne avec le nombre d\'auteurs (taille de la liste de l\'attribut authors ), puis agrégez sur cette colonne avec l\'accumulateur $count ou $sum.")

pprint(list(
    db.books.aggregate([
        {"$set":{
            "author_count":{"$size":"$authors"}
        }},
        {"$group":{"_id":"$author_count", "nbAuthor":{"$first":"$author_count"}, "nbArticles":{"$count" : {}}}},

        #{"$sort":{"nbArticle":-1}},
        {"$project":{"_id":0, "nbAuthor":1, "nbArticles":1}},
        {"$limit": 10}
    ])
))





