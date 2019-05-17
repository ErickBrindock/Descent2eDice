import numpy as np
import matplotlib.pyplot as plt
import random
import math
class Dice(object):
  color = ""
  face = None

  class Face(object):
    damage = 0
    burst = 0
    range = 0
    defend = 0

    def __init__(self, dmg, burst, range, defend):
      self.damage = dmg
      self.burst = burst
      self.range = range
      self.defend = defend

    def addFace(self, face):
        self.damage += face.damage
        self.defend += face.defend
        self.burst += face.burst
        self.range += face.range

    def normFace(self):
        net = self.damage - self.defend
        if net >= 0:
            self.damage = net
            self.defend = 0
        else:
            self.defend = -net
            self.damage = 0

    def __str__(self):
        out = "["
        if self.damage == 0 and self.burst == 0 and self.range == 0 and self.defend == 0:
            out += "XX  MISS  XX"
        else:
            out += "dmg: " + str(self.damage)
            if self.burst > 0:
                out += " * " * self.burst
            out += " rng: " + str(self.range)
            out += " def:" + str(self.defend)
        out += "]"
        return out


  def __init__(self, color):
    self.face = []
    if color == "red":
        self.face.append(self.Face(1,0,0,0))
        self.face.append(self.Face(2,0,0,0))
        self.face.append(self.Face(2,0,0,0))
        self.face.append(self.Face(2,0,0,0))
        self.face.append(self.Face(3,0,0,0))
        self.face.append(self.Face(3,1,0,0))
    elif color == "blue":
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(2,1,2,0))
        self.face.append(self.Face(2,0,3,0))
        self.face.append(self.Face(2,0,4,0))
        self.face.append(self.Face(1,0,5,0))
        self.face.append(self.Face(1,1,6,0))
    elif color == "yellow":
        self.face.append(self.Face(0,1,1,0))
        self.face.append(self.Face(1,0,1,0))
        self.face.append(self.Face(1,0,2,0))
        self.face.append(self.Face(1,1,0,0))
        self.face.append(self.Face(2,0,0,0))
        self.face.append(self.Face(2,1,0,0))
    elif color == "gray":
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,1))
        self.face.append(self.Face(0,0,0,1))
        self.face.append(self.Face(0,0,0,2))
    elif color == "brown":
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,1))
        self.face.append(self.Face(0,0,0,1))
        self.face.append(self.Face(0,0,0,2))
    elif color == "black":
        self.face.append(self.Face(0,0,0,0))
        self.face.append(self.Face(0,0,0,2))
        self.face.append(self.Face(0,0,0,2))
        self.face.append(self.Face(0,0,0,2))
        self.face.append(self.Face(0,0,0,3))
        self.face.append(self.Face(0,0,0,4))
    self.color = color



  def printface(self, index):
        out = "[" + self.color[0:3] + " "
        if self.color == "gray" or self.color == "brown" or self.color == "black":
            out += "def:" + str(self.face[index].defend)
        elif self.face[index].damage == 0 and self.face[index].burst == 0 and self.face[index].range == 0 and self.face[index].defend == 0:
            out += "--missed--"
        else:
            out += "dmg: " + str(self.face[index].damage)
            if self.face[index].burst > 0:
                out += " *burst* "
            out += " rng: " + str(self.face[index].range)
        out += "]"
        print(out)

  def print_dice(self):
      print(self.color)
      for i in range(6):
          self.printface(i)

  def roll(self, disp=False):
      r = random.randint(0,5)
      if disp == True:
          self.printface(r)
      return self.face[r]

  @staticmethod
  def roll_dice(args, disp = False):
    total = Dice.Face(0,0,0,0)
    for die in args:
        temp = die.roll(disp)
        total.addFace(temp)
    total.normFace()
    print("tot" + str(total))

def generate_pmf(dice):
    totalperm = 6**len(dice)
    dmax = 0
    bmax = 0
    rmax = 0
    defmax = 0
    d_data = np.zeros(10)
    b_data = np.zeros(10)
    r_data = np.zeros(10)
    def_data = np.zeros(10)
    for i in range(totalperm):
        local = Dice.Face(0,0,0,0)
        for j in range(len(dice)):
            local.addFace(dice[j].face[ (i // (6**j)) % 6 ])
        local.normFace()
        d_data[local.damage] += 1
        b_data[local.burst] += 1
        r_data[local.range] += 1
        def_data[local.defend] += 1
        dmax = max(dmax, local.damage)
        bmax = max(bmax, local.burst)
        rmax = max(rmax, local.range)
        defmax = max(defmax, local.defend)
    dmax += 1
    bmax += 1
    rmax+= 1
    defmax += 1
    return d_data[0:dmax] / totalperm, b_data[0:bmax] / totalperm, r_data[0:rmax] / totalperm, def_data[0:defmax] / totalperm

def generate_stats(probs):
    mu = 0
    mu2 = 0
    for i in range(len(probs)):
        mu += i * probs[i]
        mu2 += i * i *probs[i]
    var = mu2 - mu**2
    return mu, var, math.sqrt(var)

def create_hist(dice):
    d_data, b_data, r_data, def_data = generate_pmf(dice)
    plt.subplot(2, 2, 1)
    plt.bar(np.arange(len(d_data)),d_data)
    plt.title("Damage")
    plt.ylabel("%")
    plt.xlabel("Damage")
    plt.subplot(2, 2, 2)
    plt.bar(np.arange(len(b_data)),b_data)
    plt.title("Burst")
    plt.xlabel("Burst Points")
    plt.subplot(2, 2, 3)
    plt.bar(np.arange(len(r_data)),r_data)
    plt.title("Range")
    plt.ylabel("%")
    plt.xlabel("Spaces")
    plt.subplot(2, 2, 4)
    plt.bar(np.arange(len(def_data)),def_data)
    plt.title("Defense")
    plt.xlabel("Defense")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    die_types = ["red", "blue", "yellow", "brown", "gray", "black"]
    dice = []
    for die in die_types:
        dice.append(Dice(die))
    for die in dice:
        die.print_dice()
    test_dice = [dice[0], dice[1], dice[0], dice[4], dice[4]]
    for die in test_dice:
        die.print_dice()
    d, b, r, defen = generate_pmf(test_dice)
    print("       : Average  | Variance | Std. Dev.")
    print("Damage : %6f | %6f | %6f" % generate_stats(d))
    print("Burst  : %6f | %6f | %6f" % generate_stats(b))
    print("Range  : %6f | %6f | %6f" % generate_stats(r))
    print("Defense: %6f | %6f | %6f" % generate_stats(defen))
    create_hist(test_dice)
    #for i in range(2):
    #    Dice.roll_dice(dice[1], dice[4], dice[2])
