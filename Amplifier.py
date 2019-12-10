from Intcode import Intcode

class Amplifier:

  def __init__(self, code, v1=0, v2=None, stopOnOutput = False):
    self.in1 = v1
    self.in2 = v2
    if self.in2 != None:
      self.ic = Intcode([v1, v2], stopOnOutput)
    else:
      self.ic = Intcode([v1], stopOnOutput)
    self.code = code

    self.output = 0
    self.running = True

    self.ic.loadData(self.code)

  def computeOutput(self):
    self.running = self.ic.loadCode()
    self.output = self.ic.getOutput()
    #print(self.outputs)
    return self.output

  def addInput(self, value):
    self.ic.addInput(value)

