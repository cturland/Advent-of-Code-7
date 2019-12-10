from Amplifier import Amplifier
from itertools import permutations

def runAmp(code, v1=0, v2=0):
  amp = Amplifier(code, v1, v2)
  output = amp.computeOutput()
  return output

def testAllSettings(code, settings):
  highest = 0
  highestSettings = []

  for p in list(permutations(settings,5)):
    outputs = [0]
    for s in range(len(p)):
      outputs.append(runAmp(code, p[s], outputs[s]))

    if outputs[5] > highest:
      highest = outputs[5]
      highestSettings = p
      alloutputs = outputs

  print("Highest:",highest,"\n")
  print("0 -> A",alloutputs[1], "-> B",alloutputs[2], "-> C", alloutputs[3], "-> D", alloutputs[4], "-> E", alloutputs[5], "-> (to thrusters)\n")
  print(highestSettings)

def testSetting(code, settings):
  outputs = [0]
  for s in range(len(settings)):
    outputs.append(runAmp(code, settings[s], outputs[s]))
  
  print("0 -> A",outputs[1], "-> B",outputs[2], "-> C", outputs[3], "-> D", outputs[4], "-> E", outputs[5], "-> (to thrusters)\n")

def feedbackAmps(code, settings):
  amps = []
  outputs = [0, None, None, None, None]
  

  for i in range(len(settings)):
    amp = Amplifier(code, settings[i], outputs[i], True)
    amps.append(amp)

  i = 0
  while amps[0].running and amps[1].running and amps[2].running and amps[3].running and amps[4].running:
    
    outputs[i] = amps[i].computeOutput()
    
    if i+1 == len(amps):
      amps[0].addInput(outputs[i])
      i = 0
    else:
      amps[i+1].addInput(outputs[i])
      i += 1
  
  return(outputs[len(amps)-1])
    
def testAllFeedbackAmps(code, settings):
  highest = 0
  highestSettings = []
  
  for p in list(permutations(settings,len(settings))):
    output = feedbackAmps(code, p)

    if output > highest:
      highest = output
      highestSettings = p

  print(highest, highestSettings)
  


def main():
  code = "avc7.txt"
  settings = [0,1,2,3,4]
  #testAllSettings(code, settings)
  testSetting(code, settings)
  #feedbackAmps(code, settings, 5)
  #testAllFeedbackAmps(code, settings)

  
  



main()
