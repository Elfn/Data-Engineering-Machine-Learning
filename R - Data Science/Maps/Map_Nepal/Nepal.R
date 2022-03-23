install.packages("cartography")
install.packages("sf")
install.packages("tidyverse")

library(cartography)
library(sf)
library(tidyverse)


setwd("/Users/Elimane/SUPINFO 2022/Big Data/R - Data Science/Maps/Map_Nepal/R")

data<-st_read("shape_files_of_districts_in_nepal.shp")

View(data)
str(data)

 
library(haven)

poverty <- read_dta("poverty.dta")
View(poverty)
head(poverty)
poverty$pov<-poverty$poverty*100 # converts the poverty rate into percentages
View(poverty)


mapdata<-merge(data, poverty, by="dist_name")
View(mapdata)
names(mapdata)