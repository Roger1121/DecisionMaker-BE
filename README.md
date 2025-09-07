# DecisionMaker
Aplikacja umożliwiająca rozwiązywanie problemów w oparciu o analizę wielokryterialną. Pozwala ona na porównanie kilku rozwiązań danego problemu z uwzględnieniem różnych czynników wpływających na ich atrakcyjność. W aplikacji zaimplementowano dwie metody analizy - metodę AHP oraz Hellwiga. Celem utworzenia aplikacji było porównanie wyżej wymienionych metod pod względem ich skuteczności w szeregowaniu poszczególnych rozwiązań i wygody użycia. Funkcjonalności zaimplementowane w aplikacji:
 - Dodawanie problemów do analizy (tylko dla administratora)
 - Ukrywanie problemów z widoku standardowego (tylko dla admiistratora)
 - Rozwiązywanie problemów z losowo przydzieloną metodą analizy wielokryterialnej
 - Dodawanie pytań do ankiety ewaluacyjnej (tylko dla administratora)
 - Wypełnianie ankiety ewaluacyjnej po rozwiązaniu dwóch problemów
 - Możliwość resetu hasła z wykorzystaniem powiadomień mailowych

Część backendowa została napisana w Pythonie i została podzielona na dwie części:
 - REST API wykonane w Django Rest Framework
 - Bibliotekę metod analizy wielokryterialnej - ręczna implementacja metod i metryk odległości z wykorzystaniem pakietów pandas i numpy
