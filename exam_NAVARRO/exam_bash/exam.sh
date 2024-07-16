#!/bin/bash

# #####################
#   DECLARATIONS
# #####################

OUTPUT_FOLDER="/home/ubuntu/exam_NAVARRO/exam_bash/"
OUTPUT_FILE="sales.txt"
URI="http://0.0.0.0:5000/" 
# Array contenant les modeles de cartes pour faciliter l'ajout/retrait de model de CG
cardModel_lst=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")

# printToFile_cardSale() -> void
    # appel api
    # extraction de la donnée du retour 
    # ecriture dans le OUTPUT_FILE
function printToFile_cardSale(){
    # Appel API
    api_return=$(curl -s $URI$1)
    # ecriture fichier out
    # On peux faire plus court mais c'est moins lisible -> echo "$1:$(curl $URI$1)" >> $OUTPUT_FOLDER$OUTPUT_FILE  
    echo "$1:$api_return" >> $OUTPUT_FOLDER$OUTPUT_FILE 
}


# #####################
#   DEBUT DU SCRIPT
# #####################

# ecriture de la date
echo "$(date)" >> $OUTPUT_FOLDER$OUTPUT_FILE
# ecriture données pour toutes les carte de l'array cardModel_lst
for card in ${cardModel_lst[@]}; do
    printToFile_cardSale $card 
done





