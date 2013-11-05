<!--\n\n\n will create a horizontal slide, \n\n will create a vertical slide -->

# OrgES

Organic Computing for Evolution Strategies


## Anwendungsfälle

-   Einstellung von Parametern beliebiger Funktionen
-   Blackbox-Optimierung von Fitness-Funktionen
-   Erstellen von Optimierungsverfahren


## Setup

-   [cigroup-ol/orges](https://github.com/cigroup-ol/orges)
-   3-Clause-BSD
-   Python>=2.5
-   Drone.io
-   Mock
-   Nose
-   Tox



## Architekturüberlick

![](img/OrgES_Overview.png)


## Architekturüberlick

-   `Optimizer`
    nutzen `Invoker`
-   `PluggableInvoker`
    nutzt `Plugins` und andere `Invoker`
-   `PluggableInvoker`
    ist sowohl `Caller` als auch `Invoker`



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

Brute-Force (benötigt `step` für jeden Parameter)

    optimize(f, optimizer=GridSearchOptimizer())

Selbstadaptiver genetischer Algorithmus

    optimize(f, optimizer=SAESOptimizer())


## Framework für Optimierer (1/2)

    def optimize(self, f, ...):
        ...
        # Iterieren über alle möglichen Parameterbelegungen
        for args in args_creator.product():
            # Aufruf der Fitness-Funktion (parallel im Hintergrund)
            self.invoker.invoke(f, args)

        # Warten bis alle Aufrufe beendet sind
        self.invoker.wait()
        return self.best


## Framework für Optimierer (2/2)

    # Wird aufgerufen, wenn ein Aufruf beendet ist
    def on_result(self, result, args, *vargs):
        fitness = result
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)


## Invoker

-   Zuständig für den Aufruf der Fitness-Funktionen
-   Beliebige Aufruf-Strategien (Prozesse, Threads, verteilt)
-   Teil des Frameworks zur Erstellung von Optimierern


## API der Invoker

-  `invoke(f, args, ...)`
    Aufruf von Fitness-Funktion mit Parameterbelegung.
-   `wait()`
    Warten, bis alle Fitness-Funktionen beendet sind.
-   `abort()`
    Alle möglichen Aufrufe sofort beenden.
-   Resultat eines Aufrufs wird via Callback ``on_result(...)`` oder ``on_error()`` an den Optimierer übergeben.
-   Optimierer können zudem individuelle Aufrufe abbrechen


## Vorhandene Invoker

-   PluggableInvoker
    mit Andockstellen für Plugins
-   MultiProcessInvoker
    mit Ausführung in Python-Prozessen


## Ideen für weitere Invoker

-   **MutliThread**Invoker
    mit Ausführung in Threads
    für EA-beschränkte Algorithmen
-   **Distributed**Invoker
    mit Ausführung auf mehrere Maschinen
    für mehr Parallelisierung



## PluggableInvoker

-   Erweiterbarer Invoker, der intern andere Invoker nutzt
-   Veränderung der Aufrufe der Fitness-Funktion durch Plugins
-   Plugins durch Ereignise: ``on_invoke``, ``on_result``, ``on_error``


## TimeoutInvocationPlugin

Abbruch eines Aufrufs der Fitness-Funktion nach bestimmter Zeit

    class TimeoutInvocationPlugin(InvocationPlugin):
        def __init__(self, timeout):
            self.timeout = timeout

        def on_invoke(self, invocation):
            current_task = invocation.current_task
            Timer(self.timeout, current_task.cancel).start()


## PrintInvocationPlugin

Logging von Ereignissen auf der Konsole

    class PrintInvocationPlugin(InvocationPlugin):
        def on_invoke(self, invocation):
            print("Started", "f%s" % (invocation.fargs,))

        def on_result(self, invocation):
            result = invocation.current_result
            print("Finished", "f%s=%s" % (invocation.fargs, result))

        def on_error(self, invocation):
            print("Failed", "f%s" % (invocation.fargs,))


## PrintInvocationPlugin

Mögliche Ausgabe:

    Started f(α=0.7, β=0.9, a=5)
    Finished f(α=0.7, β=0.9, a=5)=0.3
    Started f(α=0.2, β=0.5, a=99)
    Failed f(α=0.2, β=0.5, a=99)


## Ideen für weitere Plugins

-   Visualisierung (z.B. Fitnesslandschaft)
-   Mehrfacher Aufruf der Fitness-Funktion
-   Speicherung von Zwischenergebnissen



## MultiProcessInvoker

Aufgabe

-   (selbstständige) Parallelisierung von
-   (beliebigen) Funktionsaufrufen mit
-   (beliebigen) Argumenten

&nbsp;

Ansatz

`>>> import multiprocess`


# Probleme & Lösungen


## IPC (1/3)

-   Inter-Prozess-Kommunikation (IPC) nötig
    &rArr; WorkerProcess und der Invoker teilen sich Queues:
    -   tasks: eingehende Aufträge
    -   status: Auftragsbesätigungen
    -   results: (Zwischen-)Ergebnisse


&nbsp;

    class MultiProcessInvoker(BaseInvoker):
        """Invoker that manages worker processes."""
        def __init__(self, resources=None):
            ...
            # queues common to all worker processes
            self._queue_results = Queue()
            self._queue_status = Queue()
            self._queue_tasks = Queue()

&nbsp;

    class WorkerProcess(Process):
        """Calls functions with arguments, both given by a queue."""
        def __init__(self, queue_results, queue_status, queue_tasks):
            self._queue_results = queue_results
            self._queue_status = queue_status
            self._queue_tasks = queue_tasks


## IPC (2/3)

-   Funktionen nicht `pickle`bar
    &rArr; `import`s übergeben

&nbsp;

    for task in self.queue_tasks.get:
        ...
        f = __import__(task.f_package, globals(), locals(), ['f'], -1).f
        value = call(f, task.args)


## IPC (3/3)

-   Worker-Management würde Polling erfordern
    &rArr; Synchronisation über `Queue`s

&nbsp;

    self._queue_tasks.put(Task(...))
    # some worker will get the task and report back before executing
    status = self._queue_status.get()


## Prozesse

-   Worker-Prozesse erzeugen ist recht teuer
    WorkerPool hält WorkerProzesse bereit
-   Worker und Tasks müssen identifiziert werden
    bei Erzeugung `uuid`s vergeben

&nbsp;

    def _provision_worker(self):
        if len(self._worker_processes) is not self.worker_count_max:
            id = uuid.uuid4()
            self._worker_processes.append(self._get_worker_process(id))



# Demo



# v0.0.1

-   mehr Tests
    aktuell: 69 % coverage
-   mehr Beispiele
    aktuell: 8
-   mehr Invoker
    aktuell: 3
-   mehr Plugins
    aktuell: 2



# The End

