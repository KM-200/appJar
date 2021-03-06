from appJar import gui
def press(btn=None):
      print(btn)
      print("names", app.getMenuRadioButton("tester", "names"))
      print("cb1", app.getMenuCheckBox("tester", "cb1"))
      print("cb2", app.getMenuCheckBox("tester", "cb2"))
      print("cb3", app.getMenuCheckBox("tester", "cb3"))

app=gui("DEMO")
app.addMenu("bbb", press)
app.addMenuList("Options", ["a", "b", "c", "d", "e"], press)
app.addMenuList("More", ["a", "b", "c", "d", "e"], press, True)
app.addMenuList("Other", ["a", "b", "c", "d", "e"], press)

app.createMenu("tester")
app.addMenuItem("tester", "this", press)
app.addMenuItem("tester", "this", press)
app.addMenuItem("tester", "-", None)
app.addMenuItem("tester", "this", press)
app.addMenuItem("tester", "this", press)
app.addMenuSeparator("tester")
app.addMenuRadioButton("tester", "names", "fred")
app.addMenuRadioButton("tester", "names", "tom")
app.addMenuRadioButton("tester", "names", "dick")
app.addMenuSeparator("tester")
app.addMenuCheckBox("tester", "cb1")
app.addMenuCheckBox("tester", "cb2")
app.addMenuCheckBox("tester", "cb3")

app.addRadioButton("name", "Fred")
app.addRadioButton("name", "Bob")
app.addRadioButton("name", "Jiull")
app.addEntry("e1")
app.setFocus("e1")
#app.addButtons(["a", "b", "c"], None)
app.addButtons(["d", "e", "f"], press)
app.addButtons(["g", "h", "i"], [press,press,press])
app.addMenuPreferences(press)
app.addMenuWindow()
app.go()
