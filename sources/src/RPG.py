import random

def shop(it):
    """ Un objet pour le shop

    Fonction qui prend en paramètre le dictionnaire contenant les objets du shop et en renvoie un aléatoirement
    """
    rng = random.randint(0,len(it)-1)
    i = 0
    for k in it.keys():
        if i == rng:
            itemAvendre = k
        i = i+1
    return itemAvendre

def pnj():
    """ La phrase que va dire le pnj

    Fonction qui renvoie aléatoirement une des phrases que peuvent dire les personnages du jeu
    """
    i = random.randint(1,10)
    if i == 1:
        return 'VILLAGEOIS:"J ai appris que le vendeur vend de l alcool parfois, mais il ne le commercialise que rarement!"'
    if i == 2:
        return 'VILLAGEOIS:"Il parait que les personnes les plus fortes de ce monde reçoivent une arme dévastatrice, qui viendrait d un autre monde ou une autre époque. Tellement dévstatrice, que personne ne l a jamais utilisée."'
    if i == 3:
        return 'VILLAGEOIS:"On m a dit que les 4 personnes qui ont crée ce monde sont des programmeurs d exception! Je me demande s ils entendent ce que je dis."'
    if i == 4:
        return 'VILLAGEOIS:"Bonjour aventurier! J espère que tu te plais ici, enfin tant que Zmeyevick ne se montre pas."'
    if i == 5:
        return 'VILLAGEOISE:"Mon mari est parti à la pèche il y a quelque heures. Je me demande s il est parti dans le lac de Verdantia, ou sur les côtes de Marelys, ou ailleurs."'
    if i == 6:
        return 'VILLAGEOIS:"J ai dit à ma femme que je suis parti pêcher, mais c est juste pour ne pas être là quand elle vera que j ai cassé la clôture.. Ne lui dis pas!"'
    if i == 7:
        return 'VILLAGEOIS:"Tu es perdu? C est dommage."'
    if i == 8:
        return 'VILLAGEOIS:"Tu es perdu? Eh bien moi aussi."'
    if i == 9:
        return 'VILLAGEOIS:"Tu es perdu? Je t aurais bien ramené chez moi pour t aider mais mon père a cassé la clôture et est parti pêcher, je n ai plus les clés."'
    if i == 10:
        return 'VILLAGEOIS:"J aime beaucoup Aurélia.. Quel dommage que je ne l intéresse pas..."'

def description(i):
    """ La description des objets du jeu

    Fonction qui prend en paramètre l'objet en question et en renvoie sa description
    """
    if i == 'potion rouge':
        return "Une potion miraculeuse qui vous rend jusqu'à 75pv"
    if i == 'grande potion rouge':
        return "Une potion encore plus élaborée, pouvant vous redonner la totalité de votre vie"
    if i == 'potion verte':
        return "Une potion miraculeuse qui vous rend jusqu'à 60 de puissance magique"
    if i == 'grande potion verte':
        return "Une potion encore plus élaborée, pouvant vous rendre la totalité de votre énergie magique"
    if i == 'viande grillée':
        return "Une belle pièce de viande qui peut vous redonner 25pv"
    if i == 'baies':
        return "De belles baies sauvages, avec un gout qui vous redonnera 20 en puissance magique"
    if i == 'pomme':
        return "Une simple pomme, mais qui vous redonne 15pv"
    if i == 'gâteau':
        return "Un délicieux met dont le gout vous rend 40pv et même 10 de puissance magique"
    if i == 'miel':
        return "Du bon miel, qui peut vous redonner 20 de puissance magique"
    if i == 'légume':
        return "Un légume sauvage dont les vertus vous offrent 25pv"
    if i == 'vodka':
        return "Un doux breuvage capale de vous redonner tous vos pv ainsi que toute votre puissance magique"
    if i == 'epee niveau2':
        return "Une nouvelle épée, qui augmentera vos performances offensives en combat"
    if i == 'epee niveau3':
        return "Une nouvelle épée, qui augmentera encore plus vos performances offensives en combat!"
    if i == 'bouclier niveau2':
        return "Un nouveau bouclier, qui vous rendra bien plus protégé en combat"
    if i == 'bouclier niveau3':
        return "Un nouveau bouclier, qui vous rendra encore bien plus protégé en combat!"
    if i == 'arbalete':
        return "Un superbe arme à munitions, recommandée pour un chevalier tel que vous"
    if i == 'lance-pierre':
        return "Une belle arme à munition, à prix abordable et plus qu'idéale pour commencer à combattre à deux armes, si vous n'en avez pas déja bien sûr"
    if i == 'marteau magique':
        return "Une beautée que j'ai trouvé à Crest. Il utilise la mana et est absolument superbe en combat"
    if i == 'fouet':
        return "Un fouet qui utilise la mana pour être puissant, absolument incroyable si vous voulez mon avis"
    if i == 'gant de puissance':
        return "Je l'ai trouvé à Ignirift, il augmente la puissance de frappe de manière incroyable, juste en utilisant la mana!"
    if i == 'munitions':
        return "30 munitions en tout genre, qui iront parfaitement avec tes armes"
    if i== 'Tsar Bomba':
        return 'Une arme destructrice, réservée au plus fortes personnes de ce monde. Mais tu ne peux l utiliser, du fait de sa puissance, et tu le sais très bien'

def mobName(a):
    """ Le monstre que l'on s'apprête à combattre

    Fonction qui prend en paramètre la zone dans laquelle le joueur se situe et renvoie un nom de monstre
    trouvable dans cette zone
    """
    choix = random.randint(1,5)
    if a == 1:
        if choix == 1:
            return 'slime'
        if choix == 2:
            return'ours'
        if choix == 3:
            return 'arachnide'
        if choix == 4:
            return 'gobelin'
        if choix == 5:
            return 'esprit'
    if a == 2:
        if choix == 1:
            return 'requin'
        if choix == 2:
            return 'homme-poisson'
        if choix == 3:
            return 'crabe géant'
        if choix == 4:
            return 'serpent des mers'
        if choix == 5:
            return 'golem marin'
    if a == 3:
        if choix == 1:
            return 'yéti'
        if choix == 2:
            return 'loup des neiges'
        if choix == 3:
            return 'zombie de glace'
        if choix == 4:
            return 'sorcier des montagnes'
        if choix == 5:
            return 'golem de glace'
    if a == 4:
        if choix == 1:
            return 'gibdo'
        if choix == 2:
            return 'squelette'
        if choix == 3:
            return 'scorpion géant'
        if choix == 4:
            return 'cobra'
        if choix == 5:
            return 'ver du sable'
    if a == 5:
        if choix == 1:
            return 'dragon'
        if choix == 2:
            return 'spectre brûlant'
        if choix == 3:
            return 'diablotin'
        if choix == 4:
            return 'phoenix'
        if choix == 5:
            return 'homme des cendres'

def questDef(q):
    """ Les quêtes secondaires du jeu

    Fonction qui prend en paramètre le numéro de la quête secondaire selectionnée et en renvoie son énoncé
    """
    if q == 1:
        return "Un villageois de Marelys attend de toi une tâche d'élimintion. Vas lui parler pour démarrer ta mission"
        #tuer un certain nb de mobs
    if q == 2:
        return "Un vilageois de Verdantia a un objet pour toi. Va lui parler pour découvrir ta mission."
        #quete d'échange
    if q == 3:
        return '"J ai quelque chose de très spécial a te demander, viens me rejoindre à Ignirift" -Une habitante de Ignirift'
        #jsp encore
    if q == 4:
        return 'Un villageois de Arduny est très troublé par quelque chose d étrange. Va voir ce qu il se passe.'
        #des mobs a tuer
    if q == 5:
        return "Un villageois érudit de Crest a besoin de tes services. Va voir ce qu'il veut"
        #veut voir des items

