# Simulating the Spread of Disease and Virus Population Dynamics 
import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

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

        if random.random() <= self.getClearProb():
            return True
        else:
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
        
        if random.random() <= self.maxBirthProb * ( 1 - popDensity):
            x = SimpleVirus(self.maxBirthProb, self.clearProb)
            return x   
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
        new_viruses = []
        for i in self.viruses: 
            # decide which virus particles are cleared and which survive by making use of
            # the doesClear method of each SimpleVirus instance
            if i.doesClear() == False:
                # then update the collection of SimpleVirus instances accordingly
                new_viruses.append(i)
        self.viruses = new_viruses
            # With the surviving SimpleVirus instances, update should then
            # call the reproduce method for each virus particle
        popDensity = float(self.getTotalPop())/ float(self.getMaxPop())
        virus_spawn = []
        for j in self.viruses:
            virus_spawn.append(j)
            try:
                spawn= j.reproduce(popDensity)
                virus_spawn.append(spawn)
            except NoChildException:
                pass
            
        self.viruses = virus_spawn
        # returns the number of virus particles in the patient at the end of the time step
        return self.getTotalPop()


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
    virus_list = []
    virus_pop = []
    for i in range(numViruses):
        virus_list.append(SimpleVirus(maxBirthProb,clearProb))

    p = Patient(virus_list, maxPop)   
    for j in range(300):  
        p.update()
        total = 0
        for i in range(numTrials):
            total += p.getTotalPop()
        avg = float(total)/float(numTrials)
        virus_pop.append(avg)
        
    pylab.plot(range(300), virus_pop)
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc = 'upper left')
    pylab.show()

#simulationWithoutDrug(1, 10, 1.0, 0.0, 1)
#simulationWithoutDrug(100,1000,0.1,0.05,30)
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

        SimpleVirus.__init__(self,maxBirthProb,clearProb)
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
        for i in self.resistances:
            if i == drug:
                if self.resistances[i] == True:
                    return True
        else:
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
        # stochastically determines whether the virus particle reproduces at a time step
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            #check if the virus is resistant to all the drugs in the activeDrugs list
            for i in activeDrugs:
                if self.isResistantTo(i) == False:
                    # if not, it will not reproduce
                    raise NoChildException
            else:
            # if yes, it will reproduce (if the virus is resistant to all drugs in active drugs)
                resDict = self.resistances.copy()
                # For each drug resistance trait of the virus 
                for drug in self.resistances:
                    if random.random() < self.mutProb:
                        resDict[drug] = not resDict[drug]
                return ResistantVirus(self.maxBirthProb,self.clearProb,resDict,self.mutProb)
            
                # reproduce = creates, returns the instance of the offspring Resistant Virus
                #newborn = ResistantVirus(self.maxBirthProb,self.clearProb,self.resistances,self.mutProb)
        else:
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

        Patient.__init__(self, viruses,maxPop)
        self.drugsList = []
        

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if not newDrug in self.drugsList:
            self.drugsList.append(newDrug)
            
    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugsList


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        virusPop = []
        flag = False
        for virus in self.viruses:
            count = 0
            for drug in drugResist:
                if virus.isResistantTo(drug) == True:
                    count +=1
            if count == len(drugResist):
                virusPop.append(virus)
        return len(virusPop)

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
        new_viruses = []
        for i in self.viruses: 
            # decide which virus particles are cleared and which survive by making use of
            # the doesClear method of each SimpleVirus instance
            if i.doesClear() == False:
                # then update the collection of SimpleVirus instances accordingly
                new_viruses.append(i)
        self.viruses = new_viruses
            # With the surviving SimpleVirus instances, update should then
            # call the reproduce method for each virus particle
        density = float(self.getTotalPop())/ float(self.getMaxPop())
        virus_spawn2 = []
        for j in self.viruses:
            #virus_spawn.append(j)
            try:
                spawn2= j.reproduce(density,self.getPrescriptions())
                virus_spawn2.append(spawn2)
            except NoChildException:
                pass
            
        for k in virus_spawn2:
            self.viruses.append(k)
        # returns the number of virus particles in the patient at the end of the time step
        return self.getTotalPop()


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
    virt = {}
    virt1 = {}
    avg = []
    avg1 = []
    for t in range(numTrials):
        listV =[]
        for v in range(numViruses):
            rv = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            listV.append(rv)
        patient = TreatedPatient(listV, maxPop)
        for n in range(300):
            patient.update()
            if virt.has_key(n):
                virt[n] += (patient.getTotalPop())
            else:
                virt[n] = (patient.getTotalPop())
            if n == 149:
                patient.addPrescription('guttagonol')
            if virt1.has_key(n):
                virt1[n] += (patient.getResistPop(['guttagonol']))
            else:
                virt1[n] = (patient.getResistPop(['guttagonol']))
    for i in virt:
        avg.append(float(virt[i])/float(numTrials))
    for j in virt1:
        avg1.append(float(virt1[j])/float(numTrials))
    pylab.figure(1)
    pylab.xlabel('timesteps')
    pylab.ylabel('number of viruses')
    pylab.title('average number of viruses considering timesteps')
    pylab.legend('total viruses pop', 'resistant virus pop',loc='upper left')
    pylab.plot(avg)
    pylab.plot(avg1)
    pylab.show()
