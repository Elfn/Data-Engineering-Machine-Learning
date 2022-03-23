# install.packages("readxl")
# install.packages("cartography")
# install.packages("sf")
# install.packages("tidyverse")

library("readxl")
library(ggplot2)

library(cartography)
library(sf)
library(tidyverse)



setwd("/Users/Elimane/SUPINFO 2022/Big Data/R - Data Science/5RBIG/data")
getwd()

FatalEncounters <- read.csv("FatalEncounters.csv")
PoliceDeaths <- read.csv("PoliceDeaths.csv")
WashingtonPostDatabase <- read.csv("WashingtonPostDatabase.csv")
TaxPolicyCenter <- read_excel("TaxPolicyCenter.xls")

colnames(FatalEncounters)[colnames(FatalEncounters) == 'Unique.ID'] <- 'id'



#Visualisation des donnees sous forme de tableau dans l'IDE
#View(FatalEncounters)
View(PoliceDeaths)
#View(WashingtonPostDatabase)
View(TaxPolicyCenter)

# Debut de tableau
head(FatalEncounters)
head(PoliceDeaths)
head(WashingtonPostDatabase)
head(TaxPolicyCenter)

# Fin de tableau
tail(FatalEncounters)
tail(PoliceDeaths)
tail(WashingtonPostDatabase)
tail(TaxPolicyCenter)

mapdata<-merge(WashingtonPostDatabase, FatalEncounters, by="id")
View(mapdata)
