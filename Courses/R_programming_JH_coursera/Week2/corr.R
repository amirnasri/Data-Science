corr <- function(directory, threshold=0) {
     file_list = list.files(directory)
     cnt = 0
     cor_vec = numeric(0)
     for (f in file_list) {
          fname = paste(directory, f, sep = '/')
          df = read.csv(fname)
          nobs_vec = (apply(is.na(df), 1, sum) == 0)
          nobs = sum(nobs_vec)
          if (nobs > threshold) {
               df_sn = df[nobs_vec,]
               cnt = cnt + 1
               cor_vec[cnt] = cor(df_sn[['sulfate']], df_sn[['nitrate']])
          }
     }
     cor_vec
}