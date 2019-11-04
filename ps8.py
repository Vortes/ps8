# CS 111 Problem Set 8
#
# Name:
# Collaborators:
# Time:

import random
import matplotlib.pyplot as plt
from ps7 import *

#
# PROBLEM 1
#
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        self.maxBirthProb = maxBirthProb
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if self.resistances[drug]:
            return True
        else:
            return False


    def isResistantToAll(self, drugList):
        """ Helper function that checks if virus is resistant to all the drugs
            in drugList """
        for drugs in range(len(drugList)):
            if self.resistances[drugList[drugs]] == True:
                continue
            else:
                return False

        return True
        

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

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
        prob = random.random()
        new_resistance = {}

        if self.isResistantToAll(activeDrugs):
            if prob < self.maxBirthProb * (1 - popDensity):
                prob_for_offspring = 1 - self.mutProb
                for drugs in self.resistances:
                    if self.isResistantTo(self.resistances[drugs]):
                        if prob < prob_for_offspring:
                            new_resistance[drugs] = True
                        else:
                            new_resistance[drugs] = False
                    else:
                        if prob > prob_for_offspring:
                            new_resistance[drugs] = True
                        else:
                            new_resistance[drugs] = False
            else:
                raise NoChildException()
            child = ResistantVirus(self.maxBirthProb, new_resistance, self.clearProb. self.mutProb)
        else:
            raise NoChildException()
        

class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop, clearProb, detectionThreshold, lossThreshold):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)

        clearProb: Maximum clearance probability (a float between 0-1).

        detectionThreshold: Viral population size at which immune response is active (an integer).

        lossThreshold: Viral population size at which immune system is ineffective (an integer).
        """
        administeredDrugs = []
        self.viruses = viruses
        self.maxPop = maxPop
        self.clearProb = clearProb
        self.detectionThreshold = detectionThreshold
        self.lossthreshold = lossThreshold
        self.administeredDrugs = administeredDrugs

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug in self.administeredDrugs:
            pass
        else:
            self.administeredDrugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.administeredDrugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        super_drugs = 0
        for drugs in drugResist:
            if drugs.isResistantTo(drugs):
                super_drugs += 1
            else:
                pass
        return super_drugs


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        for virus in self.viruses:
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
def simulationWithDrug():
    """
    Runs simulations and plots graphs for problem 2.

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
    
    # TODO


#
# PROBLEM 3
#
def simulationDelayedTreatment():
    """
    Runs simulations and make histograms for problem 3.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a list of drugs that each ResistantVirus is resistant to
                 (a list of strings, e.g., ['guttagonol'])
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO

