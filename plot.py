import matplotlib.pyplot as pyplot
import re

file = open("out.txt")

errors = []
lines = str.join("", file.readlines())
compiled = re.compile("error = (\d+.?\d*)")
errors = compiled.findall(lines)

compiled = re.compile("Actual fitness: (\d+)")
final_scores = compiled.findall(lines)

pyplot.subplot(211)
pyplot.semilogy(errors)
pyplot.subplot(212)
pyplot.semilogy(final_scores)
pyplot.show()
