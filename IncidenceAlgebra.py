# pyinstaller IncidenceAlgebra.py --windowed -F
import tkinter
import networkx as nx
import matplotlib.pyplot as plt

def _draw_graph(Graph):
    Dimension = 1
    FigDimension = 5
    fig,axes = plt.subplots(nrows=Dimension,ncols=Dimension,figsize=(FigDimension,FigDimension),dpi=200)
    nx.draw_circular(Graph, ax=axes, with_labels=True, edge_color='black', node_color='black', font_color='white')
    axes.set_title("Graph 0")

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
    return nx.parse_adjlist(AdjacencyList.splitlines(), nodetype=int, create_using=nx.DiGraph())

def _reverse_transitivity_reduce(Graph):
    DiGraph = nx.DiGraph(Graph).copy()
    for TargetNode in DiGraph.nodes():
        for SourceNode in DiGraph.nodes():
            if SourceNode == TargetNode:
                continue
            if not DiGraph.has_edge(SourceNode, TargetNode):
                if nx.has_path(DiGraph, SourceNode, TargetNode):
                    DiGraph.add_edge(SourceNode, TargetNode)
    return DiGraph

def _listlist_from_digraph(DiGraph):
    listlist = []
    for Columns in range(DiGraph.number_of_nodes()):
        Column = []
        for Rows in range(DiGraph.number_of_nodes()):
            if Rows==Columns:
                Column.append(1)
            else:
                Column.append(0)
        listlist.append(Column)
    for Edge in nx.generate_edgelist(DiGraph, data=False):
        listlist[int(Edge.split(" ")[0])-1][int(Edge.split(" ")[1])-1] = 1
    return listlist

def _relabel(DiGraph):
    Mapping = dict()
    for Node in DiGraph.nodes():
        Mapping[Node] = Node+1
    return nx.relabel_nodes(DiGraph, Mapping, True)

def _display_result(Matrix):
    window = tkinter.Tk()
    window.title("Resulting Incidence Algebra")
    GoButton = tkinter.Button(window, text="Close", command=lambda: window.destroy()).grid(row=0,column=len(Matrix)+1)
    Matrixrows = []
    for y in range(len(Matrix)):
        Matrixcolumns = []
        for x in range(len(Matrix)):
            Entry = tkinter.Entry(window, width=3)
            Entry.insert(0,Matrix[y][x])
            Entry.config(state="disabled")
            Entry.grid(row=y,column=x)
            Matrixcolumns.append(Entry)
        Matrixrows.append(Matrixcolumns)
    window.after(10, lambda: window.focus_force())
    window.bind('<Return>', lambda event:window.destroy())
    window.iconbitmap("icon.ico")
    window.mainloop()

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
    print(Matrix)
    DiGraph = _relabel(_digraph_from_list_list(Matrix))
    DiGraph = _reverse_transitivity_reduce(DiGraph)
    OutputStream = (_listlist_from_digraph(DiGraph))
    print(OutputStream)
    _display_result(OutputStream)

def _make_window(MatrixSize):
    window = tkinter.Tk()
    window.title("Matrix Entry")
    GoButton = tkinter.Button(window, text="Populate", command=lambda: _calculate_matrix(Matrixrows)).grid(row=0,column=MatrixSize+1)
    Matrixrows = []
    for y in range(MatrixSize):
        Matrixcolumns = []
        for x in range(MatrixSize):
            if x == y:
                Entry = tkinter.Entry(window, width=3)
                Entry.insert(0, "1")
                Entry.config(state="disabled")
            elif x < y:
                Entry = tkinter.Entry(window, width=3)
                Entry.insert(0, "0")
                Entry.config(state="disabled")
            else:
                Entry = tkinter.Entry(window, width=3)
            Entry.grid(row=y,column=x)
            Matrixcolumns.append(Entry)
        Matrixrows.append(Matrixcolumns)
    window.after(10, lambda: window.focus_force())
    window.bind('<Return>', lambda event: _calculate_matrix(Matrixrows))
    window.iconbitmap("icon.ico")
    window.mainloop()

top = tkinter.Tk()
top.title("Incidence Algebra Creation")
top.geometry("400x250")
# top.state("zoomed")
tkinter.Label(top, text="Matrix size:").grid(row=0)
MatrixDimentions = tkinter.Spinbox(top, from_=4, to=50, width=3)
MatrixDimentions.grid(row=0,column=1)
gobutton = tkinter.Button(top, text="Enter Matrix", command=lambda: _make_window(int(MatrixDimentions.get()))).grid(row=0,column=2)
top.bind('<Return>',lambda event:_make_window(int(MatrixDimentions.get())))
top.iconbitmap("icon.ico")
top.mainloop()