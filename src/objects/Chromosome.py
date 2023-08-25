class Chromosome:
    _genes = None
    _fitness = None
    Rank = None
    CrowdingDistance = None
    StudentsFitness = None
    All_Project_Ranks = None
    SelectedSupervisorsAndProjects = None
    SupervisorsFitness = None
    NormalizedStudentsFitness = None
    NormalizedSupervisorsFitness = None

    def __init__(self, genes):
        self._genes = genes
        # self._fitness = fitness

    def getGenes(self):
        return self._genes

    def getFitness(self):
        return self._fitness

    def __eq__(self, obj):
        obj_genes = obj.getGenes()
        # for idx in range(len(self._genes)):
        #     if self._genes[idx].projectID != obj_genes[idx].projectID:
        #         return False
        return self._genes == obj_genes

    def __str__(self):
        genes = []
        for item in self._genes:
            genes.append(str(item))
        return str(genes)

