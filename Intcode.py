class Intcode:

  def __init__(self, inputs = [], stopOnOutput = False):
    self.p = 0
    self.opcode = 0
    self.c = 0
    self.b = 0
    self.a = 0
    self.debug = False

    self.inputs = inputs
    self.output = None
    self.data = []
    self.stopOnOutput = stopOnOutput
    
  def loadData(self, fileName):
    with open (fileName, "r") as f:
      fileData = f.read()
      self.data = [ int(x) for x in fileData.split(",") ]

  def getCodes(self):
    self.opcode = self.data[self.p] % 100
    codes = self.data[self.p] // 100
    self.c = codes % 10
    codes = codes // 10
    self.b = codes % 10
    codes = codes // 10
    self.a = codes % 10

    if self.debug: print(self.data[self.p], self.opcode, self.c, self.b, self.a)

  def addMult(self, op):
    #op = 1 add
    #op = 2 Multiply
    n1 = self.data[self.p + 1]
    n2 = self.data[self.p + 2]

    #position or immediate mode
    if self.c == 0:
      n1 = self.data[n1]
    if self.b == 0:
      n2 = self.data[n2]

    if op == 1:
      total = n1 + n2
    else:
      total = n1 * n2

    store = self.data[self.p + 3]
    self.data[store] = total
    self.p = self.p + 4

  def inputData(self):
    n1 = self.data[self.p + 1]
    if len(self.inputs) > 0:
      n2 = self.inputs[0]
      del self.inputs[0]
      self.data[n1] = n2
      self.p = self.p + 2
    #else:
      #n2 = int(input("> "))
      

  def outputData(self):
    n1 = self.data[self.p + 1]
    if self.c == 0:
      n1 = self.data[n1]
    #print(n1)
    self.output = n1
    self.p = self.p + 2

  def getOutput(self):
    return self.output

  def loop(self, op):
    #op = 1 Not Zero
    #op = 2 Zero
    n1 = self.data[self.p + 1]
    n2 = self.data[self.p + 2]
    #position or immediate mode
    if self.c == 0:
      n1 = self.data[n1]
    if self.b == 0:
      n2 = self.data[n2]

    if n1 != 0 and op == 5:
      self.p = n2
    elif n1 == 0 and op == 6:
      self.p = n2
    else:
      self.p = self.p + 3

  def compare(self, op):
    #op = 7 less than
    #op = 8 equal to
    
    n1 = self.data[self.p + 1]
    n2 = self.data[self.p + 2]

    #position or immediate mode
    if self.c == 0:
      n1 = self.data[n1]
    if self.b == 0:
      n2 = self.data[n2]

    store = self.data[self.p + 3]

    if op == 7 and n1 < n2:
      self.data[store] = 1
    elif op == 8 and n1 == n2:
      self.data[store] = 1
    else:
      self.data[store] = 0
    
    self.p = self.p + 4

  def addInput(self, value):
    self.inputs.append(value)

  def loadCode(self):
    self.getCodes()
    if self.debug: print("Opcode compare: ", self.opcode, "Index:", self.p)
    while self.opcode != 99:
      if self.opcode == 1 or self.opcode == 2:
        if self.debug: print("Add or multiply")
        self.addMult(self.opcode)
      elif self.opcode == 3:
        if self.debug: print("Input data")
        self.inputData()
      elif self.opcode == 4:
        if self.debug: print("Output data")
        self.outputData()
        if self.stopOnOutput: return True
      elif self.opcode == 5 or self.opcode == 6:
        if self.debug: print("Loop")
        self.loop(self.opcode)
      elif self.opcode == 7 or self.opcode == 8:
        if self.debug: print("Compare")
        self.compare(self.opcode)
      self.getCodes()
    return False