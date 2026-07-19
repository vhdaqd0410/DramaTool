from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.preview import Preview


path = r"C:\Users\vhdaq\Desktop\DramaTest\000交付"



project = Analyzer(path).analyze()


Mapper().generate(
    project
)


preview = Preview()


result = preview.generate(
    project
)


print(result)