import numpy as np
import matplotlib.pyplot as plt
import math

from Neutron import Neutron
from Interface import Interface, InterfaceType
from Recorder import Recorder
from WorldGenerator import WorldGenerator
from RNG import CustomRNG as rng

class MC_1DTest:

    numOfParticlesDesired = 10000
    numOfParticles = 0

    numOfConvergenceCyclesDesired = 15
    numOfConvergenceCycles = 0

    convergenceCycleIndex = []
    kEff = []
    shannonEntropy = []

    recorder: Recorder
    neutrons: list[Neutron] = []
    queuedNeutrons: list[Neutron] = []

    def Start(self):
        self.CreateWorld()
        self.CreateRecorder()
        self.CreateFirstGenerationOfNeutrons()
        self.SourceTermConvergenceLoop()
        #self.Loop()
        self.Plot()

    def CreateWorld(self):
        self.world = WorldGenerator()

    def CreateRecorder(self):
        self.recorder = Recorder(-100, 100, 100)

    def CreateFirstGenerationOfNeutrons(self):
        region = self.world.GetStartingRegion()

        for _ in range(self.numOfParticlesDesired):
            self.neutrons.append(Neutron(self.world.GetStartingPointSource(), region))

    def SourceTermConvergenceLoop(self):
        while(self.numOfConvergenceCycles < self.numOfConvergenceCyclesDesired):
            fissionSites: list[Neutron] = []
            nextGeneration: list[Neutron] = []  

            numOfParticles = 0
           
            self.recorder.Reset()

            for neutron in self.neutrons:
                neutron.isAlive = True
                neutron.DetermineNewFlightAngle()
                neutron.DetermineUnrestrictedTravelDistance()
                


                # for neutron in self.neutrons:
                #     print(neutron.position[0])
                # print("**** NOW START ***")

                while(neutron.isAlive):

                    interfacesHit: list[Interface] = []
                    for interface in neutron.region.interfaces:
                        if(interface.IsHitByParticleDuringFlight(neutron.position, neutron.DesiredDestination())):
                            interfacesHit.append(interface)

                    if(interfacesHit):
                        collidedInterface = min(interfacesHit, key=lambda interface: interface.GetCollisionDistance(neutron.position, neutron.DesiredDestination()))

                        if(collidedInterface.interfaceType == InterfaceType.Coupled):
                            self.recorder.RecordFlux(neutron.position, collidedInterface.position)
                            neutron.position = collidedInterface.position
                            newRegion = collidedInterface.GetCoupledRegion(neutron.region)
                            neutron.SetRegion(newRegion)
                        elif(collidedInterface.interfaceType == InterfaceType.Void):
                            self.recorder.RecordFlux(neutron.position, collidedInterface.position)
                            neutron.position = collidedInterface.position
                            neutron.Kill()
                        elif(collidedInterface.interfaceType == InterfaceType.Reflective):
                            neutron.DetermineUnrestrictedTravelDistance()
                            self.recorder.RecordFlux(neutron.position, collidedInterface.position)
                            neutron.position = collidedInterface.position
                            
                            oldDirection = neutron.GetDirectionUnitVector()
                            newDirection = oldDirection
                            newDirection[0] = -1 * newDirection[0]
                            neutron.SetFlightAngle(newDirection)
                    else:
                        self.recorder.RecordFlux(neutron.position, neutron.DesiredDestination())
                        neutron.position = neutron.DesiredDestination()

                        division1 = neutron.region.material.ScatteringFraction(neutron.E)
                        division2 = division1 + neutron.region.material.CaptureFraction(neutron.E)

                        randomNumber = rng.RandomFromRange(0, 1)

                        self.recorder.RecordCollision(neutron.position)
                        # Scattering
                        if(randomNumber < division1):
                            neutron.Scatter()
                            self.recorder.RecordScattering(neutron.position)
                        # Cature
                        elif(randomNumber < division2):
                            self.recorder.RecordCapture(neutron.position)
                            neutron.Kill()
                        # Fission
                        else:
                            neutron.Kill()
                            self.recorder.RecordFission(neutron.position)
                            fissionSites.append(Neutron(neutron.position, neutron.region))

                numOfParticles = numOfParticles + 1
                #print(str(numOfParticles) + " / " + str(len(self.neutrons)) + " completed.")

            numOfNewNeutrons = 0

            for fissionSite in fissionSites:
                numOfNewNeutrons = numOfNewNeutrons + fissionSite.region.material.NeutronsPerFission()

            self.kEff.append(numOfNewNeutrons / self.numOfParticlesDesired)

            for _ in range(self.numOfParticlesDesired):
                randomIndex = np.random.randint(0, len(fissionSites))
                neutronToCopy = fissionSites[randomIndex]
                nextGeneration.append(Neutron(neutronToCopy.position, neutronToCopy.region))

            newShannonEntropy = 0

            for bin in self.recorder.bins:
                Si = bin.numberOfFissions / self.numOfParticlesDesired

                if(Si>0):
                    newShannonEntropy = newShannonEntropy + Si*math.log2(Si)

            newShannonEntropy = newShannonEntropy * -1

            self.shannonEntropy.append(newShannonEntropy)
            self.convergenceCycleIndex.append(self.numOfConvergenceCycles)
            self.numOfConvergenceCycles = self.numOfConvergenceCycles + 1

            self.neutrons = nextGeneration
            nextGeneration = []
            fissionSites = []

            for neutron in self.neutrons:
                if(neutron.position[0] == 1):
                    print("hit")

            print("Cycle Completed: " + str(self.numOfConvergenceCycles) + " / " + str(self.numOfConvergenceCyclesDesired))

    def Plot(self):
        x = []
        scattering = []
        capture = []
        fissions = []
        collisions = []
        flux = []

        for bin in self.recorder.bins:
            x.append((bin.xMin + bin.xMax)/2)
            fissions.append(bin.numberOfFissions)
            scattering.append(bin.numberOfScatterings)
            capture.append(bin.numberOfCaptures)
            collisions.append(bin.numberOfCollisions)

        for fluxDetector in self.recorder.fluxDetectors:
            flux.append(fluxDetector.flux)
        plt.subplot(4,2,1)
        plt.plot(self.convergenceCycleIndex, self.kEff, label = "kEff")
        plt.subplot(4,2,2)
        plt.plot(self.convergenceCycleIndex, self.shannonEntropy, label = "Shannon Entropy")
        plt.subplot(4,2,3)
        plt.plot(x, scattering)
        plt.subplot(4,2,4)
        plt.plot(x, capture)
        plt.subplot(4,2,5)
        plt.plot(x, fissions)
        plt.subplot(4,2,6)
        plt.plot(x, collisions)
        plt.subplot(4,2,7)
        plt.plot(x,flux)

        plt.show()
