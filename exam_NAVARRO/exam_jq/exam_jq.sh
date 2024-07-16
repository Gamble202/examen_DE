echo "1.a Affichez le nombre d'attributs par document ainsi que l'attribut name. Combien y a-t-il d'attribut par document ? N'affichez que les 12 premières lignes avec la commande head (notebook #2)."
cat people.json | jq .[] | jq '.name, length' | head -n 12 > res_jq.txt
echo "Commande: cat people.json | jq .[] | jq '.name, length'"
echo "Réponse : il y a 17 attributes par document"
echo -e "\n---------------------------------\n"

echo "2. Combien y a-t-il de valeur "unknown" pour l'attribut "birth_year" ? Utilisez la commande tail afin d'isoler la réponse."
cat people.json | jq '[.[] | select(.birth_year == "unknown")] | length' | tail -n 1 >> res_jq.txt
echo "Commande : cat people.json | jq '[.[] | select(.birth_year == "unknown")] | length'"
echo "Réponse : 42, je n'ai pas utilisé de tail car la reponse n'a qu'une ligne..."
echo -e "\n---------------------------------\n"

echo "3. Affichez la date de création de chaque personnage et son nom. La date de création doit être de cette forme : l'année, le mois et le jour. N'affichez que les 10 premières lignes."
cat people.json | jq '.[] | {name:.name, created:(.created | sub("\\.[0-9]{6}Z"; "") |strptime("%Y-%m-%dT%H:%M:%S")| strftime("%Y-%m-%d"))}'|head -n 10 >> res_jq.txt
echo "Commande : jq '{name:.name, created:(.created | sub("\\.[0-9]{6}Z"; "")  |strptime("%Y-%m-%dT%H:%M:%S")| strftime("%Y-%m-%d"))}'|head -n 10"
echo "Commentaire : J'ai du supprimer les miliseconds sur 6 digits avec une regExp, car elle ne collait pas avec le strptime de jq qui, apparement, gere cette donnée sur 3 digits"
echo -e "\n---------------------------------\n"

echo "4. Certains personnages sont nés en même temps. Retrouvez toutes les pairs d'ids (2 ids) des personnages nés en même temps."
cat people.json | jq '[group_by(.birth_year)[] | {birth: .[0].birth_year, ids:[.[].id]}]' >> res_jq.txt
echo "Commande : cat people.json | jq '[group_by(.birth_year)[] | {birth: .[0].birth_year, ids:[.[].id]}]'"
echo "Commentaire : Le mieux que j'ai pu faire a été de grouper les ids par date."
echo "je ne vois pas (encore) comment faire toutes les paires d'id, mais je veux bien que l'on m'explique. =)"
echo -e "\n---------------------------------\n"

echo "5. Renvoyez le numéro du premier film (de la liste) dans lequel chaque personnage a été vu suivi du nom du personnage. N'affichez que les 10 premières lignes."
cat people.json | jq '[.[] | (.films[0]|sub("http://swapi.co/api/films/";"")|sub("/";"")), .name]'  | head -n 11 >> res_jq.txt
echo "Commande : cat people.json | jq '[.[] | (.films[0]|sub("http://swapi.co/api/films/";"")|sub("/";"")), .name]'  | head -n 10"
echo -e "\n---------------------------------\n"

echo "5 BONUS. le numéro du premier film (de la série) dans lequel chaque personnage a été vu suivi du nom du personnage."
cat people.json | jq '[.[] | ((.films | sort |.[0])|sub("http://swapi.co/api/films/";"")|sub("/";"")), .name]' >> res_jq.txt
echo "Commande : cat people_light.json | jq '[.[] | ((.films | sort |.[0])|sub("http://swapi.co/api/films/";"")|sub("/";"")), .name]'"


