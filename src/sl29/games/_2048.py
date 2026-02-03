"""Module providing the logic of the 2048 game"""

from random import randint
from typing import List, Tuple

# ==========================================================
# 🔒 FONCTIONS PRIVÉES (LOGIQUE INTERNE)
# ==========================================================

def _supprimer_zeros(ligne: List[int]) -> List[int]:
    """
    Supprime les zéros d'une ligne.

    :param ligne: Une ligne de la grille.
    :type ligne: List[int]
    :return: La ligne sans zéros.
    :rtype: List[int]
    """
    return [nombre for nombre in ligne if nombre != 0]

def _fusionner(ligne: List[int]) -> Tuple[List[int], int]:
    """
    Fusionne les valeurs identiques consécutives d'une ligne.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: La ligne après fusion, les points gagnés
    :rtype: Tuple[List[int], int]
    """
    fusion = []
    i = 0
    points = 0
    while i < len(ligne):
        if i+1 < len(ligne) and ligne[i+1] == ligne[i]:
            points += 2*ligne[i]
            fusion.append(ligne[i]*2)
            i += 2
        else:
            fusion.append(ligne[i])
            i += 1
    return fusion,points

def _completer_zeros(ligne,taille): # ajouter les annotations de type
    """
    Complète la ligne avec des zéros.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :param taille: Taille de la grille de jeu
    :type taille: int
    :return: La ligne après complétion
    :rtype: List[int]
    """
    return ligne.copy() + (taille-len(ligne))*[0]

