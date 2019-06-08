from sympy import exp,pi
import LP_solve,random,math,time,Data_input

#############################################################
station_num=9
fare_type=2
section=station_num-1
capacity=300
population_size=25

fare_rate=1.1
mean_rate=1.1
sigma_rate=1.1

iteration_num=20
#############################################################
# 读取票价数据
fare = Data_input.fare_you(station_num, fare_rate)
# 读取mean数据
mean = Data_input.mean_you(station_num, fare_type, mean_rate)
# 读取标准差
sigma = Data_input.sigma_you(station_num, sigma_rate)

particle_best={}
global_best={}
particle_best_value={}
for i in range(0,population_size):
    particle_best_value[i]=0
global_best_value=0
velocity={}##velocity[迭代的代数][个体][变量]

best_value={}
best={}
#############################################################

def generation_of_initial_population(sold,population_size):
    swarm={}
    for i in range(0,population_size):
        particle={}
        for j in sold:
            particle[j]=math.ceil(sold[j]+random.uniform(-3,0))
            # particle[j]=math.ceil(random.uniform(0,sold[j]))
            # print(random.uniform(-3,3))
            if particle[j]<=0:
                particle[j]=0
        swarm[i]=particle
    return swarm

def get_obj(particle_num,particle,mean,sigma,fare):
    obj=0
    for i in particle:
        # print(i,particle[i],mean[i],sigma[i])
        z=(particle[i]-mean[i])/sigma[i]
        obj=obj+fare[i]*float(quadrature(particle[i],z,mean[i],sigma[i]))
    if obj>particle_best_value[particle_num] and if_is_feasible(particle,mean,sigma)==True:
        particle_best_value[particle_num]=obj
        particle_best[particle_num]=particle
    elif if_is_feasible(particle,mean,sigma)==False and particle_best_value[particle_num]==0:
        particle_best[particle_num]={}
        for i in particle:
            particle[i]=particle[i]-1
            particle_best[particle_num][i]=particle[i]
    #print(obj)

def if_is_feasible(particle,mean,sigma):
    #print("Check if is feasible")
    feasible=True
    sold={}
    for i in particle:
        sold[i]=float(quadrature(particle[i],(particle[i]-mean[i])/sigma[i],mean[i],sigma[i]))
        if sold[i]<0:
            sold[i]=0
    # print(sold)
    for i in range(0,section):
        subject=0
        for start in range(0,i+1):
            for end in range(i+1,section+1):
                for j in range(0,fare_type):
                    subject=subject+sold[(j,start,end)]
        if subject>capacity:
            feasible=False
            break
    return feasible

def quadrature(B,z,mean,sigma):
    a=phi(z)
    S = B-(B-mean)*a-(sigma*exp(-0.5*z*z))/((2*pi)**0.5)
    return S

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

def update_location(local_particle,par_num,iteration):
    local_velocity=velocity[iteration][par_num]
    previous_velocity={}
    if iteration>=1:
        previous_velocity=velocity[iteration-1][par_num]
    else:
        for i in local_particle:
            previous_velocity[i]=0
    for i in local_particle:
        local_velocity[i]=0
    for i in local_particle:
        # local_velocity[i]=0.5*previous_velocity[i]+0.5*random.uniform(0,0.5)*(particle_best[par_num][i]-local_particle[i])+0.5*random.uniform(0,0.5)*(global_best[i]-local_particle[i])
        local_velocity[i] = 0.5 * previous_velocity[i] + 0.5  * (
        particle_best[par_num][i] - local_particle[i]) + 0.5  * (
        global_best[i] - local_particle[i])
        local_particle[i] = math.ceil(local_particle[i] + local_velocity[i])
    return local_particle

def check():
    check = {}
    check[0, 0, 1] = 36
    check[0, 0, 2] = 37
    check[0, 0, 3] = 42
    check[0, 1, 2] = 13
    check[0, 1, 3] = 37
    check[0, 2, 3] = 35
    check[1, 0, 1] = 30
    check[1, 0, 2] = 34
    check[1, 0, 3] = 38
    check[1, 1, 2] = 0
    check[1, 1, 3] = 33
    check[1, 2, 3] = 31

    obj = 0
    for i in check:
        # print(i,particle[i],mean[i],sigma[i])
        z = (check[i] - mean[i]) / sigma[i]
        obj = obj + fare[i] * float(quadrature(check[i], z, mean[i], sigma[i]))

    print(obj)
    print(if_is_feasible(check, mean, sigma))
#############################################################
nowtime = time.clock()

##求解线性规划
sold = LP_solve.solve(station_num, fare_type, capacity, fare, mean, sigma)
##初始化种群
swarm = generation_of_initial_population(sold, population_size)
##计算目标函数（适应值），更新种群/个体最优情况
for i in range(0, population_size):
    get_obj(i, swarm[i], mean, sigma, fare)
    if particle_best_value[i] > global_best_value:
        global_best_value = particle_best_value[i]
        global_best = particle_best[i]
    if global_best_value == 0:
        for p in swarm[i]:
            global_best[p] = 0
    print(-1, i, particle_best_value[i])
##迭代计算
for ite in range(0, iteration_num):
    ##更新速度，更新个体位置
    velocity[ite] = {}
    for j in range(0, population_size):
        velocity[ite][j] = {}
        temp = update_location(swarm[j], j, ite)
        swarm[j] = temp
    ##计算目标函数（适应值），更新种群/个体最优情况
    for i in range(0, population_size):
        get_obj(i, swarm[i], mean, sigma, fare)
        if particle_best_value[i] > global_best_value:
            global_best_value = particle_best_value[i]
            global_best = particle_best[i]
        if global_best_value == 0:
            for p in swarm[i]:
                global_best[p] = 0
        print(ite, i, particle_best_value[i])
    print(ite, global_best_value)
    best_value[ite] = global_best_value
    best[ite] = global_best
print(best_value)
print(best)
print(time.clock() - nowtime, "s")


