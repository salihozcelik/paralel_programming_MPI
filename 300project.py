"""
Salih Can Özçelik
2016400207
Compiling-Working
Periodic-Checkered GoL
"""
#SECTION 1
from mpi4py import MPI
import random
import sys
import time
import numpy as np
import math

#SECTION 2
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
T = sys.argv[3]
T =int(T)                      #number of iterations
inp = np.loadtxt(dtype=int, fname=inputFileName)

#SECTION 3
comm = MPI.COMM_WORLD          #getting rank and size with mpi
rank = comm.Get_rank()
size = comm.Get_size()
Length = 360

#SECTION 4
#Tag names for MPI send and receives
leftTag = 1
rightTag =2
upTag = 3
downTag =4
upLeftTag = 5
upRightTag = 6
downRightTag = 7
downLeftTag = 8

#SECTION 5
#LengthOfRow is the squareroot of slave ranks
#iterasyon is the length of one slave's row or column length
lengthOfRow = math.sqrt(size-1)
iterasyon = Length / lengthOfRow
lengthOfRow = int(lengthOfRow)  #integer casting
iterasyon = int(iterasyon)

#SECTION 6
for k in range(T): #number of iterations to simulate Games is determined by T given in input
    c = 0
    if rank == 0 :
        for j in range(lengthOfRow) :#determining slave ranks
            for i in range(lengthOfRow) :
                px = inp[j*iterasyon : (1+j)*iterasyon,i*iterasyon : (1+i)*iterasyon]
                comm.Send(px.copy(), dest=c+1)
                c = c+1
    
    else :
        ranks = np.zeros((iterasyon,iterasyon), dtype = int) #ranks array is slaves array
        comm.Recv(ranks,source=0)

#SECTION 7
        leftTo = np.zeros(iterasyon,dtype = int)    #creating parts of array to send and receive
        rightTo = np.zeros(iterasyon,dtype = int)
        upTo = np.zeros(iterasyon,dtype = int)
        downTo = np.zeros(iterasyon,dtype = int)

        for i in range(iterasyon):                  #appending values to arrays
            leftTo[i] = ranks[i][0]
            rightTo[i] = ranks[i][iterasyon-1]
            upTo[i] = ranks[0][i]
            downTo[i] = ranks[iterasyon-1][i]

        upLeftTo = ranks[0][0]                      #appending parts to arrays
        upRightTo = ranks[0][iterasyon-1]
        downLeftTo = ranks[iterasyon-1][0]
        downRightTo = ranks[iterasyon-1][iterasyon-1]

        rankLeft=0                                  #doing necessary math calculations; given rank it finds the left of that array
        if(rank%lengthOfRow==1):
            rankLeft = rank+lengthOfRow-1 
        else:
            rankLeft = rank-1

        rankRight=0                                 #doing necessary math calculations; given rank it finds the right of that array
        if(rank%lengthOfRow==0):
            rankRight = rank-lengthOfRow+1 
        else:
            rankRight = rank+1
        
        rankUp=0                                    #doing necessary math calculations; given rank it finds the up of that array
        if(rank < lengthOfRow+1):
            rankUp = rank+(lengthOfRow*(lengthOfRow-1)) 
        else:
            rankUp = rank-lengthOfRow
    
        rankDown=0                                  #doing necessary math calculations; given rank it finds the down of that array
        if(rank > size-1-lengthOfRow):
            rankDown = rank-(lengthOfRow*(lengthOfRow-1)) 
        else:
            rankDown = rank+lengthOfRow
        
        rankUpLeft=0                                #doing necessary math calculations; given rank it finds the up-left of that array
        if(rank == 1):
            rankUpLeft = size-1 
        elif(rank < lengthOfRow+1):
            rankUpLeft = rankUp -1
        elif(rank % lengthOfRow == 1):
            rankUpLeft = rank -1
        else:
            rankUpLeft = rank - lengthOfRow-1
        
        rankUpRight=0                               #doing necessary math calculations; given rank it finds the up-right of that array
        if(rank == lengthOfRow):
            rankUpRight = size - lengthOfRow  
        elif(rank < lengthOfRow+1):
            rankUpRight = rankUp+1
        elif(rank % lengthOfRow == 0):
            rankUpRight = rank - 2*lengthOfRow +1
        else:
            rankUpRight = rank - lengthOfRow+1
        
        rankDownLeft=0                              #doing necessary math calculations; given rank it finds the down-left of that array
        if(rank == size-lengthOfRow):
            rankDownLeft = lengthOfRow
        elif(rank > size - lengthOfRow-1):
            rankDownLeft = rankDown-1
        elif(rank % lengthOfRow == 1):
            rankDownLeft = rank+2*lengthOfRow-1
        else:
            rankDownLeft = rank+lengthOfRow-1

        rankDownRight=0                             #doing necessary math calculations; given rank it finds the down-right of that array
        if(rank == size-1):
            rankDownRight = 1
        elif(rank > size-1-lengthOfRow):
            rankDownRight = rankDown+1
        elif(rank % lengthOfRow == 0):
            rankDownRight = rank+1
        else:
            rankDownRight = rank+lengthOfRow+1    
        
        #creating empty arrays for MPI receive function
        leftFrom = np.zeros(iterasyon,dtype = int)
        rightFrom = np.zeros(iterasyon,dtype = int)
        downFrom = np.zeros(iterasyon,dtype = int)
        upFrom = np.zeros(iterasyon,dtype = int)
        upLeftFrom = np.zeros((),dtype = int)
        upRightFrom = np.zeros((),dtype = int)
        downLeftFrom = np.zeros((),dtype = int)
        downRightFrom = np.zeros((),dtype = int)

