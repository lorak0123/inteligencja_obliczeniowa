# inteligencja_obliczeniowa

# To co Gościu powiedział na ćwiczeniach:
JAKIE MAJĄ BYĆ ŚREDNIE PROPORCJE LOSOWANEJ ROZNORODNOSCI I ILOSCI TOWAROW? -- rozkład jednostajny do wszystkiego<br/>
ILE MA BYC PUNKTOW NA MAPIE? -- od 100 wzwyż<br/>
CZY WSZYSTKIE POJAZDY MUSZĄ JECHAĆ?  -- nie muszą, mozna to obejsc<br/>
pojazd nie musi konczyc w magazynie<br/>

# Poczatkowe ustalenia:
dzielimy punkty po równo względem ilości pojazdów<br/>
wywalamy kota narazie<br/>

# Do zrobienia
meteode genreującą trasę dla wszystkich pojazdów<br/>
przygotować mocki dla kilku róznych tras (typowych i problematycznych)<br/>
przygotowac wizualizację<br/>
metodę do ewaluacji (losowa metoda do generacji trasy i porównanie z naszym algorytmem)<br/>

VRTP- obczaj<br/>
VRPTW- obczaj<br/>

# 3.04.2022
Do optymalizacji:
- ilośc pobieranego towaru z magazynu (na podstawie przyszłego punktu lub na podstawie całego klastru lub mapy)
- klastry (obracanie lub dorzucanie punktów do złego klastra żeby go wyzerować lub wywalać problamtyczne punkty z klastrów lub TAK PRZESUWAĆ PUNKTY MIĘDZY KLASTRAMI, ŻEBY ZOSTAŁ OSTATNI PROBLEMATYCZNY KLASTER Z NAJWIĘKSZYM ZAGĘSZCZENIEM MAGAZYNÓW)
- moduł statystyczny, testowy!!!

# 29.05 
Generalnie testy działają fest powoli i żeby mieć faktycznie 100% szansy, że coś przynosi efekty trzeba odpalić 10000 testów.
Dla stanu początkowego wyniki dla 10000 wyglądają tak:

MULTI<br/>
capacity          1497.360833<br/>
total_dist        3810.096815<br/>
points             494.999800<br/>
mag_returns         14.879500<br/>
avg_mag_dist        25.881065<br/>
avg_point_dist       7.468169<br/>
std_point_dist       9.427731<br/>

SOLO<br/>
capacity               1865.450000<br/>
total_dist             3273.646933<br/>
points                  494.999900<br/>
mag_returns               6.275700<br/>
avg_mag_dist             28.110135<br/>
avg_point_dist            6.525745<br/>
std_point_dist            9.550933<br/>

Dodałem usprawnienie które zmniejsza ilość powrotów do magazynów, ale tak naprawdę powroty do magazynów to tylko tylko promil faktycznej długości trasy i raczej bym juz olał ten temat. Po zmianach 10000 testów:

MULTI<br/>
capacity          1499.466667<br/>
total_dist        3671.902523<br/>
points             494.999800<br/>
mag_returns         12.039200<br/>
avg_mag_dist        25.401467<br/>
avg_point_dist       7.238778<br/>
std_point_dist       9.100950<br/>

SOLO<br/>
capacity          1847.150000<br/>
total_dist        3165.661180<br/>
points             494.999800<br/>
mag_returns          4.330700<br/>
avg_mag_dist        27.209247<br/>
avg_point_dist       6.337005<br/>
std_point_dist       9.145882<br/>

Potem dodałem opcję gdzie zamiast jednego najbliższego punktu wybieramy 2 najbliższe. Następnie liczmy dla nich całą trasę do końca i wybieramy punkt, który daje krótszą trasę. Robimy to na każdym kroku. Wydłuża to proces generacji tras fest. Tryb nazywa się FORTUNE_TELLER i jest w zmiennych środowiskowych.
Testowałem też dla trzech punktów, ale nie przynosi to chyba efektów. Żeby to dokładnie przetestować to trzeba mieć kompa z NASA. Dla 100 testów:

MULTI<br/>
capacity          1514.583333<br/>
total_dist        3271.251365<br/>
points             495.000000<br/>
mag_returns         11.350000<br/>
avg_mag_dist        22.483764<br/>
avg_point_dist       6.466081<br/>

SOLO<br/>
Nie testowałem bo dla jednej trasy FORTUNE_TELLER działa jeszcze dłużej.

Rzeczy, które można jeszcze poprawić to zmienić wielkość obszaru dla pojazdów względem ich wielkości. Zwiększyć obszar dla 2000 i zmniejszyć dla 1000. Tu napewno będzie zysk bo duże pojazdy sa zdecydowanie bardziej efektywne.