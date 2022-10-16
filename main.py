import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="FutbolFixture")

class Equipo():
    PJ = 0
    PG = 0
    PE = 0
    PP = 0
    GF = 0
    GC = 0
    DG = GF - GC
    Pts = 0
    def __init__(self,nomb):
        self.nombre = nomb

    @staticmethod
    def enfrentar(eq1,eq2,g1,g2):
        eq1.GF += g1
        eq2.GC += g1
        eq2.GF += g2
        eq1.GC += g2
        eq1.PJ += 1
        eq2.PJ += 1

        if temp1 > temp2:
            eq1.Pts += 3
            eq1.PG += 1
            eq2.PP += 1
        elif temp1 < temp2:
            eq2.Pts += 3
            eq2.PG += 1
            eq1.PP += 1
        else:
            eq1.Pts += 1
            eq1.PE += 1
            eq2.Pts += 1
            eq2.PE += 1
        
        eq1.DG = eq1.GF - eq1.GC
        eq2.DG = eq2.GF - eq2.GC

st.title("Torneo de Fútbol")

P1,P2,P3 = st.tabs(["Equipos","Fechas","Resultados"])

with P1:
    c1,c2 = st.columns([1,2])
    with c1:
        n = st.number_input("Nro de Equipos:",2,20,3,1)
    with c2:
        equipos = []
        for i in range(n):
            lab = "Equipo #"+str(i+1)
            equipos.append(Equipo(st.text_input(lab)))

with P2:
    goles = np.zeros((n,n))
    partidos_jugados = []
    fechas = []
    vt = n-1 if n%2==0 else n
    for i in range(vt):
        fechas.append([])
    for i in range(1,n):
        for j in range(i):
            if n%2 == 0:
                vt_f = i+j if i+j<=n-1 else i+j-n+1
                if i == n-1 and j>0:
                    vt_f = j*2 if j < n/2 else 2*j-n+1
            else:
                vt_f = i+j if i+j<=n else i+j-n
            fechas[int(vt_f-1)].append((i,j))

    lab_temp = " "

    for i in range(vt):
        st.write("**Activar el checkbox cuando ya se haya jugado el partido**")
        st.subheader(f"\nFecha #{i+1}:")
        for x in fechas[i]:
            cc6,cc1,cc2,cc3,cc4,cc5,cc7 = st.columns([1,2,2,1,2,2,1])
            with cc1:
                " "
                " "
                st.write(f"{equipos[x[0]].nombre}")
            with cc2: temp1 = st.number_input(lab_temp,0,50,0,1)
            lab_temp += " "
            with cc3:
                " "
                " "
                st.write("VS")
            with cc4: temp2 = st.number_input(lab_temp,0,50,0,1)
            lab_temp += " "
            with cc5:
                " "
                " "
                st.write(f"{equipos[x[1]].nombre}")
            with cc7:
                " "
                " "
                if st.checkbox(lab_temp):
                    partidos_jugados.append([x[0],x[1]])
                    goles[x[0],x[1]] = temp1
                    goles[x[1],x[0]] = temp2
            lab_temp += " "
        st.write("---")
    #goles
    #partidos_jugados

with P3:
    for x in partidos_jugados:
        Equipo.enfrentar(equipos[x[0]],equipos[x[1]],goles[x[0],x[1]],goles[x[1],x[0]])
    lista_t = equipos[:]
    for i in range(n-1):
        for j in range(i+1,n):
            if lista_t[i].Pts < lista_t[j].Pts:
                tt = lista_t[i]
                lista_t[i] = lista_t[j]
                lista_t[j] = tt
            elif lista_t[i].Pts == lista_t[j].Pts:
                if lista_t[i].DG < lista_t[j].DG:
                    tt = lista_t[i]
                    lista_t[i] = lista_t[j]
                    lista_t[j] = tt
                elif lista_t[i].DG == lista_t[j].DG:
                    if lista_t[i].GF < lista_t[j].GF:
                        tt = lista_t[i]
                        lista_t[i] = lista_t[j]
                        lista_t[j] = tt
    Resultados = pd.DataFrame(columns=["Equipo","PJ","PG","PE","PP","GF","GC","DG","Pts"])
    for i in range(n):
        Resultados.loc[i]=[lista_t[i].nombre,lista_t[i].PJ,lista_t[i].PG,lista_t[i].PE,lista_t[i].PP,int(lista_t[i].GF),int(lista_t[i].GC),int(lista_t[i].DG),lista_t[i].Pts]
    Resultados