class game_2048:
    def __init__(self,plateau=[],taille=4):
        self._plateau = plateau
        if plateau == [] and not self._is_valid():
            self._taille = taille
            self._plateau = self._creer_plateau_vide()
        else:
            self._taille = len(plateau)
        self._plateau_pre = []
        self._score = 0
        self._fini = self._partie_terminee()

    @property
    def taille(self):
        return self._taille
    
    @property
    def plateau(self):
        return self._plateau
    
    @property
    def score(self):
        return self._score
    
    @property
    def fini(self):
        return self._fini
    
    @property
    def plateau_pre(self):
        return self._plateau_pre
    
    def _is_valid(self)->bool:
        """
        Le plateau courant est-il correct ?
        :return: Si le plateau es correct
        :rtype: bool
        """
        long = len(self.plateau)
        for ligne in self.plateau:
            if len(ligne) != long:
                return False
        return True

    def _creer_plateau_vide(self) -> List[List[int]]:
        """
        Crée une grille TAILLExTAILLE remplie de zéros.
        :return: Une grille vide.
        :rtype: List[List[int]]
        """
        return [[0 for _ in range(self.taille)] for _ in range(self._taille)]

    def _get_cases_vides(plateau: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Retourne les coordonnées des cases vides sous forme d'une liste de coordonnées

        :param plateau: La grille actuelle.
        :type plateau: List[List[int]]
        :return: Une liste de coordonnées
        :rtype: List[Tuple[int, int]]
        """
        return [(i,j) for i in range(len(plateau)) for j in range(len(plateau)) if plateau[i][j] == 0]

    def _ajouter_tuile(self):
        """
        Ajoute une tuile de valeur 2 sur une case vide.
        """
        tuiles_vides = self._get_cases_vides()
        endroit = tuiles_vides[randint(0,len(tuiles_vides)-1)]
        plateau = self.plateau
        self._plateau = [[plateau[i][j] if (i,j) != endroit else (2 if randint(0,9) > 0 else 4) for j in range(len(plateau))] for i in range(len(plateau))]

    def _deplacer_gauche(self,plateau) : # ajouter les annotations de type
        """
        Crée la nouvelle grille lors d'un déplacement sur la gauche

        :param plateau: La grille actuelle.
        :type plateau: List[List[int]]
        :return: La grille après déplacement, les points gagnés
        :rtype: Tuple[List[List[int]], int]
        """
        nouv_plateau = []
        nouv_points = 0
        for ligne in plateau:
            ligne_sans_zero = _supprimer_zeros(ligne)
            ligne_fus,points = _fusionner(ligne_sans_zero)
            nouv_points += points
            ligne_fin = _completer_zeros(ligne_fus,self.taille)
            nouv_plateau.append(ligne_fin)
        return nouv_plateau,nouv_points

    def _inverser_lignes(self): # ajouter les annotations de type
        """
        Crée la grille symetrique par rapport aux ordonées

        :param plateau: La grille actuelle.
        :type plateau: List[List[int]]
        :return: La grille après changements
        :rtype: List[List[int]]
        """
        plateau = self.plateau
        return [ligne.copy()[::-1] for ligne in plateau]

    def _deplacer_droite(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Déplace les tuiles vers la droite en fusionnant les valeurs identiques.

        :param plateau: La grille actuelle du jeu.
        :type plateau: List[List[int]]
        :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
        :rtype: Tuple[List[List[int]], int]
        """
        grille,points = _deplacer_gauche(_inverser_lignes(plateau))
        return _inverser_lignes(grille),points

    def _transposer(plateau): # ajouter les annotations de type
        """
        Crée la grille transposée

        :param plateau: La grille actuelle.
        :type plateau: List[List[int]]
        :return: La grille après changements
        :rtype: List[List[int]]
        """
        return [[plateau[j][i] for j in range(len(plateau))] for i in range(len(plateau))]

    def _deplacer_haut(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Déplace les tuiles vers le haut en fusionnant les valeurs identiques.

        :param plateau: La grille actuelle du jeu.
        :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
        """
        grille,points = _deplacer_gauche(_transposer(plateau))
        return _transposer(grille),points


    def _deplacer_bas(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Déplace les tuiles vers le bas en fusionnant les valeurs identiques.

        :param plateau: La grille actuelle du jeu.
        :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
        """
        grille,points = _deplacer_droite(_transposer(plateau))
        return _transposer(grille),points

    def _partie_terminee(plateau: List[List[int]]) -> bool:
        """
        Retourne si la partie est finie

        :param plateau: La grille actuelle du jeu.
        :return: Un booleen si la partie est finie ou pas
        """
        # Partie non terminee si il y a des cases vides
        if len(_get_cases_vides(plateau)) > 0:
            return False
        # Partie non terminee si il y a des fusions possibles (horizontale ou verticale)
        for plateau_c in (plateau,_transposer(plateau)):
            for ligne in plateau_c:
                last = ligne[0]
                for i in range(1,len(ligne)):
                    if ligne[i] == last:
                        return False
                    last = ligne[i]
        # Sinon c'est vrai
        return True


# ==========================================================
# 🎯 FONCTION PUBLIQUE (API POUR L’INTERFACE)
# ==========================================================

def nouvelle_partie(taille = 4) -> Tuple[List[List[int]], int]:
    """
    Crée une nouvelle partie du jeu 2048.
    :param plateau: la taille du plateau à créer
    :type taille: int
    :return: Une grille taille x taille initialisée avec deux tuiles, ainsi que le score à 0.
    :rtype: Tuple[List[List[int]], int]
    """
    game = game_2048(taille)
    for _ in range(2):
        game._ajouter_tuile()
    return game.plateau

def jouer_coup(jeu: game_2048, direction: str) -> game_2048:
    """
    Effectuer un mouvement sur le plateau.

    :param jeu: Le jeu.
    :type jeu: game_2048
    :param direction: La direction du déplacement : 'g' (gauche), 'd' (droite), 'h' (haut), 'b' (bas).
    :type direction: str
    :return: Retourne le jeu après déplacement.
    :rtype: game_2048
    """
    fonctions = {'g':jeu._deplacer_gauche,'d':jeu._deplacer_droite,'h':jeu._deplacer_haut,'b':jeu._deplacer_bas}
    if direction in fonctions.keys():
        plateau_avant_dep = jeu.plateau
        fonctions[direction]()
        if jeu.plateau != plateau_avant_dep:
            jeu._ajouter_tuile()
        return jeu
