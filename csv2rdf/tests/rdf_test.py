
def create_rdf_test(filename):
    with open(filename, 'w') as file:
        print("Writing Nodes to RDF")
        rdf = '_:ebd2c69febf96b7e1ff792b7cc53088f <dgraph.type> "TestId" .'
        rdf += '\n_:ebd2c69febf96b7e1ff792b7cc53088f <name> "AsnicarF_2017.metaphlan_bugs_list.stool:MV_FEI1_t1Q14" .'
        rdf += '\n_:ebd2c69febf96b7e1ff792b7cc53088f <animal> "Human" .'
        rdf += '\n_:ebd2c69febf96b7e1ff792b7cc53088f <biome> "Digestive system:Large intestine:Fecal" .'
        rdf += '\n_:ebd2c69febf96b7e1ff792b7cc53088f <numberReadsInt> "27553455.0" .'
        rdf += '\n_:ebd2c69febf96b7e1ff792b7cc53088f <sourceDate> "2021-04-07" .'

        file.write(rdf)
        file.write('\n\n')