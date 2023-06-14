#!/usr/bin/env python
# coding: utf-8

# ---
# ## Sorbonne Université
# # <center> Mathématiques discrètes </center>
# ## <center> LU2IN005 </center>
# ## <div style="text-align:right;"> Année 2022-2023 </div>
# ---

# ---
# # <center> TME programmation d'automates finis </center>
# L'objectif de ce TME est de programmer en python quelques uns des
# algorithmes pour les automates finis vus en cours et en TD, en
# utilisant des structures de données fournies dans le code mis à votre
# disposition.
# ---
# # Consignes
# Copiez dans votre répertoire de travail les fichiers présents dans le Dossier 
# *Fichiers Python fournis* de la page Moodle de l'UE.
# 
# Ils contiennent les définitions de structures de données décrites
# ci-dessous, ainsi que des aide-mémoire sur l'utilisation de python.
# 
# **Le seul fichier que vous êtes autorisés à modifier** est celui-ci, c'est-à-dire
# `automate_etudiant.ipynb`, partiellement prérempli. 
# Les instructions `return` sont à supprimer lorsque
# vous remplirez le contenu des différentes fonctions.  Les autres
# fichiers n'ont pas besoin d'être lus (mais ils peuvent l'être).
# Si votre programme nécessite de lire des fichiers, **ceux-ci doivent être enregistrés dans le répertoire ExemplesAutomates** que vous avez téléchargé.
# ---

# _Binôme_
# ----------
# 
# **NOM**: XIA
# 
# **Prénom**: Tianxiang
# 
# **Numéro d'étudiant**: 21114252
# 
# **NOM**: SERRANO
# 
# **Prénom**: Jean-léo
# 
# **Numéro d'étudiant**: 21105113

# ### Table des matières
# 
# > [1. Présentation](#sec1)
# >> [1.1 La classe `State`](#sec1_1) <br>
# >> [1.2 La classe `Transition`](#sec1_2) <br>
# >> [1.3 La classe `Automate`](#sec1_3)
# 
# > [2. Prise en mains](#sec2)
# >> [2.1 Création d'automates](#sec2_1) <br>
# >> [2.2 Premières manipulations](#sec2_2) <br>
# 
# > [3. Exercices de base : tests et complétion](#sec3)
# 
# > [4. Déterminisation](#sec4)
# 
# > [5. Constructions sur les automates réalisant des opérations sur les langages acceptés](#sec5)
# >> [5.1 Opérations ensemblistes sur les langages](#sec5_1) <br>
# >> [5.2 Opérations rationnelles sur les langages](#sec5_2)

# In[1]:


## Import des bibliothèques nécessaires au projet.
## Ne pas modifier les fichiers "bibliothèque".

## Interpréter cette cellule avant de continuer.

from transition import *
from state import *
import os
import copy
from automateBase import AutomateBase

class Automate(AutomateBase):
    pass


# In[2]:


from functools import reduce
from random import randint, choice


# ### 1. Présentation  <a class="anchor" id="sec1"></a>
# 
# Le projet utilise le langage python avec une syntaxe légèrement
# différente de celle vue en **LU1IN001 / 011**, parce qu'il exploite en particulier
# la notion de classes d'objets. Une introduction à cette notion est présentée dans le livre associé
# au cours : cf [Chapitre 13](https://www-licence.ufr-info-p6.jussieu.fr/lmd/licence/2021/ue/LU1IN001-2021oct/cours2020.pdf).
# 
# De plus, le typage des variables est noté de façon légèrement différente, en commentaires, pour les déclarations
# comme pour les arguments des fonctions. Pour ces derniers, les types sont indiqués dans la première ligne de la documentation de la fonction.
# 
# Les particularités sont brièvement expliquées en annexe
# de ce document. Par ailleurs, vous trouverez dans la section
# `projet` de la page Moodle un mémo sur la syntaxe python, ainsi que la carte de
# référence du langage utilisée en **LU1IN001 / 011**.  On rappelle qu'une ligne
# commençant par `#` est un commentaire, ignoré par
# l'interpréteur.
# 
# Toutes les structures de données nécessaires à la construction des
# automates sont fournies sous la forme de classes python, pour les
# transitions d'un automate, ses états, et les automates
# eux-mêmes. Cette section indique comment les utiliser.

# #### 1.1 La classe `State` <a class="anchor" id="sec1_1"></a>
# 
# Un état est représenté par
# - un entier `id` (type `int`) qui définit son identifiant,
# - un booléen `init` (type `bool`) indiquant si c'est un état initial,
# - un booléen `fin` (type `bool`) indiquant si c'est un état final,
# - une chaîne de caractères `label` (type `str`) qui définit son étiquette, permettant de le *décorer*. Par défaut, cette variable est la version chaîne de caractères de l'identifiant de l'état. 
# 
# On définit l'alias de type `State` pour représenter les variables de ce type. 
# 
# Ainsi, l'instruction ci-dessous crée une variable `s` représentant un état d'identifiant `1`, qui est un état initial mais pas final, dont l'identifiant et l'étiquette  `1` :

