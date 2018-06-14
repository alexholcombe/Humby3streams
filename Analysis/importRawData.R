rawDataPath<- "../rawData"
dataFileName<- "auto_14Jun2018_14-31.txt"
fileWithPath<- file.path(rawDataPath,dataFileName)

df <-read.table(fileWithPath,sep="\t", header=TRUE)
files <- dir(path=rawDataPath,pattern='.txt')  #find all data files in this directory

df$pCorrAll <- (df$corrResp0 + df$corrResp1 + df$corrResp2) / 3

library(dplyr)
df <- df %>% mutate( numTargets =   (resp2 =="-999 ") ) #True if 3 targets, False if 2 targets
df$numTargets <- as.numeric(df$numTargets) + 2

dfAll<-data.frame()
for (i in 1:length(files)) { #read in each file
  fileThis<- file.path(rawDataPath,files[i])
  rawDataLoad=tryCatch(
    read.table(fileThis,sep='\t',header=TRUE),
    error=function(e) {
      stop( paste0("ERROR reading the file ",fileThis," :",e) )
    } )
  apparentSubjectName <- strsplit(files[i],split="_")[[1]][1]
  subjectName<- rawDataLoad$subject[[1]]
  if (apparentSubjectName != subjectName) {
    stop( paste0("WARNING apparentSubjectName",apparentSubjectName," from filename does not match subjectName inside file",subjectName) )
  }
  else { cat(paste0(' Subject ',apparentSubjectName,' read in')) }
  rawDataLoad$file <- files[i]
  
  #Eventually, try to integrate with eye movements file here
  
  tryCatch(
    dfAll<-rbind(dfAll,rawDataLoad), #if fail to bind new with old,
    error=function(e) { #Give feedback about how the error happened
      cat(paste0("Tried to merge but error:",e) )
    } )
  

