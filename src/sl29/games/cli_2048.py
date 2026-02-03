"""
Interface en ligne de commande (CLI) pour tester le jeu 2048.

Ce fichier permet de vérifier le bon fonctionnement de la logique
sans interface graphique.
"""

import os
import argparse
from typing import List

from sl29.games._2048 import (
    nouvelle_partie,
    jouer_coup,
)
def afficher_score(score: int) -> None:
    """
    Affiche le score du jeu dans le terminal.

    :param score: Le score actuel du jeu.
    :type score: int
    """
    print(f"SCORE : {score}")

def afficher_plateau(plateau: List[List[int]]) -> None:
    """
    Affiche le plateau de jeu dans le terminal.

    :param plateau: La grille actuelle du jeu, représentée par une liste de listes d'entiers.
    :type plateau: List[List[int]]
    """
    print()
    for ligne in plateau:
        for valeur in ligne:
            if valeur == 0:
                print(".", end="\t")
            else:
                print(valeur, end="\t")
        print()
    print()

def demander_commande() -> str:
    """
    Demande une commande à l'utilisateur via l'entrée standard.

    :return: La commande saisie par l'utilisateur (en minuscules et sans espaces).
    :rtype: str
    """
    print("Commandes :")
    print("  g = gauche | d = droite | h = haut | b = bas | q = quitter")
    return input("Votre choix : ").strip().lower()


def _clear_terminal() -> None:
    """
    Efface le contenu du terminal en utilisant la commande système appropriée.

    Cette fonction utilise 'clear' sur les systèmes Unix-like.
    Sur Windows, elle pourrait nécessiter une adaptation, mais ici elle est conçue pour Linux/Mac.
    """
    os.system("clear")

def jouer() -> None:
    """
    Lance une partie interactive de 2048 en mode texte dans le terminal.

    La fonction gère la boucle de jeu, affiche le plateau et le score,
    traite les commandes utilisateur, et vérifie la fin de partie.
    Supporte l'option --no-clear pour désactiver le nettoyage du terminal.
    """
    jeu = nouvelle_partie()

    # Le clear est maintenant activé par défaut
    clear = True
    try:
        parser = argparse.ArgumentParser(add_help=False)
        # On change l'argument pour permettre de désactiver le nettoyage
        parser.add_argument("--no-clear", action="store_true", help="Désactiver le nettoyage du terminal")
        args, _ = parser.parse_known_args()

        # Si --no-clear est présent, clear devient False
        if args.no_clear:
            clear = False
    except Exception:
        # En cas d'erreur, on reste sur True par sécurité
        clear = True
    while True:
        if clear:
            _clear_terminal()
        afficher_score(score)
        afficher_plateau(plateau)

        commande = demander_commande()
        if commande in ('g', 'd', 'b', 'h'):
            jeu = jouer_coup(jeu, commande)
            plateau = jeu.plateau
            score = jeu.score
            fini = jeu.fini
            if fini:

                if clear:
                    _clear_terminal()
                afficher_score(score)
                afficher_plateau(plateau)
                print("Plus de place ni de fusion possible : Fin de la partie.")
                break
        elif commande == 'q':
            print("Je quitte le jeu.")
            break
        else:
            print("Entrée incorrecte.")


if __name__ == "__main__":
    jouer()
