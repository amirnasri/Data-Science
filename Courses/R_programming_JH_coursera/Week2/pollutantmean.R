pollutantmean <- function(directory, pollutant, id=1:332) {
     s = 0.0
     count = 0
     for (fid in id) {
          fname = as.character(fid)
          zeros = paste(rep(0, 3 - nchar(fname)), collapse = '')
          fname = paste(zeros, fname, sep = '')
          fname = paste(fname, '.csv', sep = '')
          fname = paste(directory, fname, sep = '/')
          df = read.csv(fname)
          col = df[[pollutant]]
          col_na_rm = col[!is.na(col)]
          count = count + length(col_na_rm)
          s = s + sum(col_na_rm)
     }
     s/count
}