class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() < self.getClearProb():
            return True
        return False


    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.getMaxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.getMaxBirthProb() * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)       


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        density = float(len(self.viruses))/(self.maxPop)
        viruses = self.viruses[:]
        for virus in viruses:
            try:
                self.viruses.append(virus.reproduce(density))
            except NoChildException:
                pass
        return len(self.viruses)


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    trials = []
    viruses = []
    for num in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))
    for trial in range(numTrials):
        lengths = []
        patient = Patient(viruses[:], maxPop)
        for timestep in range(300):
            length = patient.update()
            lengths.append(length)
        trials.append(lengths)
    means = []
    for i in range(300):
        summ = 0.0
        for trial in trials:
            summ += trial[i]
        mean = summ/len(trials)
        means.append(mean)
    pylab.plot(range(300), means, label = 'Curve of Number of Viruses')
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend('Curve of Virus Population')
    pylab.show()
#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug not in self.resistances.keys():
            return False
        elif self.resistances[drug]:
            return True
        return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.getMaxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb, clearProb, and mutProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException
        if random.random() < self.maxBirthProb * (1 - popDensity):
            resistances = self.resistances.copy()
            for i in range(len(self.resistances.keys())):
                if random.random() < self.mutProb:
                    resistances[resistances.keys()[i]] = not self.resistances[self.resistances.keys()[i]]
            return ResistantVirus(self.maxBirthProb, self.clearProb, resistances, self.mutProb)
        raise NoChildException

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        population = []
        for virus in self.viruses:
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    try:
                        population.remove(virus)
                    except ValueError:
                        pass
                    break
                elif virus in population:
                    pass
                else:
                    population.append(virus) 
        return len(population)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        density = float(len(self.viruses))/(self.maxPop)
        viruses = self.viruses[:]
        for virus in viruses:
            try:
                if self.drugs == []:
                    self.viruses.append(virus.reproduce(density, self.drugs))
                for drug in self.drugs:
                    if virus.isResistantTo(drug):
                        self.viruses.append(virus.reproduce(density, self.drugs))
                        break
            except NoChildException:
                pass
        return len(self.viruses)

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)

    """

    viruses = []
    trials1 = []
    trials2 = []
    for num in range(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    for trial in range(numTrials):
        lengths1 = []
        lengths2 = []
        patient = TreatedPatient(viruses[:], maxPop)
        for timestep in range(150):
            length1 = patient.update()
            length2 = patient.getResistPop(['guttagonol'])
            lengths1.append(length1)
            lengths2.append(length2)
        patient.addPrescription('guttagonol')
        for timestep in range(150):
            length1 = patient.update()
            length2 = patient.getResistPop(['guttagonol'])
            lengths1.append(length1)
            lengths2.append(length2)
        trials1.append(lengths1)
        trials2.append(lengths2)
    means1 = []
    means2 = []
    for i in range(300):
        summ = 0.0
        for trial in trials1:
            summ += trial[i]
        mean1 = summ/len(trials1)
        means1.append(mean1)
        summ = 0.0
        for trial in trials2:
            summ += trial[i]
        mean2 = summ/len(trials2)
        means2.append(mean2)
    pylab.plot(range(300), means1)
    pylab.plot(range(300), means2)
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('time step')
    pylab.ylabel('# viruses')
    pylab.legend()
    pylab.show()
