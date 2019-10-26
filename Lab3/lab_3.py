import lab3dataget as td
import sys

# td.downloads(sys.argv[0])
data = td.get_area_site('Пороховы')
for key in data:
    print(key)
