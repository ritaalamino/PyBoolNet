


import subprocess
import shutil
import os
import sys

import networkx

sys.path = ['../..'] + sys.path

import PyBoolNet



def pairs(List):
    if not List:
        return List
    x = None
    result = []
    if len(List)%2:
        x = List.pop()
    for i in range(int(len(List)/2)):
        result+= [List[2*i]+", "+List[2*i+1]]
    if x:
        if result:
            result[-1] = result[-1]+","
        result+=[x]

    return result


def run():


    RUN_ALL = 1

    if 0 or RUN_ALL:
        print("modifications of networks")


        bnet = """
        v1, 0
        v2, 1
        v3, v1&v2&v3&v4
        v4, v3 & (v1|v2)
        """
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)

        constants = PyBoolNet.PrimeImplicants.find_constants(primes)
        PyBoolNet.PrimeImplicants.create_blinkers(primes, constants)

        print(PyBoolNet.FileExchange.primes2bnet(primes))

    if 0 or RUN_ALL:
        print("creates basin diagrams")
        primes = PyBoolNet.Repository.get_primes("xiao_wnt5a")
        diagram = PyBoolNet.Commitment.compute_diagram(primes, "asynchronous")
        print(diagram.order())
        print(diagram.nodes())
        print(diagram.node["4"]["formula"])
        print(diagram.node["4"]["size"])


        primes = PyBoolNet.Repository.get_primes("arellano_rootstem")
        diagram = PyBoolNet.Commitment.compute_diagram(primes, "asynchronous", FnameImage="source/figure26.pdf")

    if 0 or RUN_ALL:
        print("creates interaction graphs for all repository networks:")
        s = []
        for x in PyBoolNet.Repository.names_with_fast_analysis():
            print(x)
            primes = PyBoolNet.Repository.get_primes(x)
            igraph = PyBoolNet.InteractionGraphs.create_image(primes, "source/%s_igraph.pdf"%x)

            s+= [x]
            s+= ["-"*len(x)]
            s+= [".. figure:: %s_igraph.pdf"%x]
            s+= ["   :scale: 60%"]
            s+= ["   :align: center"]
            s+= [""]
            s+= ["   Interaction graph of %s."%x]
            s+= [""]
            s+= [""]

        print("\n".join(s))


    if 0 or RUN_ALL:
        print("model checking with accepting states")

        bnet = ["x0,   !x0&x1 | x2",
                "x1,   !x0 | x1 | x2",
                "x2,   x0&!x1 | x2"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        update = "asynchronous"
        init = "INIT !x1"
        spec = "CTLSPEC EF(AG(x0_STEADY))"

        answer, accepting = PyBoolNet.ModelChecking.check_primes_with_acceptingstates(primes, update, init, spec)
        for x in accepting.items():
            print(x)

        prop = accepting["INITACCEPTING"]
        init = "INIT %s"%prop
        spec = "CTLSPEC EF(STEADYSTATE)"
        print(PyBoolNet.ModelChecking.check_primes(primes, update, init, spec))

        for x in PyBoolNet.StateTransitionGraphs.enumerate_states(primes, prop):
            print(x)




    if 0 or RUN_ALL:
        print("primes from Python functions")

        f1 = lambda v2,v3,v4,v5: sum([v2,v3,v4,v5])>=2

        def f2(v1,v2,v3):
            if f1(v2,v3,0,0):
                return 0
            else:
                return sum([v1,v2,v3]) % 2

        f3 = lambda v4,v5: not (v4 or not f2(v4,v4,v5))
        f4 = lambda: 1
        f5 = lambda v5: v5

        funcs = {"v1":f1, "v2":f2, "v3":f3, "v4":f4, "v5":f5}
        primes = PyBoolNet.QuineMcCluskey.functions2primes(funcs)

        dnf = PyBoolNet.QuineMcCluskey.functions2mindnf(funcs)
        print(dnf["v1"])

    if 0 or RUN_ALL:
        print("figure01.pdf - basic interaction graph")

        bnet = "\n".join(["v1, v1|v3","v2, 1", "v3, v1&!v2 | !v1&v2"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        print(igraph.nodes())
        print(igraph.edges())
        print(igraph.adj["v3"]["v1"]["sign"])
        print(igraph.adj["v1"]["v3"]["sign"])

        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure01.pdf")

    if 0 or RUN_ALL:
        print("graph, node and edge attributes")

        bnet = "\n".join(["v1, v2 & (!v1 | v3)","v2, !v3","v3, v2 | v1"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        igraph.graph["node"]["shape"] = "circle"
        igraph.graph["node"]["color"] = "blue"
        igraph.node["v2"]["shape"] = "rpromoter"
        igraph.node["v2"]["color"] = "black"
        igraph.adj["v3"]["v1"]["arrowhead"] = "inv"
        igraph.adj["v3"]["v1"]["color"] = "red"
        igraph.graph["splines"] = "ortho"
        igraph.graph["label"] = "Example 3: Interaction graph with attributes"
        igraph.graph["rankdir"] = "LR"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure02.pdf")

    if 0 or RUN_ALL:
        print("the interaction signs style")

        funcs = {"v1":lambda v1,v2,v3: v1+v2+v3==1,
                 "v2":lambda v1: not v1,
                 "v3":lambda v2: v2}
        primes = PyBoolNet.QuineMcCluskey.functions2primes(funcs)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        PyBoolNet.InteractionGraphs.add_style_interactionsigns(igraph)
        igraph.graph["label"] = "Example 4: Signed interaction graph"
        igraph.graph["rankdir"] = "LR"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure03.pdf")

    if 0 or RUN_ALL:
        print("styles for inputs, outputs and constants")

        bnet = ["v1, v1", "v2, v2", "v3, 1", "v4, v1 | v3",
                "v5, v4 & v2 | v6", "v6, 0", "v7, !v5",
                "v8, v7", "v9, v5 & v7"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        PyBoolNet.InteractionGraphs.add_style_inputs(igraph)
        PyBoolNet.InteractionGraphs.add_style_constants(igraph)
        PyBoolNet.InteractionGraphs.add_style_outputs(igraph)
        igraph.graph["label"] = "Example 5: Interaction graph with styles for inputs, outputs and constants"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure04.pdf")

    if 0 or RUN_ALL:
        print("the SCC style")

        bnet = ["v1, v1", "v2, v3 & v5", "v3, v1", "v4, v1", "v5, 1",
                "v6, v7", "v7, v6 | v4", "v8, v6", "v9, v8", "v10, v7 & v11",
                "v11, v10 | v4", "v12, v10"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        PyBoolNet.InteractionGraphs.add_style_sccs(igraph)
        igraph.graph["label"] = "Example 6: Interaction graph with SCC style"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure05.pdf")

        igraph.graph["label"] = "Example 7: Interaction graph with SCC style"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure06.pdf")

    if 0 or RUN_ALL:
        print("the subgraph style")

        bnet = ["v1, v7", "v2, v1 & v6", "v3, v2 | v7", "v4, v3",
                "v5, v1 | v4", "v6, v5", "v7, v6"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        subgraphs = [(["v2","v6"], {}),
                     (["v1","v4"],{"label":"Genes", "fillcolor":"lightblue"})]
        PyBoolNet.InteractionGraphs.add_style_subgraphs(igraph, subgraphs)
        igraph.graph["label"] = "Example 8: Interaction graph with a subgraph style"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure07.pdf")

    if 0 or RUN_ALL:
        print("the activities style and animations")

        bnet = ["v1, v7",
                   "v2, v1 & v6",
                   "v3, v2 | v7",
                   "v4, v3",
                   "v5, v1 | v4",
                   "v6, v5",
                   "v7, v6"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        activities = {"v2":1, "v3":0, "v4":0}
        PyBoolNet.InteractionGraphs.add_style_activities(igraph, activities)
        igraph.graph["label"] = "Example 9: Interaction graph with a activities style"
        igraph.graph["rankdir"] = "LR"

        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure08.pdf")


    if 0 or RUN_ALL:
        print("the default style")

        bnet = ["v1, v1", "v2, v3 & !v5", "v3, !v1", "v4, v1", "v5, 1",
                "v6, v7", "v7, v6 & !v4 | !v6 & v4", "v8, !v6", "v9, v8", "v10, v7 & !v11",
                "v11, v10 | v4", "v12, v10"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        PyBoolNet.InteractionGraphs.add_style_default(igraph)
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "PyBoolNet-screenshot.jpg")
        igraph.graph["label"] = "Example 10: Interaction graph with default style"
        PyBoolNet.InteractionGraphs.igraph2image(igraph, "source/figure09.pdf")

    if 0 or RUN_ALL:
        print("Drawing the State Transition Graph - Asynchronous")


        bnet = "\n".join(["v1, v3","v2, v1", "v3, v2"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        update = "asynchronous"
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        print(repr(stg))
        print(list(stg.nodes())[0])
        print(networkx.has_path(stg, "100", "111"))
        stg.graph["label"] = "Example 11: The STG of a positive circuit"
        stg.graph["rankdir"] = "LR"
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure10.pdf")

        init = ["000", "111"]
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update, init)
        init = ["000", {"v1":1,"v2":1,"v3":1}]
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update, init)
        init = lambda x: x["v1"]>=x["v2"]
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update, init)
        init = "--1"
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update, init)
        init = {"v3":1}
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update, init)

    if 0 or RUN_ALL:
        print("Drawing the State Transition Graph - Synchronous")

        bnet = "\n".join(["v1, !v3","v2, v1", "v3, v2"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "synchronous")
        stg.graph["label"] = "Example 12: The synchronous STG of a negative circuit"
        stg.graph["rankdir"] = "LR"
        PyBoolNet.StateTransitionGraphs.add_style_tendencies(stg)
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure11.pdf")

    if 0 or RUN_ALL:
        print("path style")

        bnet = "\n".join(["x, !x|y", "y, !x&!z|x&!y&z", "z, x|!y"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 13: STG with path style"

        path = ["011","010","110","100","000"]
        PyBoolNet.StateTransitionGraphs.add_style_path(stg, path, "red")
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure12.pdf")

    if 0 or RUN_ALL:
        print("scc style for STGs")

        bnet = "\n".join(["x, !x|y", "y, x&!y|!z", "z, x&z|!y"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 14: STG with SCC style"
        PyBoolNet.StateTransitionGraphs.add_style_sccs(stg)
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure13.pdf")

    if 0 or RUN_ALL:
        print("min trap spaces style")

        bnet = "\n".join(["x, !x|y&z", "y, x&!y|!z", "z, z|!y"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 15: STG with min trap spaces style"
        PyBoolNet.StateTransitionGraphs.add_style_mintrapspaces(primes, stg)
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure14.pdf")


    if 0 or RUN_ALL:
        print("STG subspaces style")

        bnet = "\n".join(["x, !x|y&z", "y, x&!y|!z", "z, z|!y"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 16: STG with subspaces style"
        sub1 = ({"x":0},{"label":"x is zero"})
        sub2 = {"x":1,"y":0}
        subspaces = [sub1, sub2]
        PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, subspaces)

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure15.pdf")


    if 0 or RUN_ALL:
        print("STG default style")

        bnet = "\n".join(["x, !x|y&z", "y, x&!y|!z", "z, z|!y"])
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 17: STG with default style"
        PyBoolNet.StateTransitionGraphs.add_style_default(primes, stg)

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure16.pdf")

    if 0 or RUN_ALL:
        print("model checking 1")

        bnet = ["Erk,  Erk & Mek | Mek & Raf",
                "Mek,  Erk | Mek & Raf",
                "Raf,  !Erk | !Raf"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        stg.graph["label"] = "Example 18: STG of the Erk-Mek-Raf network"

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure17a.pdf")

        ## description not in the manual
        ts_basic = PyBoolNet.StateTransitionGraphs.copy(stg)
        ts_basic.graph["label"] = "Example 19: Basic transition system of Erk-Mek-Raf"
        ts_auxillary = PyBoolNet.StateTransitionGraphs.copy(stg)
        ts_auxillary.graph["label"] = "Example 20: Transition system of Erk-Mek-Raf with auxillary variables"
        for x in stg.nodes():
            x_dict = PyBoolNet.StateTransitionGraphs.state2dict(primes, x)
            ap_basic = [name for name in sorted(x_dict) if x_dict[name]]
            ap_auxillary = list(ap_basic)
            outdegree = len(list(y for y in stg.successors(x) if y!=x))

            suc = PyBoolNet.StateTransitionGraphs.successor_synchronous(primes, x_dict)
            ap_auxillary+= [name+"_STEADY" for name in sorted(x_dict) if suc[name]==x_dict[name]]
            if not outdegree:
                ap_auxillary+= ["STEADYSTATE"]
            ap_auxillary+= ["SUCCESSORS=%i"%outdegree]

            ap_basic = pairs(ap_basic)
            ts_basic.node[x]["label"] = "{"+"\\n".join(ap_basic)+"}"

            ap_auxillary = pairs(ap_auxillary)
            ts_auxillary.node[x]["label"] = "{"+"\\n".join(ap_auxillary)+"}"


        PyBoolNet.StateTransitionGraphs.stg2image(ts_basic, "source/figure17b.pdf")

        print("calling pdflatex, hope its installed")
        proc = subprocess.Popen(["pdflatex", "merge_figure17.tex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        print("calling pdfcrop, hope its installed")
        proc = subprocess.Popen(["pdfcrop", "merge_figure17.pdf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        shutil.copyfile("merge_figure17-crop.pdf", "source/figure17.pdf")

        PyBoolNet.StateTransitionGraphs.stg2image(ts_auxillary, "source/figure18.pdf")


    if 0 or RUN_ALL:
        print("LTL queries")

        bnet = ["Erk,  Erk & Mek | Mek & Raf",
                "Mek,  Erk | Mek & Raf",
                "Raf,  !Erk | !Raf"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        init = "INIT TRUE"
        spec = "LTLSPEC F(Raf)"
        update = "asynchronous"
        print(PyBoolNet.ModelChecking.check_primes(primes, update, init, spec))


        init = "INIT Erk & SUCCESSORS<2"
        spec = "LTLSPEC G(F(Raf) & F(!Raf))"
        answer = PyBoolNet.ModelChecking.check_primes(primes, "asynchronous", init, spec)
        print(init, spec, "is", answer)

        init = "INIT Mek"
        spec = "LTLSPEC G(count(Erk_STEADY,Mek_STEADY,Raf_STEADY)>=2)"
        answer = PyBoolNet.ModelChecking.check_primes(primes, "asynchronous", init, spec)
        print(init, spec, "is", answer)


        print("#### Counterexamples ####")
        init = "INIT TRUE"
        spec = "LTLSPEC F(Raf & F(STEADYSTATE))"
        update = "asynchronous"
        answer, counterex = PyBoolNet.ModelChecking.check_primes_with_counterexample(primes, update, init, spec)
        print(answer)
        if counterex:
            print(" -> ".join(PyBoolNet.StateTransitionGraphs.state2str(x) for x in counterex))

    if 0 or RUN_ALL:
        print("counterexample path style")

        bnet = ["Erk,  Erk & Mek | Mek & Raf",
                "Mek,  Erk | Mek & Raf",
                "Raf,  !Erk | !Raf"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        update = "asynchronous"

        init = "INIT TRUE"
        spec = "LTLSPEC F(Raf & F(STEADYSTATE))"
        answer, counterex = PyBoolNet.ModelChecking.check_primes_with_counterexample(primes, update, init, spec)
        if counterex:
            " -> ".join(PyBoolNet.StateTransitionGraphs.state2str(x) for x in counterex)

        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update)
        PyBoolNet.StateTransitionGraphs.add_style_path(stg, counterex, "red")
        stg.graph["label"] = "Example 19: A LTL counterexample"
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure19.pdf")

        igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)
        PyBoolNet.InteractionGraphs.activities2animation(igraph, counterex, "counterexample.gif")

    if 0 or RUN_ALL:
        print("CTL examples")

        bnet = ["GrowthFactor,  0",
                "Proliferation, GrowthFactor | Proliferation & !DNAdamage",
                "DNAdamage,     !GrowthFactor & DNAdamage"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        update = "asynchronous"

        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, update)
        for x in stg.nodes():
            x_dict = PyBoolNet.StateTransitionGraphs.state2dict(primes, x)
            if x_dict["GrowthFactor"]:
                stg.node[x]["style"] = "filled"
                stg.node[x]["fillcolor"] = "gray"
        sub = ({"Proliferation":1},{"label":"proliferation"})
        PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, [sub])
        stg.graph["label"] = "Example 20: STG of the Proliferation network"

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure20.pdf")


        init = "INIT GrowthFactor"
        spec = "LTLSPEC F(Proliferation)"
        answer, counterex = PyBoolNet.ModelChecking.check_primes_with_counterexample(primes, update, init, spec)
        print(init, spec, "is", answer)
        PyBoolNet.StateTransitionGraphs.add_style_path(stg, counterex, "red")
        stg.graph["label"] = "Example 21: Counterexample"

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure21.pdf")

        spec = "CTLSPEC EF(Proliferation)"
        answer = PyBoolNet.ModelChecking.check_primes(primes, update, init, spec)
        print(init, spec, "is", answer)

    if 0 or RUN_ALL:
        bnet = ["GrowthFactor,  0",
                "Proliferation, GrowthFactor | Proliferation & !DNAdamage",
                "DNAdamage,     !GrowthFactor & DNAdamage"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        update = "asynchronous"

        init = "INIT !DNAdamage & GrowthFactor"
        c1 = "Proliferation"
        c2 = "DNAdamage_STEADY"
        spec = "CTLSPEC AG(EF(AG(%s | %s)))"%(c1,c2)
        answer = PyBoolNet.ModelChecking.check_primes(primes, update, init, spec)
        print(init, spec, "is", answer)

        init = "INIT Proliferation"
        condition = "STEADYSTATE"
        spec = "CTLSPEC AG(EF(AG(%s)))"%condition
        answer = PyBoolNet.ModelChecking.check_primes(primes, update, init, spec)
        print(init, spec, "is", answer)

        init = "INIT Proliferation"
        condition = "STEADYSTATE | (!Proliferation & DNAdamage)"
        spec = "CTLSPEC AG(EF(AG(%s)))"%condition
        answer = PyBoolNet.ModelChecking.check_primes(primes, update, init, spec)
        print(init, spec, "is", answer)

        init = "INIT Proliferation"
        spec = "CTLSPEC EX(Proliferation)"
        answer, counterex = PyBoolNet.ModelChecking.check_primes_with_counterexample(primes, update, init, spec)
        print(init, spec, "is", answer)
        print(counterex)
        for x in counterex:
            print(PyBoolNet.StateTransitionGraphs.state2str(x))

        for x in PyBoolNet.StateTransitionGraphs.successors_asynchronous(primes, "101"):
            print(x)

    if 0 or RUN_ALL:
        bnet = ["x0,   !x0&x1 | x2",
                "x1,   !x0 | x1 | x2",
                "x2,   x0&!x1 | x2"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)

        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        attractor1 = (["010", "110"],{"label":"Attractor1"})
        attractor2 = (["111"],{"label":"Attractor2"})
        for x in stg.nodes():
            if x[1]=="0":
                stg.node[x]["style"] = "filled"
                stg.node[x]["fillcolor"] = "gray"

        stg.graph["label"] = "Example 22: Existential queries"
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure22.pdf")

        init = "INIT !x1"
        specQ1 = "CTLSPEC  EF(AG(x0_STEADY))"
        specQ2 = "CTLSPEC !EF(AG(x0_STEADY))"
        update = "asynchronous"
        Q1 = PyBoolNet.ModelChecking.check_primes(primes, update, init, specQ1)
        print(Q1)
        Q2 = not PyBoolNet.ModelChecking.check_primes(primes, update, init, specQ2)
        print(Q2)

        notQ2, counterex = PyBoolNet.ModelChecking.check_primes_with_counterexample(primes, update, init, specQ2)
        state = counterex[0]
        print(PyBoolNet.StateTransitionGraphs.state2str(state))

        print(counterex)

    if 0 or RUN_ALL:

        bnet = ["x, !x | y | z",
                "y, !x&z | y&!z",
                "z, x&y | z"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        tspaces = PyBoolNet.AspSolver.trap_spaces(primes, "all")
        for x in tspaces:
            print(PyBoolNet.StateTransitionGraphs.subspace2str(primes, x))

        print(", ".join(PyBoolNet.StateTransitionGraphs.subspace2str(primes, x) for x in tspaces))

        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, tspaces)

        stg.graph["label"] = "Example 23: All trap spaces"
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure23.pdf")


        mintspaces = PyBoolNet.AspSolver.trap_spaces(primes, "min")
        print("mintspaces", ", ".join(PyBoolNet.StateTransitionGraphs.subspace2str(primes, x) for x in mintspaces))
        for x in mintspaces:
            sub = (x,{"fillcolor":"salmon"})
            PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, [sub])
        maxtspaces = PyBoolNet.AspSolver.trap_spaces(primes, "max")
        print("maxtspaces", ", ".join(PyBoolNet.StateTransitionGraphs.subspace2str(primes, x) for x in maxtspaces))
        for x in maxtspaces:
            if x in mintspaces:
                sub = (x,{"fillcolor":"lightyellow"})
                PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, [sub])
            else:
                sub = (x,{"fillcolor":"lightblue"})
                PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, [sub])
        stg.graph["label"] = "Example 24: Minimal and maximal trap spaces"

        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure24.pdf")


    if 0 or RUN_ALL:
        bnet = ["v1, !v1 | v3",
                "v2, !v1 | v2&!v3",
                "v3, !v2"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        PyBoolNet.StateTransitionGraphs.add_style_sccs(stg)
        steady, cyclic = PyBoolNet.Attractors.compute_attractors_tarjan(stg)

        stg.graph["label"] = "Example 25: A network with a cyclic attractor and a steady state."
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figure25.pdf")

        state = PyBoolNet.Attractors.find_attractor_state_by_randomwalk_and_ctl(primes, "asynchronous")
        print(PyBoolNet.StateTransitionGraphs.state2str(state))

        update = "asynchronous"
        mintspaces = PyBoolNet.AspSolver.trap_spaces(primes, "min")
        for x in mintspaces:
            answer_univocal = PyBoolNet.Attractors.univocality( primes, update, x )
            answer_faithful = PyBoolNet.Attractors.faithfulness( primes, update, x )
            print("min trap space:", PyBoolNet.StateTransitionGraphs.subspace2str(primes, x))
            print("  is univocal:", answer_univocal)
            print("  is faithful:", answer_faithful)

        answer_complete = PyBoolNet.Attractors.completeness_naive( primes, update, mintspaces )
        print("min trap spaces are complete:", answer_complete)


    if False:

        bnet = ["v1, !v1&!v2&v3 | !v1&v2&!v3 | v1&!v2&!v3 | v1&v2&v3",
               "v2, !v1&!v2&!v3 | !v1&v2&v3 | v1&!v2&v3 | v1&v2&!v3",
               "v3, !v1&!v2&v3 | !v1&v2&!v3 | v1&!v2&!v3 | v1&v2&v3"]
        bnet = "\n".join(bnet)
        primes = PyBoolNet.FileExchange.bnet2primes(bnet)
        mintspaces = PyBoolNet.AspSolver.trap_spaces(primes, "min")
        stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
        mintspaces = PyBoolNet.AspSolver.trap_spaces(primes, "min")
        print([PyBoolNet.StateTransitionGraphs.subspace2str(primes, x) for x in mintspaces])

        PyBoolNet.StateTransitionGraphs.add_style_sccs(stg)
        PyBoolNet.StateTransitionGraphs.add_style_subspaces(primes, stg, mintspaces)

        stg.graph["label"] = "Example xx: An STG whose minimal trap space '---' is not complete"
        PyBoolNet.StateTransitionGraphs.stg2image(stg, "source/figurexx.pdf")





if __name__=="__main__":
    run()