# In[3]:


# s : State
s = State(1, True, False)


# Si l'on souhaite avoir une étiquette différente de l'identifiant, on
# utilise un quatrième argument :

# In[4]:


s = State(1, True, False, 'etat 1') 


# On accède ensuite aux différents champs de `s` par la notation pointée : exécutez les cellules suivantes pour observer l'affichage obtenu.

# In[5]:


print('La valeur de s.id est : ')
print(s.id)


# In[6]:


print('La valeur de s.init est : ')
print(s.init)


# In[7]:


print('La valeur de s.fin est : ')
print(s.fin)


# In[8]:


print('La valeur de s.label est : ')
print(s.label)


# In[9]:


print("L'affichage de s est : ")
print(s)


# Ainsi, une variable de type `State` est affichée par son étiquette et, entre parenthèses, si c'est un état initial et/ou final.

# #### 1.2 La classe `Transition` <a class="anchor" id="sec1_2"></a>
# 
# Une transition est représentée par 
# - un état `stateSrc` (type `State`) correspondant à son état de départ
# - un caractère `etiquette` (type `str`) donnant son   étiquette
# - un état `stateDest` (type `State`) correspondant à son état de destination
# 
# On définit l'alias de type `Transition` pour représenter les variables de ce type.
# 
# La séquence d'instructions suivante crée la transition d'étiquette `"a"` de l'état `s` (défini ci-dessus) vers lui-même et affiche les différents champs de la transition :

# In[10]:


# t : Transition
t = Transition(s, "a", s)


# In[11]:


print('La valeur de t.etiquette est : ')
print(t.etiquette)


# In[12]:


print("L'affichage de t.stateSrc est : ")
print(t.stateSrc)


# On remarque que la variable `stateSrc` est de type `State`, on obtient donc un état, et non uniquement un
# identifiant d'état. 

# In[13]:


print("L'affichage de t.stateDest est : ")
print(t.stateDest)


# In[14]:


print("L'affichage de t est : ")
print(t)


# #### 1.3 La classe `Automate` <a class="anchor" id="sec1_3"></a>
# 
# Un automate est représenté par
# - l'ensemble de ses transitions `allTransitions` (de type `set[Transition]`) 
# - l'ensemble de ses états `allStates` (de type `set[State]`)
# - une étiquette `label` (de type `str`) qui est éventuellement vide.
# 
# On définit l'alias de type `Automate` pour représenter les variables de ce type.
# 
# Ainsi, de même que pour les classes précédentes, l'accès aux
# différents champs se fait par la notation pointée. Par exemple, on
# obtient l'ensemble des états d'un automate `monAutomate` par
# l'instruction `monAutomate.allStates`.
# 
# Pour créer un automate, il existe trois possibilités.

# **Création à partir d'un ensemble de transitions.**<br>
# On peut d'abord utiliser le constructeur de signature `Automate : set[Transition] -> Automate`.<br>
# Il déduit alors l'ensemble des états à partir de l'ensemble des transitions et définit par défaut l'étiquette
# de l'automate comme la chaîne de caractères vide.
# 
# Par exemple, en commençant par créer les états et les transitions nécessaires :

# In[15]:


## création d'états
# s1 : State
s1 = State(1, True, False)
# s2 : State
s2 = State(2, False, True)

## création de transitions
# t1 : Transition
t1 = Transition(s1,"a",s1)
# t2 : Transition
t2 = Transition(s1,"a",s2)
# t3 : Transition
t3 = Transition(s1,"b",s2)
# t4 : Transition
t4 = Transition(s2,"a",s2)
# t5 : Transition
t5 = Transition(s2,"b",s2)
# set_transitions : set[Transition]
set_transitions = {t1, t2, t3, t4, t5}

## création de l'automate
# aut : Automate
aut = Automate(set_transitions)


# L'affichage de cet automate, par la commande `print(aut)` produit alors le résultat suivant : 

# In[16]:


print(aut)


# Les états de l'automate sont déduits de l'ensemble de transitions.
# 
# Optionnellement, on peut donner un nom à l'automate, en utilisant la variable `label`, par exemple :

# In[17]:


# aut2 : Automate
aut2 = Automate(set_transitions, label="A") 

print(aut2)


# **Création à partir d'un ensemble de transitions et d'un ensemble d'états.**<br>
# Dans le second cas, on crée un automate à partir d'un ensemble de
# transitions mais aussi d'un ensemble d'états, par exemple pour représenter des
# automates contenant des états isolés. Pour cela, on utilise le
# constructeur `Automate : set[Transition] x set[State] -> Automate`.
# 
# On peut également, optionnellement, donner un nom à l'automate :

# In[18]:


# set_etats : set[State]
set_etats = {s1, s2}

# aut3 : Automate
aut3 = Automate(set_transitions, set_etats, "B")

print(aut3)