####################################################################################
def start():
    """
    Fonction permettant de démarrer la partie
    """
    endGame = 0            #variable qui passe à 1 si le joueur arrête ou s'il finit le jeu

    #####Variables des stats du joueur:
    level = 1
    maxlife = 30
    life = 30
    maxmana = 25
    mana = 25
    items = []
    quest = []
    quete = [0,0]      #[le numéro de la quête en cours, 0 si pas commencée, 1 si lue mais pas enclenchée, 2 si enclenchée]
    objQuest = []     #l'info nécessaire à une quête
    endQuest = 0    #0 si pas de quête, 1 si démarée, 2 si finie
    bosses = []      #liste des boss que le joueur a débloqué
    weapon1 = 'epee'
    weapon2 = 'aucune'
    weapon2List = []      #contient tt les armes secondaires pour en équiper une
    #-> cette matrice contient le nom de l'arme, si elle consomme des munitions ou de la mana, et son prix si elle est au shop.
    lvlepee = 1    #augmente avec lépée niveau 2 et 3
    lvlshield = 1   #pareil que l'épée
    munition = 0
    bourse = 0
    area = 1       #la région, numérotée de 1 à 5
    areaList = [1]     #les régions débloquées
    artefacts = []    #liste des artefacts loot par les boss
    exp = 0
    #####Varables qui servent pour des événements:
    lockQuest = [1,2,3,4,5]    #quetes non débloquées
    lockWeapon = [['baguette de feu','mana'],['sac de bombes','muni'],['fusil','muni'],['boomerang enchanté','mana']]     #armes que peuvent loot les mobs
    lockBoss = [1,2,3,4,5]     #numéros des boss à débloquer (sur des parchemins)
    lockArtefacts = [['Bague du souffle',1],['Sceptre des tumultes',2],['Chapka du roi des glaces',3],['Médaillon des tempêtes',4],['Rubis millénaire',5]]   #artefacts loot par les boss avec le numéro du boss
    nbkill = 0       #nb de mobs tués

    ####Variables du shop :   {nom,prix}
    shopWeapon = {'arbalete':100,'lance-pierre':50,'marteau magique':150,'fouet':140,'gant de puissance':200} #les armes du shop| dico -> nom le l'arme, prix
    shopEpee = {'epee niveau2':100,'epee niveau3':200}  #les 2 autres épées
    shopShield = {'bouclier niveau2':100,'bouclier niveau3':200}
    shopItem = {'potion rouge':80,'potion verte':80,'grande potion rouge':300,'grande potion verte':300,'viande grillée':25,'baies':20,'pomme':10,'gâteau':40,'miel':20,'légume':20,'munitions':50}
    etat = ' '   #état de la sauvegarde(vide ou pleine)
    save = open("save.txt", "rt")
    i = 0
    for value in save.read().split(" "):
        i = i + 1
        if i == 1:
            etat = value
    save.close()
    if etat == 'empty':
        name = input("Bien le bonjour noble aventurier, quel est ton nom?")
        print("Très bien",name,"tu es donc envoyé ici sur ordre du roi pour terrasser Zmeyevick")
        print("qui menace le monde entier, comme tu le sais très bien.")
        print("Sans douter de ta force, je crains que tu ne sois encore assez puissant pour le vaincre...")
        print("Profite que tu sois sur ces contrées pour accumuler de l'expérience, au moins 50 fois plus à mon humble avis.")
        print(" ")
        print("(Tapez /help pour avoir la liste des commandes exécutables)")
    else:
        new = input("Voulez-vous commencer une nouvelle partie, ou continuer sur la sauvegarde précédente? Tapez /new pour une nouvelle partie, ou /continue pour continuer.")
        if new == '/new':
            name = input("Bien le bonjour noble aventurier, quel est ton nom?")
            print("Très bien",name,"tu es donc envoyé ici sur ordre du roi pour terrasser Zmeyevick")
            print("qui menace le monde entier, comme tu le sais très bien.")
            print("Sans douter de ta force, je crains que tu ne sois encore assez puissant pour le vaincre...")
            print("Profite que tu sois sur ces contrées pour accumuler de l'expérience, au moins 50 fois plus à mon humble avis.")
            print(" ")
            print("(Tapez /help pour avoir la liste des commandes exécutables)")
        else:
            if new != '/continue':
                print("Je n'ai pas compris, tant pis, je vous lance votre sauvegarde")
            print('Lecture de la sauvegarde...')
            print(" ")
            print("(Tapez /help pour avoir la liste des commandes exécutables)")
            save = open("save.txt", "rt")
            i = 0
            for value in save.read().split("|"):
                i = i+1
                if i == 2:
                    level = int(value)
                elif i == 3:
                    life = int(value)
                elif i == 4:
                    maxlife = int(value)
                elif i == 5:
                    mana = int(value)
                elif i == 6:
                    maxmana = int(value)
                elif i == 7:
                    items = eval(value)
                elif i == 8:
                    quest = eval(value)
                elif i == 9:
                    quete = eval(value)
                elif i == 10:
                    objQuest = eval(value)
                elif i == 11:
                    endQuest = int(value)
                elif i == 12:
                    bosses = eval(value)
                elif i == 13:
                    weapon1 = value
                elif i == 14:
                    if value == 'aucune':
                        weapon2 = value
                    else:
                        weapon2 = eval(value)
                elif i == 15:
                    weapon2List = eval(value)
                elif i == 16:
                    lvlepee = int(value)
                elif i == 17:
                    lvlshield = int(value)
                elif i == 18:
                    munition = int(value)
                elif i == 19:
                    bourse = int(value)
                elif i == 20:
                    area = int(value)
                elif i == 21:
                    areaList = eval(value)
                elif i == 22:
                    artefacts = eval(value)
                elif i == 23:
                    exp = int(value)
                elif i == 24:
                    lockQuest = eval(value)
                elif i == 25:
                    lockWeapon = eval(value)
                elif i == 26:
                    lockBoss = eval(value)
                elif i == 27:
                    lockArtefacts = eval(value)
                elif i == 28:
                    nbkill = int(value)
                elif i == 29:
                    shopWeapon = eval(value)
                elif i == 30:
                    shopEpee = eval(value)
                elif i == 31:
                    shopShield = eval(value)
                elif i == 32:
                    shopItem = eval(value)
                elif i == 33:
                    name = value


################################################################################################

    while endGame < 1:
        expSup = 25+level*25     #défini l'exp à obtenir pour levelUp
        #level-up
        while exp >= expSup:
            exp = exp - (25+level*25)
            level = level+1

            print("Bravo! Vous passez au niveau",level,".")
            if level%2 == 0:
                maxlife = maxlife+10
                print(" ")
                print("Votre vie maximum augmente de 10pv!")
            else:
                maxmana = maxmana + 5
                print(" ")
                print("Votre maximum de mana augmente de 5!")
            life = maxlife
            mana = maxmana

            if level == 5:
                areaList.append(2)
                print(" ")
                print("Vous avez débloqué l'accès à une nouvelle région: Marelys!")
            if level == 9:
                areaList.append(3)
                print(" ")
                print("Vous avez débloqué l'accès à une nouvelle région: Crest!")
            if level == 14:
                areaList.append(4)
                print(" ")
                print("Vous avez débloqué l'accès à une nouvelle région: Arduny!")
            if level == 17:
                areaList.append(5)
                print(" ")
                print("Vous avez débloqué l'accès à une nouvelle région: Ignirift!")
                print(" ")
                print("Vous avez accès à l'intégralité du royaume, c'est incroyable!")
            if level == 300:
                print("Bravo pour avoir atteint ce niveau exceptionnel !")
                print("En récompense, je vous donne cette arme secrète, venue du futur ou d'une autre époque, la Tsar Bomba!!")
                items.append('Tsar Bomba')
        
        print(' ')
        action = input("Tapez votre commande d'action : ")

        if action == "/invent":
            print("Vie:",life,"/",maxlife)
            print("Mana:",mana,"/",maxmana)
            print("Votre arme principale:", weapon1)
            if weapon2 != 'aucune':
                print("Votre seconde arme:",weapon2[0])
            if weapon2[1] == 'muni':
                print("Vos munitions :",munition)
            print("Votre bourse:",bourse,"noaï")
            print(" ")
            if len(items) !=0:
                print("Votre sac:")
                for i in items:
                    print(i)
            print(" ")
            if len(quest) != 0:
                print("Vous avez",len(quest),"parchemins de quête.")
            print(" ")
            if len(artefacts) != 0:
                print("Vous avez récupéré",len(artefacts),"artefacts anciens:")
                for i in artefacts:
                    print(i)
            print(" ")
            if len(bosses) != 0:
                print("Vous possédez",len(bosses),"parchmins de boss.")
#############################################
        if action == "/show.level":
            print("Vous êtes actuellement niveau",level)
            print("Exp:  ",exp,"/",expSup)
############################################
        if action == "/end":
            confirm = input("êtes-vous sûr de vouloir arrêter?")
            if confirm == "non":
                print("Fort bien, bonne aventure!")
            if confirm == "oui":
                print("Bien, je vous dis donc à la revoyure!")
                endGame = 1
