from src.core.analyzer import Analyzer


path = r"C:\Users\vhdaq\Desktop\DramaTest\000交付"


analyzer = Analyzer(path)


project = analyzer.analyze()


print("=================")

print(project)

print()

print(project.summary())

print()

print("拆集:")

print(project.split_map)