# L'ordre des paramètres peut ne pas être respecté **à la condition** que l'on donne leur nom explicitement. Ainsi, la ligne suivante est correcte :

# In[19]:


aut = Automate(setStates = set_etats, label = "A", setTransitions = set_transitions)

print(aut)


# **Création à partir d'un fichier contenant sa description.**<br>
# La fonction `Automate.creationAutomate : str -> Automate` prend en argument un nom de fichier qui décrit un automate et construit l'automate correspondant (voir exemple ci-dessous).
# 
# La description textuelle de l'automate doit suivre le format suivant (voir exemple ci-dessous) :
# - #E: suivi de la liste des noms des états, séparés par
#   des espaces ou des passages à la ligne. Les noms d'états peuvent
#   être n'importe quelle chaîne alphanumérique pouvant également
#   contenir le symbole `_`. Par contre, si le nom d'état
#   contient des symboles *non numériques* il ne doit pas commencer
#   par un chiffre, sous peine de provoquer une erreur à l'affichage.
#   Ainsi, `10` et `A1` sont des noms d'états possibles,
#   mais `1A` ne l'est pas.
# - #I: suivi de la liste des états initiaux
#   séparés par des espaces ou des passages à la ligne, 
# - #F: suivi de la liste des
#   états finaux séparés par des espaces ou des passages à la ligne, 
# - #T: suivi de la liste des transitions séparées par des
#   espaces ou des passages à la ligne. Chaque transition est donnée
#   sous le format `(etat1, lettre, etat2)`.
# 
# Par exemple le fichier `exempleAutomate.txt` contenant <br>
# `#E: 0 1 2 3`<br>
# `#I: 0`<br>
# `#F: 3`<br>
# `#T: (0 a 0)`<br>
# `	(0 b 0)`<br>
# `	(0 a 1)`<br>
# `	(1 a 2)`<br>
# `	(2 a 3)`<br>
# `	(3 a 3)`<br>
# `	(3 b 3)`<br>
# est formaté correctement. L'appel suivant produira l'affichage...

# In[20]:


# automate : Automate
automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
print(automate)


# **Fonctions de manipulation des automates.**<br>
# La classe automate contient également de nombreuses fonctions utiles. Elles
# s'appliquent à un objet de type `Automate` et s'utilisent donc sous la forme
# `aut.<`*fonction*`>(<`*parametres*`>)` où `aut` est une variable de type `Automate`.
# 

# - `show : float -> NoneType` <br> 
#     prend en argument facultatif un flottant (facteur de grossissement, par défaut il vaut 1.0) et produit une représentation graphique de l'automate.<br>
#     Ainsi, en utilisant l'automate défini dans le fichier d'exemple précédent, l'instruction `automate.show(1.2)` produit l'image suivante :

# In[21]:


automate.show(1.2)


# - `addTransition : Transition -> bool`<br>
#   prend en argument une transition `t`, fait la mise à jour de
#   l'automate en lui ajoutant `t` et ajoute les états impliqués
#   dans l'automate s'ils en sont absents. Elle rend `True` si l'ajout a
#   eu lieu, `False` sinon (si `t` était déjà présente dans l'automate).
#   
# - `removeTransition : Transition -> bool`<br>
#   prend en argument une transition `t` et fait la mise à jour de
#   l'automate en lui enlevant la transition, sans modifier les
#   états. Elle rend `True` si la suppression a eu lieu, `False` sinon (si
#   `t` était absente de l'automate).
# 
# - `addState : State -> bool`<br>
#   prend en argument un état `s` et fait la mise à jour de
#   l'automate en lui ajoutant `s`.  Elle rend `True` si l'ajout a eu
#   lieu, `False` sinon (si `s` était déjà présent dans l'automate).
# 
# - `nextId : -> int`<br>
#   renvoie un entier id frais, en choisissant l'entier le plus petit,
#   strictement supérieur à tous les id des états de l'automate.
# 
# - `removeState : State -> bool`<br>
#   prend en argument un état `s` et fait la mise à jour de
#   l'automate en supprimant `s` ainsi que toutes ses transitions
#   entrantes et sortantes.  Elle rend `True` si l'ajout a eu lieu, `False`
#   sinon (si `s` était absent de l'automate).
#   
# - `getSetInitialStates :  -> set[State]`<br> 
#   rend l'ensemble des états initiaux.
# 
# - `getSetFinalStates :  -> set[State]`<br>
#   rend l'ensemble des états finaux.
# 
# - `getSetTransitionsFrom : State -> set[Transition]`<br>
#   rend l'ensemble des transitions sortant de l'état passé en argument.
# 
# - `prefixStates : int -> NoneType`<br>
#   modifie les identifiants et les étiquettes de tous les états de
#   l'automate en les préfixant par l'entier passé en argument.
# 
# - `succElem : State x str -> set[State]`<br>
#   étant donné un état `s` et un caractère `a`, elle rend l'ensemble des
#   états successeurs de `s` par le caractère `a`.  Formellement,
#   
#   $$succElem(s, a) = \{s' \in S \mid  s \xrightarrow{a} s'\}.$$
#   
#   Cet ensemble peut contenir plusieurs états si l'automate n'est pas déterministe.

