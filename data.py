from prom import codigosEquipos

primera = codigosEquipos("https://www.promiedos.com.ar/primera=equipos",)
b_nacional = codigosEquipos('https://www.promiedos.com.ar/bnacional=equipos')
premier = codigosEquipos("https://www.promiedos.com.ar/inglaterra=equipos")

total_equipos = primera | b_nacional | premier