#SECTION 8       
        if((rank%lengthOfRow)%2 == 1):          #sending and receiving data for odd numbered columns
            comm.Send(leftTo, dest =rankLeft,tag=leftTag)
            comm.Send(rightTo, dest =rankRight,tag=rightTag)                  
            comm.Send(upLeftTo, dest =rankUpLeft,tag=upLeftTag) 
            comm.Send(downLeftTo, dest =rankDownLeft,tag=downLeftTag)                  
            comm.Send(upRightTo, dest =rankUpRight,tag=upRightTag)                  
            comm.Send(downRightTo, dest =rankDownRight,tag=downRightTag)   
            comm.Recv(rightFrom,source=rankLeft,tag=leftTag)
            comm.Recv(downLeftFrom,source=rankUpRight,tag=upRightTag)
            comm.Recv(upRightFrom,source=rankDownLeft,tag=downLeftTag)
            comm.Recv(leftFrom,source=rankRight,tag=rightTag)
            comm.Recv(downRightFrom,source=rankUpLeft,tag=upLeftTag)
            comm.Recv(upLeftFrom,source=rankDownRight,tag=downRightTag)#
            
            
        else:                                   #sending and receiving data for even numbered columns
            comm.Recv(leftFrom,source=rankRight,tag=leftTag)
            comm.Recv(rightFrom,source=rankLeft,tag=rightTag)
            comm.Recv(upLeftFrom,source=rankDownRight,tag=upLeftTag)
            comm.Recv(downLeftFrom,source=rankUpRight,tag=downLeftTag)
            comm.Recv(upRightFrom,source=rankDownLeft,tag=upRightTag)
            comm.Recv(downRightFrom,source=rankUpLeft,tag=downRightTag)#
            comm.Send(rightTo, dest =rankRight,tag=leftTag)
            comm.Send(downLeftTo, dest =rankDownLeft,tag=upRightTag)
            comm.Send(upRightTo, dest =rankUpRight,tag=downLeftTag)           
            comm.Send(leftTo, dest =rankLeft,tag=rightTag)
            comm.Send(downRightTo, dest =rankDownRight,tag=upLeftTag)
            comm.Send(upLeftTo, dest =rankUpLeft,tag=downRightTag)

            
        if(((rank-1)//lengthOfRow)%2 == 1):     #sending and receiving data for odd numbered rows
            comm.Send(upTo, dest =rankUp,tag=upTag)
            comm.Send(downTo, dest =rankDown,tag=downTag)
            comm.Recv(upFrom,source=rankUp,tag=downTag)
            comm.Recv(downFrom,source=rankDown,tag=upTag)
        else:                                   #sending and receiving data for even numbered rows
            comm.Recv(downFrom,source=rankDown,tag=upTag)        
            comm.Recv(upFrom,source=rankUp,tag=downTag)
            comm.Send(downTo, dest =rankDown,tag=downTag)
            comm.Send(upTo, dest =rankUp,tag=upTag)

#SECTION 9
        #creating bigger arrays for calculations of the next step.    
        newArr = np.zeros((iterasyon+2,iterasyon+2),dtype =int)
        newArr[1:iterasyon+1,1:iterasyon+1] = ranks
        newArr[1:iterasyon+1,iterasyon+1] = leftFrom
        newArr[1:iterasyon+1,0] = rightFrom
        newArr[0,1:iterasyon+1] = upFrom
        newArr[iterasyon+1,1:iterasyon+1] = downFrom
        newArr[0,iterasyon+1] = downLeftFrom
        newArr[0,0] = downRightFrom   
        newArr[iterasyon+1,iterasyon+1] =upLeftFrom
        newArr[iterasyon+1,0] = upRightFrom
        
        #game of life logic
        lastArr = np.zeros((iterasyon+2,iterasyon+2),dtype=int)
        for i in range(1,iterasyon+1):
            for j in range(1,iterasyon+1):
                sum =  newArr[i-1][j-1]+newArr[i-1][j]+newArr[i-1][j+1]+newArr[i][j-1]+newArr[i][j+1]+newArr[i+1][j-1]+newArr[i+1][j]+newArr[i+1][j+1]
                if(sum==3):
                    lastArr[i][j] = 1
                elif(sum==2):
                    lastArr[i][j] = newArr[i][j]
                else:
                    lastArr[i][j] = 0
                
        finishArr = np.copy(lastArr[1:iterasyon+1,1:iterasyon+1])
        comm.Send(finishArr,dest=0,tag=69)          #sending new values

    if rank == 0 :
        d = 0
        finito = np.zeros((iterasyon,iterasyon),dtype=int)
        for j in range(lengthOfRow) :
            for i in range(lengthOfRow) :
                comm.Recv(finito, source=d+1,tag=69)  #receiving new values
                inp[j*iterasyon : (1+j)*iterasyon,i*iterasyon : (1+i)*iterasyon] = finito           
                d = d+1

        
        np.savetxt(fname=outputFileName, X=inp,fmt="%s")