# In[22]:


# Voilà le code de succElem

def succElem(self, state, lettre):
    """ State x str -> set[State]
        rend l'ensemble des états accessibles à partir d'un état state par l'étiquette lettre
    """
    successeurs = set()
    # t: Transitions
    for t in self.getSetTransitionsFrom(state):
        if t.etiquette == lettre:
            successeurs.add(t.stateDest)
    return successeurs

Automate.succElem = succElem


# Avec l'exemple précédent, on obtient :

# In[23]:


s0 = list(automate.getSetInitialStates())[0] ## on récupère l'état initial de automate
automate.succElem(s0, 'a')


# ### 2. Prise en mains  <a class="anchor" id="sec2"></a>
# 
# #### 2.1 Création d'automates <a class="anchor" id="sec2_1"></a>
# 
# Soit l'automate $\mathcal{A}$ défini sur l'alphabet $\{ a,b \}$, d'états $0,1,2$, 
# d'état initial 0, d'état final 2 et de transitions : <br>$(0,a,0)$, $(0,b,1)$, 
# $(1,a,2)$, $(1,b,2)$, $(2,a,0)$ et $(2,b,1)$.
# 
# 1. Créer l'automate $\mathcal{A}$ à l'aide de son ensemble de transitions. Pour cela, créer un état `s0`  
# d'identifiant $0$
#   qui soit initial, un état `s1` d'identifiant $1$ et un état
#   `s2` d'identifiant $2$ qui soit final. Puis créer `t1`, `t2`, `t3`, `t4`, `t5` et
#   `t6` les 6 transitions de l'automate. Créer enfin l'automate
#   `auto` à partir de ses transitions, par exemple avec l'appel<br>
#   `auto = Automate({t1,t2,t3,t4,t5,t6})`.<br>
#   Vérifier que l'automate correspond bien à $\mathcal{A}$ en l'affichant.

# In[24]:


# A faire
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

t1 = Transition(s0,"a",s0)
t2 = Transition(s0,"b",s1)
t3 = Transition(s1,"a",s2)
t4 = Transition(s1,"b",s2)
t5 = Transition(s2,"a",s0)
t6 = Transition(s2,"b",s1)

auto = Automate({t1,t2,t3,t4,t5,t6})
auto.show(1)


# 2. Créer l'automate $\mathcal{A}$ à l'aide de sa liste de
#   transitions et d'états, par exemple à l'aide de l'appel<br>
#   `auto1 = Automate({t1,t2,t3,t4,t5,t6}, {s0,s1,s2})`<br>
#   puis afficher l'automate obtenu à l'aide de `print` puis à l'aide de `show`.
#   Vérifier que l'automate `auto1` est bien
#   identique à l'automate `auto`.

# In[25]:


# A faire
auto1 = Automate({t1,t2,t3,t4,t5,t6}, {s0, s1, s2})
auto1.show(1)


# 3. Créer l'automate $\mathcal{A}$ à partir d'un fichier. Pour cela,
#   créer un fichier `auto2.txt`, dans lequel sont indiqués les
#   listes des états et des transitions, ainsi que l'état initial et
#   l'état final, en respectant la syntaxe donnée dans la section
#   précédente. Par exemple la liste d'états est décrite par la ligne
#   `#E: 0 1 2`.  Utiliser ensuite par exemple l'appel
#   `auto2 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")`, puis afficher
#   l'automate `auto2` à l'aide de `print` ainsi qu'à l'aide de `show`.

# In[26]:


# A faire
auto2 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")
auto2.show()


# #### 2.2 Premières manipulations <a class="anchor" id="sec2_2"></a>
# 
# 1. Appeler la fonction `removeTransition` sur l'automate
#   `auto` en lui donnant en argument la transition $(0,a,1)$. Il
#   s'agit donc de créer une variable `t` de type
#   `Transition` représentant $(0,a,1)$ et d'effectuer l'appel
#   `auto.removeTransition(t)`. Observer le résultat sur un
#   affichage.  Appeler ensuite cette fonction sur `auto` en lui
#   donnant en argument la transition `t1`. Observer le résultat
#   sur un affichage. Appeler la fonction `addTransition` sur
#   l'automate `auto` en lui donnant en argument la transition
#   `t1`. Vérifier que l'automate obtenu est bien le même
#   qu'initialement.

# In[27]:


# A faire
t = Transition(s0, "a", s1)
auto.removeTransition(t)
auto.show(1)


# In[28]:


# A faire
auto.removeTransition(t1)
auto.show(1)


# 2. Appeler la fonction `removeState` sur l'automate
#   `auto` en lui donnant en argument l'état
#   `s1`. Observer le résultat. Appeler la fonction
#   `addState` sur l'automate `auto` en lui donnant en
#   argument l'état `s1`. Créer un état `s0bis` d'identifiant
#   $0$ et initial. Appeler la fonction `addState` sur
#   `auto` avec `s0bis` comme argument. Observer le résultat.

