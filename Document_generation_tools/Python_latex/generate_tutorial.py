import numpy as np
import pandas as pd
import os

#do not change - header
out1 =''
out1+= str( r"\documentclass[11pt]{article}" )
out1+= str("\n")
out1+= str(  r"\usepackage[margin=1in]{geometry}" )
out1+= str("\n")
out1+= str( r"\usepackage{amsfonts,amsmath,amssymb}" )
out1+= str("\n")
out1+= str( r"\usepackage[none]{hyphenat}" )
out1+= str("\n")
out1+= str( r"\usepackage{fancyhdr} " )
out1+= str("\n")
out1+= str( r"%\usepackage{xcolor}" )
out1+= str("\n")
out1+= str( r"\usepackage[dvipsnames]{xcolor} " )
out1+= str("\n")
out1+= str( r"\usepackage{array}" )
out1+= str("\n")
out1+= str( r"\usepackage{graphicx}")
out1+= str("\n")
out1+= str( r"\newcolumntype{L}{>{\centering \arraybackslash}m{6cm}} " )
out1+= str("\n")
out1+= str( r"\begin{document} " )
out1+= str("\n")
out1+= str( r"\begin{titlepage}" )
out1+= str("\n")
out1+= str( r"\begin{center}" )
out1+= str("\n")
out1+= str( r"\vspace*{10cm}" )
out1+= str("\n")

input_file = open("plain_text.txt","r")
input_data = input_file.read()
input_file.close()
data_rem = input_data + ''

