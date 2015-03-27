import sys

jegermegasej = sys.argv[1]
f1 = open(".idea/.name", "w")
f1.write(jegermegasej)
f1.close()
f2 = open("./app/src/main/AndroidManifest.xml", "r+")
someshit = f2.read().replace("template", jegermegasej)
f2.close()
f3 = open("./app/src/main/AndroidManifest.xml", "w")
f3.write(someshit)
f3.close()
print "Renamed solution to: " + sys.argv[1]