# In[29]:


# A faire
auto.removeState(s1)
auto.show(1)


# In[30]:


s0bis = State(0, True, False)
auto.addState(s0bis)
auto.show()


# 3. Appeler la fonction `getSetTransitionsFrom` sur
#   l'automate `auto1` avec `s1` comme argument. Afficher
#   le résultat.

# In[31]:


# A faire
print(auto1.getSetTransitionsFrom(s1))


# ### 3. Exercices de base : tests et complétion  <a class="anchor" id="sec3"></a>

# 1. Donner une définition de la fonction `succ`
#   qui, étant donné un ensemble d'états $S$ et une chaîne de caractères
#       $a$ (de longueur 1), renvoie l'ensemble des états successeurs de tous les états de $L$ par le caractère $a$. Cette fonction doit généraliser la fonction `succElem` pour qu'elle prenne en paramètre un ensemble d'états au lieu d'un seul état.  Formellement, si $S$ est un ensemble d'états et $a$ une lettre,
#   $$succ(S,a) = \bigcup_{s \in S}succ(s,a) = \{s' \in S \mid \mbox{il
#     existe } s \in L \mbox{ tel que } s \xrightarrow{a} s'\}.$$

# In[32]:


# A faire 

def succ(self, setStates, lettre):
    """ Automate x set[State] x str -> set[State]
        rend l'ensemble des états accessibles à partir de l'ensemble d'états setStates par l'étiquette lettre
    """
    # l'union de tous les succElem des états
    return reduce((lambda x, y: x|y), (self.succElem(s, lettre) for s in setStates), set())

Automate.succ = succ


# In[33]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :
auto1.show()
print('---')
assert auto1.succ({s0, s2}, 'b') == {s1}
assert auto1.succ({s0}, 'a') == {s0}
assert auto1.succ({s0, s1}, 'a') == {s0, s2}


# In[34]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    assert auto.succ(auto1.getSetInitialStates(), "a") == auto.succElem(auto1.getSetInitialStates().pop(), "a")
test()


# In[ ]:





# 2. Donner une définition de la fonction `accepte`
#   qui, étant donné une chaîne de caractères `mot`,
#   renvoie un booléen qui vaut vrai si et seulement si `mot` est accepté par l'automate. Attention, noter que l'automate peut ne pas être déterministe.

# In[35]:


# A faire 

def accepte(self, mot) :
    """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
    """
    states = self.getSetInitialStates()
    for c in mot:
        states = self.succ(states,c)
    return any(s.fin for s in states)

Automate.accepte = accepte


# In[36]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.accepte('aa') == False
assert auto1.accepte('ab') == False
assert auto1.accepte('aba') == True


# In[37]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    assert auto.accepte("aaa")
    assert not auto.accepte("a")
test()


# In[ ]:





# 3. Donner une définition de la fonction `estComplet`
#     qui, étant donné un automate `auto` et un ensemble de caractères `Alphabet`
#     renvoie un booléen qui vaut vrai si et
#     seulement si `auto` est complet par rapport à l'alphabet.
#     
#     On n'effectuera pas la vérification sur les états non accessibles depuis les états initiaux.

# In[38]:


# A faire 
def estComplet(self, Alphabet) :
    """ Automate x set[str] -> bool
        rend True si auto est complet pour les lettres de Alphabet, False sinon
        hyp : les éléments de Alphabet sont de longueur 1
    """
    return all(self.succElem(s, c) for s in self.allStates for c in Alphabet)

Automate.estComplet = estComplet


# In[39]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.estComplet({'a', 'b'}) == True
assert auto1.estComplet({'a', 'c', 'b'}) == False


# In[40]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    assert not auto.estComplet({'a', 'b'})
test()


# In[ ]:





# 4. Donner une définition de la fonction `estDeterministe`
# qui, étant donné un automate `auto`,
#  renvoie un booléen qui vaut vrai si et seulement si `auto` est déterministe.

# In[41]:


# A faire
def getAlphabet(self):
    return {t.etiquette for t in self.allTransitions}
Automate.getAlphabet = getAlphabet
def estDeterministe(self) :
    """ Automate -> bool
        rend True si auto est déterministe, False sinon
    """
    return len(self.getSetInitialStates()) == 1 and\
    all(len(self.succElem(s, c)) <= 1 for s in self.allStates for c in self.getAlphabet())
    
Automate.estDeterministe = estDeterministe


# L'appel de fonction `copy.deepcopy(auto)` renvoie un nouvel automate identique à `auto`.

# In[42]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.estDeterministe() == True

auto1bis = copy.deepcopy(auto1)
#t : Transition
t = Transition(s1, 'b', s0)
auto1bis.addTransition(t)
auto1bis.show()
print('---')
assert auto1bis.estDeterministe() == False

auto1bis.removeTransition(t)
auto1bis.show()
print('---')
assert auto1bis.estDeterministe() == True


