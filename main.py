import numpy as np

def queueServerSimulation(numberOfRecords):
    # Initializing distribution variables
    uniformMinimum = 0
    uniformMaximum = 10
    gaussianMean = 10
    gaussianSigma = 5

    # Initializing Simulation List for 7 columns
    simulationData = [[0]*7 for i in range(numberOfRecords)]

    for i in range(numberOfRecords):
        # Generating Random Independant varaiables
        # interArrivalTime
        simulationData[i][0]=np.random.uniform(uniformMinimum, uniformMaximum)
        # servingTime
        simulationData[i][4]=np.random.normal(gaussianMean, gaussianSigma)

        # Calculating Dependant variables
        if(i>0):
            # arrivalTime = prevArrivalTime + interArrivalTime
            simulationData[i][1] = simulationData[i-1][1] + simulationData[i][0]
            # waitingTime = prevDepartuteTime - arrivalTime
            simulationData[i][2] = simulationData[i - 1][5] - simulationData[i][1]
        else:
            # arrivalTime = interArrivalTime
            simulationData[i][1] = simulationData[i][0]
            # waitingTime = 0
            simulationData[i][2] = 0

        # timeOfService = arrivalTime + waitingTime
        simulationData[i][3] = simulationData[i][1] + simulationData[i][2]
        # Departute Time = timeOfService  + servingTime
        simulationData[i][5] = simulationData[i][3] + simulationData[i][4]

    # Calculating Queue length for each record
    for i in range(numberOfRecords):
        departureTime = simulationData[i][5]
        queueLength = 0

        for j in range(i+1,numberOfRecords):
            # Increase Queue Length of This.record.Arrival Time < Departure Time
            if(simulationData[j][1] < departureTime):
                queueLength+=1

                # this.record = Last Record => Store Queue length
                if (j == numberOfRecords - 1):
                    simulationData[i][6] = queueLength
                    queueLength = 0

            else:
                simulationData[i][6]=queueLength
                break;
    print(*simulationData,sep="\n")


queueServerSimulation(1000)

## List columns
## 0 - Inter Arrival Time
## 1 - Arrival Time
## 2 - Waiting Time
## 3 - Time of Service
## 4 - Serving Time
## 5 - Departure Time
## 6 - Queue Length