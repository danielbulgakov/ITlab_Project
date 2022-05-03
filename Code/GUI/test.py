class Shark():

    i = 3

    def seti(self, per):
        self.i = per

    def focus(self):
        testfocus(s1,s2)

s1 = Shark()
s2 = Shark()
s2.seti(5)
s1.focus()

def testfocus(s,p):
    s.i = p.i

print(s1.i)