# In[43]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    assert auto.estDeterministe() == False
test()


# In[ ]:





# 5. Donner une définition de la fonction `completeAutomate`
# qui, étant donné un automate `auto` et l'ensemble alphabet d'entrée `Alphabet`,
# renvoie l'automate complété d'`auto`.
#   
# Attention, il ne faut pas modifier `auto`, mais construire un nouvel automate.
# <br>Il pourra être intéressant d'utiliser l'appel de fonction
# `copy.deepcopy(auto)` qui renvoie un nouvel automate identique à `auto`.
# <br>On pourra faire appel à la fonction `nextId` afin de construire l'état $\bot$.

# In[44]:


# A faire

def completeAutomate(self : Automate, Alphabet) :
    """ Automate x str -> Automate
        rend l'automate complété de self, par rapport à Alphabet
    """
    res = copy.deepcopy(self)
    if self.estComplet(Alphabet):
        return res
    b = State(res.nextId(), False, False, "⊥")
    res.addState(b)
    for s in res.allStates:
        for c in Alphabet:
            if not self.succElem(s, c):
                res.addTransition(Transition(s,c,b))
    return res

Automate.completeAutomate = completeAutomate


# In[45]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant :

auto1.show()
print('---')
assert auto1.estComplet({'a', 'b'}) == True
auto1complet = auto1.completeAutomate({'a', 'b'})
auto1complet.show()
assert auto1complet.estComplet({'a', 'b'}) == True

print('---')
assert auto1.estComplet({'a', 'b', 'c'}) == False
auto1complet = auto1.completeAutomate({'a', 'b', 'c'})
auto1complet.show()
assert auto1complet.estComplet({'a', 'b','c'}) == True


# In[46]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    Alphabet = {"a", "b"}
    assert auto.estComplet(Alphabet) == False
    auto = auto.completeAutomate(Alphabet)
    assert auto.estComplet(Alphabet) == True
    auto.show()
test()


# In[ ]:





# ### 4. Déterminisation  <a class="anchor" id="sec4"></a>

# 1. Donner une définition de la fonction `newLabel`
# qui, étant donné un ensemble d'états renvoie une *chaîne de caractères* représentant l'ensemble de tous les labels des états.
# Par exemple, l'appel de `newLabel` sur un ensemble de 3 états dont les labels sont `'1', '2', '3'` renvoie `'{1,2,3}'`
# 
# Afin d'être assuré que l'ordre de parcours de l'ensemble des états n'a pas d'importance, il sera nécessaire de trier par ordre alphabétique la liste des `label` des états. On pourra faire appel à `L.sort()` qui étant donné la liste `L` de chaînes de caractères, la trie en ordre alphabétique.

# In[47]:


# A faire

def newLabel(S):
    """ set[State] -> str
    """
    return "{%s}" % ','.join(sorted(s.label for s in S))

def newLabelTuple(x, y):
    return "(%s, %s)"%(x.label, y.label)


# In[48]:


# On a défini auparavant un automate auto1, voilà un test le concernant :

assert newLabel(auto1.allStates) == '{0,1,2}'


# In[49]:


# Fournir un autre jeu de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
    auto.show()
    assert newLabel(auto.allStates) == "{0,1,2,3}"
test()


# La fonction suivante permet de déterminiser un automate. On remarque qu'un état peut servir de clé dans un dictionnaire.

# In[50]:


def determinisation(self) :
    """ Automate -> Automate
    rend l'automate déterminisé de self """
    # Ini : set[State]
    Ini = self.getSetInitialStates()
    # fin : bool
    fin = any(e.fin for e in Ini)
    # e : State
    for e in Ini:
        if e.fin:
            fin = True
    lab = newLabel(Ini)
    s = State(0, True, fin, lab)
    A = Automate(set())
    A.addState(s)
    Alphabet = {t.etiquette for t in self.allTransitions}
    Etats = dict()
    Etats[s] = Ini
    A.determinisation_etats(self, Alphabet, [s], 0, Etats, {lab})
    return A


# L'automate déterminisé est construit dans `A`. Pour cela la fonction récursive `determinisation_etats` modifie en place l'automate `A`, et prend en outre les paramètres suivants :
# - `auto`, qui est l'automate de départ à déterminiser
# - `Alphabet` qui contient l'ensemble des lettres étiquetant les transistions de l'automate de départ
# - `ListeEtatsATraiter` qui est la liste des états à ajouter et à traiter dans `A` au fur et à mesure que l'on progresse dans `auto`.
# - `i` qui est l'indice de l'état en cours de traitement (dans la liste `ListeEtatsATraiter`).
# - `Etats` qui est un dictionnaire dont les clés sont les états de `A` et les valeurs associées sont l'ensemble d'états issus de `auto` que cette clé représente.
# - `DejaVus` est l'ensemble des labels d'états de `A` déjà vus.

# In[51]:


# A faire

def addNewState(self : Automate, init=False, fin=False, label=None):
    res = State(self.nextId(), init, fin, label)
    self.addState(res)
    return res

