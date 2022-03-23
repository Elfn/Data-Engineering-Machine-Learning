install.packages("readxl")
install.packages("plotrix")
install.packages("lessR")
install.packages("dplyr")
install.packages("tidyverse") 
install.packages("gridExtra") 
install.packages("cartography") 
install.packages("maps")
install.packages("sf")
install.packages("ggplot2")



library("readxl")
library(plotrix)
library(lessR)
library(ggplot2)
library(dplyr)
library(data.table)
library(tidyverse)
library(gridExtra)
library(grid)
library(cartography)
library(maps)
library(sf)
library(mapproj)


 require(maps)
 require(viridis)

 # install.packages("ggplot2")
 #library(ggplot2)
 

#--------------------------Recuperation des donneés-------------------
setwd("/Users/Elimane/SUPINFO 2022/Big Data/R - Data Science/5RBIG/data")
getwd()

FatalEncounters <- read.csv("FatalEncounters.csv")
PoliceDeaths <- read.csv("PoliceDeaths.csv")
WashingtonPostDatabase <- read.csv("WashingtonPostDatabase.csv")
TaxPolicyCenter <- read_excel("TaxPolicyCenter.xls")

#Visualisation des donnees sous forme de tableau dans l'IDE
 # View(FatalEncounters)
 # View(PoliceDeaths)
 # View(WashingtonPostDatabase)
 # View(TaxPolicyCenter)

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

#--------------------------Traitement-------------------

# Suppression des lignes vides (Sur toute l'horizontale)
PoliceDeaths_cleaned <- PoliceDeaths[rowSums(is.na(PoliceDeaths)) != ncol(PoliceDeaths), ]
PoliceDeaths_cleaned$
FatalEncounters_cleaned <- FatalEncounters[rowSums(is.na(FatalEncounters)) != ncol(FatalEncounters), ]
WashingtonPostDatabase_cleaned <- WashingtonPostDatabase[rowSums(is.na(WashingtonPostDatabase)) != ncol(WashingtonPostDatabase), ]
TaxPolicyCenter_cleaned <-  TaxPolicyCenter[rowSums(is.na(TaxPolicyCenter)) != ncol(TaxPolicyCenter), ]
head(PoliceDeaths_cleaned)
head(FatalEncounters_cleaned)
head(WashingtonPostDatabase_cleaned)
head(TaxPolicyCenter_cleaned)

# Données de geolocalisation (Incomplet à ajouter pour les perspectives d'amélioration)
# WashingtonPostDatabase_geol_df <- data.frame(City=WashingtonPostDatabase_cleaned$city,State=WashingtonPostDatabase_cleaned$state,Latitude=WashingtonPostDatabase_cleaned$latitude, Longitude=WashingtonPostDatabase_cleaned$longitude)
# head(WashingtonPostDatabase_geol_df)
# 
# FatalEncounters_geo_df <- data.frame(CountryLocation=FatalEncounters_cleaned$Location.of.death..county.,CityLocation=FatalEncounters_cleaned$Location.of.death..city.,Latitude=FatalEncounters_cleaned$Latitude, Longitude=FatalEncounters_cleaned$Longitude)
# head(FatalEncounters_geo_df)



# Tendances
  # 1 Nombres de Meutres de policiers par années (Entre 2011 - 2016) J'ai choisi cet interval reduit en raison du volume consequent de donneeés
  head(PoliceDeaths_cleaned)
  data_df <- data.frame(Person=PoliceDeaths_cleaned$person,Year=PoliceDeaths_cleaned$year)
  head(data_df$)
  data_df <-  data_df%>% group_by(Year)%>% summarise(freq=n())
  data_df <- data.frame(Years=data_df$Year,DeathsNumber=data_df$freq)
  data_df <- data_df[data_df$Years >= 2011,]
  head(data_df)
  nrow(data_df)
  
  ggplot(data_df, aes(x = Years, y = DeathsNumber)) +
    geom_segment(aes(x = data_df$Years, xend = data_df$Years, y = 0, yend = data_df$DeathsNumber)) +
    geom_point() 
  
  # ggplot(data_df, aes(x = Years, y = DeathsNumber)) +
  #   geom_segment(aes(x = data_df$Years, xend = data_df$Years, y = 0, yend = data_df$DeathsNumber)) +
  #   geom_point(size = 4, pch = 21, bg = 4, col = 1) +
  #   coord_flip()

  # 2 Causes de mort les plus récurrentes des policiers 
  str(PoliceDeaths_cleaned)
  most_recurrent_police_death_cause_df <- data.frame(Tools=PoliceDeaths_cleaned$cause_short)
  head(most_recurrent_police_death_cause_df)
  policeDeath_tbl <- table(most_recurrent_police_death_cause_df)
  policeDeath_tbl
  policeDeathCause_df <- data.frame(policeDeath_tbl)
  policeDeathCause_df
  colnames(policeDeathCause_df)  <- c("Causes","Frequences")
  head(policeDeathCause_df)
  most_reccurents <- policeDeathCause_df[order(policeDeathCause_df$Frequences, decreasing = TRUE), ]
  most_reccurents
  
  MostRecurrentsPoliceDeathCause_df <- head(most_reccurents, n=3)
  MostRecurrentsPoliceDeathCause_df
  

   hsize <- 4
   df <- MostRecurrentsPoliceDeathCause_df %>% mutate(x = hsize)
   df
  ggplot(df, aes(x = hsize, y =Frequences, fill = Causes)) +geom_col() +
    geom_text(aes(label = paste0(round(Frequences/sum(Frequences) * 100, 2), "% (",Causes,")")), position = position_stack(vjust = 0.5)) +
    coord_polar(theta = "y") +xlim(c(0.2, hsize + 0.5))
  

  
  # 3 Types de mort les plus récurrentes des populations 
  most_recurrent_people_death_manner_df <- data.frame(Tools=WashingtonPostDatabase_cleaned$manner_of_death)
  head(most_recurrent_people_death_manner_df)
  peopleDeath_tbl <- table(most_recurrent_people_death_manner_df)
  peopleDeath_tbl
  peopleDeathCause_df <- data.frame(peopleDeath_tbl)
  peopleDeathCause_df
  colnames(peopleDeathCause_df)  <- c("Causes","Frequences")
  head(peopleDeathCause_df)
  most_reccurents <- peopleDeathCause_df[order(peopleDeathCause_df$Frequences, decreasing = TRUE), ]
  MostRecurrentsPeopleDeathCause_df <- head(most_reccurents, n=3)
  lab <- paste0(round(most_reccurents$Frequences/sum(most_reccurents$Frequences) * 100, 2), "% (",MostRecurrentsPeopleDeathCause_df$Causes,")")
  lab <- head(lab)
  lab
  #Resultat
  MostRecurrentsPeopleDeathCause_df
  #Graph
  pie3D(MostRecurrentsPeopleDeathCause_df$Frequences,col = hcl.colors(length(MostRecurrentsPeopleDeathCause_df$Frequences), "Spectral")
        ,labels = lab , main="Most Recurrents People Death Causes")

  
