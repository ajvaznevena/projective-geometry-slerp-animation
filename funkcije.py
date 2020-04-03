import math
import numpy as np

import sys

def normalizuj(p):
    norm = np.linalg.norm(p)
    if norm != 0:
        return p / norm


def Euler2A(phi, theta, psi):
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(phi), -np.sin(phi)],
        [0, np.sin(phi), np.cos(phi)]
    ])

    Ry = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

    Rz = np.array([
        [np.cos(psi), -np.sin(psi), 0],
        [np.sin(psi), np.cos(psi), 0],
        [0, 0, 1]
    ])

    return Rz @ Ry @ Rx

def AxisAngle(A):

    # implementiran algoritam A2AngleAxis sa 12. slajda

    # Ulaz: Ortogonalna matrica A = (aij) != E, detA = 1.
    # Izlaz: Jedinicni vektor p i ugao φ ∈ [0, π] takav da A = Rp(φ).

    # odrediti jedinicni sopstveni vektor p za λ = 1;

    E = np.eye(3)
    if (A == E).all():
        sys.stderr("Matrica A je jedinicna")
        sys.exit(0)

    if round(np.linalg.det(A)) != 1:
        sys.stderr("Determinanta je razlicita od 1")
        sys.exit(0)

    # odrediti jedini£ni sopstveni vektor p za λ = 1
    # A*p = λ*p => 0 = (A - E)p

    A_p = A - E

    v1 = A_p[0]
    v2 = A_p[1]
    v3 = A_p[2]

    # v1 x v2
    # v1 x v3
    # v2 x v3

    u = []

    # odrediti proizvoljan jedinicni vektor u ⊥ p;

    p = np.cross(v1,v2)
    if not all(np.isclose(p, [0, 0, 0])):
        u = np.array(v1)
    elif not all(np.isclose(np.cross(v2, v3), [0, 0, 0])):
        p = np.cross(v2, v3)
        u = np.array(v2)
    elif not all(np.isclose(np.cross(v1, v3), [0, 0, 0])):
        p = np.cross(v1, v3)
        u = np.array(v3)

    # postavimo da p i u budu jedinicni
    p = normalizuj(p)
    u = normalizuj(u)

    u_prim = A.dot(u)

    phi = math.acos(u.dot(u_prim))

    # mesoviti proizvod
    if (np.cross(u, u_prim)).dot(p) < 0:
        p = -p      #da bi rotacija bila u pozitivnom smeru

    return p, phi


def Rodrigez(p, phi):

    # Formula Rodrigeza implementirana sa 7. slajda

    # px je matrica vektorskog mnozenja jedinicnim vektorom prave p=(p1, p2, p3):
    px = np.array([
        [0, -p[2], p[1]],
        [p[2], 0, -p[0]],
        [-p[1], p[0], 0]
    ])

    # formula je: Rp(φ) = ppT + cosφ * (E − ppT ) + sinφ * p×

    # Transponovanje vektora p
    pT = p[np.newaxis, :].T
    ppT = np.multiply(p, pT)
    E = np.identity(3)

    drugi_sabirak = np.multiply(np.cos(phi), np.subtract(E, ppT))
    treci_sabirak = np.multiply(np.sin(phi), px)


    R = ppT + drugi_sabirak + treci_sabirak

    return np.round(R, decimals=5)


def A2Euler(A):

    # implementiran algoritam A2Euler sa 22. slajda

    # Ulaz: Ortogonalna matrica A = (aij), detA = 1.
    # Izlaz: Ojlerovi uglovi ψ, θ, φ, A = Rz(ψ)Ry(θ)Rx(φ)

    phi = 0
    theta = 0
    psi = 0

    if (A[2][0] < 1):
        if (A[2][0] > -1):  # Jedinstveno resenje
            psi = np.arctan2(A[1][0], A[0][0])
            theta = np.arcsin(-A[2][0])
            phi = np.arctan2(A[2][1], A[2][2])
        else:  # Nije jedinstveno, slucaj Ox3 = -Oz
            psi = np.arctan2(-A[0][1], A[1][1])
            theta = np.pi / 2
            phi = 0
    else:  # Nije jedinstveno, slucaj Ox3 = Oz
        psi = np.arctan2(-A[0][1], A[1][1])
        theta = - np.pi / 2
        phi = 0

    return (phi, theta, psi)


def AxisAngle2Q(p, phi):

    # implementiran algoritam AngleAxis2Q sa 34. slajda

    # Ulaz: Rotacija Rp(φ) oko ose p = (px, py, pz) za ugao φ ∈[0, 2π);
    # Izlaz: Jedinicni kvaternion q ∈ H1 takav da Cq = Rp(φ).


    w = np.cos(phi / 2)
    p = normalizuj(p)

    #x, y, z = math.sin(phi / 2) * p

    (x1, y1, z1) = p
    x = np.sin(phi / 2) * x1
    y = np.sin(phi / 2) * y1
    z = np.sin(phi / 2) * z1

    return np.array([x, y, z, w])


def Q2AxisAngle(q):

    # implementiran algoritam Q2AngleAxis sa 35. slajda

    # Ulaz: (Jedinicni) kvaternion q = xi + yj + zk + w;
    # Izlaz: Jedinicni vektor p = (px, py, pz) i ugao φ ∈ [0, 2π) (φ ∈[0, π]) tako da Cq = Rp(φ).

    q = normalizuj(q)

    # if (w < 0)
    if (q[3] < 0):  # Samo ako zelimo φ ∈ [0, π]
        q = -q

    phi = 2 * np.arccos(q[3])

    if (np.fabs(q[3]) == 1):  # Identitet - p je bilo koji jedinicni
        p = np.array([1, 0, 0])
    else:
        p = normalizuj(np.array([q[0], q[1], q[2]]))

    return (p, phi)

def slerp(q1, q2, tm, t):

    # implementiran algoritam SLerp sa 43. slajda

    # Ulaz: Jedinicni kvaternioni q1 i q2, koji zadaju pocetnu i krajnju "orjentaciju",
    # duzina interpolacije tm, parametar t∈[0, tm].
    # Izlaz: Jedinicni kvaternion qs(t) koji zadaje "orjentaciju" u trenutku t.

    if t < 0 or t > tm:
        sys.stderr("parametar t ne pripada trazenom intervalu")
        sys.exit(0)

    q1 = normalizuj(q1)
    q2 = normalizuj(q2)

    cos0 = np.dot(q1, q2)
    if cos0 < 0:       # idi po kracem luku sfere
        q1 = -q1
        cos0 = -cos0

    if cos0 > 0.95:     # kvaternioni q1 i q2 previse blizu
        return q1

    phi0 = np.arccos(cos0)
    qs = ((np.sin(phi0 * (1 - t/tm))) / np.sin(phi0))*q1 + ((np.sin(phi0 * (t/tm))) / np.sin(phi0))*q2

    return qs