Automate.addNewState = addNewState

def determinisation_etats(self : Automate, auto : Automate, Alphabet, ListeEtatsATraiter, i, Etats, DejaVus):
    """ Automate x Automate x set[str] x list[State] x int x dict[State : set[State]], set[str] -> NoneType
    """
    while i < len(ListeEtatsATraiter):
        s = ListeEtatsATraiter[i]
        i += 1
        for c in Alphabet:
            ens = auto.succ(Etats[s], c)
            lab = newLabel(ens)
            if lab in DejaVus:
                t = {x for x in self.allStates if x.label == lab}.pop()
            else:
                t = self.addNewState(label=lab)
                Etats[t] = ens
            self.addTransition(Transition(s, c, t))
            if lab not in DejaVus:
                ListeEtatsATraiter.append(t)
                DejaVus.add(lab)
    for x in self.allStates:
        x.fin = any(y.fin for y in Etats[x])

Automate.determinisation_etats = determinisation_etats
# Automate.determinisation = determinisation


# In[52]:


# version simplifiée

def determinisation(self : Automate):
    Alphabet = self.getAlphabet()
    res = Automate(set())
    stk = [frozenset(self.getSetInitialStates())]
    ini = State(0, True, False, newLabel(stk[0]))
    res.addState(ini)
    dc = {stk[0] : ini}
    # dfs sur l'ensemble des ensembles d'états
    while stk:
        s = stk.pop()
        for c in Alphabet:
            ens = frozenset(self.succ(s, c))
            if ens not in dc:
                dc[ens] = res.addNewState(label=newLabel(ens))
                stk.append(ens)
            res.addTransition(Transition(dc[s], c, dc[ens]))
    for ens, u in dc.items():
        u.fin = any(x.fin for x in ens)
    return res
Automate.determinisation = determinisation


# In[53]:


# Voici un test
# automate est l'automate construit plus haut a partir du fichier exempleAutomate.txt
automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
automate.show()
auto_det = automate.determinisation()
print(auto_det.estDeterministe())
auto_det.show()


# In[54]:


# Fournir d'autres jeux de tests
def test():
    auto = Automate.creationAutomate("ExemplesAutomates/auto2.txt")
    auto.show()
    auto_det = auto.determinisation()
    auto_det.show()
    assert(auto_det.estDeterministe())
test()


# ### 5. Constructions sur les automates réalisant  des opérations sur les langages acceptés <a class="anchor" id="sec5"></a>
# 
# 
# #### 5.1 Opérations ensemblistes sur les langages <a class="anchor" id="sec5_1"></a>
# 
# 1. Donner une définition de la fonction `complementaire` qui, étant donné un automate `auto` et un ensemble de caractères `Alphabet`, renvoie l'automate acceptant la langage complémentaire du langage accepté par `auto`. Ne pas modifier l'automate `auto`, mais construire un nouvel automate.

# In[55]:


# A faire

def complementaire(self : Automate, Alphabet):
    """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de self
    """
    res : Automate = self.completeAutomate(Alphabet).determinisation()
    for x in res.allStates:
        x.fin = not x.fin
    return res

Automate.complementaire = complementaire   


# In[56]:


# Voici un test

automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
automate.show()
Alphabet = {t.etiquette for t in auto.allTransitions}
auto_compl = automate.complementaire(Alphabet)
auto_compl.show(2)


# In[57]:


# Fournir d'autres tests
def mot_alea(Alphabet):
    Alphabet = tuple(Alphabet)
    return ''.join(choice(Alphabet) for i in range(randint(0, 10)))

def test():
    Alphabet = {'a', 'b', 'c'}
    auto = copy.deepcopy(auto2)
    auto_compl = auto.complementaire(Alphabet)
    auto.show()
    auto_compl.show()
    for i in range(10):
        s = mot_alea(Alphabet)
        assert auto.accepte(s) != auto_compl.accepte(s)
test()


# 2. Donner une définition de la fonction `intersection` qui, étant donné deux automates `auto1` et `auto2`, renvoie l'automate acceptant l'intersection des langages acceptés par `auto1` et `auto2`.
# 
# L'automate construit ne doit pas avoir d'état non accessible depuis l'état initial.

# In[58]:


# A faire

def produit(self, auto, Alphabet, fin):
    """
    produit fait le produit cartésien de 2 automates. C'est la partie commune de l'intersection et l'union
    fin est une fonction qui détermine si un état est final par 2 variables booléennes
    """
    res = Automate(set())
    stk = []
    dc = dict()
    for x in self.getSetInitialStates():
        for y in auto.getSetInitialStates():
            t = State(len(stk), True, False, newLabelTuple(x, y))
            res.addState(t)
            stk.append((x, y))
            dc[(x, y)] = t
    # dfs
    while stk:
        sx, sy = stk.pop()
        for c in Alphabet:
            for x in self.succElem(sx, c):
                for y in auto.succElem(sy, c):
                    if (x, y) not in dc:
                        dc[(x, y)] = res.addNewState(label=newLabelTuple(x, y))
                        stk.append((x, y))
                    res.addTransition(Transition(dc[(sx, sy)], c, dc[(x, y)]))
    for (x, y), u in dc.items():
        u.fin = fin(x.fin, y.fin)
    return res

