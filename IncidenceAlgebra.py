# pyinstaller IncidenceAlgebra.py --windowed --icon=icon.ico --onefile
from tkinter import (Button, Tk, LabelFrame, Entry, Spinbox, Label)
from math import ceil
from networkx import (has_path, all_simple_paths, parse_adjlist, DiGraph, generate_edgelist, draw, relabel_nodes)
from matplotlib.pyplot import (subplots)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def _diagram_layout(Graph, Height):
    BaseElements = []
    Distances = []
    for x in range(Height):
        temp = []
        for y in range(Height):
            temp.append(0)
        Distances.append(temp)
    for source in Graph:
        if Graph.in_degree(source) == 0:
            BaseElements.append(source)
        for target in Graph:
            if has_path(Graph, source, target) and source != target:
                distance = len(max(all_simple_paths(Graph, source, target), key=lambda x: len(x)))-1
                # print(f"The distance between {source-1} and {target-1} is {distance}. Distances has length {len(Distances)} and width {len(Distances[0])}")
                Distances[source-1][target-1] = distance
            else:
                Distances[source-1][target-1] = 0
    MaxX = 0
    MaxPlacedOnLevel = 0
    Positions = dict()
    for Base in BaseElements:
        MaxPlacedOnLevel = 0
        Positions[Base] = (MaxX,0)
        for distance in list(set(Distances[Base-1])):
            if distance <= 0:
                continue
            indices = [i for i in range(len(Distances[Base-1])) if Distances[Base-1][i] == distance]
            MaxPlacedOnLevel = max(len(indices), MaxPlacedOnLevel)
            XOffset = max(10, MaxPlacedOnLevel)
            for index in indices:
                if Positions.get(index+1) == None:
                    Positions[index+1] = (MaxX+(indices.index(index)*XOffset),distance)
        MaxX += (MaxPlacedOnLevel)*XOffset
    return Positions

def _digraph_from_list_list(ListList):
    AdjacencyList = ""
    RowCounter = 0
    for row in ListList:
        AdjacencyList += f"{RowCounter}"
        ColumnCounter = 0
        for column in row:
            if RowCounter != ColumnCounter:
                if ListList[RowCounter][ColumnCounter] == 1:
                    AdjacencyList += f" {ColumnCounter}"
            ColumnCounter += 1
        AdjacencyList += "\n"
        RowCounter += 1
    return parse_adjlist(AdjacencyList.splitlines(), nodetype=int, create_using=DiGraph())

def _reverse_transitivity_reduce(Graph):
    digraph = DiGraph(Graph).copy()
    for TargetNode in digraph.nodes():
        for SourceNode in digraph.nodes():
            if SourceNode == TargetNode:
                continue
            if not digraph.has_edge(SourceNode, TargetNode):
                if has_path(digraph, SourceNode, TargetNode):
                    digraph.add_edge(SourceNode, TargetNode)
    return digraph

def _transitivity_reduce(Graph):
    digraph = DiGraph(Graph).copy()
    ValidEdges = []
    for Edge in digraph.edges():
        if (len(max(all_simple_paths(digraph, Edge[0], Edge[1]), key=lambda x: len(x)))-1) == 1:
            ValidEdges.append(Edge)
    return digraph.edge_subgraph(ValidEdges)

def _listlist_from_digraph(digraph):
    listlist = []
    for Columns in range(digraph.number_of_nodes()):
        Column = []
        for Rows in range(digraph.number_of_nodes()):
            if Rows==Columns:
                Column.append(1)
            else:
                Column.append(0)
        listlist.append(Column)
    for Edge in generate_edgelist(digraph, data=False):
        listlist[int(Edge.split(" ")[0])-1][int(Edge.split(" ")[1])-1] = 1
    return listlist

def _relabel(digraph):
    Mapping = dict()
    for Node in digraph.nodes():
        Mapping[Node] = Node+1
    return relabel_nodes(digraph, Mapping, True)

def _display_both_results(Matrix, Graph):
    window = Tk()
    window.title("Resulting Incidence Alegra")
    
    Results = LabelFrame(window)
    Results.grid(row=0,column=0)
    
    MatrixResults = LabelFrame(Results, text="Incidence Matrix")
    MatrixResults.grid(row=0,column=0)
    Matrixrows = []
    for y in range(len(Matrix)):
        Matrixcolumns = []
        for x in range(len(Matrix)):
            entry = Entry(MatrixResults, width=3)
            entry.insert(0,Matrix[y][x])
            if Matrix[y][x] == 0:
                entry.config({"background" : "Grey"})
            else:
                entry.config({"background":"Yellow"})
            entry.grid(row=y,column=x)
            Matrixcolumns.append(entry)
        Matrixrows.append(Matrixcolumns)

    HasseResults = LabelFrame(Results, text="Hasse Diagram")
    HasseResults.grid(row=0,column=1)
    fig,axes = subplots(nrows=1,ncols=1,dpi=100)
    Graph=_transitivity_reduce(Graph).copy()
    draw(Graph, pos=_diagram_layout(Graph, len(Matrixrows)), ax=axes, with_labels=True, edge_color='black', node_color='black', font_color='white')
    canvas = FigureCanvasTkAgg(fig, master=HasseResults)
    canvas.draw()
    canvas.get_tk_widget().pack()

    Bottom = LabelFrame(window)
    Bottom.grid(row=1,column=0)

    ExitButton = Button(Bottom, text="Close", command=lambda: window.destroy())
    ExitButton.pack()

    window.state('zoomed')
    window.mainloop()
    return

def _calculate_matrix(Input):
    Matrix=[]
    for row in Input:
        Temp = []
        for column in row:
            value=column.get()
            if value != '1':
                value = 0
            Temp.append(int(value))
        Matrix.append(Temp)
    # print(Matrix)
    digraph = _relabel(_digraph_from_list_list(Matrix))
    digraph = _reverse_transitivity_reduce(digraph)
    OutputStream = (_listlist_from_digraph(digraph))
    # print(OutputStream)
    _display_both_results(OutputStream, digraph)
    return

def _matrix_window(MatrixSize):
    window = Tk()
    window.title("Matrix Entry")
    GoButton = Button(window, text="Populate", command=lambda: _calculate_matrix(Matrixrows)).grid(row=0,column=MatrixSize+1)
    Matrixrows = []
    for y in range(MatrixSize):
        Matrixcolumns = []
        for x in range(MatrixSize):
            if x == y:
                entry = Entry(window, width=3)
                entry.insert(0, "1")
                entry.config(state="disabled")
            elif x < y:
                entry = Entry(window, width=3)
                entry.insert(0, "0")
                entry.config(state="disabled")
            else:
                entry = Entry(window, width=3)
            entry.grid(row=y,column=x)
            Matrixcolumns.append(entry)
        Matrixrows.append(Matrixcolumns)
    window.after(10, lambda: window.focus_force())
    window.bind('<Return>', lambda event: _calculate_matrix(Matrixrows))
    window.mainloop()
    return

top = Tk()
top.title("Incidence Algebra Creation")
Label(top, text="Matrix size:").grid(row=0)
MatrixDimentions = Spinbox(top, from_=4, to=50, width=3)
MatrixDimentions.grid(row=0,column=1)
gobutton = Button(top, text="Enter Matrix", command=lambda: _matrix_window(int(MatrixDimentions.get()))).grid(row=0,column=2)
top.bind('<Return>',lambda event:_matrix_window(int(MatrixDimentions.get())))
top.mainloop()