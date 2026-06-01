import math
import numpy as np

### eigene loesung anfang

degree = lambda n: (np.pi/180) * n #-> degree to radians
radians = lambda n: (180/np.pi) * n #-> radians to degree

betrag = lambda vektor: np.sqrt((vektor[0]**2)+(vektor[1]**2)) #-> leange eines 2d vektors bzw. der betrag von einem 2d vektor
vektorAdd = lambda a, b: [a[0] + b[0], a[1] + b[1]]

lenghtBasis = 55 + 29 # lenght for base (55mm) of arm and wood platform (29mm)
lenghtAchse1 = 150
lengthAchse2 = 122
lenghtAchse3 = 50

def angleToKoordinate(angle1, angle2, angle3, angle4, angleStepper): #-> stepper, servo1, servo2, servo3, servo4
    if(35 > angle1 or angle1 > 145 or \
        50 > angle2 or angle2 > 180 or \
        0 > angle3 or angle3 > 180 or \
        100 > angle4 or angle4 > 260):
            print('Error: given angles are out of bounds.')
            return

    angle1 = degree(angle1) #+ degree(35)
    angle2 = degree(angle2)
    angle4 = degree(angle4) #+ degree(100)
    angleStepper = degree(angleStepper)

    basisVektor = [0, lenghtBasis]

    vektor1 = [np.cos(angle1) * lenghtAchse1] + [np.sin(angle1) * lenghtAchse1]

    angleVektor2 = angle2-np.pi+angle1
    vektor2 = [np.cos(angleVektor2) * lengthAchse2] + [np.sin(angleVektor2) * lengthAchse2]

    angleVektor3 = angle4-(2*np.pi)+angle1+angle2
    vektor3 = [np.cos(angleVektor3) * lenghtAchse3] + [np.sin(angleVektor3) * lenghtAchse3]

    vektorBasis_1 = vektorAdd(basisVektor, vektor1)
    vektor1_2 = vektorAdd(vektorBasis_1, vektor2)
    vektor1_3 = vektorAdd(vektor1_2, vektor3)

    vektorGround = [np.cos(angleStepper) * vektor1_3[0]] + [np.sin(angleStepper) * vektor1_3[0]]

    #koordinate = [vektorGround[0], vektorGround[1], vektor1_3[1]]
    koordinate = [round(vektorGround[0], 2), round(vektorGround[1], 2), round(vektor1_3[1], 2)]
    return koordinate

test = angleToKoordinate(60, 115, 0, 185, 40)       #0, 90+17, 150, 0, 180+13)
print(test)

def koordinateToAngles(koordinate):
    ##### ToDo - Add guard to prevent from inputing non reachable koordinate #####

    x = koordinate[0]
    y = koordinate[1]
    z = koordinate[2] - lenghtBasis

    angleStepper = round(radians(  np.arctan(y/x)  )) #math.atan() oder math.acos()

    vektor2d_ges = [betrag([x, y])] + [z]
    vektor3 = [-lenghtAchse3, 0]
    vektorFromZeroToVektor2 = vektorAdd(vektor2d_ges, vektor3)

    laengeVektorFromZeroToVektor2 = betrag(vektorFromZeroToVektor2)

    angle1 = round(radians(  np.arctan(z/vektorFromZeroToVektor2[0]) + np.arccos((lenghtAchse1**2 + laengeVektorFromZeroToVektor2**2 - lengthAchse2**2)/(2 * lenghtAchse1 * laengeVektorFromZeroToVektor2))  ))
    angle2 = round(radians(  np.arccos((lenghtAchse1**2 + lengthAchse2**2 - laengeVektorFromZeroToVektor2**2)/(2 * lenghtAchse1 * lengthAchse2)) ))
    angle3 = 0
    angle4 = 360 - angle1 - angle2

    return [angle1, angle2, angle3, angle4, angleStepper]


#      print(koordinateToAngles( test ))





      ### eigene loesung ende