Automate.produit = produit

def intersection(self, auto):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'intersection des langages des deux automates
    """
    return self.produit(auto, self.getAlphabet() & auto.getAlphabet(), lambda x,y:x and y)
    
Automate.intersection = intersection


# In[59]:


#Un premier test

automate.show()
auto2.show()
inter = automate.intersection(auto2)
inter.show(2)


# In[60]:


# Fournir d'autres tests
def test():
    Alphabet = {'a', 'b'}
    inter = automate.intersection(auto2)
    for i in range(10):
        s = mot_alea(Alphabet)
#         print(s, inter.accepte(s), automate.accepte(s), auto2.accepte(s))
        assert inter.accepte(s) == (automate.accepte(s) and auto2.accepte(s))
test()


# 3. (Question facultative) Donner une définition de la fonction `union` qui, étant donné deux automates `auto1` `auto2`, renvoie l'automate acceptant comme langage l'union des langages acceptés par `auto1` et `auto2`.

# In[61]:


#A faire par l'étudiant

def union (self : Automate, auto : Automate):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'union des langages des deux automates
    """
    Alphabet = self.getAlphabet() | auto.getAlphabet()
    return self.completeAutomate(Alphabet).produit(auto.completeAutomate(Alphabet), Alphabet, lambda x,y: x or y)

Automate.union = union


# In[62]:


#Un premier test

automate.show()
auto2.show()
uni = automate.union(auto2)
uni.show(2)


# In[63]:


def test():
    Alphabet = {'a', 'b'}
    uni = automate.union(auto2)
    for i in range(10):
        s = mot_alea(Alphabet)
#         print(uni.accepte(s), automate.accepte(s), auto2.accepte(s))
        assert uni.accepte(s) == (automate.accepte(s) or auto2.accepte(s))
test()


# #### 5.2 Opérations rationnelles sur les langages <a class="anchor" id="sec5_2"></a>
# 
# Programmer *une des deux* méthodes suivantes:
# 
# 1. Donner une définition de la fonction `concatenation` qui, étant donné deux automates `auto1` et `auto2`, renvoie l'automate acceptant comme langage la concaténation des langages acceptés par `auto1` et `auto2`.
# 
# 2. Donner une définition de la fonction `etoile` qui, étant donné un automate `auto`, renvoie l'automate acceptant comme langage l'étoile du langages accepté par `auto`.

# In[64]:


# A faire

def concatenation (self : Automate, auto : Automate):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage la concaténation des langages des deux automates
    """
    if not auto.getSetInitialStates:
        return auto
    res = copy.deepcopy(auto)
    ini = res.getSetInitialStates()
    # si self n'accepte pas epsilon
    if not any(x.init and x.fin for x in self.allStates):
        for x in res.allStates:
            x.init = False
    for x in res.allStates:
        x.label = 'j'+x.label
    # ajouter self dans res
    dc = dict()
    for t in self.allTransitions:
        u, c, v = t.stateSrc, t.etiquette, t.stateDest
        if u not in dc:
            dc[u] = res.addNewState(u.init, False, 'i'+u.label)
        u = dc[u]
        if v not in dc:
            dc[v] = res.addNewState(v.init, False, 'i'+v.label)
        for v in (ini|{dc[v]} if v.fin else {dc[v]}):
            res.addTransition(Transition(u, c, v))
    return res

Automate.concatenation = concatenation


# In[65]:


#Un premier test

automate.show()
auto2.show()
concat = automate.concatenation(auto2)
concat.show(2)


# In[66]:


#Fournir un autre jeu de test
def test():
    auto : Automate = Automate.creationAutomate("ExemplesAutomates/auto2.txt")
    x = auto.getSetInitialStates().pop()
    x.fin = True
    auto.show()
    auto2.show()
    concat = auto.concatenation(auto2)
    concat.show(2)
test()


# In[67]:


def etoile (self):
    """ Automate  -> Automate
    rend l'automate acceptant pour langage l'étoile du langage de a
    """
    res : Automate = copy.deepcopy(self)
    ini = res.getSetInitialStates()
    for t in self.allTransitions:
        u, c, v = t.stateSrc, t.etiquette, t.stateDest
        if v.fin:
            for v in ini:
                res.addTransition(Transition(u, c, v))
    if not res.accepte(""):
        res.addNewState(True, True, "e")
    return res

Automate.etoile = etoile


# In[68]:


# Un premier test

automate.show()
autoetoile = automate.etoile()
autoetoile.show()


# In[69]:


# Fournir un autre jeu de tests
def test():
    auto2.show()
    autoetoile = auto2.etoile()
    autoetoile.show()
test()


# In[ ]:




