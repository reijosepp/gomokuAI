library(dplyr)

filenames = list.files()

all_games = data.frame(matrix(nrow=0, ncol=231))


for (file in filenames) {
  data = read.csv(file) %>%
    mutate(
      filename = file
    )
  all_games = rbind(all_games, data)
}

write.csv(all_games, "all_games.csv")