########################################################
        if action == '/mob':
            fightAction = ' '  #on la définit ici pour qu'elle existe sinn ça bug avec la condition du defend (voir 6 ligne plus loin)

            levelMob = random.randint(level-3,level+3)
            if levelMob < 1:
                levelMob = 1
            nomMob = mobName(area)
            print("Attention! Un",nomMob, "de niveau",levelMob,"apparait!")
            lifeMob = levelMob*6 + 7

            while lifeMob > 0 and life > 0:
                if fightAction != '/defend':
                    defense = 1*lvlshield      #revient a 1 si le /defend n'est pas appliqué, change sinon
                print("Vie:",life,"/",maxlife,", Mana:",mana,"/",maxmana,", Munitions:",munition)
                fightAction = input("Que voulez-vous faire?   ")    #attack, defend, item
                if fightAction == '/attack1':
                    chance = random.randint(1,20)
                    hit = (random.randint(level,int(level*1.5)))*lvlepee
                    if chance == 20:
                        lifeMob = lifeMob - hit*2
                        if lifeMob < 0:
                            lifeMob = 0
                        print("Coup chance! Vous retirez",hit*2,"pv à l'enemi! Il lui reste",lifeMob,"pv.")
                    elif 16 <= chance <= 19:
                        lifeMob = lifeMob - int(hit*1.5)
                        if lifeMob < 0:
                            lifeMob = 0
                        print("Coup critique! Vous retirez",int(hit*1.5),"pv à l'enemi! Il lui reste",lifeMob,"pv.")
                    elif chance < 16:
                        lifeMob = lifeMob - hit
                        if lifeMob < 0:
                            lifeMob = 0
                        print("Vous retirez",hit,"pv à l'enemi! Il lui reste",lifeMob,"pv.")
                if fightAction == '/attack2':
                    if weapon2 == 'aucune':
                        print("Mince! Vous n'avez pas de deuxième arme! Et vous n'avez maintenant plus le temps d'attaquer!")
                    else:
                        if weapon2[1] == 'muni':
                            nb = int(input("Combien de munitions voulez vous utiliser contre lui? Vous ne pouvez pas en utiliser plus de 20 d'un seul coup."))
                            if nb > munition:
                                nb = munition
                            if nb > 20:
                                nb = 20
                            munition = munition - nb
                            hit = random.randint(level,int(level*1.5)) * nb
                        if weapon2[1] == 'mana':
                            nb = int(input("Combien de puissance magique, en mana, voulez vous utiliser contre lui? Vous ne pouvez pas en mettre plus de 10 d'un coup."))
                            if nb>mana:
                                nb = mana
                            if nb > 10:
                                nb = 10
                            mana = mana - nb
                            hit = random.randint(level,int(level*1.5)) * int(nb*(int(0.5*nb)))
                        if hit == 0:
                             print("Mince! Vous n'avez plus de stock!!")
                        else:
                            chance = random.randint(1,20)
                            if 17 <= chance <= 20:
                                lifeMob = lifeMob - int(hit*1.5)
                                if lifeMob < 0:
                                    lifeMob = 0
                                if weapon2[1] == 'muni':
                                    print("Coup chance! Vous retirez",int(hit*1.5),"pv à l'enemi! Il lui reste",lifeMob,"pv.")
                                else:
                                    print("Coup surpuissant! Vous retirez",int(hit*1.5),"pv à l'enemi! Il lui reste",lifeMob,"pv.")
                            elif chance < 17:
                                lifeMob = lifeMob - hit
                                if lifeMob < 0:
                                    lifeMob = 0
                                print("Vous retirez",hit,"pv à l'enemi! Il lui reste",lifeMob,"pv.")

                if fightAction == '/defend':
                    if defense > 1*lvlshield:   #si /defend vient déja d'être utilisé
                        print("Vous ne pouvez pas utiliser ce sort 2 fois d'affilée, et vous n'avez plus le temps d'attaquer!")
                        fightAction = ' '     #pour ne pas conserver l'effet + de deux tours
                    elif mana == 0:
                        print("Vous n'avez plus de mana! Vous ne pouvez plus utiliser cette technique!")
                    elif defense == 1*lvlshield:
                        ptDef = int(input("Combien de mana voulez vous utiliser pour vous défendre?    "))
                        if ptDef > mana:
                            ptDef = mana
                        mana = mana - ptDef
                        defense = defense + ptDef*0.25
                        print("Très bien. Votre défense est augmentée pour ce tour et le prochain.")
                if fightAction == '/item':
                    if len(items) == 0:
                        print("Vous ne possédez pas d'items, et vous n'avez plus le temps maintenant de contre-attaquer!")
                    else:
                        for k in items:
                            print(' ')
                            print(k)
                        choixItem = input('Quel item voulez-vous utiliser ?')
                        if choixItem not in items:
                            print("Vous ne possédez pas cet item")
                        else:
                            print('"',description(choixItem),'" :')
                            validation = input("Voulez-vous bien utiliser cet item?    ")
                            if validation == 'non':
                                print("Très bien, je vous laisse continuer votre combat!")
                            elif validation == 'oui':
                                supp = 0
                                if choixItem != 'Tsar Bomba':
                                    for i in range(len(items)-1):
                                        if items[i] == choixItem:
                                            supp = i
                                    items.pop(i)
                                if choixItem == 'potion rouge':
                                    life = life + 75
                                    print("Potion bue")
                                if choixItem == 'grande potion rouge':
                                    life = maxlife
                                    print("Potion bue")
                                if choixItem == 'potion verte':
                                    mana = mana + 60
                                    print("Potion bue")
                                if choixItem == 'grande potion verte':
                                    mana = maxmana
                                    print("Potion bue")
                                if choixItem == 'viande grillée':
                                    life = life + 25
                                    print("Viande mangée, et savourée")
                                if choixItem == 'baies':
                                    mana = mana + 20
                                    print("Baies mangées")
                                if choixItem == 'pomme':
                                    life = life + 15
                                    print("Pomme mangée")
                                if choixItem == 'gâteau':
                                    life = life + 40
                                    mana = mana + 10
                                    print("Gâteau mangé")
                                if choixItem == 'miel':
                                    mana = mana + 20
                                    print("Miel mangé")
                                if choixItem == 'légume':
                                    life = life + 25
                                    print("Légume mangé")
                                if choixItem == 'vodka':
                                    life = maxlife
                                    mana = maxmana
                                    print("Vodka bue")
                                if choixItem == 'Tsar Bomba':
                                    print("Je viens de vous dire que vous ne pouvez pas utiliser cette arme.....")
                                if life > maxlife:
                                    life = maxlife
                                if mana > maxmana:
                                    mana = maxmana
                #tour du mob
                if lifeMob > 0:
                    mobHit = int((random.randint(levelMob,int(levelMob*1.5)))/defense)
                    mobChance = random.randint(1,25)
                    if 23 <= mobChance <= 25:
                        print("Aie! Le monstre vous inflige",mobHit*2,"de dégats!")
                        life = life - mobHit*2
                    if 1 <= mobChance <= 2:
                        print("Quelle chance! Le monstre vous rate et vous ne perdez aucun pv!")
                    if 2 < mobChance < 23:
                        print("Aie! Le monstre vous inflige",mobHit,"de dégats!")
                        life = life - mobHit
            if lifeMob <= 0:
                print("Bien joué!")
                nbkill = nbkill + 1
                expWin = random.randint(levelMob*10,levelMob*10 + 5)
                moneyWin = random.randint(levelMob*8,levelMob*8+ 7)
                lotChance = random.randint(1,12)
                print("Vous avez gagné",expWin,"points d'exp et",moneyWin,"noaï !")
                exp = exp + expWin
                bourse = bourse + moneyWin
                if lotChance == 11:
                    if len(lockQuest) != 0:
                        lot = lockQuest.pop(random.randint(0,len(lockQuest)-1))
                        quest.append(lot)
                        print("Le monstre a laissé derrière lui un parchemin de quète! Tapez /quest pour la découvrir!")
                if lotChance == 12:
                    if len(lockWeapon) != 0:
                        lot = lockWeapon.pop(random.randint(0,len(lockWeapon)-1))
                        weapon2List.append(lot)
                        print("Le monstre a laissé derière lui une arme :",lot[0],". Vous l'obtenez donc! ")
                if lotChance == 10:
                    if len(lockBoss) != 0:
                        lot = lockBoss.pop(random.randint(0,len(lockBoss)-1))
                        bosses.append(lot)
                        print("Le monstre a laissé derière lui un parchemin d'un boss, le numéro",lot,". Plus qu'à aller le battre dans la bonne région si vous le souhaitez.")
                if nomMob == 'yéti' and quete == [3,2]:
                    print('Vous obtenez du poil de yéti, comme aurélia vous aveez demandé')
                    if 'poil' in objQuest:
                        for i in range(len(objQuest)):
                            if objQuest[i] == 'poil':
                                supp = i
                        objQuest.pop(i)
                if nomMob == 'slime' and quete == [3,2]:
                    print("Vous obtenez du slime de Verdantia, comme aurélia vous avait demandé")
                    if 'slime' in objQuest:
                        for i in range(len(objQuest)):
                            if objQuest[i] == 'slime':
                                supp = i
                        objQuest.pop(i)
                if nomMob == 'cobra' and quete == [3,2]:
                    print("Vous obtenez du venin de Cobra de Arduny, comme aurélia vous l'avait demandé")
                    if 'venin' in objQuest:
                        for i in range(len(objQuest)):
                            if objQuest[i] == 'venin':
                                supp = i
                        objQuest.pop(i)
                if nomMob == 'gibdo' and objQuest == ['rien']:
                    objQuest[0] = 'papier'
                    print("Le gibdo a laissé de nombreux papiers derière lui.")
                    print("Mais, ce n'est pas l'argent qu'il cherche! Va lui parler pour avoir des explications.")
                    objQuest.append('battu')
                if nomMob == 'cobra' and objQuest == ['papier']:
                    objQuest[0] = 'anneau'
                    print("Le cobra a laissé derière lui un anneau.")
                    print("Ce n'est toujours pas l'argent! Retourne parler au villageois pour savoir.")
                    objQuest.append('battu')
                if nomMob == 'squelette' and objQuest == ['anneau']:
                    objQuest[0] = 'argent'
                    print("Le squelette a laissé derière lui de l'argent.")
                    print("C'est enfin celui du villageois!")
                    objQuest.append('battu')
            if life <= 0:
                life = int(maxlife/2)
                retry = input("Mince, vous êtes mort! Voulez-vous continuer?")
                if retry == 'oui':
                    print("Aah fort bien! Mais faites attention la prochaine fois.")
                if retry == 'non':
                    print("Bien, je vous dis donc à la revoyure!")
                    endGame = 1


