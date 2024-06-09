
---
## **Autoria**

**Título do estudo**

- Título #TODO

**Email**

- email.com

**Link**
  
- Link

--- 
## **Objetivo do modelo**

- Forecast and transfer

- Main Target Output: Suitable #TODO: (Avaliar artigo que descreve a aplicação de modelo de background)

---
## **Focal Taxon**
---
## **Location**
---
Área de estudo: Região da Serra da mantiqueira
---
## **Escala da análise**
---
- **Extensão das observações**

Espaço | minx | miny | maxx | maxy |
|---|----------|----------|----------|----------|
| Observações | -53.516667   | -31.386923   | -40.06817  |-12.562269  |
|Serra da mantiqueira| -47.012839   | -23.489618   | -40.169585  |-18.359071  |

**Spacial resolution**

- 1km
  
**Temporal extend**

- Atualmente está com dados desde 1929, porém, é possível filtrar de 2020 para frente caso necessário (Perderíamos cerca de 50% dos dados)

**Type of extent boundary**

- Political
  
---
## **Biodiversity Data**
---
**Observation type**

- citizen science

**Response type**

- Point occurence

## **Predictors**

- Climatic
- Topographic

## **Hypotheses**

- #TODO
- 
## **Assumptions**
1- The species is in equilibrium with the environment, i.e. all suitable
habitats are occupied by the species. This rarely happens, as the
capacity of the species to occupy habitats is limited mainly by its
dispersal characteristics and biogeographic history (i.e. suitable
habitats may occur beyond a geographical barrier which is impos-
sible to cross for the species). Therefore, what should be guaranteed is that the species is in pseudo-equilibrium, i.e. the species occupies
all suitable habitats where it can disperse.

2- The biases in the modelling system are minimal (Fithian et al., 2015).
The sampling design should not be focused on particular regions of
the study area, habitat types, or activity periods.

3- All variables included in the model are related to species occurrence.

4- The species niche is conserved across space and time.

## **AlgorithmS**

- Maxent
- Random Forest
---
## **Workflow**
---
-> Descrição do workflow

## **Software**
---
modeling plataform:

codes:

data sources:

## **Obs**
---
For this, three main criteria can be
followed: 1) use biogeographical regions (Comrie and Glenn, 1999;
Sillero, 2010); 2) avoid areas where the species cannot disperse
(Anderson and Raza, 2010); and 3) avoid areas where the frequency
distribution curves of the values of critical environmental variables are
truncated (Guisan and Thuiller, 2005). Modelling inside a

biogeographical region might be the simplest way, as they work as
relatively contained systems

---

Another alternative is to reduce the study area to a buffer around the
species records (Phillips et al., 2009; B ́

aez et al., 2020). The size of the
buffer is somewhat subjective, and the best distance should be selected
from different trials or using information about the species’ dispersal
capacity, including long-distance dispersal events

The spatial location of absences will determine the results of the
model (Lobo et al., 2010). There are three types of absences (Fig. 1)

The best number of pseudo-absences depends on
the modelling technique (Barbet-Massin et al., 2012; Kanagaraj et al.,
2013): recommendations include using a large number (e.g. 10,000) of
pseudo-absences with regression techniques (e.g. generalised linear
models and generalised additive models); averaging several runs (e.g.
10) with fewer pseudo-absences (e.g. 100) for multiple adaptive
regression splines and discriminant analysis; and using the same number
of pseudo-absences as the number of available presences (averaging
several runs if this number is small) for classification techniques such as
boosted regression trees, classification trees and random forests. Despite
all studies analysing how to create pseudo-absences, true observations of
absences always provide better results

For generalised
linear models (GLM) and related methods, a recommended number of
records is 50 + 8k or 104 + k, being k the number of variables

the leave-one-out method, i.e. the test

dataset is composed of only one occurrence record set aside that changes
in each model replicate

---
Maximum number of variables
n is the # of species records,

regression-based methods,
k=(n-50)/8 or k = n-104, k being the number of
variables and n the number of species records (Field et al., 2012).

Other methods

k < n/100

---
Validating

The predictive performance of

ecological niche models can be validated by three components (Hosmer
and Lemeshow, 2000; Pearce and Ferrier, 2000; Leroy et al., 2018):
- Classification capacity: the ability of the model to correctly classify
occupied sites as suitable or probable or favourable, and unoccupied
sites as the opposite, based on a threshold value.

- Discrimination capacity: the ability of a model to generally sepa-
rate or distinguish between occupied and unoccupied sites, regard-
less of any threshold value.

- Calibration: the agreement between predicted probabilities of
occurrence and observed proportions of sites occupied. Calibration is
the most faithful assessment of the reliability of the models, but it is not easy to measure in all algorithms, and thus many authors have
focused on classification and discrimination metrics.