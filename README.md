# sdm_bio_vinaceous-breasted-amazon

**Biodiversity data**
Taxon names: e.g., names of subspecies, species, genus, families

Details on taxonomic reference system
Ecological level: choose from list or insert new values
Details on species data source: e.g., URL/DOI, accession date, database version
Sampling design: spatial design: e.g. random, uniform, stratified), temporal design, nestedness
Sample size per taxon (incl. prevalence): e.g., number of observations/counts, prevalence
Country/region mask, if applicable
Details on scaling, if applicable: e.g., rasterisation of polygon maps, spatial and temporal thinning, measures to address spatial uncertainties
Details on data cleaning/filtering steps, if applicable: e.g., taxonomically, outlier presence/treatment
Details on absence data collection, if applicable
Details on background data derivation, if applicable: e.g., spatial and temporal extent, spatial and temporal buffer, bias correction (e.g. target group sampling)
Details on potential errors and biases in data, if applicable: e.g., detection probability, misidentification potential, geo-referencing errors, sampling bias

Data partitioning
Selection of training data (for model fitting)
Selection of validation data (withheld from model fitting, used for estimating prediction error for model selection, model averaging or ensemble): e.g., cross-validation method
Selection of test (truly independent) data , sensu Hastie, et al. (2009)

Predictor variables
State predictor variables used
Details on data sources: e.g., URL/DOI, accession date, database version

Spatial extent

 
xmin
 
xmax
 
ymin
 
ymax

Spatial resolution of raw data
Coordinate reference system (CRS), e.g. proj4 string, EPSG code, ESRI PE string
Temporal extent of raw data
Temporal resolution of raw data, if applicable
Details on data processing and on spatial, temporal and thematic scaling: e.g. upscaling/downscaling, transformations, normalisations, thematic aggregations (e.g. of land cover classes), measures to address spatial uncertainties
Details on measurements errors and bias, when known
Details on dimension reduction of variable set, if applicable - if model-based, this should be contained in Model section (element: Details on pre-selection of variables)

**Transfer data**
Details on data sources: e.g., URL/DOI, accession date, database version
Spatial extent

 
xmin
 
xmax
 
ymin
 
ymax
Spatial resolution of transfer data
Temporal extent of transfer data
Temporal resolution of transfer data, if applicable
Models and scenarios used
Details on data processing and scaling (see section Predictor variables)
Quantification of novel environmental conditions and novel environmental combinations: e.g., distance to training data