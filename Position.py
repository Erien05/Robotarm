import math
import numpy as np

degree = lambda n: (np.pi/180) * n #-> degree to radians
radians = lambda n: (180/np.pi) * n #-> radians to degree

betrag = lambda vektor: np.sqrt((vektor[0]**2)+(vektor[1]**2)) #-> leange eines 2d vektors bzw. der betrag von einem 2d vektor
vektorAdd = lambda a, b: [a[0] + b[0], a[1] + b[1]]

lenghtBasis = 55 + 29 # lenght for base (55mm) of arm and wood platform (29mm)
lenghtAchse1 = 150
lengthAchse2 = 122
lenghtAchse3 = 50


add = lambda Q, R: [q+r for q,r in zip(Q, R)]
sub = lambda Q, R: [q-r for q,r in zip(Q, R)]
qround = lambda Q, n: [round(q, n) for q in Q]
norm = lambda Q: np.sqrt(sum(q*q for q in Q))
smult = lambda s,Q: [s*q for q in Q]
normalize = lambda Q: smult(1/norm(Q), Q)

def mult(Q,R):
      P = [0, 0, 0, 0]
      for i in range(4):
            for j in range(4):
                  P[abs(i-j) if i*j==0 or i==j else 6-i-j] \
                  += Q[i] * R[j] * (1 if i*j==0 or i%3+1==j else -1)
      return P

#def degree(n): #wandelt gradmass in bogenmass um
      #return (math.pi/180) * n
#degree = lambda n: (np.pi/180) * n

#print(mult([1,3,-2,2], [2,5,-6,3])) #-> (1 + 3i + -2j + 2k) * (2 + 5i + -6j + 3k)

conj = lambda q: [q[0]] + [-q[i] for i in range (1, 4)]

def rotate(Punkt, Achse, theta):
      Q = [np.cos(theta/2)] + smult(np.sin(theta/2), normalize(Achse))
      return mult(mult(Q, [0]+Punkt), conj(Q))[1:]

#print(rotate([4,2,0], [0,0,-1], -np.pi/2)) #-> drehung des punktes (4,2,0) um -pi/2 um die negative z-Achse

### quaternionen ende





### eigene loesung anfang


def angleToKoordinate(angle1, angle2, angle3, angle4, angleStepper): #-> servo1, servo2, servo3, servo4, stepper
      if(35 > angle1 or angle1 > 145 or \
         50 > angle2 or angle2 > 180 or \
          0 > angle3 or angle3 > 180 or \
        100 > angle4 or angle4 > 260):
            print('Error: given angles are out of bounds.')
            return

      angle1 = degree(angle1)
      angle2 = degree(angle2)
      angle3 = degree(angle3)
      angle4 = degree(angle4)
      angleStepper = degree(angleStepper)

      vektorBasis = [0, 0, lenghtBasis]
      vektor1 = rotate([lenghtAchse1, 0, 0], [0, -1, 0], angle1)

      angleVektor2 = angle2-np.pi+angle1
      vektor2 = rotate([lengthAchse2, 0, 0], [0, -1, 0], angleVektor2)

      angleVektor3 = angle4-(2*np.pi)+angle1+angle2
      vektor3 = rotate([lenghtAchse3, 0, 0], [0, -1, 0], angleVektor3)
      vektor3 = rotate(vektor3, vektor2, angle3)

      ortsvektor = add(add(add(vektor1, vektor2), vektor3), vektorBasis)
      koordinate = rotate(ortsvektor, [0, 0, 1], angleStepper)

      return qround(koordinate, 2)

# test = angleToKoordinate(60, 115, 0, 185, 40)
# print(test)

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
