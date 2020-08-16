import numpy as np

class Delay():
    def __init__(self, time, feedback, level):
        self.time = time
        self.feedback = feedback
        self.level = level
        self.mem = np.array([[0 for i in range(1024)]],dtype=np.float32)

    def __str__(self):
        s = "║ Delay ║ Time: " + str(self.time)+ " │ Feedback: " + str(self.feedback) + " │ Level: " + str(self.level) + " ║"
        return s

    def activate(self, input):
        output = input
        if len(self.mem) > self.time:
            first_element = self.mem[0]
            output = output + first_element*(self.level/50)
            self.mem = np.delete(self.mem,0,axis=0)
        self.mem = np.vstack([self.mem,output*(self.feedback/100)])
        return output


class Gain():
    def __init__(self,gain):
        self.gain = gain

    def __str__(self):
        s = "║ Gain ║ Gain: " + str(self.gain)+ " ║"
        return s

    def activate(self,input):
        output = input*self.gain
        return output


class Fuzz():
    def __init__(self,gain):
        self.gain = gain

    def __str__(self):
        s = "║ Fuzz ║ Gain: " + str(self.gain)+ " ║"
        return s

    def activate(self,input):
        output = ((input*self.gain)*self.gain)*self.gain
        return output

class Overdrive():
    def __init__(self):
        pass

    def __str__(self):
        s = "║ Overdrive ║"
        return s

    def activate(self,input):
        average = np.average(input)
        maxVal = np.max(input)
        minVal = np.min(input)
        avg2 = np.average([average,maxVal])
        avg3 = np.average([average,minVal])
        output = [avg2 if i >= avg2 else i for i in input]
        output = [avg3 if i <= avg3 else i for i in output]
        output = np.array(output)
        return output