#######################################################
        if action == '/weapon':
            if len(weapon2List) == 0:
                print("Malheureusement, vous n'avez pas encore acquis de deuxième arme.")
            else:
                for k in weapon2List:
                    print(" ")
                    print(k[0])
                selection = input("Quelle arme voulez-vous équiper?")
                for k in weapon2List:
                    if k[0] == selection:
                        weapon2 = k
                        print(selection,"équipé en tant que seconde arme.")
                if selection != weapon2[0]:
                    print("Vous n'avez pas cette arme, essayez avec une que vous possédez, cela marche mieux.")
########################################################
        if action == '/area':
            if len(areaList) == 1:
                print("Vous ne connaissez pas de région supplémentaire")
            else:
                for k in areaList:
                    if k != area and k == 1:
                        print("Verdantia")
                    if k != area and k == 2:
                        print("Marelys")
                    if k != area and k == 3:
                        print("Crest")
                    if k != area and k == 4:
                        print("Arduny")
                    if k != area and k == 5:
                        print("Ignirift")
                loca = input("Dans quelle zone voulez-vous aller? /stay si vous ne voulez pas bouger")
                if loca.lower() == 'verdantia':
                    if area == 1:
                        print("Je vous ai dit qu'il faut faire /stay pour rester ici.. La prochaine fois essayez de faire simple pour rester.")
                    else:
                        area = 1
                        print("Très bien. Bienvenue à Verdantia, la région des plaines et forêts!")
                if loca.lower() == 'marelys':
                    if area == 2:
                        print("Je vous ai dit qu'il faut faire /stay pour rester ici.. La prochaine fois essayez de faire simple pour rester.")
                    else:
                        area = 2
                        print("Très bien. Bienvenue à Marelys, la région océanique!")
                if loca.lower() == 'crest':
                    if area == 3:
                        print("Je vous ai dit qu'il faut faire /stay pour rester ici.. La prochaine fois essayez de faire simple pour rester.")
                    else:
                        area = 3
                        print("Très bien. Bienvenue à Crest, la région de la neige et du froid!")
                if loca.lower() == 'arduny':
                    if area == 4:
                        print("Je vous ai dit qu'il faut faire /stay pour rester ici.. La prochaine fois essayez de faire simple pour rester.")
                    else:
                        area = 4
                        print("Très bien. Bienvenue à Arduny, la région du désert!")
                if loca.lower() == 'ignirift':
                    if area == 5:
                        print("Je vous ai dit qu'il faut faire /stay pour rester ici.. La prochaine fois essayez de faire simple pour rester.")
                    else:
                        area = 5
                        print("Très bien. Bienvenue à Ignirift, la région ardente et volcanique!")
                if loca.lower() !=  'verdantia' and loca.lower() != 'marelys' and loca.lower() != 'crest' and loca.lower() != 'arduny' and loca.lower() != 'ignirift':
                        print("Hmm... Cette région m'est totalement inconnue. Je vous prie de réessayer.")
                if loca.lower() == '/stay':
                    print("Très bien. Je vous laisse continuer dans cette région")
##################################################################
        if action == '/item':
            if len(items) == 0:
                print("Vous ne possédez pas d'items.")
            else:
                for k in items:
                    print(' ')
                    print(k)
                choixItem = input('Quel item voulez-vous utiliser ?')
                if choixItem not in items:
                    print("Vous ne possédez pas cet item")
                else:
                    print('"',description(choixItem),'" :')
                    validation = input("Voulez-vous bien utiliser cet item?    ")
                    if validation == 'non':
                        print("Très bien, je vous laisse continuer votre aventure")
                    elif validation == 'oui':
                        supp = 0
                        if choixItem != 'Tsar Boba':
                            for i in range(len(items)-1):
                                if items[i] == choixItem:
                                    supp = i
                            items.pop(i)
                        if choixItem == 'potion rouge':
                            life = life + 75
                            print("Potion bue")
                        if choixItem == 'grande potion rouge':
                            life = maxlife
                            print("Potion bue")
                        if choixItem == 'potion verte':
                            mana = mana + 60
                            print("Potion bue")
                        if choixItem == 'grande potion verte':
                            mana = maxmana
                            print("Potion bue")
                        if choixItem == 'viande grillée':
                            life = life + 25
                            print("Viande mangée, et savourée")
                        if choixItem == 'baies':
                            mana = mana + 20
                            print("Baies mangées")
                        if choixItem == 'pomme':
                            life = life + 15
                            print("Pomme mangée")
                        if choixItem == 'gâteau':
                            life = life + 40
                            mana = mana + 10
                            print("Gâteau mangé")
                        if choixItem == 'miel':
                            mana = mana + 20
                            print("Miel mangé")
                        if choixItem == 'légume':
                            life = life + 25
                            print("Légume mangé")
                        if choixItem == 'vodka':
                            life = maxlife
                            mana = maxmana
                            print("Vodka bue")
                        if choixItem == 'Tsar Bomba':
                            print("Je viens de vous dire que vous ne pouvez pas utiliser cette arme.....")
                        if life > maxlife:
                            life = maxlife
                        if mana > maxmana:
                            mana = maxmana
