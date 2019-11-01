# Problem Set 7
# Name: Alan Weng
# Collaborators: 
# Time Spent: A VERY VERY VERY LONG TIME
#

import random
import matplotlib.pyplot as plt

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



class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, maxBirthProb,clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        if random.random() <= self.clearProb:
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

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

        prob = random.random()
        if prob < self.maxBirthProb * (1.0 - popDensity):
            child = SimpleVirus(self.maxBirthProb, self.clearProb)
            return child
        else:
            raise NoChildException()


'''
End helper code
'''

#
# PROBLEM 1
#

class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop, clearProb, detectionThreshold, lossThreshold):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)

        clearProb: Maximum clearance probability (a float between 0-1).

        detectionThreshold: Viral population size at which immune response is active (an integer).

        lossThreshold: Viral population size at which immune system is inactive (an integer).
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.clearProb = clearProb
        self.detectionThreshold = detectionThreshold
        self.lossThreshold = lossThreshold


    def getTotalPop(self):
        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)
    
    def get_lossThreshold(self):
        return self.lossThreshold

    def get_detectionThreshold(self):
        return self.detectionThreshold

    def get_clearprob(self):
        return self.clearProb
    
    def get_maxPop(self):
        return self.maxPop

    def get_immuneResponse(self):
        """
        The virus will illicit an immune response once above the detectionThreshold.
        If the virus population grows beyond the lossThreshold, the patient immune system can no longer clear
        viruses from the system.

        - return False if the viruses grow beyond lossThreshold
        - Use clearProb to determine if the viruses are cleared,
        while the population size is between the detection and loss thresholds.
         """
        
        if self.getTotalPop() > self.lossThreshold:
            return False #immune system not effective.

        elif self.getTotalPop() > self.detectionThreshold: #chance of active immune system fighting
            prob = random.random()
            return prob < self.get_clearprob()
            


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.
        - The current population density is calculated. This population density
          value is used until the next call to update()
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """
        for virus in self.viruses:
            # print(f'immune response: {self.get_immuneResponse()}')
            if virus.doesClear() == True:
                self.viruses.remove(virus)
            
            current_pop_density = self.getTotalPop() / float(self.maxPop)

            if current_pop_density < 1 and current_pop_density > 0:
                try:
                    virus.reproduce(current_pop_density)
                    self.viruses.append(virus)
                except NoChildException:
                    pass
                
        return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug(viruses, maxPop, clearProb, detectionThreshold, lossThreshold, trialRuns):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for pateint (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    detectionThreshold: Viral population size at which immune response is active (an integer).
    lossThreshold: Viral population size at which immune system is ineffective (an integer).
    """

    # TODO

    virus_pop = []
    for i in range(trialRuns):
        virus_pop.append([])

    for i in range(trialRuns):
        individual_virus = []
        for virus in range(viruses):
            virus = SimpleVirus(0.1, clearProb)
            individual_virus.append(virus)
        thePatients = SimplePatient(individual_virus, maxPop, clearProb, detectionThreshold, lossThreshold)
        for update in range(trialRuns):
            thePatients.update()
            virus_pop[update].append(thePatients.getTotalPop())
    
    average_pop = []

    for virus_instance in virus_pop:
        average = sum(virus_instance) / float(trialRuns)
        average_pop.append(average)
    
    plt.title("SimpleVirus simulation")
    plt.plot(range(300), average_pop)
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
    plt.legend("Virus")
    plt.show()

# simulationWithoutDrug(100, 1000, 0.05, 200, 500, 300)