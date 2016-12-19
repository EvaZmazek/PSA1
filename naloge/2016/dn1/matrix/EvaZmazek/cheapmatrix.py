# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """

    # za študiranje časovne in prostorske zahtevnosti
    # si označimo:
    #
    # n...število vrstic leve matrike
    # k...število stolpcev leve matrike, ki je enako številu vrstic desne matrike
    # m...število stolpcev desne matrike
    #
    # T(n,k,m) ... časovna zahtevnost
    # P(n,k,m) ... prostorska zahtevnos

    def multiply(self, left, right, work = None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
        """
        assert left.ncol() == right.nrow(), \
            "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
            "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow=self.nrow(), ncol=self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
                "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"

        stStolpcevLeveMatrike = left.ncol()  # izračunamo šrevilo stolpcev leve matrike, ki mora biti enako številu vrstic desne matike, da je množenje sploh definirano
        stVrsticLeveMatrike = left.nrow()  # izračunamo število vrstic leve matrike, ki je enako številu vrstic v novi matiki, ki je produkt leve in desne matrike
        stStolpcevDesneMatrike = right.ncol()  # izračunamo število stolpcev desne matrike, ki je enako število stolpcev v novi matriki, ki je produktleve in desne matrike

        # na začetku si shranimo 3 vrednosti: P(n,k,m) = O(3) = O(1)
        # na začetku naredimo tri štetja: T(n,k,m) = O(3) = O(1)

        # tako kot v SlowMatrix, tudi v primerih, ko je ena od dimenzij stStolpcevLeveMatike, stVrsticLeveMatrike in stStolpcevDesne matrike enaka 1, izracunamo matriko na roke
        if stStolpcevLeveMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                for j in range(stStolpcevDesneMatrike):
                    self[i, j] = (left[i, 0] * right[0, j])
            return self
        if stVrsticLeveMatrike == 1:
            for j in range(stStolpcevDesneMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[0, k] * right[k, j]
                self[0, j] = vrednost
            return self
        if stStolpcevDesneMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[i, k] * right[k, 0]
                self[i, 0] = vrednost
            return self

        # v teh treh primerih sta tako časovna, kot tudi prostorska zahtevnost enaki, kot v metodi SlowMatrix

        # lotimo se sedaj matrik vecjih dimenzij

        # za časovno in prostorsko zahtevnost pogledamo najslabši možen primer, ki je pri nas ta, da so vse dimenzije matrik lihe

        # najprej poglejmo mnozenje matrik, katerih dimenzije so sode:

        if stStolpcevLeveMatrike % 2 == 0 and stVrsticLeveMatrike % 2 == 0 and stStolpcevDesneMatrike % 2 == 0:

            work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] = \
                left[0:stVrsticLeveMatrike // 2, 0:stStolpcevLeveMatrike // 2] * \
                (right[0:stStolpcevLeveMatrike // 2, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike] - \
                 right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike])
            #v zgornjo levo cetrtino delovne matrike vpisemo P1 = \
            #A = ... * \
            #(F = ... - \
            # H = ...)

            work[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike] = \
                (left[0:stVrsticLeveMatrike // 2, 0:stStolpcevLeveMatrike // 2] + \
                 left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]) * \
                (right[0:stStolpcevLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] + \
                 right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike])
            #v zgorno desno cetrtino delovne matrike vpisemo P5 = \
            #(A = ... + \
            #D = ... ) * \
            #(E = ... + \
            #H = ... )

            work[stVrsticLeveMatrike // 2 : stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] = \
                (left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, 0:stStolpcevLeveMatrike // 2] + \
                 left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]) * \
                right[0:stStolpcevLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2]
            #v spodnjo levo cetrtino delovne matrike vpisemo P3 = \
            #(C = ... + \
            #D = ... ) * \
            #E = ...

            work[stVrsticLeveMatrike // 2 : stVrsticLeveMatrike, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike] = \
                (left[0:stVrsticLeveMatrike // 2, 0:stStolpcevLeveMatrike // 2] - \
                 left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, 0:stStolpcevLeveMatrike // 2]) * \
                (right[0:stStolpcevLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] + \
                 right[0:stStolpcevLeveMatrike // 2, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike])
            #v spodnjo desno cetrtino delovne matrike vpisemo P7 = \
            #(A = ... - \
            #C = ... ) * \
            #(E = ... + \
            #F = ... )

            self[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike] = \
                work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] + \
                work[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike] - \
                work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] - \
                work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike,stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]
            #spodnjo desno cetrtino koncne matrike nastavimo na
            #P1 = ... + \
            #P5 = ... - \
            #P3 = ... - \
            #P7 = ...

            #na tem koraku ne potrebujemo več P7, torej na njegovo mesto napišemo P2 (shranjene bomo imeli P1, P5, P3 in P2)

            work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike] = \
                (left[0:stVrsticLeveMatrike // 2, 0:stStolpcevLeveMatrike // 2] + \
                 left[0:stVrsticLeveMatrike // 2, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]) * \
                right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike]
            #v spodnjo desno cetrtino delovne matrike si torej zapisemo P2 = \
            #(A = ... + \
            #B = ... ) * \
            #H = ...

            self[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike] = \
                work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] + \
                work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]
            #zgornjo desno cetrtino matrike nastavimo na
            #P1 = ... + \
            #P2 = ...

            #na tem koraku ne potrebujemo več P1, zato ga nadomestimo s P4 (shranjene bomo imeli P4, P5, P3 in P2)

            work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] = \
                left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike] * \
                (right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, 0:stStolpcevDesneMatrike // 2] - \
                 right[0:stStolpcevLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2])
            #zgornjo levo cetrtino delovne matrike nastavimo na P4 = \
            #D = ... * \
            #(G = ... - \
            #E = ... )

            self[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] = \
                work[stVrsticLeveMatrike // 2 : stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] + \
                work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2]
            #spodnjo levo cetrtino koncne matrike nastavimo na
            #P3 = ... + \
            #P4 = ...

            #na tem koraku ne potrebujemo več P3, zato ga nadomestimo s P6 (shranjene bomo imeli P4, P5, P6 in P2)

            work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] = \
                (left[0:stVrsticLeveMatrike // 2, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike] - \
                 left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]) * \
                (right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, 0:stStolpcevDesneMatrike // 2] + \
                 right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike])
            #spodnjo levo cetrtino delovne matrike nastavimo na P6 = \
            #(B = ... - \
            #D = ... ) * \
            #(G = ... + \
            #H = ... )

            self[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] = \
                work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2] + \
                work[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike] + \
                work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2] - \
                work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]
            #zgornjo desno cetrtino koncne matrike nastavimo na
            #P4 = ... + \
            #P5 = ... + \
            #P6 = ... - \
            #P2 = ...
            return self

        if stVrsticLeveMatrike % 2 == 1:
            self[0:stVrsticLeveMatrike - 1, :] = left[0:stVrsticLeveMatrike - 1, :] * right
            self[stVrsticLeveMatrike - 1:stVrsticLeveMatrike, :] = left[stVrsticLeveMatrike - 1:stVrsticLeveMatrike,:] * right
            return self

        # v tem koraku porabimo O(k*m) dodatnega časa
        # v tem koraku porabimo O(1) dodatnega prostora

        if stStolpcevDesneMatrike % 2 == 1:
            self[:, 0:stStolpcevDesneMatrike - 1] = left * right[:, 0:stStolpcevDesneMatrike - 1]
            self[:, stStolpcevDesneMatrike - 1] = left * right[:, stStolpcevDesneMatrike - 1]
            return self

        # v tem koraku porabimo O(n*k) dodatnega časa
        # v tem koraku porabimo O(1) dodatnega prostora

        else:
            self[:, :] = left[:, 0:stStolpcevLeveMatrike - 1] * right[0:stStolpcevLeveMatrike - 1, :] + left[:,stStolpcevLeveMatrike - 1] * right[stStolpcevLeveMatrike - 1,:]
            return self

            # v tem koraku porabimo O(m*n) dodatnega časa
            # v tem koraku ne porabimo nobenega dodatnega prostora

            # Sklep:
            # Časovna zahtevnost: T(n,k,m) = O(1) + 7*T(n/2, k/2, m/2) + O(max(m,n)*k) + O(n*k) + O(k*m) + O(m*n)
            # Prostorska zahtevnost: P(n,k,m) = O(1) * O(k*(m+n)) + O(n*m) + 7*P(n/2,k/2,m/2) + O(1)