# 4- Moyenne des attaques ces dernières anneés (Entre 2016 et 2021)
data_moy_attaques_df <- data.frame(Years=format(as.POSIXct(WashingtonPostDatabase_cleaned$date, format = "%Y"), format="%Y")
                                   ,ThreatsLevels=WashingtonPostDatabase$threat_level)
data_moy_attaques_df <-  data_moy_attaques_df%>% group_by(data_moy_attaques_df$Years)%>% summarise(freq=n())
colnames(data_moy_attaques_df) <- c("Years","Frequences")
head(data_moy_attaques_df)
tail(data_moy_attaques_df)
avg_by_years <- data.frame(Average.attacks.2016.2021=mean(data_moy_attaques_df$Frequences))
head(avg_by_years)
tail(avg_by_years)

#Grid Table
grid.table(avg_by_years)

#----------------------------------------CROISEMENT DES DONNÉES-----------------------------
# Jointure des fichiers FatalEncounters et WashingtonPostDatabase
colnames(FatalEncounters_cleaned)[colnames(FatalEncounters_cleaned) == 'Unique.ID'] <- 'id'
mapdata<-merge(WashingtonPostDatabase_cleaned, FatalEncounters_cleaned, by="id")
View(mapdata)

# 5 Les races les plus touchées
data.Races <-  mapdata%>% group_by(mapdata$Race)%>% summarise(Frequences=n())
head(data.Races, n=4)
data.Races <- data.Races[order(data.Races$Frequences,decreasing = TRUE),]
data.Races <- head(data.Races,n=4)
colnames(data.Races) <- c("Races","Frequences")
data.Races

theme_set(theme_classic())
# Barchart
g <- ggplot(data.Races, aes(Races, Frequences))
g + geom_bar(stat="identity", width = 0.5, fill="tomato2") + 
  labs(title="Les races regulièrement victimes de meurtres", 
       subtitle="", 
       caption="") +
  theme(axis.text.x = element_text(angle=65, vjust=0.6))


# 6 Frequence de meutres par sexes 
data.Gender <-  mapdata%>% group_by(mapdata$Gender)%>% summarise(Frequences=n())
data.Gender <- data.Gender[order(data.Gender$Frequences,decreasing = TRUE),]
colnames(data.Gender) <- c("Gender","Frequences")
data.Gender$Gender[3] <- "Others"
data.Gender

theme_set(theme_bw())  

#Diverging bar
ggplot(data.Gender, aes(x=Gender, y=Frequences, label=Gender)) + 
  geom_bar(stat='identity', aes(fill=Frequences), width=.5)  + 
  labs(subtitle="", 
       title= " Frequence de meutres par sexes") + 
  coord_flip()


# 7 Top 5 des etats ayant un total de morts plus élevé
data.State <-  mapdata%>% group_by(mapdata$state)%>% summarise(Frequences=n())
data.State <- data.State[order(data.State$Frequences,decreasing = TRUE),]
colnames(data.State) <- c("States","Frequences")
data.State <- head(data.State,n=5)
data.State


#Circumplex (Polar Bar)
 ggplot(data.State, aes(x = States,y = Frequences,fill = factor(Frequences))) +
  geom_col(width = 1, color = "white") + coord_polar() + theme_minimal() +
   
   # Remove legend, axes, text, and tick marks
   theme(
     legend.position = "none",
     axis.title.x = element_blank(),
     axis.title.y = element_blank(),
     axis.ticks = element_blank(),
     axis.text.y = element_blank(),
     axis.text.x = element_text(face = "bold"),
     plot.title = element_text(size = 24, face = "bold"),
     plot.subtitle = element_text(size = 12)
   )


# 8 -Top 5 des armes les plus utilisées pour les meurtres
 data.Armed <-  mapdata%>% group_by(mapdata$armed)%>% summarise(Frequences=n())
 data.Armed <- data.Armed[order(data.Armed$Frequences,decreasing = TRUE),]
 colnames(data.Armed) <- c("Armed","Frequences")
 data.Armed <- head(data.Armed,n=5)
 data.Armed$Armed[3] <- "bare hands"
 data.Armed

 ggplot(data = data.Armed, aes(x = Armed,y = Frequences,colour = Armed))  + 
   geom_point(size = 2.5) + geom_line(aes(y = Frequences))
