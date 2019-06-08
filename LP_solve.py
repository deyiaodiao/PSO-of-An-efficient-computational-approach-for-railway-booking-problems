from gurobipy import *
from sympy import exp,pi
import math

def phi(x):
    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    # Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)/math.sqrt(2.0)

    # A&S formula 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

    return 0.5*(1.0 + sign*y)

def newton(sigma,mean,s):
    x={}
    fx={}
    dfx={}
    x[0]=s
    ite=3000
    for i in range(0,ite):
        z=(x[i]-mean)/sigma
        a=phi(z)
        temp_fx=x[i]-(x[i]-mean)*(a)-(sigma*exp(-0.5*z*z))/((2*pi)**0.5)-s
        fx[i]=float(temp_fx)
        temp_dfx=1-a
        dfx[i]=float(temp_dfx)
        x[i+1]=x[i]-fx[i]/dfx[i]
        if fx[i]*fx[i]<0.00000000001:
            break
    return x[len(x)-1]

def solve(station_num,fare_type,capacity,fare,mean,sigma):
    m = Model('IP')
    sold = m.addVars(fare_type, station_num, station_num, lb=0, vtype=GRB.CONTINUOUS, name="sold")
    m.addConstrs((quicksum(
        sold[f, i, j] for f in range(0, fare_type) for i in range(0, station_num - 1) if i <= leg for j in
        range(1, station_num) if j >= leg + 1) <= capacity for leg in range(0, station_num - 1)),
                 name="sold_less_than_capacity")
    m.addConstrs((sold[f, i, j] <= mean[f, i, j] for f in range(0, fare_type) for i in range(0, station_num) for j in
                  range(0, station_num) if i <= j - 1), name="sold_less_than_mean")
    m.setObjective((quicksum(
        sold[f, i, j] * fare[f, i, j] for f in range(0, fare_type) for i in range(0, station_num) for j in
        range(0, station_num) if i <= j - 1)), GRB.MAXIMIZE)
    m.optimize()
    m.write('IP.lp')
    m.write('IP.sol')
    solution={}
    for i in sold:
        if i[1]<=i[2]-1:
            solution[i]=sold[i].x
    for i in solution:
        a=newton(sigma[i],mean[i],solution[i])
        solution[i]=a
        print(a,solution[i],i)
    print(solution)
    return solution




#Newton.newton(3.52,18.15,18.15)




