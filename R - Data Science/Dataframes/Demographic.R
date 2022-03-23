

?read.csv()

# Select the file manually method1
stats <- read.csv(file.choose())
stats

# Set working directory and read data method2
getwd()

#Windows:
#setwd("C:\\Users\\Kirill\\Desktop\\R Programming")

#Mac:
setwd("/Users/Elimane/SUPINFO 2022/Big Data/R/Dataframes")
getwd()
rm(stats)
stats <- read.csv("P2-Demographic-Data.csv")
stats

#-----------------------------------------------------Exploring Data---------------------------------------------------
stats
nrow(stats)
ncol(stats)
head(stats, n=1)
tail(stats, n=2) #Bottom of the table
str(stats) # str() # runif()
summary(stats)

#-----------------------------------------------------Using the $ sign---------------------------------------------------
stats
head(stats, n=1)
stats[3,1]
stats[3,"Birth.rate"]
stats$Country.Name
stats$Country.Name[35]
stats[,"Country.Name"] # <=> stats$Country.Name

#------------------------------------------------Basic operations with a Data Frame---------------------------------------------------
stats[1:10,] #Subsetting
stats[c(4,100),]

# Work with []
stats[1,]
is.data.frame(stats[1,])
stats[,1,drop=F]
is.data.frame(stats[,1])
is.data.frame(stats[,1,drop=F])
stats[,1]

# Multiply columns
head(stats)
stats$Birth.rate * stats$Internet.users
stats$Birth.rate + stats$Internet.users

stats$myCalc <- stats$Birth.rate + stats$Internet.users #Adding column myCalc containing (Birth.rate + Internet.users)
stats

# Test of knowledge
stats$xyz <- 1:5 # adding column xyz with recycled interval 1-5
head(stats, n=3)

# Remove columns myCalc and xyz
head(stats)
stats$myCalc <- NULL
stats$xyz <- NULL
head(stats, n=3)

#------------------------------------------------Filtering a Data Frame---------------------------------------------------

head(stats)
internet.users.filter <- stats$Internet.users < 2
birth.rate.filter <- stats$Birth.rate > 40
income.group.filter <- stats$Income.Group == "High income"
stats[income.group.filter ,]
# stats[birth.rate.filter & birth.rate.filter & income.group.filter ,]
levels(stats$Income.Group)

#Informations about Malta
country.name.filter <- stats$Country.Name == "Malta"
stats[country.name.filter ,]

#------------------------------------------------Introduction to qplot---------------------------------------------------
#install.packages("ggplot2")
library("ggplot2")
?qplot
qplot(data=stats, x=Income.Group)
qplot(data=stats, x=Income.Group, y=Birth.rate)
qplot(data=stats, x=Income.Group, y=Birth.rate, size=I(3), colour=I("blue"))
qplot(data=stats, x=Income.Group, y=Birth.rate, geom="boxplot")

#------------------------------------------------Visualizing what we need---------------------------------------------------

qplot(data=stats, x=Internet.users, y=Birth.rate)
qplot(data=stats, x=Internet.users, y=Birth.rate,size=I(3),colour=Income.Group)


#------------------------------------------------Creating Data frames---------------------------------------------------

mydf <- data.frame(Countries_2012_Dataset, Codes_2012_Dataset, Regions_2012_Dataset)
head(mydf)
colnames(mydf) <- c("Countries","Codes","Regions")
head(mydf)
rm(mydf)
head(mydf)

mydf <- data.frame(Countries=Countries_2012_Dataset, Codes=Codes_2012_Dataset, Regions=Regions_2012_Dataset)
head(mydf)
tail(mydf)
summary(mydf)

#------------------------------------------------Merging Data frames---------------------------------------------------
head(stats)
head(mydf)
merged <- merge(stats, mydf, by.x="Country.Code", by.y="Codes")
head(merged)
merged$Countries <- NULL
str(merged)
tail(merged)

#------------------------------------------------Visualizing with new split---------------------------------------------------
qplot(data=merged, x=Internet.users, y=Birth.rate)
qplot(data=merged, x=Internet.users, y=Birth.rate,colour=Regions)

#1-Shapes
qplot(data=merged, x=Internet.users, y=Birth.rate,size=I(3),colour=Regions,shape=I(23))

#2-Transparency
qplot(data=merged, x=Internet.users, y=Birth.rate,size=I(3),colour=Regions,shape=I(19),alpha=I(0.6))

#3-Title
qplot(data=merged, x=Internet.users, y=Birth.rate,size=I(3),colour=Regions,shape=I(19),alpha=I(0.6),main="Birth Rate vs Internet Users")



