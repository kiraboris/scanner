NAME := Heterodyne_Receiver_June_14

$(NAME).pdf : $(NAME).dvi
	dvipdf $(NAME)
    
$(NAME).dvi : $(NAME).tex bibliography.bib .FORCE
	latex $(NAME)
	bibtex $(NAME)
	latex $(NAME)
	latex $(NAME)

.FORCE :