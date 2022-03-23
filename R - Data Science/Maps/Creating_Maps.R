#install.packages("ggplot2")
install.packages("tidyverse")
#install.packages("maps")

library(ggplot2)
library(tidyverse)

setwd("/Users/Elimane/SUPINFO 2022/Big Data/R - Data Science/Maps")
getwd()
EUvax <- read.csv("EUvaccine.csv")
head(EUvax)
View(EUvax)
#head(data_)

mapData <- map_data("world")
View(mapData)

mapData <- left_join(mapData,EUvax,by="region")
View(mapData)

# drop nulls columns
mapData2<-mapData %>% filter(!is.na(mapData$Perc_vaccinated))
View(mapData2)

# Create Map
map1 <- ggplot(data=mapData2, aes(x=long,y=lat,group=group)) + geom_polygon(aes(fill=Perc_vaccinated), colour="black") + xlab("Longitude") + ylab("Latitude")
map1

map2 <- map1 + scale_fill_gradient(name = "% vaccinated", low = "yellow", high =  "red", na.value = "green")+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y=element_blank(),
        axis.title.x=element_blank(),
        rect = element_blank())
map2


