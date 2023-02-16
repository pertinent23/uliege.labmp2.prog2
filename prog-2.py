import math
import pygame
import sys

BLEUCLAIR = (127, 191, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
NOIR = (0, 0, 0)

#Données pour le dessin vectoriel
A = 2
B = 5
C = 20

# Constante de coulomb
K = 8.9876 * 10**9;

RAYON_OBJET = 10

dimensions_fenetre = (1600, 900)
images_par_seconde = 25

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programmme 1")

horloge = pygame.time.Clock()

objets = []

def ajouter_objet(x, y,q):
    objets.append((x, y, q))


def retirer_objet(x, y):
    for obj in objets:
        if distance((x, y), (obj[0], obj[1])) <= RAYON_OBJET:
            objets.remove(obj)

def dessiner_objects(): 
    for obj in objets:
        x, y, q = obj;
        coleur = NOIR if q < 0 else ROUGE
        
        pygame.draw.circle(fenetre, coleur, (x, y), RAYON_OBJET)


def deplacer_pol( point, distance, orientation ):
    x, y = point
    orientation = orientation * -1
    x = distance * math.cos( orientation ) + x
    y = -1 * distance * math.sin( orientation ) + y
    return (x, y)

def distance(a, b) :
    xa, ya = a
    xb, yb = b
    return math.sqrt((xb - xa)**2  + (yb - ya)**2)

def norme(x, y):
    return math.sqrt(x**2 + y**2)

def dessiner_vecteur(couleur, origine, vecteur):
    x0, y0 = origine
    x1, y1 = vecteur
     
    p4 = ( x0 + x1, y0 + y1 )
    alpha = math.atan2( y1, x1 )
    
    if distance( origine, p4 ) > C:
        
        p1 = deplacer_pol(origine, A, alpha - (math.pi/2))
        p7 = deplacer_pol(origine, A, alpha + (math.pi/2))

        p2 = deplacer_pol(p1, distance(p4, origine) - C, alpha)
        p6 = deplacer_pol(p7, distance(p4, origine) - C, alpha)

        p3 = deplacer_pol(p2, B, alpha - (math.pi/2))
        p5 = deplacer_pol(p6, B, alpha + (math.pi/2))

        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4, p5, p6, p7])
    else: 
        p3 = p4
        p1 = deplacer_pol(p3, C, alpha + math.pi )
        p2 = deplacer_pol(p1, A + B, alpha - (math.pi / 2))
        p4 = deplacer_pol(p1, A + B, alpha + (math.pi / 2))
        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4])

def calculer_champ(x, y):
    resultat_x, resultat_y = 0, 0

    for charge in objets:
        r = distance((x, y), (charge[0], charge[1]))
        
        if r < 20:
            return None
        
        norme_v = K*abs(charge[2])/r**2
        alpha = 0
        
        if charge[2] > 0:
            alpha = math.atan2(y-charge[1], x-charge[0])
        else:
            alpha = math.atan2(charge[1]-y, charge[0]-x)
            
        vecteur_champ = (math.cos(alpha)*norme_v, math.sin(alpha)*norme_v)
            
        resultat_x += vecteur_champ[0]
        resultat_y += vecteur_champ[1]
    
    return resultat_x, resultat_y

def dessiner_champ():
    pas = 50
    y = -pas
    while y <= dimensions_fenetre[1] + pas:
        x = -pas
        while x <= dimensions_fenetre[0] + pas:
            e = calculer_champ(x, y)
            if e and norme(e[0], e[1]) > 1e-10:
                norme_e = norme(e[0], e[1]);
                e_prime = (40*e[0]/norme_e, 40*e[1]/norme_e)
                
                vecteur = (x + e_prime[0], y + e_prime[1])
                origine = (1.5*x - vecteur[0]/2, 1.5*y - vecteur[1]/2)
                resultat = (0.5*vecteur[0] + x/2 - origine[0], 0.5*vecteur[1] + y/2 - origine[1])
                
                v = math.sqrt(1000*norme_e)
                couleur = BLEU
                
                if v <= 8:
                    couleur = (255, 255*v/8, 0)
                elif v <= 16:
                    couleur = (255*(16-v)/8, 255, 255*(v-8)/8)
                elif v <= 24:
                    couleur = (0, 255*(24-v)/8, 255)
                elif v <= 32:
                    couleur = (255*(v-24)/8, 0, 255)
                else:
                    couleur = (255, 0, 255)
                
                dessiner_vecteur(couleur, origine, resultat)
            x += pas
        y += pas

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            x, y = evenement.pos
            if evenement.button == 1 or evenement.button == 3:
                ajouter_objet(x, y, 1e-7 if evenement.button == 1 else -1e-7)
            elif evenement.button == 2:
                retirer_objet(x, y)
    
    fenetre.fill(BLEUCLAIR)
    dessiner_objects()
    dessiner_champ()
    
    pygame.display.flip()
    horloge.tick(images_par_seconde)