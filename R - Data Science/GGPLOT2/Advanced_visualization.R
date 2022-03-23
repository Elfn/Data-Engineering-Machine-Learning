

setwd("/Users/Elimane/SUPINFO 2022/Big Data/R - Data Science/GGPLOT2")
getwd()
movies <- read.csv("P2-Movie-Ratings.csv")
movies
head(movies)

#------------------------Aesthetics-------------------------#
library("ggplot2")

colnames(movies) <- c("Film","Genre","CriticRatings","AudienceRatings","BudgetMillions","YearsOfRelease")

ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings))

# Add geometry
ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings)) + geom_point()


# This is the correlation between audience and critic ratings has evolved throughout the years by genre

# Add color
ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings, colour=Genre)) + geom_point()

# Add size
ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings, colour=Genre, size=Genre)) + geom_point()

# Better size
ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings, colour=Genre, size=BudgetMillions)) + geom_point()


#------------------------Plotting with layers-------------------------#
p <- ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings, colour=Genre, size=BudgetMillions)) 
lineGraph <- p + geom_line()
pointGraph <- p + geom_point()
MultiLayersGraph <- p + geom_point() + geom_line()
lineGraph
pointGraph
MultiLayersGraph


#------------------------Overriding Aesthetics-------------------------#
q <- ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings, colour=Genre, size=BudgetMillions)) 

# Add geom layer
pointGraph <- q + geom_point()
pointGraph

# Overriding aes
pointGraph <- q + geom_point(aes(size=CriticRatings))
pointGraph

pointGraph <- q + geom_point(aes(colour=BudgetMillions))
pointGraph

pointGraph <- q + geom_point(aes(x=BudgetMillions))
pointGraph

pointGraph <- q + geom_point(aes(x=BudgetMillions)) + xlab("Budget Millions in $")
pointGraph

pointGraph <- q + geom_point(aes(x=BudgetMillions)) + xlab("Budget Millions in $")
pointGraph

MultiLayersGraph <- p + geom_point() + geom_line(size=1)
MultiLayersGraph

#------------------------Mapping vs Setting-------------------------#

r <- ggplot(data=movies, aes(x=CriticRatings,y=AudienceRatings)) 

pointGraph <- r + geom_point()
pointGraph

# Add Colour 

# Mapping (Here we use aes())
pointGraph <- r + geom_point(aes(colour=Genre))
pointGraph

pointGraph <- r + geom_point(aes(size=BudgetMillions))
pointGraph

# Setting (Here we don't use aes())
# pointGraph <- r + geom_point(aes(colour="DarkGreen")) # ERROR
pointGraph <- r + geom_point(colour="DarkGreen")
pointGraph

pointGraph <- r + geom_point(size=5)
pointGraph



#------------------------Histograms and Density Charts-------------------------#
s <- ggplot(data=movies, aes(x=BudgetMillions)) 

pointGraph <- s + geom_histogram(binwidth = 5)
pointGraph

# Add Colour 
pointGraph <- s + geom_histogram(binwidth = 5, fill="Green") # Setting
pointGraph

pointGraph <- s + geom_histogram(binwidth = 10, aes(fill=Genre)) # Mapping
pointGraph

pointGraph <- s + geom_histogram(binwidth = 10, aes(fill=Genre), colour="Black") # Mapping
pointGraph

pointGraph <- s + geom_density(aes(fill=Genre), position ="stack") # Mapping
pointGraph


#------------------------Starting Layer Tips-------------------------#

t <- ggplot(data=movies, aes(x=CriticRatings)) 

graph <- t + geom_histogram(binwidth = 5,fill="white",colour="darkGreen")
graph








