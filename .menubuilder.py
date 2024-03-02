import os
import operator

def getdirlist(dir):
    dirlist = []
    for entry in dir:
        dirlist.append(entry)
    dirlist.sort(key = operator.attrgetter('name'))
    return dirlist
    # This will return proper text
    
path = os.path.expanduser('~/gMenu')
list = []
menu = []
menus = []
openingtext = """<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
  "http://www.freedesktop.org/standards/menu-spec/1.0/menu.dtd">

<Menu>
    <Name>Applications</Name>
    <DefaultDirectoryDirs/>
    <DefaultAppDirs/>
    "
    """
text = ""

# Prelude, Body, Finale
layout = ""
includes = ""

var = 0
scanlist = getdirlist(os.scandir(path))
folders = []
print("Folders: ", folders)

for entry in scanlist:
	print("Entry name: ", entry.name)
	if entry.is_dir():
		folders.append(entry)
		openingtext+= "<AppDir>"""+path+"/"+entry.name+"</AppDir>"""
openingtext+= '""'

for entry in folders:
	print(entry.name)
	if entry.is_dir:
		contents = getdirlist(os.scandir(path+"/"+entry.name))
		if(var == 1):
			if(len(contents) != 0):
				print("Including separator.")
				layout+=("\t\t<Separator/>\n")
			else:
				var = 0
		print("Contents:")
		for content in contents:
			print(content.name)
			if content.is_file():
				tempvar = ("\t\t<Filename>"+content.name+"</Filename>\n")
				includes+=tempvar
				layout+=tempvar
			elif content.is_dir():
				menus.append(content)
				layout+=("\t\t<Menuname>"+content.name+"""</Menuname>\n""")
			var = 1
text = "\t<Include>\n"+includes+"\t</Include>\n\t<Layout>\n"+layout+"\t</Layout>"

def printlist(dirlist, locmenus, letsub):
    global text
    layout = ""
    includes = ""
    for entry in dirlist:
        if entry.is_file():
            tempvar = ("\t\t<Filename>"+entry.name+"</Filename>\n")
            includes+=tempvar
            layout+=tempvar
            
        elif entry.is_dir():
            if(letsub == 1): 
                locmenus.append(entry)
            layout+=("\t\t<Menuname>"+entry.name+"""</Menuname>\n""")
    text+=("""\t<Include>\n"""+includes+"""\t</Include>\n\n""")
    text+=("""\t<Layout>\n"""+layout+"\t</Layout>")
    return dirlist, locmenus

for entry in menus:
    # Do a bunch of stuff
    newvar = (entry.path)
    openingtext+="""<AppDir>"""+newvar+"""</AppDir>
    """
    locmenus = []
    newit = getdirlist(os.scandir(newvar))
    if(len(newit) > 0):
        text+=("\n\n\t<Menu>\n\t<Name>"+entry.name+"</Name>\n")
        newlit, locmenus = printlist(newit, locmenus, 1)

        # For first-level submenus
        for locentry in locmenus:
            newervar = (locentry.path)
            newerit = getdirlist(os.scandir(newervar))

            if(len(newerit) > 0):
                text+=("\n\n\t<Menu>\n\t<Name>"+locentry.name+"</Name>\n")
                newerlit = printlist(newerit, 0, 0)
            # And now close
            text+="\n\t</Menu>"
        text+="\n\t</Menu>"
openingtext+="\n"
text+="\n</Menu>"
openingtext+=text
filename = os.path.expanduser('~/gMenu/.gMenu.menu')
with open(filename, 'w', encoding="utf-8") as file:
    file.write(openingtext)
