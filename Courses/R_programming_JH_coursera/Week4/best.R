best <- function(state, outcome) {
        
        if (class(outcome) != 'character')
                stop('outcome must be a character vector.')
        if (class(state) != 'character')
                stop('state must be a character vector.')
        
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
        
        outcome <- read.csv("outcome-of-care-measures.csv", colClasses = "character")
        
        # Select hospital name and outcome columns from outcome dataframe for rows where 'state == State' and outcome is not NA.
        df <- outcome[(outcome$State == state) & (outcome[,col] != "Not Available"), c(2, col)]
        #browser()
        # Change outcome column to numeric to allow numeric comparison
        df[, 2] = as.numeric(df[, 2])
        
        # Order df based on (outcome, hospital name) columns ascending.
        ord <- order(df[, 2], df[, 1])
        df = df[ord,]
        
        if (nrow(df) != 0)
                return(df[1, 1])
        return()
}