table_count = 1
figure_count = 1
while(len(data_rem) > 0):
    hash_start_index = data_rem.find('#')
    if ( (hash_start_index == 0) and (data_rem[1] == '&') ):#TITLE directive
        hash_end_index = data_rem.find('#', hash_start_index + 1)
        hash_string = data_rem[hash_start_index+1:hash_end_index]
        if len(hash_string) < 1:
            print("error in sysntax")
            #return        
        #count_number of #
        hash_count = 0
        for i in range(len(hash_string)):
            if hash_string[i] == '&':
                hash_count += 1
            else:
                print("syntax error")
                #return
        heading_rank = hash_count

        #print(hash_start_index, hash_end_index)
        #print(hash_string)
        print("heading_rank = ", heading_rank)
        heading_end_index = data_rem.find("\n", hash_end_index)
        if heading_end_index == -1:
                heading_end_index = len(data_rem)
        try:
            heading_string = data_rem[hash_end_index+1:heading_end_index]
        except Exception as e:
            print(e)
            heading_string = ''
        print("heading_string = ", heading_string)
        data_rem = data_rem[heading_end_index+1:]
        #print(data_rem)
        if heading_rank == 1:
            #find subtitle string
            sub_title_string = ''
            hash_start_index = data_rem.find('#')
            if hash_start_index != 0:
                heading_end_index = data_rem.find("\n", 1)
                sub_title_string = data_rem[0:heading_end_index]
                print("sub_title_string =<", sub_title_string, '>')
                data_rem = data_rem[heading_end_index+1:]
            out1 += str(r"\huge \textbf{ " )
            out1 += heading_string
            out1 += str(r" } \\ " )
            out1 += str('\n')
            if (len(sub_title_string)>0):
                out1 += str(r"\Large " )
                out1 += sub_title_string
                out1 += str('\n')
            out1 += str(r'\vfill')
            out1 += str('\n')
            out1 += str(r'\end{center}')
            out1 += str('\n')
            out1 += str(r'\end{titlepage}')
            out1 += str('\n')
        elif heading_rank == 2:
            out1 += str(r'\section{')
            out1 += heading_string
            out1 += str(r"}" )
            out1 += str('\n')
        #elif heading_rank == 3:
        else:
            out1 += str(r'\subsection{')
            out1 += heading_string
            out1 += str(r"}" )
            out1 += str('\n')

    elif ( (hash_start_index == 0) and (data_rem[1] != '&') ):#TABLE directive
        if (data_rem[1:6] == 'table'):#TABLE
            print("table to be added")
            caption_start_index = data_rem.find('"', 5)
            caption_end_index = data_rem.find('"', caption_start_index+1)
            table_caption = data_rem[caption_start_index+1:caption_end_index]
            heading_end_index = data_rem.find("\n", caption_end_index + 1)
            if heading_end_index == -1:
                heading_end_index = len(data_rem)
            table_path = data_rem[caption_end_index+2: heading_end_index]
            print("table_caption = <", table_caption,">")
            print("table path = <", table_path,">")
            data_rem = data_rem[heading_end_index:]
            #read table
            table_inst = pd.read_csv(table_path, header=None)
            table_data = table_inst.values
            num_rows = np.shape(table_data)[0]
            num_columns = np.shape(table_data)[1]
            #latex data
            out1 += str(r"\begin{table}[h!]")
            out1 += str('\n')
            out1 += str(r"\begin{center}")
            out1 += str('\n')
            out1+= str(r"\caption{")
            out1+= table_caption
            out1+= str(r"}")
            out1 += str('\n')
            out1+= str("\label{tab:")
            out1+= "table" + str(table_count) + "}"
            out1 += str('\n')
            out1 += str(r"\begin{tabular}{")
            
            #alignment details
            for i in range(num_columns):
                out1 += 'l'
                if (i != (num_columns-1)):
                    out1 += '|'
                    #out1 += "p{1cm}"#for wrapping
                else:
                    out1 += '}'
            out1 += str('\n')
            #add titles
            for i in range(num_columns):
                out1 += str(r"\textbf{")
                out1 += str(table_data[0,i])
                out1 += str(r"}")
                if (i != (num_columns-1)):
                    out1 += ' & '
                else:
                    out1 += str(r"\\")
            out1 += str('\n')
            out1 += str(r"\hline")
            out1 += str('\n')
            for i in range(num_rows-1):
                for j in range(num_columns):
                    out1 += str(table_data[i+1,j])
                    if (j != (num_columns-1)):
                        out1 += ' & '
                    else:
                        out1 += str(r"\\")
                        out1 += str('\n')
            out1 += str(r"\hline")
            out1 += str('\n')
            out1 += str(r"\end{tabular}")
            out1 += str('\n')
            out1 += str(r"\end{center}")
            out1 += str('\n')
            out1 += str(r"\end{table}")
            out1 += str('\n')
            table_count += 1
        elif (data_rem[1:7] == 'figure'):#figure
            print("figure to be added")
            caption_start_index = data_rem.find('"', 6)
            caption_end_index = data_rem.find('"', caption_start_index+1)
            figure_caption = data_rem[caption_start_index+1:caption_end_index]
            heading_end_index = data_rem.find("\n", caption_end_index + 1)
            if heading_end_index == -1:
                heading_end_index = len(data_rem)
            figure_path = data_rem[caption_end_index+2: heading_end_index]
            print("figure_caption = <", figure_caption,">")
            print("figure path = <", figure_path,">")
            data_rem = data_rem[heading_end_index:]
            #latex data
            out1 += str(r"\begin{figure}[h!]")
            out1 += str('\n')
            out1 += str(r"\includegraphics[width=\linewidth]{")
            out1 += figure_path + '}'
            out1 += str('\n')
            out1 += str(r"\caption{")
            out1 += figure_caption + '.}'
            out1 += str('\n')
            out1 += str(r"\label{")
            out1 += str(r"figure") + str(figure_count) + '}'
            out1 += str('\n')
            out1 += str(r"\end{figure}")
            out1 += str('\n')
            figure_count += 1
            
    else:#NORMAL TEXT
        print("some text in between")
        text = data_rem[0:hash_start_index-1]
        print("text= <", text,'>')
        data_rem = data_rem[hash_start_index:]
        #print("data remaining below")
        #print(data_rem)
        out1 += text
        out1 += str('\n')

out1 += str(r"\end{document}")
out_file = open("latex_generated.tex", "w")
n = out_file.write(out1)
out_file.close()

os.system("pdflatex latex_generated.tex")


