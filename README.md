# Przykładowy algorytm porównywania formularza z charakterystyką.

Aplikacja w Flask do porównywania dwóch produktów bazująca na metryce Levenshteina.  
Dla 7 cech liczy odległość Levenshteina, ignorując wielkość liter i znaki specjalne.  
Średnia liczona jest po odrzuceniu najmniejszej i największej wartości.


### Uruchomienie

```
docker build -t levenshtein-app .  
docker run -p 5000:5000 levenshtein-app 
```

Otwórz http://localhost:5000
