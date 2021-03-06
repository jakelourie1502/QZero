# from msvcrt import kbhit
import time
from pickle import FALSE
import sys
sys.path.append('..')
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from math import factorial as F
import matplotlib.pyplot as plt
from utils import support_to_scalar
import numpy as np
import torch
# from training_and_data.training import loss_func_RDN
sys.stdout = open("viewing_RDN_values.txt","w")

from global_settings import env_size, dist,  value_support, exp_v_support, observable_size
from game_play.skiing_env import skiWorld as Env
from utils import vector2d_to_tensor_for_model
from game_play.play_episode import Episode

for j in range(10000):
    jake_zero = torch.load('../saved_models/jake_zero',map_location=torch.device('cpu'))
    states = env_size[0]*env_size[1]
    pred = jake_zero.prediction
    dyn = jake_zero.dynamic
    repr =jake_zero.representation
    rdn_obj = jake_zero.rdn_obj
    jake_zero.eval()
    #1
    fut_nov_arr = np.zeros((states,))
    rdn_array = np.zeros((states,))
    val_array = np.zeros((states,))
    print(jake_zero.rdn_obj.mu, jake_zero.rdn_obj.siggy)
    np.set_printoptions(suppress=True, precision = 2)
    
    if j % 2 ==0:
        print("Looking Two ahead")
    else:
        print("Looking one ahead)")
    for move in list(range(7)):
        print("move: ", move)
        
        for i in range(80,82): ##### DOESN'T SEEM TO LIKE IT WHEN YOU TRY TO START IN A STATE THAT IS A CLIFF OR RIGHT AT THE END.
            print(i)
            env=Env(start_state = i)
            raw_obs = env.reset()
            obs = vector2d_to_tensor_for_model(torch.tensor(raw_obs).float())
            s = jake_zero.representation(obs)
            s, _ , t= jake_zero.dynamic(s,move)
            # s, _ , t= jake_zero.dynamic(s,move)
            # s, _ , t= jake_zero.dynamic(s,move)
            if j % 2 == 0:
                s, _ , t= jake_zero.dynamic(s,move)
            p, v, n = jake_zero.prediction(s)
            v = support_to_scalar(v.detach().numpy(), *value_support)
            t = torch.tensor(0)
            proj1 = jake_zero.RDN(s)
            proj2 = jake_zero.RDN_prediction(s)
            fut_nov = support_to_scalar(n.detach().numpy(), *exp_v_support)

            r_nov = rdn_obj.evaluate(proj1, proj2)
            fut_nov_arr[i] =fut_nov*(1-t)
            rdn_array[i] = (1-t.detach().numpy())*r_nov.detach().numpy()
            val_array[i] = v
    

        print("Future nov array")
        print(fut_nov_arr.reshape(*env_size))
        print("RDN value array instant")
        print(rdn_array.reshape(*env_size))
        sys.stdout.flush()
        # if j == 0:
        print("value array")
        print(val_array.reshape(env_size))
    time.sleep(2.5*60)



# models = [repr, dyn, pred]
# epsilon = 0
# temperature = 0.01
# ep_h = []
# def Play_Episode_Wrapper():
#     with torch.no_grad():
#         ep = Episode(jake_zero,epsilon)
#         metrics, rew,_ = ep.play_episode(jake_zero.rdn_obj,False, epoch = 30, view_game =True)
#         # replay_buffer.add_ep_log(metrics)
#         print(rew)
#         ep_h.append(rew)


# def plot_beta(a,b):

#     def normalisation_beta(a,b):
#         return 1/ (F(a-1)*F(b-1) / F(a+b-1))

#     def beta_val(a,b,val):
#         return normalisation_beta(a,b) * val**(a-1) * (1-val)**(b-1)
    
#     X = np.linspace(0,1,100)
#     y = [beta_val(a,b,x) for x in X]
#     plt.plot(X,y)

# tn = time.time()
# fig = plt.figure()
# plt.savefig('saved_plt.png')

# for _ in range(0):
#     Play_Episode_Wrapper()
#     a = int(1 + np.sum(ep_h))
#     b = int(2 + len(ep_h) - np.sum(ep_h))
#     plot_beta(a,b)
#     plt.savefig('saved_plt.png')

#     plt.pause(0.001)
#     plt.close()


# print(np.sum(ep_h), np.mean(ep_h))
# print(time.time()- tn)