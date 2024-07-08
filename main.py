import dbus
import time
import pyautogui
from pyautogui import ImageNotFoundException

pyautogui.FAILSAFE = True

def desactiver_screensaver():
    print("Désactivation du ScreenSaver")
    bus = dbus.SessionBus()
    saver = bus.get_object('org.freedesktop.ScreenSaver', '/ScreenSaver')
    saver_interface = dbus.Interface(saver, dbus_interface='org.freedesktop.ScreenSaver')

    return saver_interface.Inhibit("er_automater", "Parce que je veux beaucoup de runes")

def reactiver_screensaver(cookie):
    print("Réactivation du ScreenSaver")
    bus = dbus.SessionBus()
    saver = bus.get_object('org.freedesktop.ScreenSaver', '/ScreenSaver')
    saver_interface = dbus.Interface(saver, dbus_interface='org.freedesktop.ScreenSaver')

    saver_interface.UnInhibit(cookie)

def detecter_interface_jeu():
    try:
        print("- Détection de l'interface de jeu")
        res = pyautogui.locateOnScreen("screenshots/jeu/in_game.png", grayscale=True, confidence=0.9, region=(0,0, 1920, 1080))
        print("On est dans le jeu")
        return True
    except ImageNotFoundException:
        return False

def detecter_carte_ouverte():
    try:
        print("- Détection de la carte")
        res = pyautogui.locateOnScreen("screenshots/jeu/carte/generale.png", region=(0,0, 1920, 1080))
        print("On est dans la carte")
        return True
    except ImageNotFoundException:
        return False

def detecter_site_de_grace():
    try:
        print("- Détection du site de grâce")
        res = pyautogui.locateOnScreen("screenshots/jeu/site_de_grace_ouvert.png", region=(0,0, 1920, 1080))
        print("On est dans le menu du site de grâce")
        return True
    except ImageNotFoundException:
        return False

def decouverte_initiale():
    print("Détection initiale:")
    state = None
    while True:
        if state is None:
            # Steam
            try:
                print("- Détection de Steam")
                res = pyautogui.locateOnScreen("screenshots/menu/steam.png", region=(0,0, 1920, 1080))
                print("On est dans Steam et le jeu n'est pas ouvert")
                try:
                    res = pyautogui.locateOnScreen("screenshots/menu/steam_jouer.png", region=(0,0, 1920, 1080))
                    x = res.left + res.width / 2
                    y = res.top + res.height / 2
                    print(f"On clique sur le bouton (x = {x}, y = {y})")
                    pyautogui.click(x = x, y = y)
                    state = "demarrage"
                    continue
                except ImageNotFoundException:
                    print("ERREUR: Impossible de trouver la position exacte du bouton Jouer")
            except ImageNotFoundException:
                pass

        if state is None or state == "demarrage":
            # Menu principal
            try:
                print("- Détection du menu principal")
                res = pyautogui.locateOnScreen("screenshots/menu/principal.png", region=(0,0, 1920, 1080))
                print("On est dans le menu principal")
                x = res.left + res.width / 2
                y = res.top + res.height / 2
                print(f"On clique à la position (x = {x}, y = {y})")
                pyautogui.keyDown("e")
                pyautogui.keyUp('e')
                state = "menu_general"
                continue
            except ImageNotFoundException:
                pass

        if state is None or state == "menu_general":
            # Menu d'information
            try:
                print("- Détection du menu d'informations")
                res = pyautogui.locateOnScreen("screenshots/menu/informations.png", region=(0,0, 1920, 1080))
                print("Le dialogue d'informations est ouvert, on doit le fermer et charger la partie")
                pyautogui.keyDown('e')
                pyautogui.keyUp('e')
                time.sleep(1)
                pyautogui.keyDown('e')
                pyautogui.keyUp('e')
                state = "menu_information"
                continue
            except ImageNotFoundException:
                pass

        # En jeu
        if detecter_interface_jeu():
            return "jeu"

        # Dans la carte
        if detecter_carte_ouverte():
            return "carte"

        # Dans le menu du site de grâce
        if detecter_site_de_grace():
            return "site_de_grace"

        print("Rien n'a été trouvé, on attend avant de recommencer")
        time.sleep(3)

def ouvrir_carte():
    # Détecter si la carte est ouverte
    try:
        print("Détection de la carte:")
        res = pyautogui.locateOnScreen("screenshots/jeu/carte/generale.png", region=(0,0, 1920, 1080))
        print("- On est déjà dans la carte")
    except ImageNotFoundException:
        print("- La carte n'est pas ouverte, on l'ouvre")
        pyautogui.keyDown('g')
        time.sleep(0.1)
        pyautogui.keyUp('g')
        ouvrir_carte()

