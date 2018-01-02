complete <- function(directory, id=1:332) {
     file_list = list.files(directory)
     complete_df = data.frame(matrix(ncol = 2, nrow = 0))
     for (fid in id) {
          fname = as.character(fid)
          zeros = paste(rep(0, 3 - nchar(fname)), collapse = '')
          fname = paste(zeros, fname, sep = '')
          fname = paste(fname, '.csv', sep = '')
          fname = paste(directory, fname, sep = '/')
          df = read.csv(fname)
          nobs = sum(apply(is.na(df), 1, sum) == 0)
          complete_df = rbind(complete_df, c(fid, nobs))
     }
     colnames(complete_df) = c('id', 'nobs')
     complete_df
}