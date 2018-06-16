rawDataPath<- "../rawData"
dataFileName<- "Hubert_14Jun2018_15-24_150soams.txt" # "auto_14Jun2018_15-04.txt"
fileWithPath<- file.path(rawDataPath,dataFileName)

df <-read.table(fileWithPath,sep="\t", header=TRUE)
files <- dir(path=rawDataPath,pattern='.txt')  #find all data files in this directory

library(dplyr)
df <- df %>% mutate( numTargets =   (resp2 !="-999 ") ) #True if 3 targets, False if 2 targets
df$numTargets <- as.numeric(df$numTargets) + 2

#Calculate corrStream0, corrStream1, corrStream2
df<-df %>% mutate(corrStrm0 = case_when( whichStreamResp0==0 ~ corrResp0,
                                         whichStreamResp1==0 ~ corrResp1,
                                         whichStreamResp2==0 ~ corrResp2,
                                         TRUE ~ NA_real_ ) )
df<-df %>% mutate(corrStrm1 = case_when( whichStreamResp0==1 ~ corrResp0,
                                         whichStreamResp1==1 ~ corrResp1,
                                         whichStreamResp2==1 ~ corrResp2,
                                         TRUE ~ NA_real_ ) )
df<-df %>% mutate(corrStrm2 = case_when( whichStreamResp0==2 ~ corrResp0,
                                         whichStreamResp1==2 ~ corrResp1,
                                         whichStreamResp2==2 ~ corrResp2,
                                         TRUE ~ NA_real_ ) )
table(df$corrStrm0,df$numTargets)
#table(df$whichStreamResp0,df$corrResp0)
#table(df$whichStreamResp0,df$corrResp1)
#table(df$whichStreamResp2,df$corrResp2)
table(df$corrStrm1,df$numTargets)

df<-df %>% mutate(pCorrAll = case_when(numTargets == 2 ~ (corrResp0 + corrResp1) / 2,
                                       numTargets == 3 ~ (corrResp0+corrResp1+corrResp2) / 3,
                                       TRUE ~ -900))
table(df$numTargets,df$pCorrAll)

df %>% group_by(numTargets) %>% summarise_at(vars(corrStrm0:corrStrm2), mean, na.rm=TRUE)



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
  