###################################################################
        if action == '/boss':
            if len(bosses) == 0:
                print("Vous ne connaissez aucun boss")
            else:
                for k in bosses:
                    print("Parchemin numéro",k)
                numero = int(input("Quel boss voulez-vous tenter d'appeler ?   "))
                if numero != area:
                    print("Vous n'êtes pas dans la bonne région pour trouver ce boss")
                else:
                    if area == 1:
                        levelBoss = 22
                        lifeBoss = 2000
                        print("Il a surgi! Grangar, le guerrier déchu et gardien de la forêt! Fais attention",name)
                    if area == 2:
                        levelBoss = 25
                        lifeBoss = 2300
                        print("Il a surgi! Néréus, le mythique léviathan maître des eaux de Marelys! Fais attention",name)
                    if area == 3:
                        levelBoss = 28
                        lifeBoss = 2550
                        print("Elle a surgi! L'âme gelée d'Elidra, ancienne reine de Crest et du pays entier, aujourd'hui rongée par la haine et le froid! Fais attention", name)
                    if area == 4:
                        levelBoss = 30
                        lifeBoss = 2750
                        print("Il a surgi! Thornas, le pharaon momifié, qui attendait un mortel pour pouvoir revenir sur ses terres! Fais attention",name)
                    if area == 5:
                        levelBoss = 32
                        lifeBoss = 3000
                        print("Il a surgi! Phyroxia, le titan des flammes et protecteur du volcan! Fais attention",name)
                    fightAction = ' '
                    while lifeBoss > 0 and life > 0:
                        if fightAction != '/defend':
                            defense = 1 * lvlshield
                        print("Vie:",life,"/",maxlife,", Mana:",mana,"/",maxmana,", Munitions:",munition)
                        fightAction = input("Que voulez-vous faire?   ")
                        if fightAction == '/attack1':
                            chance = random.randint(1,20)
                            hit = (random.randint(level,int(level*1.5)))*lvlepee
                            if chance == 20:
                                lifeBoss = lifeBoss - hit*2
                                if lifeBoss < 0:
                                    lifeBoss = 0
                                print("Coup chance! Vous retirez",hit*2,"pv au boss! Il lui reste",lifeBoss,"pv.")
                            elif 16 <= chance <= 19:
                                lifeBoss = lifeBoss - int(hit*1.5)
                                if lifeBoss < 0:
                                    lifeBoss = 0
                                print("Coup critique! Vous retirez",int(hit*1.5),"pv au boss! Il lui reste",lifeBoss,"pv.")
                            elif chance < 16:
                                lifeBoss = lifeBoss - hit
                                if lifeBoss < 0:
                                    lifeBoss = 0
                                print("Vous retirez",hit,"pv au boss! Il lui reste",lifeBoss,"pv.")
                        if fightAction == '/attack2':
                            if weapon2 == 'aucune':
                                print("Mince! Vous n'avez pas de deuxième arme! Et vous n'avez maintenant plus le temps d'attaquer!")
                            else:
                                if weapon2[1] == 'muni':
                                    nb = int(input("Combien de munitions voulez vous utiliser contre lui? Vous ne pouvez pas en utiliser plus de 20 d'un seul coup."))
                                    if nb > munition:
                                        nb = munition
                                    if nb > 20:
                                        nb = 20
                                    munition = munition - nb
                                    hit = random.randint(level,int(level*1.5)) * nb
                                if weapon2[1] == 'mana':
                                    nb = int(input("Combien de puissance magique, en mana, voulez vous utiliser contre lui? Vous ne pouvez pas en mettre plus de 10 d'un coup."))
                                    if nb>mana:
                                        nb = mana
                                    if nb > 10:
                                        nb = 10
                                    mana = mana - nb
                                    hit = random.randint(level,int(level*1.5)) * int(nb*(int(0.5*nb)))
                                if hit == 0:
                                    print("Mince! Vous n'avez plus de stock!!")
                                else:
                                    chance = random.randint(1,20)
                                    if 17 <= chance <= 20:
                                        lifeBoss = lifeBoss - int(hit*1.5)
                                        if lifeBoss < 0:
                                            lifeBoss = 0
                                        if weapon2[1] == 'muni':
                                            print("Coup chance! Vous retirez",int(hit*1.5),"pv au boss! Il lui reste",lifeBoss,"pv.")
                                        else:
                                            print("Coup surpuissant! Vous retirez",int(hit*1.5),"pv au boss! Il lui reste",lifeBoss,"pv.")
                                    elif chance < 17:
                                        lifeBoss = lifeBoss - hit
                                        if lifeBoss < 0:
                                            lifeBoss = 0
                                        print("Vous retirez",hit,"pv au boss! Il lui reste",lifeBoss,"pv.")
                        if fightAction == '/defend':
                            if defense > 1*lvlshield:   #si /defend vient déja d'être utilisé
                                print("Vous ne pouvez pas utiliser ce sort 2 fois d'affilée, et vous n'avez plus le temps d'attaquer!")
                                fightAction = ' '     #pour ne pas conserver l'effet + de deux tours
                            elif mana == 0:
                                print("Vous n'avez plus de mana! Vous ne pouvez plus utiliser cette technique!")
                            elif defense == 1*lvlshield:
                                ptDef = int(input("Combien de mana voulez vous utiliser pour vous défendre?    "))
                                if ptDef > mana:
                                    ptDef = mana
                                mana = mana - ptDef
                                defense = defense + ptDef*0.25
                                print("Très bien. Votre défense est augmentée pour ce tour et le prochain.")
                        if fightAction == '/item':
                            if len(items) == 0:
                                print("Vous ne possédez pas d'items, et vous n'avez plus le temps maintenant de contre-attaquer!")
                            else:
                                for k in items:
                                    print(' ')
                                    print(k)
                                choixItem = input('Quel item voulez-vous utiliser ?')
                                if choixItem not in items:
                                    print("Vous ne possédez pas cet item")
                                else:
                                    print('"',description(choixItem),'" :')
                                    validation = input("Voulez-vous bien utiliser cet item?    ")
                                    if validation == 'non':
                                        print("Très bien, je vous laisse continuer votre combat!")
                                    elif validation == 'oui':
                                        supp = 0
                                        if choixItem != 'Tsar Bomba':
                                            for i in range(len(items)-1):
                                                if items[i] == choixItem:
                                                    supp = i
                                            items.pop(supp)
                                        if choixItem == 'potion rouge':
                                            life = life + 75
                                            print("Potion bue")
                                        if choixItem == 'grande potion rouge':
                                            life = maxlife
                                            print("Potion bue")
                                        if choixItem == 'potion verte':
                                            mana = mana + 60
                                            print("Potion bue")
                                        if choixItem == 'grande potion verte':
                                            mana = maxmana
                                            print("Potion bue")
                                        if choixItem == 'viande grillée':
                                            life = life + 25
                                            print("Viande mangée, et savourée")
                                        if choixItem == 'baies':
                                            mana = mana + 20
                                            print("Baies mangées")
                                        if choixItem == 'pomme':
                                            life = life + 15
                                            print("Pomme mangée")
                                        if choixItem == 'gâteau':
                                            life = life + 40
                                            mana = mana + 10
                                            print("Gâteau mangé")
                                        if choixItem == 'miel':
                                            mana = mana + 20
                                            print("Miel mangé")
                                        if choixItem == 'légume':
                                            life = life + 25
                                            print("Légume mangé")
                                        if choixItem == 'vodka':
                                            life = maxlife
                                            mana = maxmana
                                            print("Vodka bue")
                                        if ChoixItem == 'Tsar Bomba':
                                            print("Je viens de vous dire que vous ne pouvez pas utiliser cette arme.....")
                                        if life > maxlife:
                                            life = maxlife
                                        if mana > maxmana:
                                            mana = maxmana
                        #tour du boss
                        if lifeBoss > 0:
                            bossHit = int((random.randint(levelBoss,int(levelBoss*1.5)))/defense)
                            bossChance = random.randint(1,25)
                            if 23 <= bossChance <= 25:
                                print("Aie! Le boss vous inflige",bossHit*2,"de dégats!")
                                life = life - bossHit*2
                            if 1 <= bossChance <= 2:
                                print("Quelle chance! Le boss vous rate et vous ne perdez aucun pv!")
                            if 2 < bossChance < 23:
                                print("Aie! Le boss vous inflige",bossHit,"de dégats!")
                                life = life - bossHit
                    if life <= 0:
                        life = int(maxlife/2)
                        retry = input("Mince, vous êtes mort! Voulez-vous continuer?")
                        if retry == 'oui':
                            print("Aah fort bien! Mais faites attention la prochaine fois.")
                        if retry == 'non':
                            print("Bien, je vous dis donc à la revoyure!")
                            endGame = 1
                    if lifeBoss <= 0:
                        print("Félicitations! Vous l'avez fait!")
                        if area == 1:
                            expWin = 230
                            moneyWin = 185
                        if area == 2:
                            expWin = 260
                            moneyWin = 210
                        if area == 3:
                            expWin = 290
                            moneyWin = 235
                        if area == 4:
                            expWin = 310
                            moneyWin = 255
                        if area == 5:
                            expWin = 330
                            moneyWin = 270
                        exp = exp + expWin
                        bourse = bourse + exp
                        print("Vous gagnez",moneyWin,"noaïs ainsi que",expWin,"points d'exp!")

                        print("Le boss a laissé derière lui un des 5 artefacts anciens, prenez-le, il vous sera utile!")
                        art = lockArtefacts[numero-1][0]
                        artefacts.append(art)
                        print("Vous obtenez:",art)
                        for k in range(len(bosses)):
                            if bosses[k] == numero:
                                supp = k     #prend l'indice du numéro du boss battu pour le supp de la liste
                        bosses.pop(supp)
