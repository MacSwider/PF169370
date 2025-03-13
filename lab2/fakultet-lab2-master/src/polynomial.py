class Polynomial:
    """
    Klasa reprezentująca wielomian.
    Współczynniki są przechowywane w liście coeff, gdzie:
    - pierwszy element to współczynnik przy najwyższej potędze
    - ostatni element to wyraz wolny

    Przykład: 3x^2 + 2x + 1 będzie reprezentowane jako [3, 2, 1]
    """

    def __init__(self, coefficients):
        """
        Inicjalizacja wielomianu z listy współczynników.

        Args:
            coefficients: Lista współczynników, pierwszy element to współczynnik przy najwyższej potędze
        """
        # Kopiujemy listę, aby uniknąć przypadkowych modyfikacji zewnętrznych
        self.coeff = list(coefficients)

        # Usuwamy zbędne zera z lewej strony
        self._remove_leading_zeros()

        # Jeśli lista jest pusta, to ustawiamy wielomian zerowy [0]
        if not self.coeff:
            self.coeff = [0]

    def _remove_leading_zeros(self):
        """Usuwa zbędne zera z lewej strony (przy najwyższych potęgach)."""
        pass

    def degree(self):
        """Zwraca stopień wielomianu."""
        pass

    def evaluate(self, x):
        """
        Oblicza wartość wielomianu dla danego x za pomocą schematu Hornera.

        Args:
            x: Wartość, dla której obliczamy wielomian

        Returns:
            Wartość wielomianu w punkcie x
        """
        pass

    def __str__(self):
        """Zwraca czytelną reprezentację wielomianu jako string."""
        pass

    def __repr__(self):
        """Zwraca reprezentację wielomianu do debugowania."""
        pass

    def __eq__(self, other):
        """
        Porównuje dwa wielomiany.

        Args:
            other: Inny wielomian lub liczba do porównania

        Returns:
            True jeśli wielomiany są równe, False w przeciwnym przypadku
        """
        pass

    def __add__(self, other):
        """
        Dodaje dwa wielomiany lub wielomian i liczbę.

        Args:
            other: Inny wielomian lub liczba do dodania

        Returns:
            Nowy wielomian będący sumą
        """
        pass

    def __radd__(self, other):
        """
        Obsługuje dodawanie z liczbą po lewej stronie.

        Args:
            other: Liczba do dodania po lewej stronie

        Returns:
            Nowy wielomian będący sumą
        """
        pass

    def __sub__(self, other):
        """
        Odejmuje wielomian lub liczbę od tego wielomianu.

        Args:
            other: Wielomian lub liczba do odjęcia

        Returns:
            Nowy wielomian będący różnicą
        """
        pass

    def __rsub__(self, other):
        """
        Obsługuje odejmowanie wielomianu od liczby (liczba po lewej stronie).

        Args:
            other: Liczba, od której odejmujemy wielomian

        Returns:
            Nowy wielomian będący różnicą
        """
        pass

    def __mul__(self, other):
        """
        Mnoży wielomian przez inny wielomian lub liczbę.

        Args:
            other: Wielomian lub liczba do pomnożenia

        Returns:
            Nowy wielomian będący iloczynem
        """
        pass

    def __rmul__(self, other):
        """
        Obsługuje mnożenie liczby przez wielomian (liczba po lewej stronie).

        Args:
            other: Liczba do pomnożenia po lewej stronie

        Returns:
            Nowy wielomian będący iloczynem
        """
        pass