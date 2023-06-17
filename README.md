PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

sox: Convertim els arxius d'audio a format raw.

x2x: Canviem el format de les dades de raw a float.

frame: Dividim l'arxiu en trames de 30ms cada 10ms.

window: Apliquem un enfinestrat a cada trama.

lpc: Calculem els primers coeficients de predicció lineal.


- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 51 del script `wav2lp.sh`).

Busquem el nombre de columnes i files que tendra el nostre fixer. Un cop preparat, ho pasem de ascii a unit32 i cream un fixer amb les columnes i files per a poder observar-ho d'una manera mes comode.

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

El format fmatrix es més convenient que el SPTK perqué és més fàcil de llegir i utilitzar.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:

```python
# Main command for feature extration
sox $inputfile -t raw -e signed -b 16 - |
   $X2X +sf | 
   $FRAME -l 240 -p 80 | 
   $WINDOW -l 240 -L 240 |
	$LPC -l 240 -m $lpc_order | 
   $LPCC -m $lpc_order -M $lpcc_order > $base.lpcc || exit 1
   

# Our array files need a header with the number of cols and rows:
ncol=$((lpcc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
nrow=`$X2X +fa < $base.lpcc | wc -l | perl -ne 'print $_/'$ncol', "\n";'`
```

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

```python
# Main command for feature extration
sox $inputfile -t raw -e signed -b 16 - | 
   $X2X +sf | 
   $FRAME -l 240 -p 80 | 
   $WINDOW -l 240 -L 240 |
	$MFCC -l 240 -s 8 -w 0 -m $mfcc_order -n $mel_filter_bank_order > $base.mfcc || exit 1
   

# Our array files need a header with the number of cols and rows:
ncol=$((mfcc_order)) # mfcc p =>  (c0 ... cp-1) 
nrow=`$X2X +fa < $base.mfcc | wc -l | perl -ne 'print $_/'$ncol', "\n";'`
```

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.

```python
import matplotlib.pyplot as plt


# coeficientes LP
X, Y = [], []
for line in open('lp_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(1)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LP',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('lp_2_3.png')
#plt.show()

# coeficientes LPCC
X, Y = [], []
for line in open('lpcc_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(2)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LPCC',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('lpcc_2_3.png')
#plt.show()

# coeficientes MFCC
X, Y = [], []
for line in open('mfcc_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(3)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('MFCC',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('mfcc_2_3.png')
#plt.show()
```
  
LP:

![](https://github.com/LlorencSastre/P4/blob/Matamala-Sastre/lp_2_3.png)

LPCC:

![](https://github.com/LlorencSastre/P4/blob/Matamala-Sastre/lpcc_2_3.png)

MFCC:

![](https://github.com/LlorencSastre/P4/blob/Matamala-Sastre/mfcc_2_3.png)


  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

La parametrització que conté més informació es la LPCC, te els coeficients millor distribuits i no son tant susceptibles a depencencies y correlacions entre si. El cas contrari es el de LP que la distribució s'assembla molt a una funció lineal. 

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |  -0.818326    |  0.198087    |   -0.11145   |

```python
export FEAT=lp; pearson work/$FEAT/BLOCK00/SES000/* | grep "rho\[2\]\[3\]"

export FEAT=lpcc; pearson work/$FEAT/BLOCK00/SES000/* | grep "rho\[2\]\[3\]"

export FEAT=mfcc; pearson work/$FEAT/BLOCK00/SES000/* | grep "rho\[2\]\[3\]"
```

  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.

Em valor absolut el LP es molt major que els altres dos, aixo ens indica que estan molt més correlats, cosa que te sentit si mirem les gràfiques anteriors.

- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

LPCC: Seguint la teoria, el paràmetre adequat és l'ordre del coeficients de la predicció lineal del LPCC.

MFCC: El paràmetre per el calcul de coeficients MFCC es l'ordre dels coeficients cepstrals en escala Mel.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

![](https://github.com/LlorencSastre/P4/blob/Matamala-Sastre/funcio_densitat_mfcc_bo.png)

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

![](https://github.com/LlorencSastre/P4/blob/Matamala-Sastre/punts_mfcc.png)

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

 |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | Tasa de error |  40.76%    |  3.18%    |   7.13%   |

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.

LP:
```
run_spkid lp train test classerr trainworld verify verifyerr

==============================================
THR: 0.678547558659198
Missed:     151/250=0.6040
FalseAlarm: 23/1000=0.0230
----------------------------------------------
==> CostDetection: 81.1
==============================================
Sat Jun 17 18:13:54 CEST 2023
```

LPCC:
```
run_spkid lpcc train test classerr trainworld verify verifyerr

==============================================
THR: 0.909916475240501
Missed:     52/250=0.2080
FalseAlarm: 9/1000=0.0090
----------------------------------------------
==> CostDetection: 28.9
==============================================
Sat Jun 17 18:18:18 CEST 2023
```

MFCC:
```
run_spkid mfcc train test classerr trainworld verify verifyerr

==============================================
THR: 1.6947896311739
Missed:     125/250=0.5000
FalseAlarm: 6/1000=0.0060
----------------------------------------------
==> CostDetection: 55.4
==============================================
Sat Jun 17 18:23:30 CEST 2023
```
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

Els fixers `class_test.log` i `verif_test.log` estan dintre de la carpeta <code>work</code>

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
