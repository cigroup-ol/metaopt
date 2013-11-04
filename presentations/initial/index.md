<!--\n\n\n will create a horizontal slide, \n\n will create a vertical slide -->
# OrgES

Organic Computing for Evolution Strategies


## Allgemeines zum Projekt

-   GitHub/cigroup-ol
-   3-Clause-BSD
-   TravisCI
-   Tox
-   Nose
-   Mock
-   Python 2.5+


## Ziel von OrgES

- Einstellung von Parametern beliebiger Funktionen
- Blackbox-Optimierung von Fitness-Funktionen
- Framework für Erstellung eigener Optimierungsverfahren


## Fitness-Funktionen
    @param.float("a", interval=(0, 1), step=0.1, display_name="α")
    @param.float("b", interval=(-1, 1), step=0.2, display_name="β")
    @param.int("c", interval=(1, 100), display_name="β")
    def f(a, b, c):
        # Berechnung basierend auf a, b und c...
        return fitness_wert

Eine Funktion mit 3 Parametern a,b∊ℝ und c∊ℤ mit jeweils verschiedenen
Intervallen und Schrittgrößen.


## Optimierung

    >>> optimize(f, timeout=60) # Abbruch spätestens nach 60 Sekunden
    (α=0.5, β=0.7, c=55)


## Optimierer

- Brute-Force (benötigt `step` für jeden Parameter)
        optimize(f, optimizer=ExhaustiveSearchOptimizer())
- Selbstadaptiver genetischer Algorithmus
        optimize(f, optimizer=SAESOptimizer())


## Framework für Optimierer

    def optimize(self, f, ...):
        ...
        # Iterieren über alle möglichen Parameterbelegungen
        for args in args_creator.product():
            # Aufruf der Fitness-Funktion (parallel im Hintergrund)
            self.invoker.invoke(f, args)

        # Warten bis alle Aufrufe beendet sind
        self.invoker.wait()

    # Wird aufgerufen, wenn ein Aufruf beendet ist
    def on_result(self, result, args, *vargs):
        fitness = result
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)


## Invoker
- Zuständig für den Aufruf der Fitness-Funktionen
- Beliebige Aufruf-Strategien (Prozesse, Threads, verteilt)
- Teil des Frameworks zur Erstellung von Optimierern


## API der Invoker
- `invoke(f, args, ...)` – Aufruf der Fitness-Funktion mit bestimmter Parameterbelegung im Hintergrund.
<br><br>
- `wait()` – Warten, bis alle Aufrufe der Fitness-Funktion beendet sind
<br><br>
- `abort()` – Alle derzeitigen und zukünftigen Aufrufe sofort beenden
<br><br>
- Resultat eines Aufrufs wird via Callback ``on_result(...)`` oder ``on_error()``
an den Optimierer übergeben.
<br><br>
- Optimierer können zudem individuelle Aufrufe abbrechen


## MultiprocessInvoker

-   Multiprocessing.Queue
-   Multiprocessing.Process


## PluggableInvoker

- Erweiterbarer Invoker, der intern andere Invoker nutzt
- Veränderung der Aufrufe der Fitness-Funktion durch Plugins
- Plugins durch Ereignise: ``on_invoke``, ``on_result``, ``on_error``


## Beispiel: TimeoutInvocationPlugin
Abbruch eins Aufrufs der Fitness-Funktion nach bestimmter Zeit

    class TimeoutInvocationPlugin(InvocationPlugin):
        def __init__(self, timeout):
            self.timeout = timeout

        def on_invoke(self, invocation):
            current_task = invocation.current_task
            Timer(self.timeout, current_task.cancel).start()


## Beispiel: PrintInvocationPlugin
Logging von Ereignissen auf der Konsole

    class PrintInvocationPlugin(InvocationPlugin):
        def on_invoke(self, invocation):
            print("Started", "f%s" % (invocation.fargs,))

        def on_result(self, invocation):
            result = invocation.current_result
            print("Finished", "f%s=%s" % (invocation.fargs, result))

        def on_error(self, invocation):
            print("Failed", "f%s" % (invocation.fargs,))

Mögliche Ausgabe:

    Started f(α=0.7, β=0.9, a=5)
    Finished f(α=0.7, β=0.9, a=5)=0.3
    Started f(α=0.2, β=0.5, a=99)
    Failed f(α=0.2, β=0.5, a=99)


## Ideen für weitere Plugins
- Visualisierung (z.B. Fitnesslandschaft)
- Mehrfacher Aufruf der Fitness-Funktion
- Speicherung von Zwischenergebnissen


# Aussicht


