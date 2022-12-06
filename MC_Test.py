import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, log2

from Neutron import Neutron
from Interface import Interface, InterfaceType
from Recorder import Recorder
from WorldGenerator import WorldGenerator
from RNG import CustomRNG as rng
from time import sleep

class MC_1DTest:

    numOfParticlesDesired = 10000
    numOfParticles = 0

    numOfConvergenceCyclesDesired = 10
    numOfConvergenceCycles = 0

    convergenceCycleIndex = []
    kEff = []
    shannonEntropy = []

    recorder: Recorder
    neutrons: list[Neutron] = []

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
        self.recorder = Recorder(-100, 100, 200)
        

    def CreateFirstGenerationOfNeutrons(self):
        region = self.world.GetStartingRegion()

        for _ in range(self.numOfParticlesDesired):
            #position = rng.RandomFromRange(75,100)


            #self.neutrons.append(Neutron([position, 0, 0], self.world.regions[2]))
            self.neutrons.append(Neutron(self.world.startingSourcePosition, region))

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

                while(neutron.isAlive):
                    #print("position: " + str(neutron.position[0]) + ", direction: " + str(neutron.direction[0]) + ", energy: " + str(neutron.E))
                    #sleep(1)
                    interfacesHit: list[Interface] = []
                    for interface in neutron.region.interfaces:
                        if(interface.IsHitByParticleDuringFlight(neutron.position, neutron.DesiredDestination())):
                            interfacesHit.append(interface)

                    if(interfacesHit):
                        collidedInterface = min(interfacesHit, key=lambda interface: interface.GetCollisionDistance(neutron.position, neutron.DesiredDestination()))

                        if(collidedInterface.interfaceType == InterfaceType.Coupled):
                            newPosition = collidedInterface.GetCollisionLocation(neutron.position, neutron.DesiredDestination())
                            self.recorder.RecordFlux(neutron.position, newPosition)
                            neutron.position = newPosition
                            newRegion = collidedInterface.GetCoupledRegion(neutron.region)
                            neutron.SetRegion(newRegion)
                            neutron.DetermineUnrestrictedTravelDistance()
                        elif(collidedInterface.interfaceType == InterfaceType.Void):                      
                            newPosition = collidedInterface.GetCollisionLocation(neutron.position, neutron.DesiredDestination())
                            self.recorder.RecordFlux(neutron.position, newPosition)
                            neutron.position = newPosition
                            neutron.Kill()
                            #print("Killed in void at " + str(neutron.position[0]))
                        elif(collidedInterface.interfaceType == InterfaceType.Reflective):

                            newPosition = collidedInterface.GetCollisionLocation(neutron.position, neutron.DesiredDestination())
                            #print(neutron.position[0])
                            #print(newPosition[0])
                            self.recorder.RecordFlux(neutron.position, newPosition)
                            neutron.position = newPosition
                            vectorToCollision = [(newPosition[0] - neutron.position[0]), (newPosition[1] - neutron.position[1]), (newPosition[2] - neutron.position[2])]

                            distanceTraveled = sqrt((vectorToCollision[0]**2)+(vectorToCollision[1]**2)+(vectorToCollision[2]**2))
                            neutron.travelDistance = neutron.travelDistance - distanceTraveled
                            
                            oldDirection = neutron.GetDirectionUnitVector()
                            newDirection = oldDirection
                            newDirection[0] = -1 * newDirection[0]
                            neutron.SetFlightAngle(newDirection)
                            #print("Reflected at " + str(neutron.position[0]))
                    else:
                        self.recorder.RecordFlux(neutron.position, neutron.DesiredDestination())
                        neutron.position = neutron.DesiredDestination()

                        division1 = neutron.region.material.ScatteringFraction(neutron.E)
                        division2 = division1 + neutron.region.material.CaptureFraction(neutron.E)

                        randomNumber = rng.RandomFromRange(0, 1)

                        self.recorder.RecordCollision(neutron.position)

                        # if(neutron.position[0] < -15 and neutron.position[0] > -25):
                        #     print("hit")
                        #     print(neutron.position[0])
                        #     print(neutron.direction[0])
                        #     print(neutron.travelDistance)
                        # Scattering
                        if(randomNumber < division1):
                            neutron.Scatter()
                            self.recorder.RecordScattering(neutron.position)
                            #print("Scattered at " + str(neutron.position[0]))
                        # Cature
                        elif(randomNumber < division2):
                            self.recorder.RecordCapture(neutron.position)
                            neutron.Kill()
                            #print("Captured at " + str(neutron.position[0]))
                        # Fission
                        else:
                            #print("Fission at " + str(neutron.position[0]))
                            neutron.Kill()
                            self.recorder.RecordFission(neutron.position)
                            fissionSites.append(Neutron(neutron.position, neutron.region))

                numOfParticles = numOfParticles + 1
                #print(str(numOfParticles) + " / " + str(len(self.neutrons)) + " completed.")

            numOfNewNeutrons = 0

            for fissionSite in fissionSites:
                numOfNewNeutrons = numOfNewNeutrons + fissionSite.region.material.NeutronsPerFission()

            self.kEff.append(numOfNewNeutrons / self.numOfParticlesDesired)
            #self.kEff.append(1)
            for _ in range(self.numOfParticlesDesired):
                randomIndex = np.random.randint(0, len(fissionSites))
                neutronToCopy = fissionSites[randomIndex]
                nextGeneration.append(Neutron(neutronToCopy.position, neutronToCopy.region))
                #nextGeneration.append(Neutron([0,0,0], self.world.startingRegion))

            newShannonEntropy = 0

            for bin in self.recorder.bins:
                Si = bin.numberOfFissions / self.numOfParticlesDesired

                if(Si>0):
                    newShannonEntropy = newShannonEntropy + Si*log2(Si)

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
        x_flux = []
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
            x_flux.append(fluxDetector.position[0])

        # plt.plot(self.convergenceCycleIndex, self.kEff, label = "kEff")
        # plt.show()

        # plt.plot(self.convergenceCycleIndex, self.shannonEntropy, label = "Shannon Entropy")
        # plt.show()

        # plt.plot(x, scattering)
        # plt.show()

        # plt.plot(x, capture)
        # plt.show()

        # plt.plot(x, fissions)
        # plt.show()

        # plt.plot(x, collisions)
        # plt.show()

        plt.plot(x_flux,flux)

        plt.show()
