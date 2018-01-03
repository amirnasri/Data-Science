rankhospital <- function(state, outcome, num = 'best') {
        
        if (class(outcome) != 'character')
                stop('outcome must be a character vector.')
        if (class(state) != 'character')
                stop('state must be a character vector.')
        if (class(num) == 'character') {
                if (num != 'best' && num != 'worst')
                        stop('invalid num.')
        }
        else if (class(num) != 'integer' && class(num) != 'numeric')
                stop('invalid num: num must be an integer.')
        else if (round(num) != num)
                stop('invalid num: num must be an integer.')
        col = NA
        if (outcome == 'heart attack') 
                col = 11
        else if (outcome == 'heart failure')
                col = 17
        else if (outcome == 'pneumonia')
                col = 23
        
        if (is.na(col)) {
                stop('outcome not recognized.')
        }
        
        outcome_df <- read.csv("outcome-of-care-measures.csv", colClasses = "character")
        
        # Select hospital name and outcome columns from outcome dataframe for rows where 'state == State' and outcome is not NA.
        df <- outcome_df[(outcome_df$State == state) & (outcome_df[,col] != "Not Available"), c(2, col)]
        #browser()
        # Change outcome column to numeric to allow numeric comparison
        df[, 2] = as.numeric(df[, 2])
        
        # Order df based on (outcome, hospital name) columns ascending.
        ord <- order(df[, 2], df[, 1])
        df = df[ord,]
        
        if (nrow(df) == 0)
                return()
        
        if (num == 'best')
                return(df[1, 1])
        if (num == 'worst') {
                #browser()
                return(df[dim(df)[1], 1])
        }
        
        return(df[num, 1])
}