def teleporter_bon_endroit(detecter_carte = True):
    # Détecter la carte et se rendre dans la carte principale (ou du DLC)
    try:
        print("Détection de la carte spécifique qui est ouverte:")
        res = pyautogui.locateOnScreen("screenshots/jeu/carte/principale.png", region=(0,0, 1920, 1080))
        print("- On est dans la carte principale (surface ou sous-sol)")
    except ImageNotFoundException:
        print("- On est dans la carte du DLC, ouverture de la carte principale")
        pyautogui.keyDown('x')
        pyautogui.keyUp('x')
    
    # Zoom out pour voir l'ensemble de la carte
    print("Zoom out pour voir l'ensemble de la carte")
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    print("Déplacement dans le bas de la carte pour permettre la détection")
    pyautogui.keyDown("s")
    time.sleep(5)
    pyautogui.keyUp("s")

    try:
        print("Détection de l'emplacement (surface ou sous-sol):")
        res = pyautogui.locateOnScreen("screenshots/jeu/carte/principale_surface.png", region=(0,0, 1920, 1080))
        print("- On est dans la carte principale (surface), affichage de la carte du sous-sol")
        pyautogui.keyDown('y')
        pyautogui.keyUp('y')
    except ImageNotFoundException:
        print("- On est dans la carte principale (sous-sol)")

    print("Déplacement dans le bas à droite de la carte pour faciliter le positionnement")
    pyautogui.keyDown('s')
    time.sleep(5)
    pyautogui.keyUp('s')
    pyautogui.keyDown('d')
    time.sleep(5)
    pyautogui.keyUp('d')
    print("Positionnement sur le point de téléportation")
    pyautogui.keyDown('w')
    time.sleep(0.95)
    pyautogui.keyUp('w')
    pyautogui.keyDown('a')
    time.sleep(1.65)
    pyautogui.keyUp('a')

    teleporter()

def teleporter():
    print("Ouverture du dialogue de téléportation")
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')
    while True:
        try:
            print("Validation qu'on est au bon endroit:")
            res = pyautogui.locateOnScreen("screenshots/jeu/carte/validation_teleportation.png", region=(0,0, 1920, 1080))
            print("- On est au bon endroit, confirmation de la téléportation")
            pyautogui.keyDown('e')
            pyautogui.keyUp('e')
            break
        except ImageNotFoundException:
            print("ERREUR: Le dialogue de téléportation n'est pas ouvert ou pointe sur le mauvais point de téléportation")
            time.sleep(1)

    # Attendre la fin du chargement
    while True:
        time.sleep(3)
        if detecter_interface_jeu():
            break

def ouvrir_site_grace():
    print("Ouverture du site de grâce")
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')
    # Attendre la fin du chargement
    while True:
        time.sleep(3)
        if detecter_site_de_grace():
            break

def fermer_site_grace():
    try:
        print("Fermeture du site de grâce")
        res = pyautogui.locateOnScreen("screenshots/jeu/site_de_grace_quitter.png", region=(0,0, 1920, 1080))
        x = res.left + res.width / 2
        y = res.top + res.height / 2
        print(f"On clique à la position (x = {x}, y = {y})")
        pyautogui.click(x = x, y = y)
    except ImageNotFoundException:
        # La sélection est déjà sur le bouton Quitter
        pass
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')
        
    # Attendre la fin du chargement
    while True:
        time.sleep(3)
        if detecter_interface_jeu():
            break

def utiliser_pouvoir_arme():
    print("Utilisation du pouvoir de l'arme")
    pyautogui.keyDown('ctrl')
    pyautogui.keyUp('ctrl')
    time.sleep(2.5)

def avancer(temps):
    pyautogui.keyDown('w')
    time.sleep(temps)
    pyautogui.keyUp('w')

if __name__ == "__main__":
    cookie = desactiver_screensaver()
    try:
        # Ouvrir le jeu et charger la partie
        state = decouverte_initiale()

        # Cliquer dans le jeu
        #pyautogui.moveTo(1, 1)
        #pyautogui.mouseDown()
        #pyautogui.mouseUp()

        if state == "site_de_grace":
            fermer_site_grace()
        # On se téléporte à la corniche menant au palais
        if state != "carte":
            ouvrir_carte()
        teleporter_bon_endroit()

        # Main loop
        while True:
            print("Boucle principale:")
            print("- Avancer vers le site de grâce")
            avancer(0.5)
            # Monter de niveau
            # if assez_souls():
            #     ouvrir_site_grace()
            #     monter_niveau()
            #     fermer_site_grace()

            # Se déplacer au bon endroit pour ramasser le XP
            print("- Marcher jusqu'à la colline")
            avancer(4)
            # On tourne
            pyautogui.keyDown('j')
            time.sleep(.12)
            pyautogui.keyUp('j')
            # Rotation du corps
            avancer(0.1)
            # Attaquer avec le pouvoir de l'arme
            utiliser_pouvoir_arme()
            avancer(1.5)
            utiliser_pouvoir_arme()
            avancer(1.5)
            utiliser_pouvoir_arme()

            # S'éloigner pour permettre la téléportation, même si certains ennemis sont encore en vie
            pyautogui.keyDown('s')
            time.sleep(5)
            pyautogui.keyUp('s')
            # Retéléportation à la corniche menant au palais
            ouvrir_carte()
            time.sleep(1)
            print("Ouverture de la liste des sites de grâce")
            pyautogui.keyDown('f')
            pyautogui.keyUp('f')
            time.sleep(1)
            teleporter()
    finally:
        reactiver_screensaver(cookie)
