library(igraph)
tweets <- read.csv("/Users/omkarsunkersett/Desktop/SI608/project/21stcenturywire.com.csv", header = FALSE)
dir_graph <- graph.data.frame(d = tweets, directed = TRUE)
write.graph(graph = dir_graph, file = '/Users/omkarsunkersett/Desktop/SI608/project/tweets.gml', format = 'gml')
inp_graph <- read.graph(file = '/Users/omkarsunkersett/Desktop/SI608/project/tweets.gml', format = 'gml')
inp_graph