##    totpoplist=[]
##    resvir=[]
##    time=[]
##    for i in range(numTrials):
##        viruses=[]
##        for i in range(numViruses):
##          v = ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)
##          viruses.append(v)
##        pat = TreatedPatient(viruses, maxPop)
##        for t in range(300):
##            pop = 0.0
##            res = 0.0
##            pat.update()
##            if t==150:
##                pat.addPrescription("guttagonol")
##            time.append(t)
##            pop +=pat.getTotalPop()
##            totpoplist.append(float(pop)/float(numTrials))
##            res +=pat.getResistPop(['guttagonol'])
##            resvir.append(float(res)/float(numTrials))
##            
##    pylab.plot(time, totpoplist)
##    pylab.plot(time, resvir)
##    pylab.title('ResistantVirus simulation')
##    pylab.xlabel('time step')
##    pylab.ylabel('# viruses')
##    pylab.legend(loc = 'upper left')
##    pylab.show()        
##    virus_list = []
##    ans1 = []
##    ans2 = []
##    for i in range(numViruses):
##        v = ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)
##        virus_list.append(v)
##
##    p = TreatedPatient(virus_list, maxPop) 
##    for j in range(300):
##        p.update()
##        t1 = 0.0
##        t2=0.0
##        for i in range(numTrials):
##            if j == 150:
##                p.addPrescription('guttagonol')
##                #p.update()
##            t1 += p.getTotalPop()
##            t2 += p.getResistPop(['guttagonol'])
##        
##        ans1.append(float(t1)/float(numTrials))
##        ans2.append(float(t2)/float(numTrials))
##    
##        
##    pylab.plot(range(300), ans1)
##    pylab.plot(range(300), ans2)
##    pylab.title('ResistantVirus simulation')
##    pylab.xlabel('time step')
##    pylab.ylabel('# viruses')
##    pylab.legend(loc = 'upper left')
##    pylab.show()

    # getting total population
##    for k in range(300):
##        patient.update()
##        popAtStep[k] += patient.getTotalPop()
##        resAtStep[k] += patient.getResistPop(['guttagonol'])

            
simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)    
##    virus_list = []
##    virus_pop = []
##    for i in range(numViruses):
##        virus_list.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
##        
##    for trial in numTrials:
##        p = TreatedPatient(virus_list, maxPop)
##        for k in range(150):
##            p.updates()
##        resistances['guttagonol'] = False
##        for n in range(150):
##            p.updates()