################################################################################
        if action == '/finalboss':
            print("Prépares-toi",name,"il arrive, Zmeyevick...")
            fightAction = ' '   #initialisation de fightAction
            levelBoss = 50
            lifeBoss = 50000
            if len(artefacts) == 1:
                print("La puissance de l'artefact ancien que tu as récupéré affaiblit Zmeyevick!")
                lifeBoss = 48000

            if len(artefacts) > 1:
                print("Tes artefacts anciens! Ils affaiblissent Zmeyevick!")
                if len(artefacts) == 2:
                    lifeBoss = 45000
                if len(artefacts) == 3:
                    lifeBoss = 38000
                if len(artefacts) == 4:
                    lifeBoss = 31000
                if len(artefacts) == 5:
                    lifeBoss = 25000

            while lifeBoss > 0 and life > 0:
                if fightAction != '/defend':
                    defense = 1*lvlshield
                print("Vie:",life,"/",maxlife,", Mana:",mana,"/",maxmana,", Munitions:",munition)
                fightAction = input("Que voulez-vous faire?   ")
                if fightAction == '/attack1':
                    chance = random.randint(1,20)
                    hit = (random.randint(level,int(level*1.5)))*lvlepee
                    if chance == 20:
                        lifeBoss = lifeBoss - hit*2
                        if lifeBoss < 0:
                            lifeBoss = 0
                        print("Coup chance! Vous retirez",hit*2,"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                    elif 16 <= chance <= 19:
                        lifeBoss = lifeBoss - int(hit*1.5)
                        if lifeBoss < 0:
                            lifeBoss = 0
                        print("Coup critique! Vous retirez",int(hit*1.5),"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                    elif chance < 16:
                        lifeBoss = lifeBoss - hit
                        if lifeBoss < 0:
                            lifeBoss = 0
                        print("Vous retirez",hit,"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                if fightAction == '/attack2':
                    if weapon2 == 'aucune':
                        print("Mince! Vous n'avez pas de deuxième arme! Et vous n'avez maintenant plus le temps d'attaquer!")
                    else:
                        if weapon2[1] == 'muni':
                            nb = int(input("Combien de munitions voulez vous utiliser contre lui? Vous ne pouvez pas en utiliser plus de 20 d'un seul coup."))
                            if nb > munition:
                                nb = munition
                            if nb > 20:
                                nb = 20
                            munition = munition - nb
                            hit = random.randint(level,int(level*1.5)) * nb
                        if weapon2[1] == 'mana':
                            nb = int(input("Combien de puissance magique, en mana, voulez vous utiliser contre lui? Vous ne pouvez pas en mettre plus de 10 d'un coup."))
                            if nb>mana:
                                nb = mana
                            if nb > 10:
                                nb = 10
                            mana = mana - nb
                            hit = random.randint(level,int(level*1.5)) * int(nb*(int(0.5*nb)))
                        if hit == 0:
                            print("Mince! Vous n'avez plus de stock!!")
                        else:
                            chance = random.randint(1,20)
                            if 17 <= chance <= 20:
                                lifeBoss = lifeBoss - int(hit*1.5)
                                if lifeBoss < 0:
                                    lifeBoss = 0
                                if weapon2[1] == 'muni':
                                    print("Coup chance! Vous retirez",int(hit*1.5),"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                                else:
                                    print("Coup surpuissant! Vous retirez",int(hit*1.5),"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                            elif chance < 17:
                                lifeBoss = lifeBoss - hit
                                if lifeBoss < 0:
                                    lifeBoss = 0
                                print("Vous retirez",hit,"pv à Zmeyevick! Il lui reste",lifeBoss,"pv.")
                if fightAction == '/defend':
                    if defense > 1 * lvlshield:
                        print("Vous ne pouvez pas utiliser ce sort 2 fois d'affilée, et vous n'avez plus le temps d'attaquer!")
                        fightAction = ' '
                    elif mana == 0:
                        print("Vous n'avez plus de mana! Vous ne pouvez plus utiliser cette technique!")
                    elif defense == 1*lvlshield:
                        ptDef = int(input("Combien de mana voulez vous utiliser pour vous défendre?    "))
                        if ptDef > mana:
                            ptDef = mana
                        mana = mana - ptDef
                        defense = defense + ptDef*0.25
                        print("Très bien. Votre défense est augmentée pour ce tour et le prochain.")
                if fightAction == '/item':
                    if len(items) == 0:
                        print("Vous ne possédez pas d'items, et vous n'avez plus le temps maintenant de contre-attaquer!")
                    else:
                        for k in items:
                            print(' ')
                            print(k)
                        choixItem = input('Quel item voulez-vous utiliser ?')
                        if choixItem not in items:
                            print("Vous ne possédez pas cet item")
                        else:
                            print('"',description(choixItem),'" :')
                            validation = input("Voulez-vous bien utiliser cet item?    ")
                            if validation == 'non':
                                print("Très bien, je vous laisse continuer votre combat!")
                            elif validation == 'oui':
                                supp = 0
                                if choixItem != 'Tsar Bomba':
                                    for i in range(len(items)-1):
                                        if items[i] == choixItem:
                                            supp = i
                                    items.pop(supp)
                                if choixItem == 'potion rouge':
                                    life = life + 75
                                    print("Potion bue")
                                if choixItem == 'grande potion rouge':
                                    life = maxlife
                                    print("Potion bue")
                                if choixItem == 'potion verte':
                                    mana = mana + 60
                                    print("Potion bue")
                                if choixItem == 'grande potion verte':
                                    mana = maxmana
                                    print("Potion bue")
                                if choixItem == 'viande grillée':
                                    life = life + 25
                                    print("Viande mangée, et savourée")
                                if choixItem == 'baies':
                                    mana = mana + 20
                                    print("Baies mangées")
                                if choixItem == 'pomme':
                                    life = life + 15
                                    print("Pomme mangée")
                                if choixItem == 'gâteau':
                                    life = life + 40
                                    mana = mana + 10
                                    print("Gâteau mangé")
                                if choixItem == 'miel':
                                    mana = mana + 20
                                    print("Miel mangé")
                                if choixItem == 'légume':
                                    life = life + 25
                                    print("Légume mangé")
                                if choixItem == 'vodka':
                                    life = maxlife
                                    mana = maxmana
                                    print("Vodka bue")
                                if choixItem == 'Tsar Bomba':
                                    print("Je viens de vous dire que vous ne pouvez pas utiliser cette arme.....")
                                if life > maxlife:
                                    life = maxlife
                                if mana > maxmana:
                                    mana = maxmana
                #tour de zmeyevick
                if lifeBoss > 0:
                    bossHit = int((random.randint(levelBoss,int(levelBoss*1.5)))/defense)
                    bossChance = random.randint(1,25)
                    if 23 <= bossChance <= 25:
                        print("Aie! Il utilise sa technique ultime; la foudre interdite! Il vous inflige",bossHit*4,"de dégats!")
                        life = life - bossHit*4
                    elif 17 <= bossChance <= 22:
                        print("Aie! Il utilise son attaque spéciale; le souffle des enfers! Il vous inflige",bossHit*2,"de dégats!")
                        life = life - bossHit*2
                    elif bossChance <=  1:
                        print("Quelle chance! Zmeyevick vous rate et vous ne perdez aucun pv!")
                    elif 3 <= bossChance <= 16:
                        print("Aie! Zmeyevick vous inflige",bossHit,"de dégats!")
                        life = life - bossHit
            if life <= 0:
                life = int(maxlife/2)
                retry = input("Mince, vous êtes mort! Voulez-vous continuer ?")
                if retry == 'oui':
                    print("Aah fort bien! Mais faites attention la prochaine fois.")
                elif retry == 'non':
                    print("Bien, je vous dis donc à la revoyure!")
                    endGame = 1
            if lifeBoss <= 0:
                print("Félicitations",name,"vous avez terrassé Zmeyevick et sauvé le royaume!")
                print("Je vous laisse donc la liberté de partir, vous avez accompli votre mission.")
                print("Vous obtenez en récompense de ce périple la dague de Zmeyevick, faite il y a de cela quelques sciecles avec une de des dents.")
                if ["dague de Zmeyevick","mana"] not in weapon2List:
                    weapon2List.append(["dague de Zmeyevick","mana"])
                print("Et je vous dis à la revoyure, et bonne continuation,",name)
                endGame = 1
##################################################
        if action == '/shop':
            shopEnter = 0    #se met a 1 quand on sort du shop
            print(" ")
            print('VENDEUR:"Oh un client, bienvenue dans ma boutique!')
            print('        Tu peux acheter tout type de choses ici, fait toi plaisir!"')
            print(" ")
            avendre = []
            for i in range(4):
                shopChance = random.randint(1,15)
                if 8 <= shopChance <= 10:
                    if len(shopWeapon) != 0:
                        rng = random.randint(0,len(shopWeapon)-1)
                        i = 0
                        for k in shopWeapon.keys():
                            if i == rng:
                                armeAvendre = k
                            i = i+1
                        if armeAvendre not in avendre:
                            avendre.append(armeAvendre)
                        else:
                            itAvendre = shop(shopItem)
                            avendre.append(itAvendre)
                    else:
                        itAvendre = shop(shopItem)
                        avendre.append(itAvendre)
                elif 11 <= shopChance <= 12:
                    if len(shopEpee) != 0:
                        if 'epee niveau2' not in avendre and 'epee niveau3' not in avendre:
                            rng = 0
                            i = 0
                            for k in shopEpee.keys():
                                if i == rng:
                                    avendre.append(k)
                                i = i+1
                        else:
                            itAvendre = shop(shopItem)
                            avendre.append(itAvendre)
                    else:
                        itAvendre = shop(shopItem)
                        avendre.append(itAvendre)
                elif 13 <= shopChance <= 14:
                    if len(shopShield) != 0:
                        if 'bouclier niveau2' not in avendre and 'bouclier niveau3' not in avendre:
                            rng = 0
                            i = 0
                            for k in shopShield.keys():
                                if i == rng:
                                    avendre.append(k)
                                i = i+1
                        else:
                            itAvendre = shop(shopItem)
                            avendre.append(itAvendre)
                    else:
                        itAvendre = shop(shopItem)
                        avendre.append(itAvendre)
                elif shopChance == 15:
                    shopVodka = {'vodka':150}
                    avendre.append('vodka')
                elif shopChance < 8:
                    itAvendre = shop(shopItem)
                    avendre.append(itAvendre)
            prix = []
            for k in avendre:
                if k in shopWeapon.keys():
                    prix.append(shopWeapon[k])
                if k in shopEpee.keys():
                    prix.append(shopEpee[k])
                if k in shopShield.keys():
                    prix.append(shopShield[k])
                if k in shopItem.keys():
                    prix.append(shopItem[k])
                else:
                    prix.append(150)
                    
            while shopEnter < 1:
                for k in range(len(avendre)):
                    print(avendre[k],":",prix[k],"noaïs")
                achat = input('VENDEUR:"Quel article veut-tu acheter ? Dis moi /exit si tu veux partir."')

                if achat == '/exit':
                    print('VENDEUR:"Très bien, bonne route petit!"')
                    shopEnter = 1
                if achat not in avendre and achat != '/exit':
                    print('VENDEUR:"Hmm je ne connais pas cet article, ou peut être juste qu il n est pas à vendre pour le moment')
                    print('        Ne m arnaque pas petit!"')
                if achat in avendre:
                    print('VENDEUR:"',description(achat),'" :')
                    validation = input('VENDEUR:"Est-ce bien ceci que tu veux acheter?"')
                    if validation == 'non':
                        print('VENDEUR:"Très bien, voit ce qui te ferait plaisir alors."')
                    elif validation == 'oui':
                        prixItem = 0
                        for i in range(len(avendre)):
                            if avendre[i] == achat:
                                prixItem = prix[i]
                        if bourse < prixItem:
                            print('VENDEUR:"Tu n as pas assez de noaïs pour cela, petit."')
                        else:
                            bourse = bourse - prixItem
                            if achat in shopWeapon.keys():
                                if achat == 'arbalete':
                                    weapon2List.append(['arbalete','muni'])
                                    del shopWeapon['arbalete']
                                if achat == 'lance-pierre':
                                    weapon2List.append(['lance-pierre','muni'])
                                    del shopWeapon['lance-pierre']
                                if achat == 'marteau magique':
                                    weapon2List.append(['marteau magique','mana'])
                                    del shopWeapon['marteau magique']
                                if achat == 'fouet':
                                    weapon2List.append(['fouet','mana'])
                                    del shopWeapon['fouet']
                                if achat == 'gant de puissance':
                                    weapon2List.append(['gant de puissance','mana'])
                                    del shopWeapon['gant de puissance']
                            if achat in shopEpee.keys():
                                lvlepee = lvlepee+1
                                del shopEpee[achat]
                            if achat in shopShield.keys():
                                lvlshield = lvlshield+1
                                del shopShield[achat]
                            if achat in shopItem or achat == 'vodka':
                                items.append(achat)

                            for i in range(len(avendre)):
                                if avendre[i] == achat:
                                    supp = i
                            avendre.pop(supp)
                            prix.pop(supp)
                if len(avendre) == 0:
                    print('VENDEUR:" Olala! Je n ai plus de stock! Je pense qu il est temps de se quitter, bonne route petit!"')
                    shopEnter = 1
#################################################################
        if action == '/quest':
            if quete[1] != 0:
                print("Vous avez déja commencé une quête")
                print(" ")
            else:
                if len(quest) == 0:
                    print("Vous n'avez obtenu aucun parchemin de quête. Continuez d'explorer pour en trouver !")
                else:
                    for k in quest:
                        print("Parchemin de la quête numéro",k)
                    select = int(input("Quel parchemin voulez-vous lire ?"))
                    if select not in quest:
                        print("Vous n'avez pas ce parchemin.")
                    else:
                        print(questDef(select))
                        quete[0] = select
                        quete[1] = 1     #pour indiquer le commencement d'une quête
                        print("Quête commencée. Tapez /quest.verif pour voir votre progression.")
##################################################################
        if action == '/quest.verif':
            if quete[1] == 0:
                print("Vous n'avez commencé aucune quête")
            if quete[1] == 1:
                print("Vous n'avez pas encore démaré la quête numéro",quete[0])
            else:
                if quete[0] == 1:
                    if nbkill < objQuest[0] + 30:
                        print("Il vous reste encore",(30-(nbkill-objQuest[0])),"monstres à tuer.")
                    else:
                        endQuest = 2
                        print("Félicitations! Allez maintenant voir cet homme de Marelys pour avoir votre récompense!")
                if quete[0] == 2:
                    if objQuest[0] != 'clé de la librairie de Crest':
                        print("Vous possédez cet objet:",objQuest[0],",allez l'apporter à la personne demandée.")
                    else:
                        endQuest = 2
                        print("Félicitations! Allez donner la clé à ce villageois de Verdantia.")
                if quete[0] == 3:
                    if len(objQuest) > 0:
                        print("Vous n'avez pas encore tout les ingrédients pour Aurélia.")
                        print("Vous devez encore récupérer :")
                        for k in objQuest:
                            print("     ")
                            print("       ",k)
                    else:
                        endQuest = 2
                        print("Félicitations! Allez maintenant rapporter tout cela à Aurélia.")
                if quete[0] == 4:
                    if objQuest != ['argent','battu']:
                        if objQuest[0] == 'rien':
                            print("Vous devez aller battre le voleur")
                        if len(objQuest) == 1 and objQuest[0] != 'rien':
                            print("Vous possèdez actuelement :",objQuest[0],", allez battre le voleur!")
                        else:
                            print("Vous devez aller demander des explications au villageois pour votre touvaille")
                    else:
                        endQuest = 2
                        print("Félicitations! Allez rapporter l'argent au villageois!")


##################################################################
        if action == '/talk':
            talking = 0      #passe à 1 lorsqu'un dialogue est fini pour éviter quun autre ne se lance
            ### quete 1 ###
            if quete == [1,1] and area == 2 and talking == 0:
                print('"VILLAGEOIS: Ah! vous êtes là!')
                print('             Je vous avoue qu en ce moment, je ne me sens pas très en sécurité avec tout')
                print('             ce qui se passe, Zmeyevick, et tout ça.... Je sais que vous travaillez dur')
                print('             pour nous, mais j aimerais que vous me rapportiez la tête de 30 monstres."')
                print(' ')
                print('VILLAGEOIS:" J étais chasseur, ne vous inquiétez pas, mais cela me rassurerait de voir ')
                print('             qu il y a des monstres en moins dans ce royaume. Merci à vous."')
                print(' ')
                print('Tapez /quest.verif une fois la quête terminée pour la valider, ou revenez parler à ce villageois.')
                quete[1] = 2
                objQuest.append(nbkill)
                endQuest = 1
                talking = 1
            if quete == [1,2] and area == 2 and talking == 0:
                if endQuest == 1 and nbkill < objQuest[0] + 30:
                    print('VILLAGEOIS:"Vous n avez pas encore tué les 30 monstres? Pas grave, je vous attends!"')
                if endQuest == 2 or nbkill > objQuest[0] + 30:
                    print('VILLAGEOIS:"Aah je vous remercie! Tenez, je vous offre 400 noaïs et 450 points d exp pour ce service!"')
                    bourse = bourse + 400
                    exp = exp + 450
                    endQuest = 0
                    objQuest = []
                    for i in range(len(quest)):
                        if quest[i] == quete[0]:
                            supp = i
                    quest.pop(supp)
                    quete = [0,0]
                talking = 1
            ### quete 2 ###
            if quete == [2,1] and area == 1 and talking == 0:
                print('VILLAGEOIS:"Aventurier! J ai quelque chose à vous confier.')
                print('            Il faut que je rende ce livre à mon ami de Crest, mais je n ai pas le temps.')
                print('            Il aura normalement quelque chose à me rapporter en échange. Rapportez-le moi')
                print('            en échange de ce livre, et je vous récompenserai"')
                print(' ')
                print("Vous obtenez un vieux livre")
                quete[1] = 2
                objQuest.append('livre')
                endQuest = 1
                talking = 1
            if quete == [2,2] and area == 1 and talking == 0:
                if endQuest == 1 and objQuest[0] != 'clé de la librairie de Crest':
                    print('VILLAGEOIS:"Vous n avez pas encore l objet qu il doit me rendre? Pas grave, je vous attend."')
                if endQuest == 2 or objQuest[0] == 'clé de la librairie de Crest':
                    print('VILLAGEOIS:"Je vous remercie, vous m avez retrouvé le clé que je cherchais!')
                    print('            Je me dois de vous offrir ces 300 noaïs et ces 250 points d exp, prenez-les!"')
                    bourse = bourse + 300
                    exp = exp + 250
                    endQuest = 0
                    objQuest = []
                    for i in range(len(quest)):
                        if quest[i] == quete[0]:
                            supp = i
                    quest.pop(supp)
                    quete = [0,0]
                talking = 1
            if quete == [2,2] and area == 3 and objQuest[0] == 'livre' and talking == 0:
                print('VILLAGEOIS:"Oh mais c est le livre que je cherchais, merci beaucoup.')
                print('            Je sais de qui il vient, mais j ai donné ce qu il attend à un ami de Arduny...')
                print('            Oh je sais! Je dois rendre à cet ami son chapeau, donne lui en échange!"')
                print(' ')
                print("Vous obtenez un chapeau")
                objQuest[0] = 'chapeau'
                talking = 1
            if quete == [2,2] and area == 4 and objQuest == 'chapeau' and talking == 0:
                print('VILLAGEOIS:"C est mon chapeau, merci!')
                print('            Mince, je pense qu il attend que je lui rende la clé de la librairie en échange')
                print('            mais je l aie confié à un proche de Marelys... Tu sais quoi, va donner ceci')
                print('            à ce gars, il devrait te rendre la clé en échange"')
                print(' ')
                print("Vous obtenez une noix de coco")
                objQuest[0] = 'noix de coco'
                talking = 1
            if quete == [2,2] and area == 2 and objQuest == 'noix de coco' and talking == 0:
                print('VILLAGEOIS:" Une noix de coco, il m en devais une c est vrai!"')
                print('VILLAGEOIS:" Comment? La clé de la librairie? Aah oui! mais je l ai donnée à mon père, à Crest,')
                print('             il en avait besoin. Au pire, donne lui cette loupe que j avais oublié de lui rendre.')
                print('             Il te rendra la clé en échange."')
                print(' ')
                print("Vous obtenez une loupe")
                objQuest[0] = 'loupe'
                talking = 1
            if quete == [2,2] and area == 3 and objQuest[0] == 'loupe' and talking == 0:
                print('VILLAGEOIS:" Oh ma loupe! Elle vient de mon fils je présume. Je t en remercie"')
                print('VILLAGEOIS:" Tu veux la clé ? Ah oui c est vrai. Tiens je te la donne, je n en')
                print('             ai plus besoin maintenant."')
                print(" ")
                print("Vous obtenez la clé de la librairie de Crest")
                objQuest[0] = 'clé de la librairie de Crest'
                talking = 1
            ###quete 3 ###
            if quete == [3,1] and area == 5 and talking == 0:
                print('VILLAGEOISE:" Je vous attendais, aventurier. Mon nom est Aurélia."')
                print('AURELIA:" En fait, il se trouve que ma mère est très malade, et comme nous avons toujours')
                print('          vécu à Ignirift, je ne peux sortir de la région pour aller chercher les ingrédients')
                print('          nécéssaires à son traitement."')
                print('AURELIA:" Pourriez-vous donc allez me chercher ce qu il me faut je vous en prie.')
                print('          Il me faudra du poil de yéti, il me semble qu on trouve des yétis à Crest, du Slime ')
                print('          de Verdantia, et du venin de Cobra de Arduny. Je vous en supplie ramenez-moi cela pour')
                print('          ma mère."')
                print(' ')
                objQuest = ['poil','slime','venin']
                quete[1] = 2
                endQuest = 1
                talking = 1
            if quete == [3,2] and area == 5 and talking == 0:
                if endQuest == 1 and len(objQuest) > 0:
                    print('AURELIA:" Tu n as pas encore les ingrédients? Pas grave, je t attends..."')
                if endQuest == 2 or len(objQuest) == 0:
                    print('AURELIA:"Merci beaucoup, je vais pouvoir soigner ma mère!!"')
                    print('AURELIA:" Je me dois de te remercier! Tiens pour toi, 400 noaïs et 300 points d exp.')
                    print('          Je te donne même, juste pour toi, un peu de ce médicamment, au cas où, tiens!"')
                    bourse = bourse + 400
                    exp = exp + 300
                    endQuest = 0
                    objQuest = []
                    for i in range(len(quest)):
                        if quest[i] == quete[0]:
                            supp = i
                    quest.pop(supp)
                    quete = [0,0]
                talking = 1
            ### quete 4 ###
            if quete == [4,1] and area == 4 and talking == 0:
                print('VILLAGEOIS:"Je t attendais aventurier. Il se trouve qu on m a volé une importante somme,')
                print('            et je suspecte fort que cela soit l oeuvre d un gibdo. Pourrais-tu aller le')
                print('            battre pour me rapporter l argent, je t en prie."')
                objQuest = ['rien']
                quete[1] = 2
                endQuest = 1
                talking = 1
            if quete == [4,2] and area == 4 and talking == 0:
                if endQuest == 1 and len(objQuest) == 1:
                    print('VILLAGEOIS:"Tu n es pas encore allé le battre? Pas grave, j attendrai."')
                if endQuest == 2 or objQuest == ['argent','battu']:
                    print('VILLAGEOIS:"Mon argent, il est retrouvé, merci beaucoup!"')
                    print('VILLAGEOIS:"Pour cela, je vais t en donner une partie. Tiens, 400 noaïs ainsi que 300 points d exp."')
                    bourse = bourse + 400
                    exp = exp + 300
                    endQuest = 0
                    objQuest = []
                    for i in range(len(quest)):
                        if quest[i] == quete[0]:
                            supp = i
                    quest.pop(supp)
                    quete = [0,0]
                if objQuest == ['papier','battu']:
                    print('VILLAGEOIS:"Ce n etais donc pas ce gibdo qui m a volé... Peut être alors était-ce un cobra.')
                    print('            Oui c est cela! C est un cobra! Va battre ce cobra je t en prie!"')
                    objQuest.pop(1)
                if objQuest == ['anneau','battu']:
                    print('VILLAGEOIS:" Toujours pas? Hmmm.... Ah oui je sais! C est un squelette qui m a volé, j en ')
                    print('             suis sûr cette fois-ci! C est lui que tu dois tuer!"')
                    objQuest.pop(1)
                talking = 1
            ### quete 5 ###
            if quete == [5,1] and area == 3 and talking == 0:
                print('VILLAGEOIS:"Je t attendais aventurier. J ai entendu dire que tu étais en mission ici, et j aimerais')
                print('            un petit service de ta part. Je suis très intressé par la magie, mais aujourd hui trop')
                print('            vieux pour partir faire mes découvertes moi-même, j aimerais donc que tu me trouves et me')
                print('            montres quelques objets magiques."')
                print(' ')
                print('VILLAGEOIS:" Pour commencer, j aimerais beaucoup voir une "potion rouge", tu veux bien? "')
                objQuest = ['potion rouge']
                quete[1] = 2
                endQuest = 1
                talking = 1
            if quete == [5,2] and area == 3 and talking == 0:
                if objQuest[0] == 'potion rouge' and 'potion rouge' in items:
                    print('VILLAGEOIS:" C est donc ça une potion rouge, très interressant! Je te remercie!')
                    print('             J aimerais maintenant voir un gâteau. Cela parrait banal, mais on')
                    print('             raconte qu ils sont magiques!"')
                    objQuest = ['gâteau']
                if objQuest[0] == 'gâteau' and 'gâteau' in items:
                    print('VILLAGEOIS:"Voila donc ce fameux gâteau! Hmm, je n arrive pas à dire s il est magique,')
                    print('            mais une chose est sûre, c est qu il est spécial, je t en remercie!')
                    print('            Maintenant, j aimerais voir une grande potion verte. On dit qu elles sont ')
                    print('            très rares et encore plus éfficaces que les simples!"')
                    objQuest = ['grande potion verte']
                if objQuest[0] == 'grande potion verte' and 'grande potion verte' in items:
                    print('VILLAGEOIS:" Ooh très interressant! C est vrai qu il émane d elle une force vraiment ')
                    print('             spéciale! Je te remercie!')
                    print('             Pour finir, je voudrais voir le gant de puissance. Je ne sais où il se ')
                    print('             trouve, mais toi et moi serons heureux en le trouvant!"')
                    objQuest = ['gant de puissance']
                if objQuest[0] == 'gant de puissance' and ['gant de puissance','mana',200] in weapon2List:
                    print('VILAGEOIS:" Ooh quelle manifique objet, je te remercie pour toutes ces découvertes!')
                    print('            Pour te remercier, prends-donc ces 400 noaïs et ces 350 points d exp!"')
                    bourse = bourse + 400
                    exp = exp + 350
                    endQuest = 0
                    objQuest = []
                    for i in range(len(quest)):
                        if quest[i] == quete[0]:
                            supp = i
                    quest.pop(supp)
                    quete = [0,0]
                else:
                    print('VILLAGEOIS:"Tu ne l as pas encore? Ce n est pas grave, je t attends."')
                talking = 1
            ### hors quete ###
            else:
                if talking == 0:
                    print(pnj())
                    talking = 1
######################################################
        if action == '/help':
            print('/invent :')
            print(" -> Permet d'afficher votre inventaire")
            print('/show.level :')
            print(" -> Permet de voir votre niveau actuel et le nombre d'exp restant pour augmenter de niveau")
            print('/shop :')
            print(" -> Permet d'accéder à la boutique et d'acheter des objets/")
            print('/talk :')
            print(" -> Permet de parler à des personnages de la contrée.")
            print('/area :')
            print(" -> Permet de changer de région dans la contrée, quand vous en avez débloqué l'accès.")
            print('/weapon :')
            print(" -> Permet d'équiper une arme secondaire, lorque vous en possédez.")
            print('/quest :')
            print(" -> Permet de lire un parchemin de quête, et de la commencer.")
            print('/quest.verif :')
            print(" -> Permet de vérifier votre avancement dans ma quête que vous avez démaré")
            print('/item :')
            print(" -> Permet de comsommer un des objets de son inventaire.")
            print('/mob :')
            print(" -> Permet de lancer un combat contre un ennemi.")
            print('/boss :')
            print(" -> Lorsque vous avez obtenu un parchemin de boss, permet de l'invoquer dans la bonne zone.")
            print('/finalboss :')
            print(" -> Permet d'invoquer le boss final, Zmeyevick, et de lancer le combat contre lui.")
            print(' -> /attack1 :')
            print("   -> Permet d'attaquer à l'épée (commande uniquement dans un combat).")
            print(' -> /attack2 :')
            print("   -> Permet d'attaquer à l'aide de son arme secondaire, uniquement si elle est équipée (commande uniquement dans un combat).")
            print(' -> /defend :')
            print("   -> Permet d'utiliser de la mana pour se défendre le temps de 2 tours (commande uniquement dans un combat).")
            print(' -> /item :')
            print("   -> Permet de consommer un objet de son inventaire en combat.")
            print('/save :')
            print(" -> Permet de sauvegarder votre progression")
            print('/end :')
            print(" -> Permet d'arrêter sa partie, et de sauvegarder.")
########################################################
        if action == '/save':
            donnees = ['full',level,life,maxlife,mana,maxmana,items,quest,quete,objQuest,endQuest,bosses,weapon1,weapon2,weapon2List,lvlepee,lvlshield,munition,bourse,area,areaList,artefacts,exp,lockQuest,lockWeapon,lockBoss,lockArtefacts,nbkill,shopWeapon,shopEpee,shopShield,shopItem,name]
            print("Sauvegarde...")
            sauvegarde = open("save.txt", "wt")
            sauvegarde.writelines([str(donnees[x]) + "|" for x in range(len(donnees))])
            sauvegarde.close()
            
##########################################################


    donnees = ['full',level,life,maxlife,mana,maxmana,items,quest,quete,objQuest,endQuest,bosses,weapon1,weapon2,weapon2List,lvlepee,lvlshield,munition,bourse,area,areaList,artefacts,exp,lockQuest,lockWeapon,lockBoss,lockArtefacts,nbkill,shopWeapon,shopEpee,shopShield,shopItem,name]
    print("Sauvegarde...")
    sauvegarde = open("save.txt", "wt")
    sauvegarde.writelines([str(donnees[x]) + "|" for x in range(len(donnees))])
    sauvegarde.close()


start()
