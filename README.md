# WikiBooks : ETL d'extraction des données sur Books to Scrape
depuis le dossier des application de la société 
se positionner dans le dossier qui contient le depot git:
cd OCR_P02_WikiBooks

## Créer et activer l'environnement virtuel venv
## Saisir les commmandes ci-dessous:
python -m venv env
source env/bin/activate

## Installer les packages à partir de requirements.txt
pip install -r requirements.txt

## Verifier que les packages sont bien installés en comparant avec requirements.txt
pip freeze
le resultalt doit contenir a minima:
beautifulsoup4==4.13.4
requests==2.32.3

## se positionner dans le dossier src puis lancer le programme:
cd src
python src/scrapt_book.py

## Execution du programme
lorsque le programme sera terminé, il aura créé :
1. un dossier log contenant les logs de chaque execution du programme
2. un dossier data/output contenant le fichier csv wikibooks.csv qui 
contient l'extration des données de tous les livres du site
3. un dossier data/output/images contenant une arborescen de dossiers par catégories avec les images des livres de chaque catégorie

